from db.db_interface import get_db


def get_categorie(gestione_id, flat=False):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "SELECT id, nome, macrocategoria, colore FROM categorie WHERE gestione_id IS NULL OR gestione_id = ?",
        (gestione_id,),
    )
    rows = cursor.fetchall()
    if flat:
        return {row['id']:dict(row) for row in rows}
    categorie = {}
    for row in rows:
        macro = row["macrocategoria"]
        cat = f"{row["nome"]} - {row["macrocategoria"]}"
        k = row["id"]

        categorie.setdefault(macro, {})[k] = cat
    return categorie


def get_nomi_categorie(gestione_id):
    categorie = get_categorie(gestione_id, True)
    return {k:f"{v["nome"]} - {v["macrocategoria"]}" for k,v in categorie.items()}