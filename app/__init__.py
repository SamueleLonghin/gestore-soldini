from datetime import datetime, date
from flask import Flask
from dotenv import load_dotenv
from app.db.database import init_db

load_dotenv()


def create_app():
    app = Flask(__name__)

    init_db()

    @app.template_filter("date_display")
    def date_display(value):
        if isinstance(value, str):
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

    @app.template_filter("inverso")
    def inverso(s):
        return s[::-1]

    app.config.from_object("config.Config")

    # Rendi `attribute` disponibile nei template
    app.jinja_env.globals["attribute"] = getattr

    for k, v in app.config.items():
        print("Config: ", k, "->", v)

    from .routes import main

    app.register_blueprint(main)

    from .gestione import gestionebp

    app.register_blueprint(gestionebp)

    return app
