from django.shortcuts import render
from .models import City, Weather
from django.utils import timezone
# When we ask weather, we need an function sends request to
# WeatherAPI to get a weather response, response will be
# in JSON format?, also urllib is needed?

import requests, json

def main(request):
    url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid=90fdc1f0beb1ae5812273c9b26256614"
    #city = "Las Vegas"
    # try:
    #     response = requests.get(url.format(city)).json()
    # except requests.exceptions.RequestException as e:
    #     raise SystemExit(e)
    weather_list = []
    citys = City.objects.all()
    print(citys)
    for city in citys:
        try:
            response = requests.get(url.format(city.name)).json()
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        weather = {
            "city" : city,
            "temperature" : response["main"]["temp"],
            'description' : response['weather'][0]['description'],
            'icon' : response['weather'][0]['icon']
        }
        weather_list.append(weather)
    context = {"weather_list" : weather_list}
    print(json.dumps(response, indent=4))
    return render(request, 'main/main.html', context)