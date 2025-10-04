from django.shortcuts import render
from geopy.geocoders import Nominatim

# Create your views here.
def home_page(request):
    return render(request,'index.html')

def track_location(request):
    location_data = None
    error = None

    if request.method == "POST":
        location_name = request.POST.get("location")
        if location_name:
            try:
                geolocator = Nominatim(user_agent="carbon_tracker_app")
                location = geolocator.geocode(location_name)

                if location:
                    location_data = {
                        "name": location_name,
                        "latitude": location.latitude,
                        "longitude": location.longitude,
                        "address": location.address
                    }
                else:
                    error = "Location not found. Please try again."
            except Exception as e:
                error = f"Error occurred: {str(e)}"

    return render(request, "Guest.html", {
        "location_data": location_data,
        "error": error
    })