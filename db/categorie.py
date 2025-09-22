from flask import g

def get_categorie(gestione_id, flat=False):
    g.cur.execute(
        "SELECT id, nome, macrocategoria, colore FROM categorie WHERE gestione_id IS NULL OR gestione_id = %s",
        (gestione_id,),
    )
    rows = g.cur.fetchall()
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