"""
Keycloak aut views for the Django weather app

Flow:

"""

import urllib.parse
import requests
from django.conf import settings
from django.shortcuts import redirect
from django.http import HttpResponse

#NOTE Same as keycloak-go-app
_BASE       = settings.KEYCLOAK_URL
# _AUTH_URL   = _BASE + "/protocol/openid-connect/auth"
# _TOKEN_URL  = _BASE + "/protocol/openid-connect/token"
# _LOGOUT_URL = _BASE + "/protocol/openid-connect/logout"

_AUTH_URL    = settings.KEYCLOAK_BROWSER_URL + "/protocol/openid-connect/auth"   # browser redirect
_TOKEN_URL   = _BASE + "/protocol/openid-connect/token"      # Django calls this directly
_LOGOUT_URL  = settings.KEYCLOAK_BROWSER_URL + "/protocol/openid-connect/logout" # browser redirect

def keycloak_login(request):
    """
    Build the Keycloak authorization URL and redirect the user there.
    Keycloak will show its login page, then redirect back to our callback.
    """
    params = {
        "client_id":     settings.KEYCLOAK_CLIENT_ID,
        "response_type": "code",
        "scope":         "openid email profile",
        "redirect_uri":  settings.KEYCLOAK_REDIRECT_URI,
    }
    return redirect(_AUTH_URL + "?" + urllib.parse.urlencode(params))


def keycloak_callback(request):
    """
    Keycloak redirects here after a successful login with ?code=<authorization_code>.
    We POST the code to Keycloak's token endpoint to get an access token,
    then store it in the Django session and redirect to the weather search page.
    """
    code = request.GET.get("code")
    if not code:
        return HttpResponse("Missing authorization code from Keycloak.", status=400)

    # Exchange the authorization code for tokens
    token_response = requests.post(
        _TOKEN_URL,
        data={
            "grant_type":    "authorization_code",
            "code":          code,
            "redirect_uri":  settings.KEYCLOAK_REDIRECT_URI,
            "client_id":     settings.KEYCLOAK_CLIENT_ID,
            "client_secret": settings.KEYCLOAK_CLIENT_SECRET,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=10,
    )

    if token_response.status_code != 200:
        return HttpResponse(
            f"Token exchange failed: {token_response.text}", status=500
        )

    token_data = token_response.json()

    # Store tokens in Django's server-side session (never exposed to the client)
    request.session["access_token"] = token_data.get("access_token")
    request.session["id_token"]     = token_data.get("id_token")

    # Also fetch and store basic user info so templates can show it
    userinfo_response = requests.get(
        _BASE + "/protocol/openid-connect/userinfo",
        headers={"Authorization": "Bearer " + request.session["access_token"]},
        timeout=10,
    )
    if userinfo_response.status_code == 200:
        request.session["userinfo"] = userinfo_response.json()

    # Redirect to the weather search page after successful login
    return redirect("main:search")

def keycloak_logout(request):
    """
    1. Clear the Django session.
    2. Redirect to Keycloak's logout endpoint so the SSO session is also ended.
       Keycloak will redirect the user back to /home/ afterwards.
    """
    id_token = request.session.get("id_token", "")
    request.session.flush()  # wipe everything from the Django session

    post_logout_uri = urllib.parse.quote("http://127.0.0.1:8000/home/", safe="")
    logout_url = (
        f"{_LOGOUT_URL}"
        f"?client_id={settings.KEYCLOAK_CLIENT_ID}"
        f"&id_token_hint={id_token}"
        f"&post_logout_redirect_uri={post_logout_uri}"
    )
    return redirect(logout_url)
