from flask import Blueprint, redirect, render_template, request, url_for

from app.services.sheets_api import (
    add_data_ingresso,
    add_ingresso,
    get_categorie,
    get_ingressi,
    update_ingresso,
)
from app.services.google_auth import login_is_required
from flask import current_app
from datetime import datetime

from app.services.tools import prepare_data


ingressibp = Blueprint(
    "ingressi",
    __name__,
    template_folder="templates/ingressi",
    url_prefix="/<file_id>/ingressi",
)


@ingressibp.route("/", methods=["GET"])
@login_is_required
def ingressi(file_id):
    ingressi = get_ingressi(file_id)
    oggi = datetime.now().strftime(current_app.config["FORM_DATE_FORMAT"])
    categorie = get_categorie(file_id)
    return render_template(
        "ingressi.html",
        file_id=file_id,
        ingressi=ingressi,
        oggi=oggi,
        categorie=categorie,
    )


@ingressibp.route("/salva_data", methods=["POST"])
@login_is_required
def salva_data(file_id):
    ingresso_id = request.form.get("ingresso_id")
    data = request.form.get("data")

    print("Salvataggio data ingresso:", ingresso_id, data)

    add_data_ingresso(file_id, ingresso_id, data)

    return redirect(request.referrer)


@ingressibp.route("/modifica", methods=["POST"])
@login_is_required
def modifica(file_id):
    ingresso_id = request.form.get("ingresso_id")
    attributo = request.form.get("attributo")
    valore = request.form.get("valore")

    update_ingresso(file_id, ingresso_id, attributo, valore)

    return redirect(request.referrer)


@ingressibp.route("/aggiungi", methods=["POST"])
@login_is_required
def aggiungi(file_id):
    data = request.form.get("data")
    descrizione = request.form.get("descrizione")
    euro = request.form.get("euro")
    categoria = request.form.get("categoria")
    mese = request.form.get("mese")
    print("Aggiungo ingresso:", data, descrizione, euro, categoria, mese)

    # Estrai anno e mese dalla data
    mese_anno_parsed = datetime.strptime(mese, current_app.config["FORM_MONTH_FORMAT"])
    anno = mese_anno_parsed.year
    mese = mese_anno_parsed.month
    data_google = ""

    if data:
        data_parsed = datetime.strptime(data, current_app.config["FORM_DATE_FORMAT"])
        data_google = prepare_data(data_parsed)

    ingresso = {
        "data": data_google,
        "euro": euro,
        "descrizione": descrizione,
        "categoria": categoria,
        "mese": mese,
        "anno": anno,
        "note": "",
        "conto": "",
    }

    add_ingresso(file_id, ingresso)

    return redirect(request.referrer)
