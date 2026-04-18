from rest_framework import status, views
from rest_framework.response import Response
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings

from .serializers import UserRegistrationSerializer, UserProfileSerializer, DeleteAccountSerializer
from rest_framework.exceptions import ValidationError
from django.db import transaction

User = get_user_model()

class RegisterView(views.APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    user = serializer.save()
                    
                    current_site = get_current_site(request)
                    mail_subject = 'Activate your Nile Fund account'
                    
                    uid = urlsafe_base64_encode(force_bytes(user.pk))
                    token = default_token_generator.make_token(user)
                    
                    # Frontend: fixed the hared codded http://localhost:5173 , Dynamically pulled from settings!
                    activation_link = f"{settings.FRONTEND_URL}/activate/{uid}/{token}/"
                    
                    message = f"Hi {user.first_name},\n\nPlease click on the link below to activate your account:\n{activation_link}\n\nThis link will expire in 24 hours."
                    
                    email = EmailMessage(mail_subject, message, to=[user.email])
                    email.send()
                    
                return Response(
                    {"message": "Registration successful! Please check your email to activate your account."},
                    status=status.HTTP_201_CREATED
                )
            except Exception as e:
                # This catches email sending errors and triggers a transaction rollback
                print(f"REGISTRATION ERROR: {str(e)}")
                return Response(
                    {"error": f"Failed to send activation email: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class ActivateAccountView(views.APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({"message": "Account activated successfully!"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Activation link is invalid or expired!"}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        serializer = UserProfileSerializer(instance=request.user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            
            token.blacklist()

            return Response(
                {"message": "Logged out successfully. Token blacklisted."}, 
                status=status.HTTP_205_RESET_CONTENT
            )
        except Exception:
            return Response(
                {"error": "Invalid token or already logged out."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        


class DeleteAccountView(views.APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        serializer = DeleteAccountSerializer(data=request.data, context={'request': request})
        
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            # Check if this is our 10-attempt lockout trigger
            if 'action' in e.detail and 'terminate_session' in e.detail['action']:
                # Blacklist the token
                try:
                    refresh_token = request.data.get("refresh")
                    if refresh_token:
                        token = RefreshToken(refresh_token)
                        token.blacklist()
                except Exception:
                    pass
                
                # Send the 403 Forbidden back to React
                return Response(
                    {"action": "terminate_session", "message": "Security limit reached."},
                    status=status.HTTP_403_FORBIDDEN
                )
            # If it's a normal wrong password, raise the standard error
            raise e

        # Standard deletion logic (runs only if password is correct)
        user = request.user
        user.is_active = False
        user.save()

        try:
            refresh_token = request.data.get("refresh")
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
        except Exception:
            pass

        return Response(
            {"message": "Account has been successfully deactivated."},
            status=status.HTTP_204_NO_CONTENT
        )