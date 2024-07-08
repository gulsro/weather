from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from .models import Block
from django.utils import timezone
from .forms import BlockForm
from django.views.generic import ListView
import requests, json

# To use API_KEY
from django.conf import settings

# To get county name of given city
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

def main(request):
    api_key = settings.API_KEY
    url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}"

    #city = "Las Vegas"
    # try:
    #     response = requests.get(url.format(city)).json()
    # except requests.exceptions.RequestException as e:
    #     raise SystemExit(e)


    weather_list = []
    #read about Post/Redirect/Get PRG pattern! remember httpRedirect 

    if request.method == "POST":
         # csrf token is automatically checked by the middleware
        
        #Create a form instance from POST data.
        form = BlockForm(request.POST)
        if form.is_valid():
            #city = form.save(commit=False)
            block = form.save()
            response = requests.get(url.format(block.city, api_key)).json()
            if response.get('cod') == 200:
                weather = {
                    "city" : block.city,
                    #"temperature" : response['main']['temp'],
                    #"description" : response['weather'][0]['description'],
                    #"icon" : response['weather'][0]['icon']
                    }
                weather_list.append(weather)
            context = {"weather_list" : weather_list, 'form' : form}
            #return redirect("main")
            #city.country = get_country(city.name)
            #city.save()

        else:
            print(form.errors)  # Print form errors for debugging

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


