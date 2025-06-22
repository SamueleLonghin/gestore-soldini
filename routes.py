from flask import Blueprint, render_template, redirect, request, session, url_for
from db.db_interface import get_or_create_user
from db.gestione import create_gestione, get_gestioni
from services.google_auth import login_is_required, get_user_info, oauth_flow, credentials_to_dict


main = Blueprint("main", __name__)


@main.route("/")
@login_is_required
def index():
    user = session["user"]
    gestioni = get_gestioni(user["user_id"])
    if len(gestioni) == 0:
        gestione_name = f"Gestione Spese - {user['name']}"
        create_gestione(user["user_id"], gestione_name)
        gestioni = get_gestioni(user["user_id"])
    # files = get_shared_files_with_user(user.get("email"))
    print("Gestioni:", gestioni)
    return render_template("gestioni.html", user=user, gestioni=gestioni)


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
    google_user = get_user_info()
    session["user"] = google_user
    print(session["user"])
    app_user_id = get_or_create_user(google_user["email"])
    session["user"]["user_id"] = app_user_id
    return redirect(url_for("main.index"))
