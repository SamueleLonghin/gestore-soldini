from flask import redirect, render_template, request, url_for

from app.services.tools import parse_date
from . import gestione
from app.services.sheets_api import (
    add_spesa,
    get_categorie,
    get_spese_from_file,
    get_spreadsheet_name,
)
from app.services.google_auth import login_is_required
from flask import current_app
from datetime import datetime


@gestione.route("/gestione/<file_id>")
@login_is_required
def visualizza_spese(file_id):
    title = get_spreadsheet_name(file_id)
    spese = get_spese_from_file(file_id)
    query = request.args.get("q", "").lower()
    categoria = request.args.get("categoria", "")
    data_da = request.args.get("data_da", "")
    data_a = request.args.get("data_a", "")

    data_da_date = (
        parse_date(data_da, current_app.config["FORM_DATE_FORMAT"]) if data_da else None
    )
    data_a_date = (
        parse_date(data_a, current_app.config["FORM_DATE_FORMAT"]) if data_a else None
    )

    filtrate = []
    for s in spese:
        if query and query not in s["descrizione"].lower():
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

    # Esempio di utilizzo:
    # file_id = "1A2B3C4D5E6F7G8H9I0J"  # Sostituisci con il tuo file_id reale
    # nuova_spesa = ["01/06/2024", "Giugno", "2024", "50", "Cena fuori", "Ristorante"]
    add_spesa(file_id, nuova_spesa)

    return redirect(url_for("gestione.visualizza_spese", file_id=file_id))
