from flask import redirect, render_template, request, url_for

from app.services.tools import parse_date
from . import gestione
from app.services.sheets_api import (
    add_data_ingresso,
    add_ingresso,
    add_spesa,
    get_categorie,
    get_ingressi,
    get_spese_from_file,
    get_spreadsheet_name,
    update_ingresso,
)
from app.services.google_auth import login_is_required
from flask import current_app
from datetime import datetime


@gestione.route("/gestione/<file_id>", methods=["GET", "POST"])
@login_is_required
def visualizza_spese(file_id):

    title = get_spreadsheet_name(file_id)
    spese = get_spese_from_file(file_id)
    descrizione = request.form.get("descrizione", "").lower()
    categoria = request.form.get("categoria", "").lower()
    data_da = request.form.get("data_da", "").lower()
    data_a = request.form.get("data_a", "").lower()
    print("Query:", descrizione, categoria, data_da, data_a)

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
        if data_da_date and (not s["data_value"] or data_da_date > s["data_value"]):
            continue
        if data_a_date and (not s["data_value"] or data_a_date < s["data_value"]):
            continue
        filtrate.append(s)

    categorie = get_categorie(file_id)
    return render_template(
        "gestione.html",
        spese=filtrate,
        file_id=file_id,
        categorie=categorie,
        title=title,
    )


@gestione.route("/gestione/<file_id>/aggiungi_spesa", methods=["GET"])
@login_is_required
def aggiungi_spesa_form(file_id):
    categorie = get_categorie(file_id)
    return render_template("aggiungi_spesa.html", file_id=file_id, categorie=categorie)


@gestione.route("/gestione/<file_id>/aggiungi_spesa", methods=["POST"])
@login_is_required
def aggiungi_spesa(file_id):
    data = request.form.get("data")
    descrizione = request.form.get("descrizione")
    euro = request.form.get("euro")
    categoria = request.form.get("categoria")

    # Estrai anno e mese dalla data
    data_parsed = datetime.strptime(data, current_app.config["FORM_DATE_FORMAT"])
    data_google = data_parsed.strftime(current_app.config["GOOGLE_SHEET_DATE_FORMAT"])

    nuova_spesa = {
        "data": data_google,
        "euro": euro,
        "descrizione": descrizione,
        "categoria": categoria,
    }

    add_spesa(file_id, nuova_spesa)

    return redirect(url_for("gestione.visualizza_spese", file_id=file_id))


@gestione.route("/gestione/<file_id>/ingressi", methods=["GET"])
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


@gestione.route("/gestione/<file_id>/salva_data_ingresso", methods=["POST"])
@login_is_required
def salva_data_ingresso(file_id):
    ingresso_id = request.form.get("ingresso_id")
    data = request.form.get("data")

    print("Salvataggio data ingresso:", ingresso_id, data)

    add_data_ingresso(file_id, ingresso_id, data)

    return redirect(url_for("gestione.ingressi", file_id=file_id))


@gestione.route("/gestione/<file_id>/modifica_ingresso", methods=["POST"])
@login_is_required
def modifica_ingresso(file_id):
    ingresso_id = request.form.get("ingresso_id")
    attributo = request.form.get("attributo")
    valore = request.form.get("valore")

    update_ingresso(file_id, ingresso_id, attributo, valore)

    return redirect(url_for("gestione.ingressi", file_id=file_id))


@gestione.route("/gestione/<file_id>/aggiungi_ingresso", methods=["POST"])
@login_is_required
def aggiungi_ingresso(file_id):
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
        data_google = data_parsed.strftime(
            current_app.config["GOOGLE_SHEET_DATE_FORMAT"]
        )

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

    return redirect(url_for("gestione.ingressi", file_id=file_id))
