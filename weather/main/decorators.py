"""
A simple decorator that checks for a keycloak access token in the django session.
If the user is not logged in they are redirected to home to click the login button.
"""

from functools import wraps
from django.shortcuts import redirect


def keycloak_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get("access_token"):
            return redirect("main:home")
        return view_func(request, *args, **kwargs)
    return wrapper
