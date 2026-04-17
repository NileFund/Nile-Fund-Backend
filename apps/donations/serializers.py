from rest_framework import serializers
from django.db.models import Sum
from .models import Donation
from apps.projects.models import Project
from apps.accounts.models import User


class UserMiniSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['email', 'full_name', 'profile_picture']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    
class DonationSerializer(serializers.ModelSerializer):
    donor = UserMiniSerializer(read_only=True)

    class Meta:
        model = Donation
        fields = ['id', 'project', 'donor', 'amount', 'created_at']

    def validate_amount(self, value):
        if value < 1:
            raise serializers.ValidationError("Donation must be at least 1 EGP.")
        return value

    def validate_project(self, project):
        if project.status != Project.Status.RUNNING:
            raise serializers.ValidationError("You can only donate to running projects.")
        return project

    
    def validate(self, attrs):
        project = attrs.get('project')
        amount = attrs.get('amount')

        # Defensive check for PATCH requests
        if not project or not amount:
            return attrs

        # FIX: Re-fetch and lock the project row for this transaction
        locked_project = Project.objects.select_for_update().get(id=project.id)

        # Calculate the total using the locked row
        current_total = locked_project.donations.aggregate(
            total=Sum('amount')
        )['total'] or 0

        if current_total + amount > locked_project.total_target:
            remaining = locked_project.total_target - current_total
            raise serializers.ValidationError(
                f"Donation exceeds target. Remaining allowed amount is {remaining} EGP."
            )

        return attrs