# utils/categories.py
import json
from typing import Dict


def serialize_options(categorie) -> str:
    """
    -> stringa JSON compatta (UTF-8) pronta da salvare.
    """
    return json.dumps(categorie, ensure_ascii=False, separators=(",", ":"))

def deserialize_options(s: str) :
    """
    <- ripristina le chiavi a int (JSON le salva come stringhe).
    """
    raw = json.loads(s)
    return raw
