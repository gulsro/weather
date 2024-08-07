from django.urls import path
from . import views

app_name = "main"
urlpatterns = [
    path('home/', views.home, name="home"), #welcome
    path('search/', views.search, name="search"), #views.search is referencable with name=
    path('citys/', views.CityListView.as_view(), name='citys'), #list of cities i have
    path('city/<int:pk>', views.CityDetailView.as_view(), name='city_detail'), #detail view of a city
]