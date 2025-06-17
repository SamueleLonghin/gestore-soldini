import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev_key")
    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
    GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"
    SHEET_ID = os.environ.get("SHEET_ID")
    SERVICE_ACCOUNT_FILE = os.environ.get("SERVICE_ACCOUNT_FILE", "service_account.json")
    FORM_DATE_FORMAT = os.environ.get("FORM_DATE_FORMAT", "%Y-%m-%d")
    FORM_MONTH_FORMAT = os.environ.get("FORM_MONTH_FORMAT", "%Y-%m")
    GOOGLE_SHEET_DATE_FORMAT = os.environ.get("GOOGLE_SHEET_DATE_FORMAT", "%d/%m/%Y")
