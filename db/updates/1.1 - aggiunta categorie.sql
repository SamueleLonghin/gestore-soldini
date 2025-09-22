
CREATE TABLE IF NOT EXISTS categorie (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    macrocategoria TEXT NOT NULL,
    gestione_id INTEGER,
    autore_id INTEGER,
    nome TEXT NOT NULL,
    colore TEXT,
    FOREIGN KEY (gestione_id) REFERENCES gestioni(id)
);

INSERT INTO categorie (macrocategoria, gestione_id, autore_id, nome, colore) VALUES
('Casa', NULL, NULL, 'Affitto', '#FFB300'),
('Casa', NULL, NULL, 'Bollette', '#FF7043'),
('Casa', NULL, NULL, 'Manutenzione', '#8D6E63'),
('Casa', NULL, NULL, 'Spesa supermercato', '#43A047'),
('Trasporti', NULL, NULL, 'Carburante', '#1976D2'),
('Trasporti', NULL, NULL, 'Mezzi pubblici', '#388E3C'),
('Alimentari', NULL, NULL, 'Ristorante', '#D32F2F'),
('Salute', NULL, NULL, 'Farmacia', '#7B1FA2'),
('Salute', NULL, NULL, 'Visite mediche', '#0288D1'),
('Tempo libero', NULL, NULL, 'Svago', '#FBC02D'),
('Istruzione', NULL, NULL, 'Libri', '#C2185B'),
('Istruzione', NULL, NULL, 'Corsi', '#512DA8'),
('Casa', NULL, NULL, 'Abbonamenti', '#0097A7'),
('Casa', NULL, NULL, 'Finanziamenti', '#455A64');