from django.core.mail import EmailMessage
from django.dispatch import receiver
from django.template.loader import render_to_string
from django_rest_passwordreset.signals import reset_password_token_created
from django.conf import settings

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    # Frontend: fixed the hared codded http://localhost:5173 , Dynamically pulled from settings!
    reset_url = f"{settings.FRONTEND_URL}/reset-password/{reset_password_token.key}/"   
    
    message = f"Hi {reset_password_token.user.first_name},\n\nClick the link below to reset your password:\n{reset_url}\n\nIf you didn't request this, please ignore this email."

    email = EmailMessage(
        "Password Reset for Nile Fund",
        message,
        to=[reset_password_token.user.email]
    )
    email.send()