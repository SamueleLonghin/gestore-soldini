from flask import g


def get_ingressi(gestione_id):
    g.cur.execute(
        """
        SELECT i.* FROM ingressi i
        WHERE i.gestione_id = %s
        ORDER BY i.data DESC
        """,
        (gestione_id,),
    )
    rows = g.cur.fetchall()
    return [dict(r) for r in rows]


def aggiungi_ingresso(gestione_id, utente_id, ingresso):
    g.cur.execute(
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
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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
    g.db.commit()


def modifica_ingresso(ingresso_id, ingresso):
    print(ingresso)
    g.cur.execute(
        """
        UPDATE ingressi
        SET data = %s,
            mese = %s,
            anno = %s,
            importo = %s,
            descrizione = %s,
            categoria = %s,
            note = %s,
            conto = %s
        WHERE id = %s
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
    g.db.commit()


def aggiungi_data_ingresso(ingresso_id, data):
    g.cur.execute(
        """
        UPDATE ingressi
        SET data = %s
        WHERE id = %s
        """,
        (data, ingresso_id),
    )
    g.db.commit()
