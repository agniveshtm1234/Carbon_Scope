from django.shortcuts import render
from geopy.geocoders import Nominatim
import geopandas as gpd
import pandas as pd
import geodatasets
import folium
# Create your views here.
def home_page(request):
    return render(request,'index.html')

def track_location(request):
    location_data = None
    error = None

    if request.POST:
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

def all_data(request):

    # 1️⃣ Load the world map
    world = gpd.read_file(geodatasets.get_path('naturalearth.land'))

    # 2️⃣ Example AQI data
    aqi_data = pd.DataFrame({
        'name': ['India', 'China', 'United States', 'Brazil', 'Australia'],
        'AQI': [210, 180, 80, 120, 40]
    })

    # 3️⃣ Merge AQI data with the map
    world = world.merge(aqi_data, on='name', how='left')

    # 4️⃣ Define a color function based on AQI
    def get_color(aqi):
        if pd.isna(aqi):
            return 'gray'
        elif aqi > 150:
            return 'red'
        elif aqi > 75:
            return 'yellow'
        else:
            return 'green'

    # 5️⃣ Create a base map
    m = folium.Map(location=[20, 0], zoom_start=2, tiles='cartodb positron')

    # 6️⃣ Add GeoJSON layer with color styling
    folium.GeoJson(
        world,
        style_function=lambda feature: {
            'fillColor': get_color(feature['properties']['AQI']),
            'color': 'black',
            'weight': 0.5,
            'fillOpacity': 0.7,
        },
        tooltip=folium.GeoJsonTooltip(
            fields=['name', 'AQI'],
            aliases=['Country:', 'AQI:'],
            localize=True
        )
    ).add_to(m)

    # 7️⃣ Add a custom legend
    legend_html = '''
    <div style="
        position: fixed; 
        bottom: 30px; left: 30px; width: 180px; height: 130px; 
        border:2px solid grey; z-index:9999; font-size:14px;
        background-color:white; padding:10px;">
        <b>Air Quality Index (AQI)</b><br>
        <i style="background:green;width:20px;height:20px;float:left;margin-right:8px"></i> Low (≤75)<br>
        <i style="background:yellow;width:20px;height:20px;float:left;margin-right:8px"></i> Medium (76–150)<br>
        <i style="background:red;width:20px;height:20px;float:left;margin-right:8px"></i> High (>150)<br>
        <i style="background:gray;width:20px;height:20px;float:left;margin-right:8px"></i> No Data
    </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))

    # 8️⃣ Save to HTML file
    m.save("All_data.html")

    return render(request,'All_data.html')