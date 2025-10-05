from django.shortcuts import render
from geopy.geocoders import Nominatim
from django.contrib.auth.decorators import login_required

# Create your views here.
def home_page(request):
    return render(request,'index.html')

@login_required(login_url='login/')
def user_data(request):
    return render(request,'User_Data.html')

def guest(request):
    return render(request,'Guest.html')

def dashboard(request):
    return render(request,'Dashboard.html')
