from rest_framework import viewsets, permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Comments
from .serializers import CommentsSerializer

class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    
    def get_queryset(self):
        return Comments.objects.select_related('author', 'project', 'parent').all()

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        elif self.request.method == 'DELETE':
            return [
                permissions.IsAuthenticated(),
                self.DeletePermission()
            ]
        elif self.request.method in ['PUT', 'PATCH']:
            return [
                permissions.IsAuthenticated(),
                self.EditPermission()
            ]
        else:
            return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    class DeletePermission(BasePermission):
        def has_object_permission(self, request, view, obj):
            return (
                obj.author == request.user or
                obj.project.owner == request.user or
                request.user.is_staff or
                request.user.is_superuser
            )

    class EditPermission(BasePermission):
        def has_object_permission(self, request, view, obj):
            if request.method in SAFE_METHODS:
                return True
            return obj.author == request.user