from flask import g


def get_or_create_user(email):
    g.cur.execute("SELECT * FROM utenti WHERE email = %s", (email,))
    user = g.cur.fetchone()
    if user:
        return user["id"]
    g.cur.execute("INSERT INTO utenti (email) VALUES (%s)", (email,))
    g.db.commit()
    return g.cur.lastrowid

