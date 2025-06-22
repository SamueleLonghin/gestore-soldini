from flask import Flask
from dotenv import load_dotenv
from db.database import init_db
from tools.template_filters import init_template_filters

load_dotenv()


def create_app():
    app = Flask(__name__)

    init_db()

    init_template_filters(app)

    # Carica la configurazione da un file
    app.config.from_object("config.Config")

    # Rendi la funzione `attribute` disponibile nei template
    app.jinja_env.globals["attribute"] = getattr

    print("Configurazione dell'applicazione:")
    print("================================")
    for k, v in app.config.items():
        print(k, "->", v)
    print("================================")

    from routes import main

    app.register_blueprint(main)

    from gestione import gestionebp

    app.register_blueprint(gestionebp)

    return app


if __name__ == "__main__":
    app = create_app()
    print("Avvio dell'applicazione Flask...")
    app.run(debug=False)
    print("Applicazione Flask avviata con successo.")
