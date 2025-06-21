from datetime import datetime, timedelta
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse


def parse_date(date_str, date_format):
    try:
        if date_format == "GOOGLE_SHEET_DATE_FORMAT":
            return google_sheets_serial_to_date(date_str)
        return datetime.strptime(date_str, date_format).date()
    except (ValueError, TypeError):
        return None


def google_sheets_serial_to_date(serial_number):
    epoch = datetime(1899, 12, 30)  # Google Sheets epoch
    return (epoch + timedelta(days=serial_number)).date()


def date_to_google_sheets_serial(date_obj):
    epoch = datetime(1899, 12, 30).date()  # Google Sheets epoch
    if isinstance(date_obj, datetime):
        date_obj = date_obj.date()
    return (date_obj - epoch).days


def prepare_data(value):
    return date_to_google_sheets_serial(value)


def add_args_to_url(url, args):
    url_parts = list(urlparse(url))
    query = parse_qs(url_parts[4])
    query.update(args)
    url_parts[4] = urlencode(query, doseq=True)
    return urlunparse(url_parts)
