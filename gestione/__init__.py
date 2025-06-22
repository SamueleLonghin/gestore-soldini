from flask import Blueprint

gestionebp = Blueprint(
    "gestione", __name__, template_folder="templates", url_prefix="/gestione"
)

from . import routes
from . import ricorrenti
from . import ingressi
from . import spese

gestionebp.register_blueprint(ricorrenti.ricorrentibp)
gestionebp.register_blueprint(ingressi.ingressibp)
gestionebp.register_blueprint(spese.spesebp)
