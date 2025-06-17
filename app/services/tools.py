from datetime import datetime


def parse_date(date_str, date_format):
    try:
        return datetime.strptime(date_str, date_format).date()
    except (ValueError, TypeError):
        return None
