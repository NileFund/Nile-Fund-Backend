import os
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

from rest_framework import status, views
from rest_framework.response import Response
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from django.db import transaction

from .serializers import UserRegistrationSerializer, UserProfileSerializer, DeleteAccountSerializer

User = get_user_model()


def send_activation_email(user_email, user_first_name, activation_link):
    try:
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = os.environ.get('BREVO_API_KEY')

        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
            sib_api_v3_sdk.ApiClient(configuration)
        )

        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=[{"email": user_email, "name": user_first_name}],
            subject="Activate your Nile Fund account",
            text_content=f"Hi {user_first_name},\n\nPlease click on the link below to activate your account:\n{activation_link}\n\nThis link will expire in 24 hours.",
            sender={"name": "FundEgypt", "email": os.environ.get('EMAIL_HOST_USER')}
        )

        api_instance.send_transac_email(send_smtp_email)
    except ApiException as e:
        print(f"Brevo email error: {e}")


class RegisterView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                user = serializer.save()
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                activation_link = f"{settings.FRONTEND_URL}/activate/{uid}/{token}"

            # Send email — if it fails, registration still succeeds
            send_activation_email(user.email, user.first_name, activation_link)

            return Response(
                {"message": "Registration successful! Please check your email to activate your account."},
                status=status.HTTP_201_CREATED
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
        serializer.is_valid(raise_exception=True)

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