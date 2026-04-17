from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import ProjectReport, CommentReport
from .serializers import ProjectReportSerializer, CommentReportSerializer
from apps.projects.models import Project
from apps.comments.models import Comment


class ReportProjectView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)

        serializer = ProjectReportSerializer(
            data=request.data,
            context={'request': request, 'project': project}
        )
        serializer.is_valid(raise_exception=True)

        ProjectReport.objects.create(
            project=project,
            reporter=request.user,
            reason=serializer.validated_data.get('reason', '')
        )

        return Response(
            {"message": "Project reported successfully"},
            status=status.HTTP_201_CREATED
        )


class ReportCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)

        serializer = CommentReportSerializer(
            data=request.data,
            context={'request': request, 'comment': comment}
        )
        serializer.is_valid(raise_exception=True)

        CommentReport.objects.create(
            comment=comment,
            reporter=request.user,
            reason=serializer.validated_data.get('reason', '')
        )

        return Response(
            {"message": "Comment reported successfully"},
            status=status.HTTP_201_CREATED
        )