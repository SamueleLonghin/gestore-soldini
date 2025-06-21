from flask import Blueprint, render_template, request, redirect, session
from app.db.categorie import get_categorie
from app.services.tools import add_args_to_url, parse_date, prepare_data

from app.db.spese import *
from app.services.google_auth import login_is_required
from flask import current_app
from datetime import datetime

spesebp = Blueprint(
    "spese", __name__, template_folder="templates/spese", url_prefix="/<id>/spese"
)


@spesebp.route("/", methods=["GET", "POST"])
@login_is_required
def spese(id):

    spese = get_spese(id)
    descrizione = request.form.get("descrizione", "").lower()
    categoria = request.form.get("categoria", "").lower()
    data_da = request.form.get("data_da", "").lower()
    data_a = request.form.get("data_a", "").lower()

    data_da_date = (
        parse_date(data_da, current_app.config["FORM_DATE_FORMAT"]) if data_da else None
    )
    data_a_date = (
        parse_date(data_a, current_app.config["FORM_DATE_FORMAT"]) if data_a else None
    )

    filtrate = []
    for s in spese:
        if descrizione and descrizione not in s["descrizione"].lower():
            continue
        if categoria and categoria.lower() not in s["categoria"].lower():
            continue
        if data_da_date and (not s["data"] or data_da_date > s["data"]):
            continue
        if data_a_date and (not s["data"] or data_a_date < s["data"]):
            continue
        filtrate.append(s)

    categorie = get_categorie(id)

    return render_template("spese.html", spese=filtrate, categorie=categorie)


@spesebp.route("/aggiungi", methods=["GET"])
@login_is_required
def form_aggiungi(id):
    categorie = get_categorie(id)
    return render_template("aggiungi_spesa.html", categorie=categorie)


@spesebp.route("/aggiungi", methods=["POST"])
@login_is_required
def aggiungi(id):
    user_id = session.get("user").get("user_id")

    data = request.form.get("data")
    descrizione = request.form.get("descrizione")
    importo = request.form.get("importo")
    categoria = request.form.get("categoria")

    # Estrai anno e mese dalla data
    data_parsed = datetime.strptime(data, current_app.config["FORM_DATE_FORMAT"])
    data_db = data_parsed.strftime(current_app.config["DB_DATE_FORMAT"])

    oggi = datetime.today()
    if data_parsed > oggi:
        return redirect(
            add_args_to_url(
                request.referrer,
                {"error": "La data non può essere successiva al giorno corrente"},
            )
        )

    nuova_spesa = {
        "data": data_db,
        "importo": importo,
        "descrizione": descrizione,
        "categoria": categoria,
    }

    aggiungi_spesa(user_id, id, nuova_spesa)

    return redirect(request.referrer)
