from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import Rating
from .serializers import RatingSerializer , RatingListSerializer
from .filters import RatingFilter
from apps.common.pagination import StandardPagination
from apps.projects.models import Project


class RatingCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)

        serializer = RatingSerializer(
            data=request.data,
            context={'request': request, 'project': project}
        )
        serializer.is_valid(raise_exception=True)

        rating = Rating.objects.create(
            project=project,
            user=request.user,
            value=serializer.validated_data['value']
        )

        return Response(
            {
                "message": "Rating created successfully",
                "data": {
                    "project": project.id,
                    "value": rating.value
                }
            },
            status=status.HTTP_201_CREATED
        )


class RatingUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)

        rating = get_object_or_404(
            Rating,
            project=project,
            user=request.user
        )

        serializer = RatingSerializer(
            rating,
            data=request.data,
            partial=True ,
            context={'request': request, 'project': project}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                "message": "Rating updated successfully",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

class ProjectRatingsListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)

        queryset = Rating.objects.filter(project=project).select_related('user')

        rating_filter = RatingFilter(request.GET, queryset=queryset)
        queryset = rating_filter.qs

        paginator = StandardPagination()
        paginated = paginator.paginate_queryset(queryset, request)

        serializer = RatingListSerializer(paginated, many=True, context={'request': request})

        return paginator.get_paginated_response(serializer.data)