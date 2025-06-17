from google.oauth2 import service_account
from googleapiclient.discovery import build
from flask import current_app
from google.oauth2 import service_account
from googleapiclient.discovery import build
from flask import current_app
import os

from app.services.tools import parse_date


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


def get_spreadsheet_data(file_id, range_name):
    service = get_service()
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=file_id, range=range_name).execute()
    return result.get("values", [])


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


def add_spesa(file_id, spesa):
    """
    Inserisce una nuova spesa in testa al file (seconda riga, dopo l'intestazione).
    spesa: lista o tupla con i valori [data, mese, anno, euro, descrizione, categoria]
    """
    print("Aggiungo spesa:", spesa)
    service = get_service()
    spese_tab = os.getenv("SHEET_TAB_SPESA_INPUT", "ELENCO SPESE")
    # Trova l'ultima riga non vuota
    rows = get_spreadsheet_data(file_id, f"{spese_tab}!A2:F")
    next_row = len(rows) + 2  # +2 perché A2 è la prima riga dati
    range_name = f"{spese_tab}!A{next_row}:F{next_row}"

    spesa["euro"] = str(spesa["euro"]).replace(".", ",")  # Converti in formato europeo
    row = [spesa["data"], spesa["euro"], spesa["descrizione"], spesa["categoria"]]

    service.spreadsheets().values().update(
        spreadsheetId=file_id,
        range=range_name,
        valueInputOption="USER_ENTERED",
        body={"values": [row]},
    ).execute()


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
