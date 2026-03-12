from django.urls import path
from . import auth_views

urlpatterns = [
    path('login/', auth_views.keycloak_login, name="keycloak_login"),
    path('callback/', auth_views.keycloak_callback, name="keycloak_callback"),
    path('logout/', auth_views.keycloak_logout, name="keycloak_logout")
]