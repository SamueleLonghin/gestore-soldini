from datetime import datetime, date
from flask import Flask
from dotenv import load_dotenv

load_dotenv()


def create_app():
    app = Flask(__name__)

    @app.template_filter("date_display")
    def date_display(value):
        print("Converto", value)
        if isinstance(value, datetime) or isinstance(value, date):
            return value.strftime(app.config["DISPLAY_DATE_FORMAT"])
        return value

    @app.template_filter("date_form")
    def date_form(value):
        if isinstance(value, datetime) or isinstance(value, date):
            return value.strftime(app.config["FORM_DATE_FORMAT"])
        return value

    @app.template_filter("inverso")
    def inverso(s):
        return s[::-1]

    app.config.from_object("config.Config")

    for k, v in app.config.items():
        print("Config: ", k, "->", v)

    from .routes import main

    app.register_blueprint(main)

    from .gestione import gestionebp

    app.register_blueprint(gestionebp)

    return app
