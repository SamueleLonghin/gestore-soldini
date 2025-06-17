from google.oauth2 import service_account
from googleapiclient.discovery import build
from flask import current_app
from google.oauth2 import service_account
from googleapiclient.discovery import build
from flask import current_app
import os

from app.services.tools import parse_date
import re

INGRESSO_COLONNE = {
    "data": "A",
    "mese": "B",
    "anno": "C",
    "euro": "D",
    "descrizione": "E",
    "categoria": "F",
    "note": "G",
    "conto": "H",
}


def get_service():
    """
    Crea e restituisce un client per l'API Google Sheets.
    Utilizza le credenziali del file di servizio specificato nella configurazione dell'app.
    """
    creds = service_account.Credentials.from_service_account_file(
        current_app.config["SERVICE_ACCOUNT_FILE"],
        scopes=["https://www.googleapis.com/auth/spreadsheets"],
    )
    return build("sheets", "v4", credentials=creds)


def get_spreadsheet_data(file_id, range_name, with_row_id=False):
    service = get_service()
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=file_id, range=range_name).execute()
    values = result.get("values", [])

    if not with_row_id:
        return values

    # Calcola il numero della prima riga del range (es: "A2:F" -> 2)
    match = re.search(r"[A-Z]+(\d+)", range_name)
    start_row = int(match.group(1)) if match else 1

    # Restituisce una lista di tuple (row_id, row_values)
    return [(start_row + idx, *row) for idx, row in enumerate(values)]


def get_spreadsheet_name(file_id):
    """Restituisce il nome del foglio di calcolo dato l'ID."""
    service = get_service()
    spreadsheet = service.spreadsheets().get(spreadsheetId=file_id).execute()
    return spreadsheet.get("properties", {}).get("title", "Sconosciuto")


def get_sheet_id(service, file_id, sheet_name):
    """Restituisce l'ID del foglio dato il nome."""
    spreadsheet = service.spreadsheets().get(spreadsheetId=file_id).execute()
    for sheet in spreadsheet.get("sheets", []):
        if sheet.get("properties", {}).get("title") == sheet_name:
            return sheet.get("properties", {}).get("sheetId")
    raise ValueError(f"Sheet '{sheet_name}' not found")


def get_spese_from_file(file_id):
    spese_tab = os.getenv("SHEET_TAB_SPESA", "ELENCO SPESE")
    rows = get_spreadsheet_data(file_id, spese_tab + "!A2:F")
    spese = []
    for row in rows:
        if len(row) < 6:
            print("Riga non valida:", row)
            continue
        spese.append(
            {
                "data": row[0],
                "mese": row[1],
                "anno": row[2],
                "euro": row[3],
                "descrizione": row[4],
                "categoria": row[5],
                "data_value": parse_date(
                    row[0], current_app.config["GOOGLE_SHEET_DATE_FORMAT"]
                ),
            }
        )
    return spese


def append_row_to_sheet(file_id, sheet_name, row_data):
    """
    Aggiunge una riga al foglio specificato dopo l'ultima riga scritta.
    file_id: ID del foglio di calcolo.
    sheet_name: Nome del foglio in cui aggiungere la riga.
    row_data: Lista o tupla con i dati della riga da aggiungere.
    """
    service = get_service()
    range_name = f"{sheet_name}!A1"  # Il range è solo indicativo per append
    body = {"values": [row_data]}

    return (
        service.spreadsheets()
        .values()
        .append(
            spreadsheetId=file_id,
            range=range_name,
            valueInputOption="USER_ENTERED",
            insertDataOption="INSERT_ROWS",  # Garantisce inserimento dopo l'ultima riga
            body=body,
        )
        .execute()
    )


def add_spesa(file_id, spesa):
    """
    Inserisce una nuova spesa in fondo al file.
    spesa: dizionario con i valori [data, euro, descrizione, categoria]
    """
    print("Aggiungo spesa:", spesa)
    spese_tab = os.getenv("SHEET_TAB_SPESA_INPUT", "ELENCO SPESE")
    spesa["euro"] = str(spesa["euro"]).replace(".", ",")  # Converti in formato europeo
    row = [
        spesa.get("data", ""),
        spesa.get("euro", ""),
        spesa.get("descrizione", ""),
        spesa.get("categoria", ""),
    ]
    append_row_to_sheet(file_id, spese_tab, row)


