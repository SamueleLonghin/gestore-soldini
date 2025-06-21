from .db_interface import get_db


def get_spese_ricorrenti(gestione_id):
    db = get_db()
    rows = db.execute(
        """
        SELECT sr.* FROM spese_ricorrenti sr
     
        WHERE sr.gestione_id = ?
        ORDER BY sr.data_inizio DESC
        """,
        (gestione_id,),
    ).fetchall()
    return [dict(r) for r in rows]


def aggiungi_spesa_ricorrente(utente_id, gestione_id, spesa_ricorrente):
    db = get_db()
    db.execute(
        """
        INSERT INTO spese_ricorrenti (
            gestione_id,
            autore_id,
            nome,
            categoria,
            data_inizio,
            frequenza_unità,
            frequenza_intervallo,
            importo
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            gestione_id,
            utente_id,
            spesa_ricorrente.get("nome"),
            spesa_ricorrente.get("categoria"),
            spesa_ricorrente.get("data_inizio"),
            spesa_ricorrente.get("frequenza_unità"),
            spesa_ricorrente.get("frequenza_intervallo"),
            spesa_ricorrente.get("importo"),
        ),
    )
    db.commit()


def modifica_spesa_ricorrente(spesa_ricorrente_id, spesa_ricorrente):
    db = get_db()
    db.execute(
        """
        UPDATE spese_ricorrenti
        SET nome = ?,
            categoria = ?,
            data_inizio = ?,
            frequenza_unità = ?,
            frequenza_intervallo = ?,
            importo = ?
        WHERE id = ?
        """,
        (
            spesa_ricorrente.get("nome"),
            spesa_ricorrente.get("categoria"),
            spesa_ricorrente.get("data_inizio"),
            spesa_ricorrente.get("frequenza_unità"),
            spesa_ricorrente.get("frequenza_intervallo"),
            spesa_ricorrente.get("importo"),
            spesa_ricorrente_id,
        ),
    )
    db.commit()
