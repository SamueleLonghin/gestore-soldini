from app.db.database import get_db


def get_or_create_user(email):
    db = get_db()
    user = db.execute("SELECT * FROM utenti WHERE email = ?", (email,)).fetchone()
    if user:
        return user["id"]
    cur = db.execute("INSERT INTO utenti (email) VALUES (?)", (email,))
    db.commit()
    return cur.lastrowid

