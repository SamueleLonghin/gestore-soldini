from datetime import datetime
from flask import Blueprint, current_app, redirect, render_template, request, session
from db.categorie import get_categorie
from services.google_auth import login_is_required
from db.spese_ricorrenti import (
    get_spese_ricorrenti,
    aggiungi_spesa_ricorrente,
    modifica_spesa_ricorrente,
)

ricorrentibp = Blueprint(
    "ricorrenti",
    __name__,
    template_folder="templates/ricorrenti",
    url_prefix="/<id>/ricorrenti",
)


@ricorrentibp.route("/", methods=["GET"])
@login_is_required
def ricorrenti(id):
    """
    Visualizza le spese ricorrenti.
    """
    ricorrenti = get_spese_ricorrenti(id)
    categorie = get_categorie(id)

    headers = {
        "nome": "Nome",
        "categoria": "Categoria",
        "data_inizio": "Data di Inizio:date",
        "frequenza_unità": "Unità di Ricorrenza:options:giorno|mese|anno",
        "frequenza_intervallo": "Intervallo di Ricorrenza:number",
        "importo": "Importo:number",
    }

    return render_template(
        "ricorrenti.html",
        ricorrenti=ricorrenti,
        rows=ricorrenti,
        categorie=categorie,
        headers=headers,
    )


@ricorrentibp.route("/modifica", methods=["POST"])
@login_is_required
def modifica(id):
    ricorrente_id = request.form.get("row_id")

    nome = request.form.get("nome")
    categoria = request.form.get("categoria")
    data = request.form.get("data_inizio", None)
    frequenza_unità = request.form.get("frequenza_unità")
    frequenza_intervallo = request.form.get("frequenza_intervallo")
    importo = request.form.get("importo")

    data_parsed = datetime.strptime(data, current_app.config["FORM_DATE_FORMAT"])
    data_db = data_parsed.strftime(current_app.config["DB_DATE_FORMAT"])
    print(f"Data convertita: {data} -> {data_db}")

    ricorrenza = {
        "nome": nome,
        "data_inizio": data_db,
        "importo": importo,
        "categoria": categoria,
        "frequenza_unità": frequenza_unità,
        "frequenza_intervallo": frequenza_intervallo,
    }

    print(f"Modifico ricorrenza {ricorrente_id}:", ricorrenza)

    modifica_spesa_ricorrente(ricorrente_id, ricorrenza)

    return redirect(request.referrer)


@ricorrentibp.route("/aggiungi", methods=["POST"])
@login_is_required
def aggiungi(id):
    user_id = session.get("user").get("user_id")

    nome = request.form.get("nome")
    categoria = request.form.get("categoria")
    data = request.form.get("data")
    tipo_ricorrenza = request.form.get("tipo_ricorrenza")
    unita_ricorrenza = request.form.get("unita_ricorrenza")
    importo = request.form.get("importo")

    data_parsed = datetime.strptime(data, current_app.config["FORM_DATE_FORMAT"])
    data_db = data_parsed.strftime(current_app.config["DB_DATE_FORMAT"])
    print(f"Data convertita: {data} -> {data_db}")

    ricorrenza = {
        "nome": nome,
        "data_inizio": data_db,
        "importo": importo,
        "categoria": categoria,
        "frequenza_unità": tipo_ricorrenza,
        "frequenza_intervallo": unita_ricorrenza,
    }

    aggiungi_spesa_ricorrente(id, user_id, ricorrenza)

    return redirect(request.referrer)
