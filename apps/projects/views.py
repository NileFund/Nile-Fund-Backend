from rest_framework import viewsets, permissions, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.common.pagination import StandardPagination
from .models import Project, Tag
from .serializers import ProjectSerializer, TagSerializer
from django.db.models import Avg, Count
from .models import Project
from .serializers import ProjectSerializer
from apps.comments.models import Comments
from apps.comments.serializers import CommentDetailSerializer
from django.db.models import Avg, Count, Q

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

        featured = self.request.query_params.get('featured')
        if featured is not None:
            qs = qs.filter(is_featured=featured.lower() == 'true')

        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(
                Q(title__icontains=search) |
                Q(details__icontains=search) |
                Q(category__name__icontains=search) |
                Q(tags__name__icontains=search)
            ).distinct()

        ordering = self.request.query_params.get('ordering')
        if ordering == 'rating':
            qs = qs.annotate(avg_rating=Avg('ratings__value')).order_by('-avg_rating')
        elif ordering == 'popular':
            qs = qs.annotate(ratings_count=Count('ratings')).order_by('-ratings_count')
        elif ordering == 'oldest':
            qs = qs.order_by('created_at')
        else:
            qs = qs.order_by('-created_at')

        return qs

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['get'], permission_classes=[permissions.AllowAny])
    def comments(self, request, pk=None):
        project = self.get_object()
        
        comments = Comments.objects.filter(
            project=project,
            parent__isnull=True
        ).select_related('author').prefetch_related('replies').order_by('-created_at')
        
        serializer = CommentDetailSerializer(comments, many=True)
        return Response(serializer.data)

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
                {'message': 'Cannot cancel, donations have reached 25% or more of the target'},
                status=status.HTTP_400_BAD_REQUEST
            )

        project.status = Project.Status.CANCELLED
        project.save(update_fields=['status'])
        return Response({'message': 'Project cancelled successfully'})

    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def top_rated(self, request):
        projects = (
            Project.objects
            .select_related('owner', 'category')
            .prefetch_related('tags', 'pictures')
            .annotate(
                avg_rating=Avg('ratings__value'),
                ratings_count=Count('ratings')
            )
            .filter(ratings_count__gt=0)
            .order_by('-avg_rating')[:5]
        )
        serializer = self.get_serializer(projects, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def latest(self, request):
        projects = Project.objects.order_by('-created_at')[:5]
        projects = (
            Project.objects
            .select_related('owner', 'category')
            .prefetch_related('tags', 'pictures')
            .order_by('-created_at')[:5]
        )
        serializer = self.get_serializer(projects, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def featured(self, request):
        projects = Project.objects.filter(is_featured=True)[:5]
        projects = (
            Project.objects
            .select_related('owner', 'category')
            .prefetch_related('tags', 'pictures')
            .filter(is_featured=True)[:5]
        )
        serializer = self.get_serializer(projects, many=True)
        return Response(serializer.data)


class TagListView(generics.ListAPIView):
    queryset = Tag.objects.all().order_by('name')
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]
