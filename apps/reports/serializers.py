from rest_framework import serializers
from .models import ProjectReport, CommentReport


class ProjectReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectReport
        fields = ['reason']

    def validate(self, attrs):
        request = self.context.get('request')
        project = self.context.get('project')

        if project.owner == request.user:
            raise serializers.ValidationError("You cannot report your own project.")

        if ProjectReport.objects.filter(project=project, reporter=request.user).exists():
            raise serializers.ValidationError("You already reported this project.")

        return attrs


class CommentReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentReport
        fields = ['reason']

    def validate(self, attrs):
        request = self.context.get('request')
        comment = self.context.get('comment')

        if CommentReport.objects.filter(comment=comment, reporter=request.user).exists():
            raise serializers.ValidationError("You already reported this comment.")

        return attrs