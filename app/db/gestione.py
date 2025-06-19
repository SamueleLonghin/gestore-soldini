from db_interface import get_db


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

    # Associa subito l'utente alla gestione
    db.execute(
        "INSERT INTO gestione_utenti (utente_id, gestione_id) VALUES (?, ?)",
        (utente_id, gestione_id),
    )

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
