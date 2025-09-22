# db_mysql.py
import os
import mysql.connector
from datetime import datetime



# Parametri presi da env
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_SOCKET_PATH = os.getenv("DB_SOCKET_PATH")  # opzionale, per socket Unix

def get_db():
    """
    Ritorna una connessione MySQL.
    Usa:
      with get_db() as conn:
          cur = conn.cursor(dictionary=True)
          cur.execute("SELECT 1")
          print(cur.fetchone())
    """
    
    conn = mysql.connector.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        
    )
    return conn

def init_db():
    """
    Inizializza il DB: esegue schema.sql se necessario
    e applica eventuali updates/*.sql.
    """
    base_dir = os.path.dirname(__file__)
    updates_dir = os.path.join(base_dir, "updates")

    conn = get_db()
    cur = conn.cursor()

    # Crea tabella versioni se non esiste
    cur.execute("""
        CREATE TABLE IF NOT EXISTS versioni (
            id INT AUTO_INCREMENT PRIMARY KEY,
            versione VARCHAR(255) NOT NULL,
            data DATETIME NOT NULL
        )
    """)
    conn.commit()

    # Esegui schema.sql (una tantum)
    # if os.path.exists(schema_path):
    #     with open(schema_path, "r", encoding="utf-8") as f:
    #         sql = f.read()
    #     for stmt in [s.strip() for s in sql.split(";") if s.strip()]:
    #         try:
    #             cur.execute(stmt)
    #         except mysql.connector.Error as e:
    #             print("Nota: errore non critico durante init schema:", e)
    #     conn.commit()

    # Applica gli updates
    if os.path.exists(updates_dir):
        for script in sorted(f for f in os.listdir(updates_dir) if f.endswith(".sql")):
            cur.execute("SELECT COUNT(*) FROM versioni WHERE versione=%s", (script,))
            if cur.fetchone()[0] == 0:
                print(f"Eseguo update {script}")
                with open(os.path.join(updates_dir, script), "r", encoding="utf-8") as f:
                    sql = f.read()
                for stmt in [s.strip() for s in sql.split(";") if s.strip()]:
                    cur.execute(stmt)
                cur.execute(
                    "INSERT INTO versioni (data, versione) VALUES (%s, %s)",
                    (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), script),
                )
                conn.commit()
            else:
                print(f"Update {script} già eseguito")
    else:
        print("Cartella 'updates' non trovata.")

    cur.close()
    conn.close()
