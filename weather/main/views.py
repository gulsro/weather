from django.shortcuts import render
from .models import City, Weather
from django.utils import timezone
from .forms import CityForm
# When we ask weather, we need an function sends request to
# WeatherAPI to get a weather response, response will be
# in JSON format?, also urllib is needed?

import requests, json

# To use API_KEY
from django.conf import settings


def main(request):
    #city_name = ""
    api_key = settings.API_KEY
    url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}"

    #city = "Las Vegas"
    # try:
    #     response = requests.get(url.format(city)).json()
    # except requests.exceptions.RequestException as e:
    #     raise SystemExit(e)
    weather_list = []
    citys = City.objects.all()
    #print(citys)
    for city in citys:
        try:
            response = requests.get(url.format(city.name, api_key)).json()
            weather = {
                "city" : city,
                "temperature" : response['main']['temp'],
                'description' : response['weather'][0]['description'],
                'icon' : response['weather'][0]['icon']
                }
            weather_list.append(weather)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
    context = {"weather_list" : weather_list}
    print(json.dumps(response, indent=4))
    return render(request, 'main/main.html', context)




def get_city(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = CityForm(request.POST)
        # check whether it's valid:
        # if form.is_valid():
        #     # process the data in form.cleaned_data as required
        #     # ...
        #     # redirect to a new URL:
        #     return HttpResponseRedirect("/thanks/")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CityForm()

    return render(request, "city.html", {"form": form})