from rest_framework import viewsets, permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Comments
from .serializers import CommentsSerializer


class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer

    def get_permissions(self):
        if self.action == 'create':
            # POST: authenticated users
            return [permissions.IsAuthenticated()]
        elif self.action == 'destroy':
            # DELETE: comment owner, project owner, or admin
            return [
                permissions.IsAuthenticated(),
                self.DeletePermission()
            ]
        elif self.action in ['update', 'partial_update']:
            # PATCH/PUT: comment owner
            return [
                permissions.IsAuthenticated(),
                self.EditPermission()
            ]
        else:
            # GET: everyone
            return [permissions.AllowAny()]

    class DeletePermission(BasePermission):
        def has_object_permission(self, request, view, obj):
            return (
                obj.user == request.user or
                obj.project.owner == request.user or
                request.user.is_staff or
                request.user.is_superuser
            )

    class EditPermission(BasePermission):
        def has_object_permission(self, request, view, obj):
            if request.method in SAFE_METHODS:
                return True
            return obj.user == request.user