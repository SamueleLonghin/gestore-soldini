from flask import Blueprint, render_template, request, redirect
from app.services.tools import parse_date, prepare_data

from app.services.sheets_api import (
    add_spesa,
    get_categorie,
    get_spese_from_file,
    get_spreadsheet_name,
)
from app.services.google_auth import login_is_required
from flask import current_app
from datetime import datetime

spesebp = Blueprint("spese", __name__, template_folder="templates/spese", url_prefix="/<file_id>/spese")


@spesebp.route("/", methods=["GET", "POST"])
@login_is_required
def spese(file_id):
    title = get_spreadsheet_name(file_id)
    spese = get_spese_from_file(file_id)
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

    categorie = get_categorie(file_id)

    return render_template(
        "spese.html", spese=filtrate, file_id=file_id, title=title, categorie=categorie
    )


@spesebp.route("/aggiungi", methods=["GET"])
@login_is_required
def form_aggiungi(file_id):
    categorie = get_categorie(file_id)
    return render_template("aggiungi_spesa.html", file_id=file_id, categorie=categorie)


@spesebp.route("/aggiungi", methods=["POST"])
@login_is_required
def aggiungi(file_id):
    data = request.form.get("data")
    descrizione = request.form.get("descrizione")
    euro = request.form.get("euro")
    categoria = request.form.get("categoria")

    # Estrai anno e mese dalla data
    data_parsed = datetime.strptime(data, current_app.config["FORM_DATE_FORMAT"])
    data_google = prepare_data(data_parsed)

    nuova_spesa = {
        "data": data_google,
        "euro": euro,
        "descrizione": descrizione,
        "categoria": categoria,
    }

    add_spesa(file_id, nuova_spesa)

    return redirect(request.referrer)
