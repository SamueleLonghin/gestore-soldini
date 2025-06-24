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
    print("Controllo se il database esiste...", os.path.abspath("db/data/database.db"))
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

    # Controlla se esistono script di aggiornamento nella cartella "updates"
    UPDATES_DIR = os.path.join(os.path.dirname(__file__), "updates")
    if os.path.exists(UPDATES_DIR):
        update_scripts = sorted(
            [f for f in os.listdir(UPDATES_DIR) if f.endswith(".sql")]
        )
        if update_scripts:
            conn = get_db()
            try:
                # Crea la tabella versioni se non esiste
                conn.execute(
                    """
                    CREATE TABLE IF NOT EXISTS versioni (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        versione TEXT NOT NULL,
                        data DATE NOT NULL
                    );
                    """
                )
                for script in update_scripts:
                    # Controlla se lo script è già stato eseguito
                    cur = conn.execute(
                        "SELECT COUNT(*) as cnt FROM versioni WHERE versione = ?",
                        (script,),
                    )
                    result = cur.fetchone()
                    if result["cnt"] == 0:
                        print(f"Eseguo script di aggiornamento: {script}")
                        with open(os.path.join(UPDATES_DIR, script), "r") as f:
                            conn.executescript(f.read())
                        conn.execute(
                            "INSERT INTO versioni (data, versione) VALUES (?, ?)",
                            (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), script),
                        )
                        conn.commit()
                        print(f"Script {script} eseguito e registrato.")
                    else:
                        print(f"Script {script} già eseguito, salto.")
            except Exception as e:
                print("Errore durante l'esecuzione degli script di aggiornamento:", e)
            finally:
                conn.close()
        else:
            print("Nessuno script di aggiornamento trovato nella cartella 'updates'.")
    else:
        print("Cartella 'updates' non trovata.")
    
