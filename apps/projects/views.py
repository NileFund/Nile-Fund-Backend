from rest_framework import viewsets, permissions, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.common.pagination import StandardPagination
from .models import Project, Tag
from .serializers import ProjectSerializer, TagSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    pagination_class = StandardPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        qs = (
            Project.objects
            .select_related('owner', 'category')
            .prefetch_related('tags', 'pictures')
            .order_by('-created_at')
        )
        status_param = self.request.query_params.get('status')
        if status_param:
            qs = qs.filter(status=status_param)

        category_id = self.request.query_params.get('category')
        if category_id:
            qs = qs.filter(category_id=category_id)

        return qs

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        project = self.get_object()

        if project.owner != request.user:
            return Response({'message': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

        if project.status == Project.Status.CANCELLED:
            return Response({'message': 'Project is already cancelled'}, status=status.HTTP_400_BAD_REQUEST)

        if project.status == Project.Status.COMPLETED:
            return Response({'message': 'Cannot cancel a completed project'}, status=status.HTTP_400_BAD_REQUEST)

        if project.donation_percentage >= 25:
            return Response(
                {'message': 'Cannot cancel — donations have reached 25% or more of the target'},
                status=status.HTTP_400_BAD_REQUEST
            )

        project.status = Project.Status.CANCELLED
        project.save(update_fields=['status'])
        return Response({'message': 'Project cancelled successfully'})


class TagListView(generics.ListAPIView):
    queryset = Tag.objects.all().order_by('name')
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]
