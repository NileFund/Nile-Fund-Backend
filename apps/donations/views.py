from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404

from django.db.models import Sum, F, Value
from django.db.models.functions import Concat

from .models import Donation
from .serializers import DonationSerializer
from .filters import DonationFilter
from apps.common.pagination import StandardPagination, SmallPagination
from apps.projects.models import Project


# CREATE DONATION
class DonationCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = DonationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        donation = serializer.save(donor=request.user)

        return Response(
            {
                "message": "Donation created successfully",
                "data": DonationSerializer(
                    donation,
                    context={'request': request}
                ).data
            },
            status=status.HTTP_201_CREATED
        )


# LIST ALL DONATIONS
class DonationListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        donations = Donation.objects.select_related('donor', 'project').all().order_by('-created_at')

        donations = DonationFilter(request.GET, queryset=donations).qs

        paginator = StandardPagination()
        paginated = paginator.paginate_queryset(donations, request)

        serializer = DonationSerializer(
            paginated,
            many=True,
            context={'request': request}
        )

        return paginator.get_paginated_response(serializer.data)


# MY DONATIONS
class MyDonationsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        donations = Donation.objects.filter(
            donor=request.user
        ).select_related('project').order_by('-created_at')

        donations = DonationFilter(request.GET, queryset=donations).qs

        paginator = StandardPagination()
        paginated = paginator.paginate_queryset(donations, request)

        serializer = DonationSerializer(
            paginated,
            many=True,
            context={'request': request}
        )

        return paginator.get_paginated_response(serializer.data)


# PROJECT DONATIONS
class ProjectDonationsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)

        donations = Donation.objects.filter(project=project).select_related('donor').order_by('-created_at')

        donations = DonationFilter(request.GET, queryset=donations).qs

        paginator = StandardPagination()
        paginated = paginator.paginate_queryset(donations, request)

        serializer = DonationSerializer(
            paginated,
            many=True,
            context={'request': request}
        )

        return paginator.get_paginated_response(serializer.data)


# DONATION DETAIL
class DonationDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, donation_id):
        donation = get_object_or_404(
            Donation.objects.select_related('donor', 'project'),
            id=donation_id
        )

        serializer = DonationSerializer(
            donation,
            context={'request': request}
        )

        return Response(serializer.data)


# PROJECT SUMMARY
class ProjectDonationSummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)

        total = Donation.objects.filter(project=project).aggregate(
            total=Sum('amount')
        )['total'] or 0

        return Response({
            "project_id": project.id,
            "target": project.total_target,
            "total_donated": total,
            "remaining": project.total_target - total,
            "percentage": (total / project.total_target * 100) if project.total_target else 0
        })


# TOP DONORS
class TopDonorsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)

        donors = (
            Donation.objects.filter(project=project)
            .values(
                'donor__email',
                'donor__first_name',
                'donor__last_name',
                'donor__profile_picture'
            )
            .annotate(total=Sum('amount'))
            .order_by('-total')[:5]
        )

        data = [
            {
                "email": d["donor__email"],
                "full_name": f"{d['donor__first_name']} {d['donor__last_name']}",
                "profile_picture": d["donor__profile_picture"],
                "total": d["total"]
            }
            for d in donors
        ]

        return Response(data)


# RECENT DONATIONS
class RecentDonationsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        donations = Donation.objects.select_related('donor', 'project').all().order_by('-created_at')

        paginator = SmallPagination()
        paginated = paginator.paginate_queryset(donations, request)

        serializer = DonationSerializer(
            paginated,
            many=True,
            context={'request': request}
        )

        return paginator.get_paginated_response(serializer.data)