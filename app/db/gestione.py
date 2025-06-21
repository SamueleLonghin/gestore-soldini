from flask import current_app
from .db_interface import get_db
from datetime import date


def get_gestione(gestione_id):
    db = get_db()
    g = db.execute(
        """
        SELECT g.* FROM gestioni g
        
        WHERE g.id = ?
        """,
        (gestione_id,),
    ).fetchone()
    return dict(g)


def get_gestioni(utente_id):
    db = get_db()
    rows = db.execute(
        """
        SELECT g.* FROM gestioni g
        JOIN gestione_utenti gu ON g.id = gu.gestione_id
        WHERE gu.utente_id = ?
        """,
        (utente_id,),
    ).fetchall()
    return [dict(r) for r in rows]


def create_gestione(utente_id, nome):
    db = get_db()

    # Crea la gestione
    cur = db.execute("INSERT INTO gestioni (nome) VALUES (?)", (nome,))
    gestione_id = cur.lastrowid

    print("Creata gestione", nome)

    # Associa subito l'utente alla gestione
    db.execute(
        "INSERT INTO gestione_utenti (utente_id, gestione_id) VALUES (?, ?)",
        (utente_id, gestione_id),
    )
    print(f"Associata gestione {nome} ({gestione_id}) all'utente {utente_id}")
    # Commit finale unico
    db.commit()

    return gestione_id


def create_gestione_utente(utente_id, gestione_id):
    db = get_db()
    cur = db.execute(
        "INSERT INTO gestione_utenti (utente_id, gestione_id) VALUES (?, ?)",
        (utente_id, gestione_id),
    )
    db.commit()
    return cur.lastrowid


def get_somma_spese_mese(gestione_id, mese, anno):
    db = get_db()

    # Calcola il primo e l'ultimo giorno del mese
    start_date = date(int(anno), int(mese), 1)
    if int(mese) == 12:
        end_date = date(int(anno) + 1, 1, 1)
    else:
        end_date = date(int(anno), int(mese) + 1, 1)
    result = db.execute(
        """
        SELECT sum(s.importo) FROM spese s
        WHERE s.gestione_id = ?
        AND s.data >= ? AND s.data < ?
        """,
        (
            gestione_id,
            start_date.strftime(current_app.config["DB_DATE_FORMAT"]),
            end_date.strftime(current_app.config["DB_DATE_FORMAT"]),
        ),
    ).fetchone()

    return result[0] if result and result[0] is not None else 0


def get_somma_spese_anno(gestione_id, anno):
    db = get_db()

    # Calcola il primo e l'ultimo giorno del mese
    start_date = date(int(anno), 1, 1).strftime(current_app.config["DB_DATE_FORMAT"])
    end_date = date(int(anno) + 1, 1, 1).strftime(current_app.config["DB_DATE_FORMAT"])

    result = db.execute(
        """
        SELECT sum(s.importo) FROM spese s
        WHERE s.gestione_id = ?
        AND s.data >= ? AND s.data < ?
        """,
        (
            gestione_id,
            start_date,
            end_date,
        ),
    ).fetchone()
    return result[0] if result and result[0] is not None else 0

def get_somma_ingressi_previsti_mese(gestione_id, mese, anno):
    db = get_db()

    result = db.execute(
        """
        SELECT sum(i.importo) FROM ingressi i
        WHERE i.gestione_id = ?
        AND i.mese = ?
        AND i.anno = ?
        """,
        (gestione_id, mese, anno),
    ).fetchone()
    return result[0] if result and result[0] is not None else 0


def get_somma_ingressi_previsti_anno(gestione_id, anno):
    db = get_db()

    result = db.execute(
        """
        SELECT sum(i.importo) FROM ingressi i
        WHERE i.gestione_id = ?
        AND i.anno = ?
        """,
        (gestione_id, anno),
    ).fetchone()
    return result[0] if result and result[0] is not None else 0


def get_somma_ingressi_ricevuti_mese(gestione_id, mese, anno):
    db = get_db()

    result = db.execute(
        """
        SELECT sum(i.importo) FROM ingressi i
        WHERE i.gestione_id = ?
        AND data != NULL
        AND i.mese = ?
        AND i.anno = ?
        """,
        (gestione_id, mese, anno),
    ).fetchone()
    return result[0] if result and result[0] is not None else 0


def get_somma_ingressi_ricevuti_anno(gestione_id, anno):
    db = get_db()

    result = db.execute(
        """
        SELECT sum(i.importo) FROM ingressi i
        WHERE i.gestione_id = ?
        AND data != NULL
        AND i.anno = ?
        """,
        (gestione_id, anno),
    ).fetchone()
    return result[0] if result and result[0] is not None else 0
