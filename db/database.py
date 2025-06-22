import sqlite3
import os
from datetime import datetime

from flask import current_app

DB_PATH = os.path.join(os.path.dirname(__file__), "data/database.db")
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema.sql")


def get_db():
    def adapt_empty_string(value):
        return None if value == "" else value

    sqlite3.register_adapter(str, adapt_empty_string)

    def convert_date(val):
        try:
            return datetime.strptime(
                val.decode(), current_app.config["DB_DATE_FORMAT"]
            ).date()
        except Exception:
            return val

    sqlite3.register_converter("DATE", convert_date)

    conn = sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
    conn.row_factory = sqlite3.Row  # per accedere ai risultati come dict
    return conn


def init_db():
    print("Controllo se il database esiste...")
    if not os.path.exists(DB_PATH):
        print("Database non trovato, lo creo...")
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        print("Inizializzo database...")
        conn = get_db()
        with open(SCHEMA_PATH, "r") as f:
            conn.executescript(f.read())
        conn.commit()
        conn.close()
    else:
        print("Database già esistente, non è necessario inizializzarlo.", DB_PATH)
