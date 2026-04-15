from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status , permissions
from rest_framework.permissions import AllowAny
from apps.accounts.models import User
from .serializers import DonationSerializer
from .models import Donation
from .filters import DonationFilter
from apps.common.pagination import StandardPagination , SmallPagination
from django.shortcuts import get_object_or_404
from apps.projects.models import Project
from django.db.models import Sum , F, Value
from django.db.models.functions import Concat

# create Donation
class DonationCreateView(APIView):
     permission_classes = [permissions.IsAuthenticated]
     def post(self, request):
        serializer = DonationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        donation = serializer.save(donor=request.user)

        return Response(
            {
                "message": "Donation created successfully",
                "data": DonationSerializer(donation).data
            },
            status=status.HTTP_201_CREATED
        )
 # List Donation
 
class DonationListView(APIView): 
 permission_classes = [permissions.IsAuthenticated]
 def get(self, request):
        donations = Donation.objects.select_related('donor', 'project').all().order_by('-created_at')

        donation_filter = DonationFilter(request.GET, queryset=donations)
        donations = donation_filter.qs

        paginator = StandardPagination()
        paginated = paginator.paginate_queryset(donations, request)

        serializer = DonationSerializer(paginated, many=True)
        return paginator.get_paginated_response(serializer.data)
 
# My Donations
class MyDonationsView(APIView):
     permission_classes=[permissions.IsAuthenticated]
     def get(self, request):
        user = request.user
        donations = Donation.objects.filter(donor=user).select_related('project').order_by('-created_at')

        donation_filter = DonationFilter(request.GET, queryset=donations)
        donations = donation_filter.qs

        paginator = StandardPagination()
        paginated = paginator.paginate_queryset(donations, request)

        serializer = DonationSerializer(paginated, many=True)
        return paginator.get_paginated_response(serializer.data)  

# Project Donations
class ProjectDonationsView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def get(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)
        donations = Donation.objects.filter(project=project).order_by('-created_at')

        donation_filter = DonationFilter(request.GET, queryset=donations)
        donations = donation_filter.qs

        paginator = StandardPagination()
        paginated = paginator.paginate_queryset(donations, request)

        serializer = DonationSerializer(paginated, many=True)
        return paginator.get_paginated_response(serializer.data)   

 # Donation Detail
class DonationDetailView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def get(self, request, donation_id):
        donation = get_object_or_404(Donation, id=donation_id)
        serializer = DonationSerializer(donation)
        return Response(serializer.data)

  # project donations summary
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
    
  # Top Donors for a project
class TopDonorsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)

        donors = (
            Donation.objects.filter(project=project)
            .annotate(
                email=F('donor__email'),
                full_name=Concat(
                    F('donor__first_name'),
                    Value(' '),
                    F('donor__last_name')
                )
            )
            .values('email', 'full_name')
            .annotate(total=Sum('amount'))
            .order_by('-total')[:5]
        )

        return Response(donors)
    
# Recent Donations
class RecentDonationsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        donations = Donation.objects.all().order_by('-created_at')

        paginator = SmallPagination()
        paginated = paginator.paginate_queryset(donations, request)

        serializer = DonationSerializer(paginated, many=True)
        return paginator.get_paginated_response(serializer.data) 
     

