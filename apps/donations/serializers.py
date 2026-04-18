from rest_framework import serializers
from django.db.models import Sum
from rest_framework.exceptions import ValidationError
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
    project_title = serializers.CharField(source='project.title', read_only=True)

    class Meta:
        model = Donation
        fields = ['id', 'project', 'project_title', 'donor', 'amount', 'created_at']

    def validate_amount(self, value):
        if value < 1:
            raise ValidationError({"detail": "Donation must be at least 1 EGP."})
        return value

    def validate_project(self, project):
        if project.status != Project.Status.RUNNING:
            raise ValidationError({
                "detail": "This project is completed. Donations are closed."
            })
        return project

    def validate(self, attrs):
        project = attrs.get('project')
        amount = attrs.get('amount')

        if not project or not amount:
            return attrs

        locked_project = Project.objects.select_for_update().get(id=project.id)

        current_total = locked_project.donations.aggregate(
            total=Sum('amount')
        )['total'] or 0

        if current_total + amount > locked_project.total_target:
            remaining = locked_project.total_target - current_total

            if remaining <= 0:
                raise ValidationError({
                    "detail": "This project has reached its target. Donations are closed."
                })

            raise ValidationError({
                "detail": f"Donation exceeds target. You can only donate up to {remaining} EGP."
            })

        return attrs