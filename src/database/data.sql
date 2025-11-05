

CREATE TABLE IF NOT EXISTS Indicador(
    id_indicador SERIAL PRIMARY KEY,
    indicador_nome VARCHAR NOT NULL(40),
    formato VARCHAR(15) NOT NULL
)

CREATE TABLE IF NOT EXISTS Periodo(
    id_indicador SERIAL PRIMARY KEY,
    ano INTEGER NOT NULL
)

CREATE TABLE IF NOT EXISTS Regiao(
    id_regiao SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    populacao INTEGER NOT NULL
)