def add_ingresso(file_id, ingresso):
    """
    Inserisce un nuovo ingresso in fondo al file.
    ingresso: dizionario con i valori [data, mese, anno, euro, descrizione, categoria, note, conto]
    """
    print("Aggiungo ingresso:", ingresso)
    ingressi_tab = os.getenv("SHEET_TAB_INGRESSI", "ELENCO INGRESSI")
    ingresso["euro"] = str(ingresso["euro"]).replace(
        ".", ","
    )  # Converti in formato europeo
    row = [
        ingresso.get("data", ""),
        ingresso.get("mese", ""),
        ingresso.get("anno", ""),
        ingresso.get("euro", ""),
        ingresso.get("descrizione", ""),
        ingresso.get("categoria", ""),
        ingresso.get("note", ""),
        ingresso.get("conto", ""),
    ]
    res = append_row_to_sheet(file_id, ingressi_tab, row)
    print("Risultato append:", res)
    #  """
    # Inserisce un nuovo ingresso in testa al file (seconda riga, dopo l'intestazione).
    # ingresso: lista o tupla con i valori [data, mese, anno, euro, descrizione, categoria]
    # """
    # print("Aggiungo ingresso:", ingresso)
    # service = get_service()
    # ingressi_tab = os.getenv("SHEET_TAB_INGRESSI", "Ingressi")
    # # Trova l'ultima riga non vuota
    # rows = get_spreadsheet_data(file_id, f"{ingressi_tab}!A2:F")
    # next_row = len(rows) + 2  # +2 perché A2 è la prima riga dati
    # range_name = f"{ingressi_tab}!A{next_row}:F{next_row}"

    # ingresso["euro"] = str(ingresso["euro"]).replace(
    #     ".", ","
    # )  # Converti in formato europeo
    # row = [
    #     ingresso["data"],
    #     ingresso["mese"],
    #     ingresso["anno"],
    #     ingresso["euro"],
    #     ingresso["descrizione"],
    #     ingresso["categoria"],
    #     ingresso["note"],
    #     ingresso["conto"],
    # ]

    # service.spreadsheets().values().update(
    #     spreadsheetId=file_id,
    #     range=range_name,
    #     valueInputOption="USER_ENTERED",
    #     body={"values": [row]},
    # ).execute()


def get_categorie(file_id):
    """
    Restituisce le categorie raggruppate per tipo.
    Utilizza le variabili d'ambiente SHEET_TAB_CATEGORIE e SHEET_RANGE_CATEGORIE.
    Il range deve contenere due colonne: 'Categoria' e 'tipo'.
    """
    categorie_tab = os.getenv("SHEET_TAB_CATEGORIE", "Categorizzazione")
    categorie_range = os.getenv("SHEET_RANGE_CATEGORIE", "A2:B")
    rows = get_spreadsheet_data(file_id, f"{categorie_tab}!{categorie_range}")
    categorie_by_tipo = {}
    for row in rows:
        if len(row) < 2:
            continue
        categoria, tipo = row[0], row[1]
        if tipo not in categorie_by_tipo:
            categorie_by_tipo[tipo] = []
        categorie_by_tipo[tipo].append(categoria)
    return categorie_by_tipo


def get_ingressi(file_id):
    """
    Restituisce le categorie raggruppate per tipo.
    Utilizza le variabili d'ambiente SHEET_TAB_CATEGORIE e SHEET_RANGE_CATEGORIE.
    Il range deve contenere otto colonne: DATA di Accreditamento, MESE, ANNO, EURO, DESCRIZIONE, CATEGORIA, NOTE, CONTO di Accreditamento.
    """
    categorie_tab = os.getenv("SHEET_TAB_INGRESSI", "Ingressi")
    categorie_range = os.getenv("SHEET_RANGE_INGRESSI", "A2:H")
    rows = get_spreadsheet_data(
        file_id, f"{categorie_tab}!{categorie_range}", with_row_id=True
    )
    ingressi = []
    for row in rows:
        if len(row) < 9:
            row = list(row) + [""] * (9 - len(row))  # Completa con vuoti se necessario
        id, data, mese, anno, euro, descrizione, categoria, note, conto = row
        ingressi.append(
            {
                "id": id,
                "data": data,
                "data_value": parse_date(
                    data, current_app.config["GOOGLE_SHEET_DATE_FORMAT"]
                ),
                "mese": mese,
                "anno": anno,
                "euro": euro,
                "descrizione": descrizione,
                "categoria": categoria,
                "note": note,
                "conto": conto,
            }
        )
    return ingressi


def update_ingresso(file_id, id_ingresso, attributo, valore):
    service = get_service()
    ingressi_tab = os.getenv("SHEET_TAB_INGRESSI", "Ingressi")
    # Aggiorna la cella della prima colonna (colonna A) alla riga id_ingresso con il valore "data"
    lettera = INGRESSO_COLONNE[attributo]
    range_name = f"{ingressi_tab}!{lettera}{id_ingresso}:{lettera}{id_ingresso}"
    print(f"Aggiorno {range_name} con {valore}")
    service.spreadsheets().values().update(
        spreadsheetId=file_id,
        range=range_name,
        valueInputOption="USER_ENTERED",
        body={"values": [[valore]]},
    ).execute()


def add_data_ingresso(file_id, id_ingresso, data):
    data = parse_date(data, current_app.config["FORM_DATE_FORMAT"]).strftime(
        current_app.config["GOOGLE_SHEET_DATE_FORMAT"]
    )
    update_ingresso(file_id, id_ingresso, "data", data)
