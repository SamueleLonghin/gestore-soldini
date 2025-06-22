import google.auth.transport.requests
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from flask import current_app, session, redirect, url_for
import functools


def oauth_flow():
    redirect_uri = current_app.config["OAUTH_REDIRECT_URI"]

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


def credentials_to_dict(credentials):
    return {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes,
    }
