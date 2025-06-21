from flask import redirect, render_template, request, url_for

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
        # title = get_ges(file_id)
        # if title:
        #     current_app.jinja_env.globals["title"] = title
        pass


@gestionebp.route("/<id>", methods=["GET"])
@login_is_required
def gestione(id):
    spese = get_spese(id)
    categorie = get_categorie(id)
    mese = {"spese": 0, "ingressi": 0, "ingressi_previsti": 0}
    anno = {"spese": 0, "ingressi": 0, "ingressi_previsti": 0}

    return render_template(
        "dashboard.html",
        spese=spese,
        categorie=categorie,
        mese=mese,
        anno=anno,
    )
