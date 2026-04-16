from django.utils import timezone
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.common.pagination import StandardPagination
from .models import Project
from .serializers import ProjectSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    pagination_class = StandardPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        now = timezone.now()
        qs = (
            Project.objects
            .select_related('owner', 'category')
            .prefetch_related('tags', 'pictures')
            .order_by('-created_at')
        )

        # Filter by status using time — no stored status field needed
        status_param = self.request.query_params.get('status')
        if status_param == 'pending':
            qs = qs.filter(is_cancelled=False, start_time__gt=now)
        elif status_param == 'running':
            qs = qs.filter(is_cancelled=False, start_time__lte=now, end_time__gte=now)
        elif status_param == 'completed':
            qs = qs.filter(is_cancelled=False, end_time__lt=now)
        elif status_param == 'cancelled':
            qs = qs.filter(is_cancelled=True)

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

        if project.is_cancelled:
            return Response({'message': 'Project is already cancelled'}, status=status.HTTP_400_BAD_REQUEST)

        if project.status == Project.Status.COMPLETED:
            return Response({'message': 'Cannot cancel a completed project'}, status=status.HTTP_400_BAD_REQUEST)

        if project.donation_percentage >= 25:
            return Response(
                {'message': 'Cannot cancel — donations have reached 25% or more of the target'},
                status=status.HTTP_400_BAD_REQUEST
            )

        project.is_cancelled = True
        project.save(update_fields=['is_cancelled'])
        return Response({'message': 'Project cancelled successfully'})
