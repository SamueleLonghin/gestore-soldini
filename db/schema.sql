CREATE TABLE IF NOT EXISTS versioni (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    versione TEXT NOT NULL,
    data DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS utenti (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS gestioni (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS gestione_utenti (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    utente_id INTEGER NOT NULL,
    gestione_id INTEGER NOT NULL,
    FOREIGN KEY (utente_id) REFERENCES utenti(id),
    FOREIGN KEY (gestione_id) REFERENCES gestioni(id),
    UNIQUE (utente_id, gestione_id) -- ogni utente può essere associato una sola volta
);

CREATE TABLE IF NOT EXISTS categorie (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    macrocategoria TEXT NOT NULL,
    gestione_id INTEGER,
    autore_id INTEGER,
    nome TEXT NOT NULL,
    colore TEXT,
    FOREIGN KEY (gestione_id) REFERENCES gestioni(id)
);


CREATE TABLE IF NOT EXISTS spese (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    gestione_id INTEGER NOT NULL,
    autore_id INTEGER NOT NULL,
    data DATE,
    mese TEXT,
    anno TEXT,
    importo REAL,
    descrizione TEXT,
    categoria TEXT,
    id_ricorrenza INTEGER,
    FOREIGN KEY (gestione_id) REFERENCES gestioni(id),
    FOREIGN KEY (autore_id) REFERENCES utenti(id),
    FOREIGN KEY (id_ricorrenza) REFERENCES spese_ricorrenti(id)
);

CREATE TABLE IF NOT EXISTS ingressi (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    gestione_id INTEGER NOT NULL,
    autore_id INTEGER NOT NULL,
    data DATE,
    mese TEXT,
    anno TEXT,
    importo REAL,
    descrizione TEXT,
    categoria TEXT,
    note TEXT,
    conto TEXT,
    FOREIGN KEY (gestione_id) REFERENCES gestioni(id),
    FOREIGN KEY (autore_id) REFERENCES utenti(id)
);

CREATE TABLE IF NOT EXISTS spese_ricorrenti (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    gestione_id INTEGER NOT NULL,
    autore_id INTEGER NOT NULL,
    nome TEXT,
    categoria TEXT,
    data_inizio DATE,
    frequenza_unità TEXT CHECK (frequenza_unità IN ('giorno', 'mese', 'anno')),
    frequenza_intervallo INTEGER,
    importo REAL,
    FOREIGN KEY (gestione_id) REFERENCES gestioni(id),
    FOREIGN KEY (autore_id) REFERENCES utenti(id)
);
