from django.urls import path
from . import views

app_name = "main"
urlpatterns = [
    path('main/', views.main),
    path('citys/', views.CityListView.as_view(), name='citys'),

]