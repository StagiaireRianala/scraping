CREATE DATABASE rag;

\c rag

CREATE TABLE utilisateur (
    id_utilisateur SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    mdp VARCHAR(255) NOT NULL,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) DEFAULT 'active'  -- Pour gérer actif/inactif
);

CREATE TABLE contexte (
    id_contexte SERIAL PRIMARY KEY,
    sujet VARCHAR(255),
    description TEXT,                    -- Ajouter des détails sur le contexte
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE conversation (
    id_conversation SERIAL PRIMARY KEY,
    id_utilisateur INT NOT NULL,
    id_contexte INT,                     -- Relie la conversation à un contexte
    start_conv TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_utilisateur) REFERENCES utilisateur(id_utilisateur),
    FOREIGN KEY (id_contexte) REFERENCES contexte(id_contexte)
);
CREATE TABLE message (
    id_message SERIAL PRIMARY KEY,
    id_conversation INT NOT NULL,
    sender VARCHAR(50) ,         -- 'user' ou 'bot'
    type VARCHAR(50) DEFAULT 'text',     -- Ajoute le type (texte, image, etc.)
    message TEXT ,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_conversation) REFERENCES conversation(id_conversation)
);
