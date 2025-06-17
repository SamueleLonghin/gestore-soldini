from flask import Flask
from flask_session import Session
from dotenv import load_dotenv

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    # Session(app)

    from .routes import main

    app.register_blueprint(main)

    from .gestione import gestione

    app.register_blueprint(gestione)

    return app
