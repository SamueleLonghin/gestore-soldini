from flask import g


def get_spese(gestione_id):
    g.cur.execute(
        """
        SELECT s.* FROM spese s
        WHERE s.gestione_id = %s
        ORDER BY s.data DESC
        """,
        (gestione_id,),
    )
    rows = g.cur.fetchall()
    return [dict(r) for r in rows]



def aggiungi_spesa(utente_id, gestione_id, spesa):
    g.cur.execute(
        """
        INSERT INTO spese (autore_id, gestione_id, data, mese, anno, importo, descrizione, categoria, id_ricorrenza, num_rata)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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
            spesa.get("num_rata", None),
        ),
    )
    g.db.commit()


def modifica_spesa(spesa_id, spesa):
    g.cur.execute(
        """
        UPDATE spese
        SET data = %s,
            mese = %s,
            anno = %s,
            importo = %s,
            descrizione = %s,
            categoria = %s,
            id_ricorrenza = %s
            num_rata = %s
        WHERE id = %s
        """,
        (
            spesa.get("data"),
            spesa.get("mese"),
            spesa.get("anno"),
            spesa.get("importo"),
            spesa.get("descrizione"),
            spesa.get("categoria"),
            spesa.get("id_ricorrenza", None),
            spesa.get("num_rata", None),
            spesa_id,
        ),
    )
    g.db.commit()
