from db.db_interface import get_db


def get_ingressi(gestione_id):
    db = get_db()
    rows = db.execute(
        """
        SELECT i.* FROM ingressi i
        WHERE i.gestione_id = ?
        ORDER BY i.data DESC
        """,
        (gestione_id,),
    ).fetchall()
    return [dict(r) for r in rows]


def aggiungi_ingresso(gestione_id, utente_id, ingresso):
    db = get_db()
    db.execute(
        """
        INSERT INTO ingressi (
            gestione_id,
            autore_id,
            data,
            mese,
            anno,
            importo,
            descrizione,
            categoria,
            note,
            conto
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            gestione_id,
            utente_id,
            ingresso.get("data"),
            ingresso.get("mese"),
            ingresso.get("anno"),
            ingresso.get("importo"),
            ingresso.get("descrizione"),
            ingresso.get("categoria"),
            ingresso.get("note"),
            ingresso.get("conto"),
        ),
    )
    db.commit()


def modifica_ingresso(ingresso_id, ingresso):
    db = get_db()
    db.execute(
        """
        UPDATE ingressi
        SET data = ?,
            mese = ?,
            anno = ?,
            importo = ?,
            descrizione = ?,
            categoria = ?,
            note = ?,
            conto = ?
        WHERE id = ?
        """,
        (
            ingresso.get("data"),
            ingresso.get("mese"),
            ingresso.get("anno"),
            ingresso.get("importo"),
            ingresso.get("descrizione"),
            ingresso.get("categoria"),
            ingresso.get("note"),
            ingresso.get("conto"),
            ingresso_id,
        ),
    )
    db.commit()


def aggiungi_data_ingresso(ingresso_id, data):
    db = get_db()
    db.execute(
        """
        UPDATE ingressi
        SET data = ?
        WHERE id = ?
        """,
        (data, ingresso_id),
    )
    db.commit()
