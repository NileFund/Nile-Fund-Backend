from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status , permissions
from rest_framework.permissions import AllowAny
from apps.accounts.models import User
from .serializers import DonationSerializer


class DonationCreateView(APIView):
     permission_classes = [permissions.IsAuthenticated]
    #permission_classes = [AllowAny]
     def post(self, request):
        serializer = DonationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
       
       # user = User.objects.get(id=6)
        #donation = serializer.save(donor=user)
        donation = serializer.save(donor=request.user)

        return Response(
            {
                "message": "Donation created successfully",
                "data": DonationSerializer(donation).data
            },
            status=status.HTTP_201_CREATED
        )