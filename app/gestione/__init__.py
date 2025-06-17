from flask import Blueprint

gestione = Blueprint("gestione", __name__, template_folder="templates")

from . import routes
