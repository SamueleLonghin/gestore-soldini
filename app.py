import os
from flask import Flask, g
from dotenv import load_dotenv
load_dotenv()
from db.database import get_db, init_db
from tools.template_filters import init_template_filters

app = Flask(__name__)

init_db()

init_template_filters(app)

# Carica la configurazione da un file
app.config.from_object("config.Config")

# Rendi la funzione `attribute` disponibile nei template
app.jinja_env.globals["attribute"] = getattr
app.jinja_env.globals["type"] = type

# print("Configurazione dell'applicazione:")
# print("================================")
# for k, v in app.config.items():
#     print(k, "->", v)
print("================================")
@app.before_request
def before_request():
    # Apri connessione e cursore, disponibili in tutta la request
    print("Before Action")
    g.db = get_db()
    g.cur = g.db.cursor(dictionary=True)

@app.after_request
def after_request(response):
    # Chiudi cursore e connessione al termine della request
    cur = getattr(g, "cur", None)
    if cur is not None:
        cur.close()
    conn = getattr(g, "db", None)
    if conn is not None:
        conn.close()
    return response

from routes import main

app.register_blueprint(main)

from gestione import gestionebp

app.register_blueprint(gestionebp)


if __name__ == "__main__":
    
    print("Avvio dell'applicazione Flask...")
    
    app.run(debug=True)
    print("Applicazione Flask avviata con successo.")

