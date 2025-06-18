from flask import redirect, render_template, request, url_for

from app.services.tools import parse_date
from . import gestionebp
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


@gestionebp.before_app_request
def before_request():
    file_id = request.view_args.get("file_id", None) if request.view_args else None
    current_app.jinja_env.globals["file_id"] = file_id
    if file_id:
        # title = get_spreadsheet_name(file_id)
        # if title:
        #     current_app.jinja_env.globals["title"] = title
        pass


@gestionebp.route("/<file_id>", methods=["GET"])
@login_is_required
def gestione(file_id):
    spese = get_spese_from_file(file_id)
    categorie = get_categorie(file_id)

    return render_template(
        "dashboard.html", spese=spese, file_id=file_id, categorie=categorie
    )
