from django.shortcuts import render
from .models import City, Weather
from django.utils import timezone
from .forms import CityForm

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

    if request.method == "POST":
        form = CityForm(request.POST)
        if form.is_valid():
            #city = form.save(commit=False)
            form.save()
            #city.country = get_country(city.name)
            #city.save()
        else:
            print(form.errors)  # Print form errors for debugging

    form = CityForm()
    weather_list = []
    citys = City.objects.all()

    #print(citys)
    for city in citys:
        try:
            response = requests.get(url.format(city.name, api_key)).json()
            if response.get('cod') == 200:
                weather = {
                    "city" : city,
                    "temperature" : response['main']['temp'],
                    "description" : response['weather'][0]['description'],
                    #"icon" : response['weather'][0]['icon']
                    }
                weather_list.append(weather)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
    context = {"weather_list" : weather_list, 'form' : form}
    #print(json.dumps(response, indent=4))
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