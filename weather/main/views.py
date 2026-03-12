from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from .models import City
from django.utils import timezone
from .forms import CityForm
from django.views.generic import ListView, DetailView
from .decorators import keycloak_login_required
import requests, json

from django.contrib import messages


# To use API_KEY
from django.conf import settings

from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

#https://github.com/django/django/blob/main/django/views/generic/list.py
class CityListView(ListView):
    model = City

    def dispatch(self, request, *args, **kwargs):
        # Protect the list view: redirect to home if not logged in
        if not request.session.get("access_token"):
            return redirect("main:home")
        return super().dispatch(request, *args, **kwargs)

# detail_list.html and main.html are actually same
#any other way to combine them? dry dry dry
class CityDetailView(DetailView):
    model = City

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get("access_token"):
            return redirect("main:home")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        #retrieves the existing context prepared by DetailView
        context = super().get_context_data(**kwargs)
        city = self.get_object()
        weather = {
            "city": city.name,
            "temperature": city.temperature,
            "description": city.description,
            "icon": city.icon
        }
        context["weather"] = weather
        return context

       

def home(request):
    """
    Public landing page.
    - If the user is already logged in: show their username + a logout button.
    - If not logged in: show a login with k/eycloak button.
    """
    userinfo = request.session.get("userinfo")
    context = {
        "title":    "WEATHER APP",
        "userinfo": userinfo,
    }
    return render(request, "main/home.html", context)

@keycloak_login_required
def search(request):
    api_key = settings.API_KEY
    url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}"

    weather_list = []
    #unbound form, no data to bound
    form = CityForm()
    context = {
        "weather_list": weather_list,
        "form":         form,
        "userinfo":     request.session.get("userinfo"),
    }
    #read about Post/Redirect/Get PRG pattern! remember httpRedirect 

    if request.method == "POST":
         # csrf token is automatically checked by the middleware
        
        #Create a form instance from POST data.
        #bound data, not validated yet
        #cleaned_data() get the content(after validation)
        form = CityForm(request.POST)
        #validated form data will be in the form.cleaned_data dictionary
        if form.is_valid():
            #get cityname from validated bound data
            name = form.cleaned_data["name"]
            print(name)
            #check if data already exist in db
            if City.objects.filter(name=name).exists():
                messages.error(request, f"The city {name} already exists in the database.")
            else:
                response = requests.get(url.format(name, api_key)).json()
                #import pdb;pdb.set_trace()
                if response.get('cod') == 200:
                    city = City(
                        name = name,
                        temperature = response['main']['temp'],
                        description = response['weather'][0]['description'],
                        icon = response['weather'][0]['icon']
                    )
                    city.save()
                    weather = {
                        "city" : city.name,
                        "temperature" : city.temperature,
                        "description" : city. description,
                        "icon" : city.icon
                        }
                    weather_list.append(weather)
                    context = {
                        "weather_list": weather_list,
                        "form":         form,
                        "userinfo":     request.session.get("userinfo"),
                    }
            #city.country = get_country(city.name)

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


