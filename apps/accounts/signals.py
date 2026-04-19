import os
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
from django.conf import settings


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    reset_url = f"{settings.FRONTEND_URL}/reset-password/{reset_password_token.key}"
    user = reset_password_token.user

    try:
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = os.environ.get('BREVO_API_KEY')

        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
            sib_api_v3_sdk.ApiClient(configuration)
        )

        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=[{"email": user.email, "name": user.first_name}],
            subject="Password Reset for Nile Fund",
            text_content=f"Hi {user.first_name},\n\nClick the link below to reset your password:\n{reset_url}\n\nIf you didn't request this, please ignore this email.",
            sender={"name": "FundEgypt", "email": os.environ.get('EMAIL_HOST_USER')}
        )

        api_instance.send_transac_email(send_smtp_email)
    except ApiException as e:
        print(f"Brevo email error: {e}")