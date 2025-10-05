from django.core.mail import send_mail
from django.conf import settings

def send_verification_email(user):
    subject = "Verify your email"
    verification_link = f"http://127.0.0.1:8000/users/verify/{user.verification_token}/"
    message = f"Hi {user.username},\n\nPlease verify your email by clicking this link: {verification_link}"
    
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,
    )
