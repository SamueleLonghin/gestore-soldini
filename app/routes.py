from flask import Blueprint, render_template, redirect, request, session, url_for
from app.services.google_auth import login_is_required, get_user_info, oauth_flow

from app.services.drive_service import get_shared_files_with_user

main = Blueprint("main", __name__)


@main.route("/")
@login_is_required
def index():
    user = get_user_info()
    files = get_shared_files_with_user(user.get("email"))
    return render_template("gestioni.html", user=user, files=files)


@main.route("/login")
def login():
    flow = oauth_flow()
    authorization_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent",  # forza Google a mostrare il consenso ogni volta → rilascia refresh_token
    )
    session["state"] = state
    return redirect(authorization_url)


@main.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("main.index"))


@main.route("/oauth2callback")
def oauth2callback():
    flow = oauth_flow()
    flow.fetch_token(authorization_response=request.url)
    credentials = flow.credentials
    session["credentials"] = credentials_to_dict(credentials)
    return redirect(url_for("main.index"))


def credentials_to_dict(credentials):
    return {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes,
    }
