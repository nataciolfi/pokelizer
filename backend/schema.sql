PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS USUARIO (
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_usuario TEXT NOT NULL COLLATE NOCASE UNIQUE,
    email TEXT NOT NULL COLLATE NOCASE UNIQUE,
    senha_hash TEXT NOT NULL,
    data_cadastro TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ESPECIE (
    id_especie INTEGER PRIMARY KEY AUTOINCREMENT,
    numero_nacional INTEGER NOT NULL UNIQUE CHECK (numero_nacional > 0),
    nome_pt TEXT NOT NULL COLLATE NOCASE UNIQUE,
    nome_en TEXT,
    geracao_origem INTEGER CHECK (geracao_origem IS NULL OR geracao_origem > 0)
);

CREATE TABLE IF NOT EXISTS FORMA (
    id_forma INTEGER PRIMARY KEY AUTOINCREMENT,
    id_especie INTEGER NOT NULL,
    codigo_forma TEXT NOT NULL,
    nome_forma TEXT NOT NULL,
    categoria TEXT NOT NULL DEFAULT 'padrao',
    estado_forma TEXT,
    descricao TEXT,
    forma_padrao INTEGER NOT NULL DEFAULT 0 CHECK (forma_padrao IN (0, 1)),
    fonte_url TEXT,
    data_verificacao TEXT,
    UNIQUE (id_especie, codigo_forma),
    FOREIGN KEY (id_especie) REFERENCES ESPECIE(id_especie) ON DELETE RESTRICT
);

CREATE UNIQUE INDEX IF NOT EXISTS ux_forma_padrao_por_especie
    ON FORMA(id_especie) WHERE forma_padrao = 1;

CREATE TABLE IF NOT EXISTS JOGO (
    id_jogo INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL COLLATE NOCASE UNIQUE,
    categoria TEXT,
    geracao INTEGER CHECK (geracao IS NULL OR geracao > 0),
    plataforma TEXT
);

CREATE TABLE IF NOT EXISTS DADOS_FORMA_JOGO (
    id_dados_forma INTEGER PRIMARY KEY AUTOINCREMENT,
    id_forma INTEGER NOT NULL,
    id_jogo INTEGER NOT NULL,
    status_presenca TEXT NOT NULL DEFAULT 'nao_verificada'
        CHECK (status_presenca IN ('nativa', 'transferivel', 'ausente', 'nao_verificada')),
    pode_ser_registrada TEXT
        CHECK (pode_ser_registrada IS NULL OR pode_ser_registrada IN ('sim', 'nao')),
    altura_m REAL CHECK (altura_m IS NULL OR altura_m >= 0),
    peso_kg REAL CHECK (peso_kg IS NULL OR peso_kg >= 0),
    hp_base INTEGER CHECK (hp_base IS NULL OR hp_base >= 0),
    ataque_base INTEGER CHECK (ataque_base IS NULL OR ataque_base >= 0),
    defesa_base INTEGER CHECK (defesa_base IS NULL OR defesa_base >= 0),
    ataque_especial_base INTEGER CHECK (ataque_especial_base IS NULL OR ataque_especial_base >= 0),
    defesa_especial_base INTEGER CHECK (defesa_especial_base IS NULL OR defesa_especial_base >= 0),
    velocidade_base INTEGER CHECK (velocidade_base IS NULL OR velocidade_base >= 0),
    fonte_url TEXT,
    data_verificacao TEXT,
    UNIQUE (id_forma, id_jogo),
    FOREIGN KEY (id_forma) REFERENCES FORMA(id_forma) ON DELETE RESTRICT,
    FOREIGN KEY (id_jogo) REFERENCES JOGO(id_jogo) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS TIPO (
    id_tipo INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_tipo TEXT NOT NULL COLLATE NOCASE UNIQUE
);

CREATE TABLE IF NOT EXISTS TIPO_FORMA_JOGO (
    id_dados_forma INTEGER NOT NULL,
    id_tipo INTEGER NOT NULL,
    posicao INTEGER NOT NULL CHECK (posicao IN (1, 2)),
    PRIMARY KEY (id_dados_forma, id_tipo),
    UNIQUE (id_dados_forma, posicao),
    FOREIGN KEY (id_dados_forma) REFERENCES DADOS_FORMA_JOGO(id_dados_forma) ON DELETE CASCADE,
    FOREIGN KEY (id_tipo) REFERENCES TIPO(id_tipo) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS HABILIDADE (
    id_habilidade INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL COLLATE NOCASE UNIQUE,
    descricao TEXT
);

CREATE TABLE IF NOT EXISTS HABILIDADE_FORMA_JOGO (
    id_habilidade_forma INTEGER PRIMARY KEY AUTOINCREMENT,
    id_dados_forma INTEGER NOT NULL,
    id_habilidade INTEGER NOT NULL,
    slot TEXT NOT NULL,
    condicao TEXT,
    UNIQUE (id_dados_forma, id_habilidade, slot),
    FOREIGN KEY (id_dados_forma) REFERENCES DADOS_FORMA_JOGO(id_dados_forma) ON DELETE CASCADE,
    FOREIGN KEY (id_habilidade) REFERENCES HABILIDADE(id_habilidade) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS METODO_OBTENCAO (
    id_metodo INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL COLLATE NOCASE UNIQUE,
    descricao TEXT
);

CREATE TABLE IF NOT EXISTS METODO_FORMA_JOGO (
    id_dados_forma INTEGER NOT NULL,
    id_metodo INTEGER NOT NULL,
    condicao TEXT,
    PRIMARY KEY (id_dados_forma, id_metodo),
    FOREIGN KEY (id_dados_forma) REFERENCES DADOS_FORMA_JOGO(id_dados_forma) ON DELETE CASCADE,
    FOREIGN KEY (id_metodo) REFERENCES METODO_OBTENCAO(id_metodo) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS NATUREZA (
    id_natureza INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL COLLATE NOCASE UNIQUE,
    atributo_aumentado TEXT,
    atributo_reduzido TEXT
);

CREATE TABLE IF NOT EXISTS POKEMON_COLECAO (
    id_pokemon_colecao INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER NOT NULL,
    id_dados_forma_atual INTEGER NOT NULL,
    id_jogo_origem INTEGER,
    id_metodo_obtencao INTEGER,
    id_natureza INTEGER,
    id_habilidade_forma INTEGER,
    apelido TEXT,
    nivel INTEGER CHECK (nivel IS NULL OR nivel BETWEEN 1 AND 100),
    data_registro TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    observacao TEXT,
    FOREIGN KEY (id_usuario) REFERENCES USUARIO(id_usuario) ON DELETE CASCADE,
    FOREIGN KEY (id_dados_forma_atual) REFERENCES DADOS_FORMA_JOGO(id_dados_forma) ON DELETE RESTRICT,
    FOREIGN KEY (id_jogo_origem) REFERENCES JOGO(id_jogo) ON DELETE RESTRICT,
    FOREIGN KEY (id_metodo_obtencao) REFERENCES METODO_OBTENCAO(id_metodo) ON DELETE RESTRICT,
    FOREIGN KEY (id_natureza) REFERENCES NATUREZA(id_natureza) ON DELETE RESTRICT,
    FOREIGN KEY (id_habilidade_forma) REFERENCES HABILIDADE_FORMA_JOGO(id_habilidade_forma) ON DELETE RESTRICT
);

CREATE INDEX IF NOT EXISTS ix_colecao_usuario ON POKEMON_COLECAO(id_usuario);
CREATE INDEX IF NOT EXISTS ix_dados_forma_jogo ON DADOS_FORMA_JOGO(id_jogo, id_forma);
