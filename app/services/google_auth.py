import os
import google.auth.transport.requests
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from flask import session, redirect, url_for
import functools
from flask import request


def oauth_flow(state=None):
    import os

    redirect_uri = os.getenv(
        "OAUTH_REDIRECT_URI", "http://localhost:5000/oauth2callback"
    )

    flow = Flow.from_client_secrets_file(
        "credentials.json",
        scopes=[
            "openid",
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/userinfo.profile",
        ],
        redirect_uri=redirect_uri,
    )
    return flow


def login_is_required(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        if "credentials" not in session:
            return redirect(url_for("main.login"))
        return function(*args, **kwargs)

    return wrapper


def get_user_info():
    import requests

    credentials = Credentials(**session["credentials"])
    auth_req = google.auth.transport.requests.Request()
    credentials.refresh(auth_req)
    response = requests.get(
        "https://openidconnect.googleapis.com/v1/userinfo",
        headers={"Authorization": f"Bearer {credentials.token}"},
    )
    return response.json()
