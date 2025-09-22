from flask import g


def get_spese_ricorrenti(gestione_id):
    g.cur.execute(
        """
        SELECT sr.* FROM spese_ricorrenti sr
     
        WHERE sr.gestione_id = %s
        ORDER BY sr.data_inizio DESC
        """,
        (gestione_id,),
    )
    rows = g.cur.fetchall()
    return [dict(r) for r in rows] 


def get_spesa_ricorrente(id_spesa):
    g.cur.execute(
        """
        SELECT * FROM spese_ricorrenti
        WHERE id = %s
        """, 
        (id_spesa,),
    )
    row = g.cur.fetchone()
    return dict(row) if row else None


def get_spese_by_spesa_ricorrente(spesa_ricorrente_id):
    g.cur.execute(
        """
        SELECT * FROM spese
        WHERE id_ricorrenza = %s
        ORDER BY data DESC
        """,
        (spesa_ricorrente_id,),
    )
    rows = g.cur.fetchall()
    return [dict(r) for r in rows]

def find_spese_by_spesa_ricorrente(spesa_ricorrente_id, num_rata=None):
    if num_rata == None:
        g.cur.execute(
            """
            SELECT * FROM spese
            WHERE id_ricorrenza = %s
            ORDER BY data DESC
            """,
            (spesa_ricorrente_id),
        )
    else:
        g.cur.execute(
            """
            SELECT * FROM spese
            WHERE id_ricorrenza = %s
            AND num_rata = %s
            ORDER BY data DESC
            """,
            (spesa_ricorrente_id, num_rata),
        )
    rows = g.cur.fetchall()
    return [dict(r) for r in rows]


def aggiungi_spesa_ricorrente(utente_id, gestione_id, spesa_ricorrente):
    g.cur.execute("SELECT id FROM gestioni WHERE id=%s", (gestione_id,))
    if not g.cur.fetchone():
        raise ValueError(f"Gestione {gestione_id} inesistente")

    g.cur.execute("SELECT id FROM utenti WHERE id=%s", (utente_id,))
    if not g.cur.fetchone():
        raise ValueError(f"Utente {utente_id} inesistente")
    
    g.cur.execute(
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
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
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
    g.db.commit()


def modifica_spesa_ricorrente(spesa_ricorrente_id, spesa_ricorrente):
    g.cur.execute(
        """
        UPDATE spese_ricorrenti
        SET nome = %s,
            categoria = %s,
            data_inizio = %s,
            frequenza_unità = %s,
            frequenza_intervallo = %s,
            importo = %s
        WHERE id = %s
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
    g.db.commit()
