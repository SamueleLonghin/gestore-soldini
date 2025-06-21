from .db_interface import get_db


def get_spese(gestione_id):
    db = get_db()
    rows = db.execute(
        """
        SELECT s.* FROM spese s
        WHERE s.gestione_id = ?
        ORDER BY s.data DESC
        """,
        (gestione_id,),
    ).fetchall()
    return [dict(r) for r in rows]


def aggiungi_spesa(utente_id, gestione_id, spesa):
    db = get_db()
    db.execute(
        """
        INSERT INTO spese (autore_id, gestione_id, data, mese, anno, importo, descrizione, categoria, id_ricorrenza)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            utente_id,
            gestione_id,
            spesa.get("data"),
            spesa.get("mese"),
            spesa.get("anno"),
            spesa.get("importo"),
            spesa.get("descrizione"),
            spesa.get("categoria"),
            spesa.get("id_ricorrenza", None),
        ),
    )
    db.commit()


def modifica_spesa(spesa_id, spesa):
    db = get_db()
    db.execute(
        """
        UPDATE spese
        SET data = ?,
            mese = ?,
            anno = ?,
            importo = ?,
            descrizione = ?,
            categoria = ?,
            id_ricorrenza = ?
        WHERE id = ?
        """,
        (
            spesa.get("data"),
            spesa.get("mese"),
            spesa.get("anno"),
            spesa.get("importo"),
            spesa.get("descrizione"),
            spesa.get("categoria"),
            spesa.get("id_ricorrenza", None),
            spesa_id,
        ),
    )
    db.commit()
