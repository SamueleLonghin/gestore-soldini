from datetime import datetime
from flask import redirect, render_template, request, url_for

from app.db.gestione import *
from app.db.spese import get_spese
from app.services.tools import parse_date
from . import gestionebp
from app.db.categorie import get_categorie
from app.services.google_auth import login_is_required
from flask import current_app


@gestionebp.before_app_request
def before_request():
    print("Svolgo before gestione")
    gestione_id = request.view_args.get("id", None) if request.view_args else None
    current_app.jinja_env.globals["gestione_id"] = gestione_id
    if gestione_id:
        g = get_gestione(gestione_id)
        if g:
            current_app.jinja_env.globals["title"] = g.get("nome")
        # if title:
        pass


@gestionebp.route("/<id>", methods=["GET"])
@login_is_required
def gestione(id):
    spese = get_spese(id)
    categorie = get_categorie(id)
    oggi = datetime.now()
    mese = {
        "spese": get_somma_spese_mese(id, oggi.month, oggi.year),
        "ingressi": get_somma_ingressi_ricevuti_mese(id, oggi.month, oggi.year),
        "ingressi_previsti": get_somma_ingressi_previsti_mese(id, oggi.month, oggi.year),
    }
    anno = {"spese": 0, "ingressi": 0, "ingressi_previsti": 0}

    return render_template(
        "dashboard.html",
        spese=spese,
        categorie=categorie,
        mese=mese,
        anno=anno,
    )


@gestionebp.route("/<id>/api/mese", methods=["GET"])
@login_is_required
def dati_mese(id):
    previsti = 0
    effettivi = 0
    spese = 0
    return {"ingressi_previsti": previsti, "ingressi": effettivi, "spese": spese}
