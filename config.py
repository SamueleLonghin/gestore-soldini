import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev_key")
    APP_PORT = os.environ.get("APP_PORT", 5000)
    OAUTH_REDIRECT_URI = os.environ.get(
        "OAUTH_REDIRECT_URI", "http://localhost:5000/oauth2callback"
    )
    GOOGLE_DISCOVERY_URL = (
        "https://accounts.google.com/.well-known/openid-configuration"
    )
    SERVICE_ACCOUNT_FILE = os.environ.get(
        "SERVICE_ACCOUNT_FILE", "service_account.json"
    )
    FORM_DATE_FORMAT = os.environ.get("FORM_DATE_FORMAT", "%Y-%m-%d")
    FORM_MONTH_FORMAT = os.environ.get("FORM_MONTH_FORMAT", "%Y-%m")
    GOOGLE_SHEET_DATE_FORMAT = os.environ.get("GOOGLE_SHEET_DATE_FORMAT", "ciao")
    DB_DATE_FORMAT = os.environ.get("DB_DATE_FORMAT", "%Y-%m-%d")
    DISPLAY_DATE_FORMAT = os.environ.get("DISPLAY_DATE_FORMAT", "%d/%m/%Y")
    SHEET_TAB_SPESE_RICORRENTI = os.environ.get(
        "SHEET_TAB_SPESE_RICORRENTI", "ELENCO SPESE RICORRENTI"
    )
    SHEET_RANGE_SPESE_RICORRENTI = os.environ.get(
        "SHEET_RANGE_SPESE_RICORRENTI", "A2:F"
    )
    SHEET_TAB_SPESE = os.environ.get("SHEET_TAB_SPESE", "SPESE")
    SHEET_RANGE_SPESE = os.environ.get("SHEET_RANGE_SPESE", "A2:F")
    SHEET_TAB_INGRESSI = os.environ.get("SHEET_TAB_INGRESSI", "INGRESSI")
    SHEET_RANGE_INGRESSI = os.environ.get("SHEET_RANGE_INGRESSI", "A2:F")
