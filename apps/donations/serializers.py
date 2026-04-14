from rest_framework import serializers
from django.db.models import Sum
from .models import Donation
from apps.projects.models import Project


class DonationSerializer(serializers.ModelSerializer):
    donor = serializers.StringRelatedField(read_only=True)

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

        current_total = project.donations.aggregate(
            total=Sum('amount')
        )['total'] or 0

        if current_total + amount > project.total_target:
            remaining = project.total_target - current_total
            raise serializers.ValidationError(
                f"Donation exceeds target. Remaining allowed amount is {remaining} EGP."
            )

        return attrs