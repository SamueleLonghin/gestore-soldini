from flask import Blueprint, redirect, render_template, request, session

from db.categorie import get_categorie, get_nomi_categorie
from db.ingressi import *
from services.google_auth import login_is_required
from flask import current_app
from datetime import datetime

from tools.dates import parse_date
from tools.mapper import serialize_options


ingressibp = Blueprint(
    "ingressi",
    __name__,
    template_folder="templates/ingressi",
    url_prefix="/<id>/ingressi",
)


@ingressibp.route("/", methods=["GET"])
@login_is_required
def ingressi(id):
    ingressi = get_ingressi(id)
    oggi = datetime.now().strftime(current_app.config["FORM_DATE_FORMAT"])
    categorie = get_categorie(id)

    headers = {
        "descrizione": "Descrizione",
        "importo": "Importo;currency",
        "anno": "Anno",
        "mese": "Mese",
        "data": "Data di Accreditamento;widget;widget_set_date",
        "categoria": "Categoria;options;" + serialize_options(categorie),
        "note": "Note;textarea",
    }
    print(ingressi)
    return render_template(
        "ingressi.html",
        ingressi=ingressi,
        oggi=oggi,
        categorie=categorie,
        headers=headers,
        rows=ingressi,
    )


@ingressibp.route("/salva_data", methods=["POST"])
@login_is_required
def salva_data(id):
    ingresso_id = request.form.get("row_id")
    data = request.form.get("data")
    data = parse_date(data, current_app.config["FORM_DATE_FORMAT"])

    print("Salvataggio data ingresso:", ingresso_id, data)

    aggiungi_data_ingresso(ingresso_id, data)

    return redirect(request.referrer)


@ingressibp.route("/modifica", methods=["POST"])
@login_is_required
def modifica(id):
    ricorrente_id = request.form.get("row_id")

    data = request.form.get("data")
    descrizione = request.form.get("descrizione")
    importo = request.form.get("importo")
    categoria = request.form.get("categoria")
    mese = request.form.get("mese")
    anno = request.form.get("anno")
    conto = request.form.get("conto")
    note = request.form.get("note")

    data_db = ""

    if data:
        data_parsed = datetime.strptime(data, current_app.config["FORM_DATE_FORMAT"])
        data_db = data_parsed.strftime(current_app.config["DB_DATE_FORMAT"])

    # print(
    #     f"Modifico ingresso {ricorrente_id}: {descrizione}, {data_db}, {importo}, {categoria}, {mese}, {anno}, {note}"
    # )
    ingresso = {
        "data": data_db,
        "importo": importo,
        "descrizione": descrizione,
        "categoria": categoria,
        "mese": mese,
        "anno": anno,
        "note": note,
        "conto": conto,
    }

    print(ingresso)

    modifica_ingresso(ricorrente_id, ingresso)

    return redirect(request.referrer)


@ingressibp.route("/aggiungi", methods=["POST"])
@login_is_required
def aggiungi(id):
    user_id = session.get("user").get("user_id")

    data = request.form.get("data")
    descrizione = request.form.get("descrizione")
    importo = request.form.get("importo")
    categoria = request.form.get("categoria")
    mese = request.form.get("mese")
    note = request.form.get("note", "")
    conto = request.form.get("conto", "")
    print("Aggiungo ingresso:", data, descrizione, importo, categoria, mese)

    # Estrai anno e mese dalla data
    mese_anno_parsed = datetime.strptime(mese, current_app.config["FORM_MONTH_FORMAT"])
    anno = mese_anno_parsed.year
    mese = mese_anno_parsed.month
    data_db = None

    if data:
        print("Data", data)
        data_parsed = datetime.strptime(data, current_app.config["FORM_DATE_FORMAT"])
        data_db = data_parsed.strftime(current_app.config["DB_DATE_FORMAT"])
    ingresso = {
        "data": data_db,
        "importo": importo,
        "descrizione": descrizione,
        "categoria": categoria,
        "mese": mese,
        "anno": anno,
        "note": note,
        "conto": conto,
    }

    aggiungi_ingresso(id, user_id, ingresso)

    return redirect(request.referrer)
