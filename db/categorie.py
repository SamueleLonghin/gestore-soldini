from db.db_interface import get_db


def get_categorie(gestione_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "SELECT id, nome, macrocategoria, colore FROM categorie WHERE gestione_id IS NULL OR gestione_id = ?",
        (gestione_id,),
    )
    rows = cursor.fetchall()
    categorie = {}
    for row in rows:
        macro = row["macrocategoria"]
        cat = f"{row["nome"]} - {row["macrocategoria"]}"
        k = row["id"]

        categorie.setdefault(macro, {})[k] = cat
    return categorie
