import google.auth.transport.requests
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from googleapiclient.discovery import build
from flask import current_app, session


def get_drive_service_oauth():
    credentials = Credentials(**session["credentials"])
    credentials.refresh(google.auth.transport.requests.Request())
    return build("drive", "v3", credentials=credentials)


def get_drive_service_service_account():
    creds = service_account.Credentials.from_service_account_file(
        current_app.config["SERVICE_ACCOUNT_FILE"],
        scopes=["https://www.googleapis.com/auth/drive.readonly"],
    )
    return build("drive", "v3", credentials=creds)
