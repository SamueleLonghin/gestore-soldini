import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "spese.db")
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema.sql")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # per accedere ai risultati come dict
    return conn


def init_db():
    if not os.path.exists(DB_PATH):
        print("Inizializzo database...")
        conn = get_db()
        with open(SCHEMA_PATH, "r") as f:
            conn.executescript(f.read())
        conn.commit()
        conn.close()
