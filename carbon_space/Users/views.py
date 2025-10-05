from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.conf import settings
import uuid
from .models import EmailVerification  # new model for email verification

# Create your views here.
def register(request):
    user = None
    error_msg = None
    if request.POST:
        name = request.POST["name"]
        uname = request.POST["username"]
        cmpny = request.POST["company"]
        email = request.POST["email"]
        passwd = request.POST["password"]
        try:
            # Existing user creation code
            user = User.objects.create_user(username=uname, password=passwd, email=email, first_name=name, last_name=cmpny, is_active=False)
            
            # NEW: Create email verification token
            verification = EmailVerification.objects.create(user=user, token=uuid.uuid4())
            
            # NEW: Send verification email
            verification_link = f"http://127.0.0.1:8000/verify/{verification.token}/"
            send_mail(
                "Verify your email",
                f"Hi {name}, please verify your email by clicking this link: {verification_link}",
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )

        except Exception as e:
            error_msg = "Username Already Exists"
    return render(request, 'Register.html', {'User': user, 'Error_Message': error_msg})


def verify_email(request, token):
    """NEW VIEW: Activate user when they click the verification link"""
    try:
        verification = EmailVerification.objects.get(token=token)
        verification.user.is_active = True
        verification.user.save()
        verification.delete()  # optional: remove token after verification
        return render(request, 'Login.html', {"message": "Email verified! You can now log in."})
    except EmailVerification.DoesNotExist:
        return render(request, 'Register.html', {"Error_Message": "Invalid verification link."})


def Login(request):
    error_msg = None
    if request.POST:
        uname = request.POST["username"]
        passwd = request.POST["password"]
        user = authenticate(username=uname, password=passwd)
        if user:
            if user.is_active:
                login(request, user)
                return redirect('User_Data')
            else:
                error_msg = "Please verify your email first."
        else:
            error_msg = "Invalid Credentials"
    return render(request, 'login.html', {'Error_Message': error_msg})


def Logout(request):
    logout(request)
    return redirect('Home_Page')
