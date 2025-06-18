from datetime import datetime
from flask import Blueprint, current_app, redirect, render_template, request
from app.services.google_auth import login_is_required
from app.services.sheets_api import (
    get_spese_ricorrenti,
    get_spreadsheet_name,
    get_categorie,
    add_ricorrente,
    update_ricorrente,
)
from app.services.tools import prepare_data

ricorrentibp = Blueprint(
    "ricorrenti",
    __name__,
    template_folder="templates/ricorrenti",
    url_prefix="/<file_id>/ricorrenti",
)


@ricorrentibp.route("/", methods=["GET"])
@login_is_required
def ricorrenti(file_id):
    """
    Visualizza le spese ricorrenti.
    """
    title = get_spreadsheet_name(file_id)
    ricorrenti = get_spese_ricorrenti(file_id)
    categorie = get_categorie(file_id)

    headers = {
        "nome": "Nome",
        "categoria": "Categoria",
        "data_inizio": "Data di Inizio:date",
        "tipo_ricorrenza": "Tipo di Ricorrenza:options:giorno|mese|anno",
        "euro": "Importo:number",
    }

    return render_template(
        "ricorrenti.html",
        ricorrenti=ricorrenti,
        file_id=file_id,
        title=title,
        categorie=categorie,
        headers=headers,
        rows=ricorrenti,
    )


@ricorrentibp.route("/modifica", methods=["POST"])
@login_is_required
def modifica(file_id):
    ricorrente_id = request.form.get("row_id")

    nome = request.form.get("nome")
    categoria = request.form.get("categoria")
    data = request.form.get("data_inizio", None)
    tipo_ricorrenza = request.form.get("tipo_ricorrenza")
    unita_ricorrenza = request.form.get("unita_ricorrenza")
    euro = request.form.get("euro")

    data_parsed = datetime.strptime(data, current_app.config["FORM_DATE_FORMAT"])
    data_google = prepare_data(data_parsed)
    print(f"Data convertita: {data} -> {data_google}")

    print(
        f"Modifico ricorrenza {ricorrente_id}: {nome}, {data_google}, {euro}, {categoria}, {tipo_ricorrenza}, {unita_ricorrenza}"
    )
    ricorrenza = {
        "nome": nome,
        "data": data_google,
        "euro": euro,
        "categoria": categoria,
        "tipo_ricorrenza": tipo_ricorrenza,
        "unita_ricorrenza": unita_ricorrenza,
    }
    update_ricorrente(file_id, ricorrente_id, ricorrenza)

    return redirect(request.referrer)


@ricorrentibp.route("/aggiungi", methods=["POST"])
@login_is_required
def aggiungi(file_id):
    nome = request.form.get("nome")
    categoria = request.form.get("categoria")
    data = request.form.get("data")
    tipo_ricorrenza = request.form.get("tipo_ricorrenza")
    unita_ricorrenza = request.form.get("unita_ricorrenza")
    euro = request.form.get("euro")

    data_parsed = datetime.strptime(data, current_app.config["FORM_DATE_FORMAT"])
    data_google = data_parsed.strftime(current_app.config["GOOGLE_SHEET_DATE_FORMAT"])
    print(f"Data convertita: {data} -> {data_google}")

    print(
        f"Aggiungo ricorrenza: {nome}, {data_google}, {euro}, {categoria}, {tipo_ricorrenza}, {unita_ricorrenza}"
    )
    ricorrenza = {
        "nome": nome,
        "data": data_google,
        "euro": euro,
        "categoria": categoria,
        "tipo_ricorrenza": tipo_ricorrenza,
        "unita_ricorrenza": unita_ricorrenza,
    }

    add_ricorrente(file_id, ricorrenza)

    return redirect(request.referrer)
