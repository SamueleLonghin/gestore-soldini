from google.oauth2 import service_account
from googleapiclient.discovery import build
from flask import current_app
from google.oauth2 import service_account
from googleapiclient.discovery import build
from flask import current_app
import os

from app.services.tools import parse_date, prepare_data
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
    result = (
        sheet.values()
        .get(
            spreadsheetId=file_id,
            range=range_name,
            valueRenderOption="UNFORMATTED_VALUE",
        )
        .execute()
    )
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
    spese_tab = os.getenv("SHEET_TAB_SPESA")
    rows = get_spreadsheet_data(file_id, spese_tab + "!A2:F")
    spese = []
    for row in rows:
        if len(row) < 6:
            print("Riga non valida:", row)
            continue

        data = parse_date(row[0], current_app.config["GOOGLE_SHEET_DATE_FORMAT"])
        spese.append(
            {
                "data": data,
                "mese": row[1],
                "anno": row[2],
                "euro": row[3],
                "descrizione": row[4],
                "categoria": row[5],
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
    spese_tab = os.getenv("SHEET_TAB_SPESA_INPUT")
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
    ingressi_tab = os.getenv("SHEET_TAB_INGRESSI")
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


def add_ricorrente(file_id, ricorrenza):
    """
    Inserisce un nuovo ricorrente in fondo al file.
    ricorrenza: dizionario con i valori [nome, categoria, data_inizio, tipo_ricorrenza, unita_ricorrenza, euro]
    """
    print("Aggiungo ricorrente:", ricorrenza)
    ricorrenti_tab = os.getenv("SHEET_TAB_SPESE_RICORRENTI")
    ricorrenza["euro"] = str(ricorrenza["euro"]).replace(
        ".", ","
    )  # Converti in formato europeo
    row = [
        ricorrenza.get("nome", ""),
        ricorrenza.get("categoria", ""),
        ricorrenza.get("data", ""),
        ricorrenza.get("tipo_ricorrenza", ""),
        ricorrenza.get("unita_ricorrenza", ""),
        ricorrenza.get("euro", ""),
    ]
    res = append_row_to_sheet(file_id, ricorrenti_tab, row)
    print("Risultato append:", res)


def update_row(file_id, range_name, row):
    service = get_service()
    service.spreadsheets().values().update(
        spreadsheetId=file_id,
        range=range_name,
        valueInputOption="USER_ENTERED",
        body={"values": [row]},
    ).execute()


def update_ricorrente(file_id, id_ricorrente, ricorrenza):
    ricorrenti_tab = os.getenv("SHEET_TAB_SPESE_RICORRENTI")
    range_name = f"{ricorrenti_tab}!{id_ricorrente}:{id_ricorrente}"

    row = [
        ricorrenza.get("nome", ""),
        ricorrenza.get("categoria", ""),
        ricorrenza.get("data", ""),
        ricorrenza.get("tipo_ricorrenza", ""),
        ricorrenza.get("unita_ricorrenza", ""),
        ricorrenza.get("euro", ""),
    ]
    update_row(file_id, range_name, row)


def get_categorie(file_id):
    """
    Restituisce le categorie raggruppate per tipo.
    Utilizza le variabili d'ambiente SHEET_TAB_CATEGORIE e SHEET_RANGE_CATEGORIE.
    Il range deve contenere due colonne: 'Categoria' e 'tipo'.
    """
    categorie_tab = os.getenv("SHEET_TAB_CATEGORIE")
    categorie_range = os.getenv("SHEET_RANGE_CATEGORIE")
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
    categorie_tab = os.getenv("SHEET_TAB_INGRESSI")
    categorie_range = os.getenv("SHEET_RANGE_INGRESSI")
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
                "data": parse_date(
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


def get_spese_ricorrenti(file_id):
    """
    Restituisce le spese ricorrenti dal foglio dedicato.
    Le colonne sono: NOME SPESA RICORRENTE, CATEGORIA, DATA INIZIO, TIPO RICORRENZA, UNITÀ DI RICORRENZA, EURO
    """
    tab = os.getenv("SHEET_TAB_SPESE_RICORRENTI")
    range_ = os.getenv("SHEET_RANGE_SPESE_RICORRENTI")
    rows = get_spreadsheet_data(file_id, f"{tab}!{range_}", with_row_id=True)

    ricorrenti = []
    for row in rows:
        data = parse_date(row[3], current_app.config["GOOGLE_SHEET_DATE_FORMAT"])
        ricorrenti.append(
            {
                "id": row[0],
                "nome": row[1],
                "categoria": row[2],
                "data_inizio": data,
                "tipo_ricorrenza": row[4],
                "unita_ricorrenza": row[5],
                "euro": row[6],
                "euro_value": row[6],
            }
        )

    return ricorrenti


def update_ingresso(file_id, id_ingresso, ingresso):
    ingressi_tab = os.getenv("SHEET_TAB_INGRESSI")
    range_name = f"{ingressi_tab}!{id_ingresso}:{id_ingresso}"

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

    update_row(file_id, range_name, row)


def add_data_ingresso(file_id, id_ingresso, data):
    data = prepare_data(data)
    update_ingresso(file_id, id_ingresso, "data", data)
