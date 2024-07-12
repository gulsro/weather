from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from .models import City
from django.utils import timezone
from .forms import CityForm
from django.views.generic import ListView
import requests, json

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
    form = CityForm()
    context = {"weather_list" : weather_list, 'form' : form}

    #read about Post/Redirect/Get PRG pattern! remember httpRedirect 

    if request.method == "POST":
         # csrf token is automatically checked by the middleware
        
        #Create a form instance from POST data.
        form = CityForm(request.POST)
        if form.is_valid():
            #city = form.save(commit=False)
            city = form.save()
            response = requests.get(url.format(city.name, api_key)).json()
            if response.get('cod') == 200:
                weather = {
                    "city" : city.name,
                    "temperature" : response['main']['temp'],
                    "description" : response['weather'][0]['description'],
                    #"icon" : response['weather'][0]['icon']
                    }
                weather_list.append(weather)
            context = {"weather_list" : weather_list, 'form' : form}
            #return redirect("main")
            #city.country = get_country(city.name)
            #city.save()

        else:
            print(form.errors)  # Print form errors for debugging
    # else:
    #     form = BlockForm()

    return render(request, 'main/main.html', context)
    #form = BlockForm()

    #print(citys)
    # else:
    #     blocks = Block.objects.all()
    #     for block in blocks:
    #         try:
    #             #could be replaced w/ get_object_or_404()
    #             response = requests.get(url.format(block.city, api_key)).json()
    #             if response.get('cod') == 200:
    #                 weather = {
    #                     "city" : block.city,
    #                     #"temperature" : response['main']['temp'],
    #                     #"description" : response['weather'][0]['description'],
    #                     #"icon" : response['weather'][0]['icon']
    #                     }
    #                 weather_list.append(weather)
    #         except requests.exceptions.RequestException as e:
    #             raise SystemExit(e)
    #     context = {"weather_list" : weather_list, 'form' : form}
    # #print(json.dumps(response, indent=4))
    # return render(request, 'main/main.html', context)


def get_country(city_name):
    geolocator = Nominatim(user_agent="weather_app")
    try:
        location = geolocator.geocode(city_name)
        if location:
            return location.address.split(',')[-1].strip()  # Extract the country from the address
    except (GeocoderTimedOut, GeocoderServiceError) as e:
        print(f"Geocoding error: {e}")
    return "Unknown"


