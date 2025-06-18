from datetime import datetime, timedelta


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