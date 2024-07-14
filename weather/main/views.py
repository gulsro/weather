from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from .models import City
from django.utils import timezone
from .forms import CityForm
from django.views.generic import ListView
import requests, json
#add messages to your views that can be displayed to users
from django.contrib import messages


# To use API_KEY
from django.conf import settings

# To get county name of given city
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

class CityListView(ListView):
    model = City

def home(request):
    context = {"title":"WEATHER APP"}
    return render(request, "main/home.html", context)


def search(request):
    api_key = settings.API_KEY
    url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}"

    weather_list = []
    #unbound form, no data to bound
    form = CityForm()
    context = {"weather_list" : weather_list, 'form' : form}

    #read about Post/Redirect/Get PRG pattern! remember httpRedirect 

    if request.method == "POST":
         # csrf token is automatically checked by the middleware
        
        #Create a form instance from POST data.
        #bound data, not validated yet
        #cleaned_data() get the content(after validation)
        form = CityForm(request.POST)
        #validated form data will be in the form.cleaned_data dictionary
        if form.is_valid():
            city = form.save()
            
            #get cityname from validated bound data
            name = form.cleaned_data["name"]
            print(name)
            #check if data already exist in db
            if City.objects.filter(name=name).exists():
                messages.error(request, f"The city {name} already exists in the database.")
            else:
                response = requests.get(url.format(city.name, api_key)).json()
                #import pdb;pdb.set_trace()
                if response.get('cod') == 200:
                    weather = {
                        "city" : city.name,
                        "temperature" : response['main']['temp'],
                        "description" : response['weather'][0]['description'],
                        #"icon" : response['weather'][0]['icon']
                        }
                    weather_list.append(weather)
            context = {"weather_list" : weather_list, 'form' : form}
            #city.country = get_country(city.name)
            city.save()

        else:
            print(form.errors)  # Print form errors for debugging
    # else:
    #     form = BlockForm()

    return render(request, 'main/main.html', context)


def get_country(city_name):
    geolocator = Nominatim(user_agent="weather_app")
    try:
        location = geolocator.geocode(city_name)
        if location:
            return location.address.split(',')[-1].strip()  # Extract the country from the address
    except (GeocoderTimedOut, GeocoderServiceError) as e:
        print(f"Geocoding error: {e}")
    return "Unknown"


