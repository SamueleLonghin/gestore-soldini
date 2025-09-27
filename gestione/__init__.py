from flask import Blueprint
from datetime import datetime
from flask import render_template, request
from db.gestione import *
from db.spese import get_spese
from db.categorie import get_categorie
from services.google_auth import login_is_required
from flask import current_app


gestionebp = Blueprint(
    "gestione", __name__, template_folder="templates", url_prefix="/gestione"
)

from . import ricorrenti
from . import ingressi
from . import spese

gestionebp.register_blueprint(ricorrenti.ricorrentibp)
gestionebp.register_blueprint(ingressi.ingressibp)
gestionebp.register_blueprint(spese.spesebp)


@gestionebp.before_request
def before_request():
    print("Svolgo before gestione", request.view_args)
    gestione_id = request.view_args.get("id_gestione", None) if request.view_args else None
    current_app.jinja_env.globals["gestione_id"] = gestione_id
    
    if gestione_id:
        g = get_gestione(gestione_id)
        # todo controllare la proprietà
        if g:
            current_app.jinja_env.globals["title"] = g.get("nome")
        else:
            return "Errore 403"
        # if title:
        pass


@gestionebp.route("/<id_gestione>", methods=["GET"])
@login_is_required
def gestione(id_gestione):
    spese = get_spese(id_gestione)
    categorie = get_categorie(id_gestione)
    oggi = datetime.now()
    mese = {
        "spese": get_somma_spese_mese(id_gestione, oggi.month, oggi.year),
        "ingressi": get_somma_ingressi_ricevuti_mese(id_gestione, oggi.month, oggi.year),
        "ingressi_previsti": get_somma_ingressi_previsti_mese(
            id_gestione, oggi.month, oggi.year
        ),
    }
    anno = {"spese": 0, "ingressi": 0, "ingressi_previsti": 0}

    return render_template(
        "dashboard.html",
        spese=spese,
        categorie=categorie,
        mese=mese,
        anno=anno,
    )


@gestionebp.route("/<id_gestione>/api/mese", methods=["GET"])
@login_is_required
def dati_mese(id_gestione):
    previsti = 0
    effettivi = 0
    spese = 0
    return {"ingressi_previsti": previsti, "ingressi": effettivi, "spese": spese}
