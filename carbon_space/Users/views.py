from django.shortcuts import render,redirect
from django.contrib.auth.models import User
<<<<<<< HEAD
from django.contrib.auth import authenticate, login, logout

=======
from django.contrib.auth import authenticate,login,logout
>>>>>>> 68af31982ee001cd5f19c86f942579716e934edc

# Create your views here.
def register(request):
    user=None
    error_msg=None
    if request.POST:
        name=request.POST["name"]
        uname=request.POST["username"]
        cmpny=request.POST["company"]
        email=request.POST["email"]
        passwd=request.POST["password"]
        try:
<<<<<<< HEAD
            # Existing user creation code
            user = User.objects.create_user(username=uname, password=passwd, email=email, first_name=name, last_name=cmpny)
            
        except Exception as e:
            error_msg = "Username Already Exists"
    return render(request, 'Register.html', {'User': user, 'Error_Message': error_msg})
=======
            user=User.objects.create_user(username=uname,password=passwd,email=email,first_name=name,last_name=cmpny)
        except Exception as e:
            error_msg="Username Already Exists"
    return render(request,'Register.html',{'User':user,'Error_Message':error_msg})
>>>>>>> 68af31982ee001cd5f19c86f942579716e934edc

def Login(request):
    error_msg=None
    if request.POST:
        uname=request.POST["username"]
        passwd=request.POST["password"]
        user=authenticate(username=uname,password=passwd)
        if user:
            login(request,user)
            return redirect('User_Data')
        else:
            error_msg="Invalid Credentials"
    return render(request,'login.html',{'Error_Message':error_msg})

def Logout(request):
    logout(request)
    return redirect('Home_Page')