from datetime import date, datetime


def init_template_filters(app):
    @app.template_filter("date_display")
    def date_display(value):
        if isinstance(value, str) and value != "":
            value = datetime.strptime(value, app.config["DB_DATE_FORMAT"])

        if isinstance(value, datetime) or isinstance(value, date):
            return value.strftime(app.config["DISPLAY_DATE_FORMAT"])

        return value

    @app.template_filter("date_form")
    def date_form(value):
        if isinstance(value, str):
            value = datetime.strptime(value, app.config["DB_DATE_FORMAT"])

        if isinstance(value, datetime) or isinstance(value, date):
            return value.strftime(app.config["FORM_DATE_FORMAT"])
        return value
