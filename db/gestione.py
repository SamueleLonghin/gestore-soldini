from flask import current_app, g
from datetime import date


def get_gestione(gestione_id):
    g.cur.execute(
        """
        SELECT * FROM gestioni
        
        WHERE id = %s
        """,
        (gestione_id,),
    )
    return dict(g.cur.fetchone())


def get_gestioni(utente_id):
    g.cur.execute(
        """
        SELECT g.* FROM gestioni g
        JOIN gestione_utenti gu ON g.id = gu.gestione_id
        WHERE gu.utente_id = %s
        """,
        (utente_id,),
    )
    rows = g.cur.fetchall()
    return [dict(r) for r in rows]


def create_gestione(utente_id, nome):
    # Crea la gestione
    g.cur.execute("INSERT INTO gestioni (nome) VALUES (%s)", (nome,))
    gestione_id = g.cur.lastrowid

    print("Creata gestione", nome)

    # Associa subito l'utente alla gestione
    g.cur.execute(
        "INSERT INTO gestione_utenti (utente_id, gestione_id) VALUES (%s, %s)",
        (utente_id, gestione_id),
    )
    print(f"Associata gestione {nome} ({gestione_id}) all'utente {utente_id}")
    # Commit finale unico
    g.db.commit()


    return gestione_id


def create_gestione_utente(utente_id, gestione_id):
    g.cur.execute(
        "INSERT INTO gestione_utenti (utente_id, gestione_id) VALUES (%s, %s)",
        (utente_id, gestione_id),
    )
    g.db.commit()

    return g.cur.lastrowid


def get_somma_spese_mese(gestione_id, mese, anno):
    # Calcola il primo e l'ultimo giorno del mese
    start_date = date(int(anno), int(mese), 1)
    if int(mese) == 12:
        end_date = date(int(anno) + 1, 1, 1)
    else:
        end_date = date(int(anno), int(mese) + 1, 1)
    g.cur.execute(
        """
        SELECT sum(s.importo) as sum FROM spese s
        WHERE s.gestione_id = %s
        AND s.data >= %s AND s.data < %s
        """,
        (
            gestione_id,
            start_date.strftime(current_app.config["DB_DATE_FORMAT"]),
            end_date.strftime(current_app.config["DB_DATE_FORMAT"]),
        ),
    )
    result = g.cur.fetchone()
    print("RES:",result)

    return result["sum"] if result and result["sum"] is not None else 0


def get_somma_spese_anno(gestione_id, anno):
    # Calcola il primo e l'ultimo giorno del mese
    start_date = date(int(anno), 1, 1).strftime(current_app.config["DB_DATE_FORMAT"])
    end_date = date(int(anno) + 1, 1, 1).strftime(current_app.config["DB_DATE_FORMAT"])

    g.cur.execute(
        """
        SELECT sum(s.importo) as sum FROM spese s
        WHERE s.gestione_id = %s
        AND s.data >= %s AND s.data < %s
        """,
        (
            gestione_id,
            start_date,
            end_date,
        ),
    )
    result = g.cur.fetchone()
    return result["sum"] if result and result["sum"] is not None else 0


def get_somma_ingressi_previsti_mese(gestione_id, mese, anno):
    g.cur.execute(
        """
        SELECT sum(i.importo) as sum FROM ingressi i
        WHERE i.gestione_id = %s
        AND i.mese = %s
        AND i.anno = %s
        """,
        (gestione_id, mese, anno),
    )
    result = g.cur.fetchone()
    return result["sum"] if result and result["sum"] is not None else 0


def get_somma_ingressi_previsti_anno(gestione_id, anno):
    g.cur.execute(
        """
        SELECT sum(i.importo) as sum FROM ingressi i
        WHERE i.gestione_id = %s
        AND i.anno = %s
        """,
        (gestione_id, anno),
    )
    result = g.cur.fetchone()
    return result["sum"] if result and result["sum"] is not None else 0


def get_somma_ingressi_ricevuti_mese(gestione_id, mese, anno):
    g.cur.execute(
        """
        SELECT sum(i.importo) as sum FROM ingressi i
        WHERE i.gestione_id = %s
        AND data != NULL
        AND i.mese = %s
        AND i.anno = %s
        """,
        (gestione_id, mese, anno),
    )
    result = g.cur.fetchone()
    return result["sum"] if result and result["sum"] is not None else 0


def get_somma_ingressi_ricevuti_anno(gestione_id, anno):
    g.cur.execute(
        """
        SELECT sum(i.importo) as sum FROM ingressi i
        WHERE i.gestione_id = %s
        AND data != NULL
        AND i.anno = %s
        """,
        (gestione_id, anno),
    )
    result = g.cur.fetchone()
    return result["sum"] if result and result["sum"] is not None else 0
