from django.shortcuts import render

# When we ask weather, we need an function sends request to
# WeatherAPI to get a weather response, response will be
# in JSON format?, also urllib is needed?

import requests, json

def main(request):
    url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid=90fdc1f0beb1ae5812273c9b26256614"
    #city = "Las Vegas"
    city = "Kayseri"
    city_weather = requests.get(url.format(city)).json()
    weather = {
        "city" : city,
        "temperature" : city_weather["main"]["temp"],
        'description' : city_weather['weather'][0]['description'],
        'icon' : city_weather['weather'][0]['icon']
    }
    context = {"weather" : weather}
    print(json.dumps(city_weather, indent=4))
    return render(request, 'main/main.html', context)