from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from flask import Blueprint, current_app, redirect, render_template, request, session, url_for
from db.categorie import get_categorie
from db.spese import aggiungi_spesa
from services.google_auth import login_is_required
from db.spese_ricorrenti import (
    find_spese_by_spesa_ricorrente,
    get_spese_ricorrenti,
    aggiungi_spesa_ricorrente,
    modifica_spesa_ricorrente,
    get_spesa_ricorrente,
    get_spese_by_spesa_ricorrente,
)
from tools.dates import add_args_to_url
from tools.mapper import serialize_options
from tools.tabella import build_table

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
        "nome": "Nome;link-",
        "categoria": "Categoria;options;"+serialize_options(categorie),
        "data_inizio": "Data di Inizio;date",
        "frequenza_unità": "Unità di Ricorrenza;options;"+serialize_options({"giorno":"Giorno","mese":"Mese","anno":"Anno"}),
        "frequenza_intervallo": "Intervallo di Ricorrenza;number",
        "importo": "Importo;currency",
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

    aggiungi_spesa_ricorrente(gestione_id=id, utente_id=user_id, spesa_ricorrente=ricorrenza)

    return redirect(request.referrer)


@ricorrentibp.route("/<id_spesa>", methods=["GET"])
@login_is_required
def visualizza(id, id_spesa):
    gestione_id = id
    spesa_ricorrente = get_spesa_ricorrente(id_spesa)
    spese = get_spese_by_spesa_ricorrente(id_spesa)

    spese = {spesa['num_rata']: {**spesa,"stato":"eseguita"} for spesa in spese}

    if not spesa_ricorrente:
        return redirect(request.referrer)
    
    # Ora pianifico le spese ricorrenti dal giorno di inizio al giorno corrente considerando il seguente schema:
    data_inizio = spesa_ricorrente["data_inizio"]

    data_corrente = datetime.now().date()
    data_fine_anno = datetime(data_corrente.year, 12, 31).date()

    frequenza_intervallo = spesa_ricorrente["frequenza_intervallo"]
    frequenza_unità = spesa_ricorrente["frequenza_unità"]
    i = 1

    print(spese)
    while data_inizio <= data_fine_anno:
        if(i not in spese.keys()):
            spese[i] = {
                "id": None,  # ID sarà generato al momento della creazione della spesa
                "descrizione": f"{spesa_ricorrente["nome"]} - rata {i}",
                "num_rata" : i,
                "categoria": spesa_ricorrente["categoria"],
                "data": data_inizio ,
                "importo": spesa_ricorrente["importo"],
                "stato":"pianificata" if data_corrente>= data_inizio else "futuro"
            }

        if frequenza_unità == "giorno":
            data_inizio += timedelta(days=frequenza_intervallo)
        elif frequenza_unità == "mese":
            data_inizio += relativedelta(months=frequenza_intervallo)
        elif frequenza_unità == "anno":
            data_inizio += relativedelta(years=frequenza_intervallo)
        i+=1

    # Ordino le spese per data
    spese = sorted(spese.values(), key=lambda x: x["data"])

    columns = {
        "data": {"label": "Data", "type": "widget", "extra":"data", "editable": True},
        "id": {"label": "Data", "type": "text",  "editable": True},
        "importo": {"label": "Importo", "type": "widget", "extra":"importo", "editable": True},
        "descrizione": {"label": "Descrizione", "type": "textarea", "editable": True},
        "num_rata": {"label": "Rata", "type": "number", "editable": True},
        "stato": {
            "label": "Azioni",
            "type": "prerender-widgets",
            "extra": "stato",
            "editable": True,
        },
    }
    states={
        'eseguita':"<p class='m-0 p-0 text-center'>Eseguita</p>",
        'futuro':"<p class='m-0 p-0 text-center'>Futuro</p>",
        'pianificata':f"<button type='submit' class='form-control form-control-sm'>Convalida</button> "
    }
    def stato(row):
        return states.get(row['stato'], "Errore")

    table_config = build_table(
        form_action=url_for('gestione.ricorrenti.convalida',id=id,id_spesa =id_spesa),
        # editable_fields=["descrizione", "categoria", "stato"],
        # row_click_url=f"/{id}/ricorrenti/{id_spesa}/spesa/{{id}}",
        actions=[
            # {
            #     "label": "Visualizza",
            #     "url": f"{id}",
            #     "class": "btn btn-primary",
            # },
            # {
            #     "label": "<i class='bi bi-trash'></i>",
            #     "url": "{id}/elimina",
            #     "class": "",
            # },
        ],
        widgets={
            "data": lambda row: row["data"].strftime(
                current_app.config["DISPLAY_DATE_FORMAT"]
            ),
            "importo": lambda row: f"{row['importo']} €",
            'stato':stato
                
        },
        columns=columns,
        rows=spese,
        generate_ids=True
    )

    categorie = get_categorie(gestione_id,True)
    spesa_ricorrente['categoria'] = categorie.get(int(spesa_ricorrente['categoria']),'-')
    return render_template(
        "ricorrente.html", spesa_ricorrente=spesa_ricorrente, table_config=table_config
    )

@ricorrentibp.route("/<id_spesa>/convalida", methods=["POST"])
@login_is_required
def convalida(id, id_spesa):
    user_id = session.get("user").get("user_id")
    id_gestione = id
    id_spesa_ricorrente = id_spesa
    num_rata = request.form['num_rata']

    spesa_esistente=find_spese_by_spesa_ricorrente(id_spesa_ricorrente, num_rata)
    if len(spesa_esistente)>0:
        return redirect(request.referrer)

    spesa_ricorrente = get_spesa_ricorrente(id_spesa_ricorrente)

    spesa = dict()

     # Estrai anno e mese dalla data
    data_parsed = datetime.strptime(request.form.get('data'), current_app.config["FORM_DATE_FORMAT"])
    data_db = data_parsed.strftime(current_app.config["DB_DATE_FORMAT"])

    oggi = datetime.today()
    if data_parsed > oggi:
        return redirect(
            add_args_to_url(
                request.referrer,
                {"error": "La data non può essere successiva al giorno corrente"},
            )
        )

    spesa['categoria'] = spesa_ricorrente.get('categoria')
    spesa['data'] = data_db
    spesa['descrizione'] = request.form.get('descrizione')
    spesa['importo'] = spesa_ricorrente.get('importo')
    spesa['num_rata'] = num_rata
    spesa['id_ricorrenza'] = id_spesa_ricorrente

    aggiungi_spesa(user_id, id_gestione, spesa)
    
    return redirect(request.referrer)
