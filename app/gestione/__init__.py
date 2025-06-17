from flask import Blueprint

gestionebp = Blueprint("gestione", __name__, template_folder="templates")

from . import routes
