
CREATE TABLE USUARIO (
    id_usuario INTEGER PRIMARY KEY,
    nome_usuario TEXT NOT NULL COLLATE NOCASE UNIQUE CHECK(length(trim(nome_usuario))>=3),
    email TEXT NOT NULL COLLATE NOCASE UNIQUE CHECK(length(trim(email))>3 AND instr(email,'@')>1),
    senha_hash TEXT NOT NULL CHECK(length(senha_hash)>=40),
    data_cadastro TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
) STRICT;

CREATE TABLE ESPECIE (
    id_especie INTEGER PRIMARY KEY,
    numero_nacional INTEGER NOT NULL UNIQUE CHECK(numero_nacional>0),
    nome_pt TEXT NOT NULL CHECK(length(trim(nome_pt))>0),
    nome_en TEXT,
    geracao_origem INTEGER CHECK(geracao_origem>0),
    status_catalogo TEXT NOT NULL DEFAULT 'rascunho' CHECK(status_catalogo IN ('rascunho','completo')),
    fonte_url TEXT,
    data_verificacao TEXT,
    CHECK((fonte_url IS NULL)=(data_verificacao IS NULL)),
    CHECK(data_verificacao IS NULL OR (date(data_verificacao,'+0 days') IS NOT NULL AND date(data_verificacao,'+0 days')=data_verificacao)),
    CHECK(status_catalogo!='completo' OR (fonte_url IS NOT NULL AND length(trim(fonte_url))>0))
) STRICT;

CREATE TABLE FORMA (
    id_forma INTEGER PRIMARY KEY,
    id_especie INTEGER NOT NULL REFERENCES ESPECIE(id_especie) ON UPDATE RESTRICT ON DELETE RESTRICT,
    codigo_forma TEXT NOT NULL CHECK(length(trim(codigo_forma))>0),
    nome_forma TEXT NOT NULL CHECK(length(trim(nome_forma))>0),
    categoria TEXT NOT NULL DEFAULT 'padrao' CHECK(length(trim(categoria))>0),
    estado_forma TEXT CHECK(estado_forma IN ('permanente','condicional','temporario','nao_verificado')),
    descricao TEXT,
    forma_padrao INTEGER NOT NULL DEFAULT 0 CHECK(forma_padrao IN (0,1)),
    fonte_url TEXT,
    data_verificacao TEXT,
    UNIQUE(id_especie,codigo_forma),
    CHECK((fonte_url IS NULL)=(data_verificacao IS NULL)),
    CHECK(data_verificacao IS NULL OR (date(data_verificacao,'+0 days') IS NOT NULL AND date(data_verificacao,'+0 days')=data_verificacao))
) STRICT;
CREATE UNIQUE INDEX ux_forma_padrao_por_especie ON FORMA(id_especie) WHERE forma_padrao=1;

CREATE TABLE JOGO (
    id_jogo INTEGER PRIMARY KEY,
    nome TEXT NOT NULL COLLATE NOCASE UNIQUE CHECK(length(trim(nome))>0),
    categoria TEXT,
    geracao INTEGER CHECK(geracao>0),
    plataforma TEXT,
    data_lancamento TEXT CHECK(data_lancamento IS NULL OR (date(data_lancamento,'+0 days') IS NOT NULL AND date(data_lancamento,'+0 days')=data_lancamento)),
    fonte_url TEXT,
    data_verificacao TEXT,
    CHECK((fonte_url IS NULL)=(data_verificacao IS NULL)),
    CHECK(data_verificacao IS NULL OR (date(data_verificacao,'+0 days') IS NOT NULL AND date(data_verificacao,'+0 days')=data_verificacao))
) STRICT;

CREATE TABLE DADOS_FORMA_JOGO (
    id_dados_forma INTEGER PRIMARY KEY,
    id_forma INTEGER NOT NULL REFERENCES FORMA(id_forma) ON UPDATE RESTRICT ON DELETE RESTRICT,
    id_jogo INTEGER NOT NULL REFERENCES JOGO(id_jogo) ON UPDATE RESTRICT ON DELETE RESTRICT,
    status_presenca TEXT NOT NULL DEFAULT 'nao_verificada' CHECK(status_presenca IN ('nativa','transferivel','ausente','nao_verificada')),
    pode_ser_registrada TEXT CHECK(pode_ser_registrada IN ('sim','nao')),
    motivo_registro TEXT,
    status_tipos TEXT NOT NULL DEFAULT 'nao_verificado' CHECK(status_tipos IN ('aplicavel','nao_aplicavel','nao_verificado')),
    altura_m REAL CHECK(altura_m>=0),
    peso_kg REAL CHECK(peso_kg>=0),
    hp_base INTEGER CHECK(hp_base>=0),
    ataque_base INTEGER CHECK(ataque_base>=0),
    defesa_base INTEGER CHECK(defesa_base>=0),
    ataque_especial_base INTEGER CHECK(ataque_especial_base>=0),
    defesa_especial_base INTEGER CHECK(defesa_especial_base>=0),
    velocidade_base INTEGER CHECK(velocidade_base>=0),
    fonte_url TEXT,
    data_verificacao TEXT,
    UNIQUE(id_forma,id_jogo),
    CHECK((fonte_url IS NULL)=(data_verificacao IS NULL)),
    CHECK(data_verificacao IS NULL OR (date(data_verificacao,'+0 days') IS NOT NULL AND date(data_verificacao,'+0 days')=data_verificacao)),
    CHECK((status_presenca='nao_verificada' AND pode_ser_registrada IS NULL AND status_tipos='nao_verificado') OR (fonte_url IS NOT NULL AND length(trim(fonte_url))>0)),
    CHECK(status_presenca!='ausente' OR pode_ser_registrada IS NULL OR pode_ser_registrada='nao')
) STRICT;

CREATE TABLE TIPO (
    id_tipo INTEGER PRIMARY KEY,
    nome_tipo TEXT NOT NULL COLLATE NOCASE UNIQUE CHECK(length(trim(nome_tipo))>0)
) STRICT;
CREATE TABLE TIPO_FORMA_JOGO (
    id_dados_forma INTEGER NOT NULL REFERENCES DADOS_FORMA_JOGO(id_dados_forma) ON UPDATE RESTRICT ON DELETE CASCADE,
    id_tipo INTEGER NOT NULL REFERENCES TIPO(id_tipo) ON UPDATE RESTRICT ON DELETE RESTRICT,
    posicao INTEGER NOT NULL CHECK(posicao IN (1,2)),
    PRIMARY KEY(id_dados_forma,id_tipo),
    UNIQUE(id_dados_forma,posicao)
) STRICT;

CREATE TABLE HABILIDADE (
    id_habilidade INTEGER PRIMARY KEY,
    nome TEXT NOT NULL COLLATE NOCASE UNIQUE CHECK(length(trim(nome))>0),
    descricao TEXT
) STRICT;
CREATE TABLE HABILIDADE_FORMA_JOGO (
    id_habilidade_forma INTEGER PRIMARY KEY,
    id_dados_forma INTEGER NOT NULL REFERENCES DADOS_FORMA_JOGO(id_dados_forma) ON UPDATE RESTRICT ON DELETE CASCADE,
    id_habilidade INTEGER NOT NULL REFERENCES HABILIDADE(id_habilidade) ON UPDATE RESTRICT ON DELETE RESTRICT,
    slot TEXT NOT NULL CHECK(length(trim(slot))>0),
    condicao TEXT,
    fonte_url TEXT NOT NULL CHECK(length(trim(fonte_url))>0),
    data_verificacao TEXT NOT NULL CHECK(date(data_verificacao,'+0 days') IS NOT NULL AND date(data_verificacao,'+0 days')=data_verificacao),
    UNIQUE(id_dados_forma,id_habilidade,slot),
    UNIQUE(id_dados_forma,slot),
    UNIQUE(id_habilidade_forma,id_dados_forma)
) STRICT;

CREATE TABLE METODO_OBTENCAO (
    id_metodo INTEGER PRIMARY KEY,
    nome TEXT NOT NULL COLLATE NOCASE UNIQUE CHECK(length(trim(nome))>0),
    descricao TEXT
) STRICT;
CREATE TABLE METODO_FORMA_JOGO (
    id_dados_forma INTEGER NOT NULL REFERENCES DADOS_FORMA_JOGO(id_dados_forma) ON UPDATE RESTRICT ON DELETE CASCADE,
    id_metodo INTEGER NOT NULL REFERENCES METODO_OBTENCAO(id_metodo) ON UPDATE RESTRICT ON DELETE RESTRICT,
    condicao TEXT,
    fonte_url TEXT NOT NULL CHECK(length(trim(fonte_url))>0),
    data_verificacao TEXT NOT NULL CHECK(date(data_verificacao,'+0 days') IS NOT NULL AND date(data_verificacao,'+0 days')=data_verificacao),
    PRIMARY KEY(id_dados_forma,id_metodo)
) STRICT;

CREATE TABLE ATRIBUTO_BATALHA (
    id_atributo INTEGER PRIMARY KEY,
    codigo TEXT NOT NULL UNIQUE CHECK(length(trim(codigo))>0),
    nome TEXT NOT NULL CHECK(length(trim(nome))>0)
) STRICT;
CREATE TABLE NATUREZA (
    id_natureza INTEGER PRIMARY KEY,
    nome TEXT NOT NULL COLLATE NOCASE UNIQUE CHECK(length(trim(nome))>0),
    atributo_aumentado TEXT REFERENCES ATRIBUTO_BATALHA(codigo) ON UPDATE RESTRICT ON DELETE RESTRICT,
    atributo_reduzido TEXT REFERENCES ATRIBUTO_BATALHA(codigo) ON UPDATE RESTRICT ON DELETE RESTRICT,
    estado_efeito TEXT NOT NULL DEFAULT 'nao_verificado' CHECK(estado_efeito IN ('neutro','modificador','nao_verificado')),
    fonte_url TEXT,
    data_verificacao TEXT,
    CHECK((fonte_url IS NULL)=(data_verificacao IS NULL)),
    CHECK(data_verificacao IS NULL OR (date(data_verificacao,'+0 days') IS NOT NULL AND date(data_verificacao,'+0 days')=data_verificacao)),
    CHECK((estado_efeito IN ('neutro','nao_verificado') AND atributo_aumentado IS NULL AND atributo_reduzido IS NULL) OR (estado_efeito='modificador' AND atributo_aumentado IS NOT NULL AND atributo_reduzido IS NOT NULL AND atributo_aumentado!=atributo_reduzido)),
    CHECK(estado_efeito='nao_verificado' OR (fonte_url IS NOT NULL AND length(trim(fonte_url))>0))
) STRICT;

CREATE TABLE MECANICA_JOGO (
    id_mecanica INTEGER PRIMARY KEY,
    id_jogo INTEGER NOT NULL REFERENCES JOGO(id_jogo) ON UPDATE RESTRICT ON DELETE RESTRICT,
    versao TEXT NOT NULL CHECK(length(trim(versao))>0),
    usa_natureza TEXT NOT NULL DEFAULT 'nao_verificado' CHECK(usa_natureza IN ('sim','nao','nao_verificado')),
    usa_habilidade TEXT NOT NULL DEFAULT 'nao_verificado' CHECK(usa_habilidade IN ('sim','nao','nao_verificado')),
    usa_nivel TEXT NOT NULL DEFAULT 'nao_verificado' CHECK(usa_nivel IN ('sim','nao','nao_verificado')),
    nivel_minimo INTEGER CHECK(nivel_minimo>=0),
    nivel_maximo INTEGER CHECK(nivel_maximo>=nivel_minimo),
    data_inicio TEXT,
    data_fim TEXT,
    fonte_url TEXT,
    data_verificacao TEXT,
    UNIQUE(id_jogo,versao),
    CHECK((fonte_url IS NULL)=(data_verificacao IS NULL)),
    CHECK(data_verificacao IS NULL OR (date(data_verificacao,'+0 days') IS NOT NULL AND date(data_verificacao,'+0 days')=data_verificacao)),
    CHECK(data_inicio IS NULL OR (date(data_inicio,'+0 days') IS NOT NULL AND date(data_inicio,'+0 days')=data_inicio)),
    CHECK(data_fim IS NULL OR (date(data_fim,'+0 days') IS NOT NULL AND date(data_fim,'+0 days')=data_fim)),
    CHECK(data_fim IS NULL OR data_inicio IS NULL OR data_fim>=data_inicio),
    CHECK(usa_nivel='sim' OR (nivel_minimo IS NULL AND nivel_maximo IS NULL)),
    CHECK((usa_natureza='nao_verificado' AND usa_habilidade='nao_verificado' AND usa_nivel='nao_verificado') OR (fonte_url IS NOT NULL AND length(trim(fonte_url))>0))
) STRICT;

CREATE TABLE SISTEMA_ATRIBUTO (
    id_sistema_atributo INTEGER PRIMARY KEY,
    codigo TEXT NOT NULL UNIQUE CHECK(length(trim(codigo))>0),
    nome TEXT NOT NULL CHECK(length(trim(nome))>0),
    descricao TEXT
) STRICT;
CREATE TABLE MECANICA_SISTEMA_ATRIBUTO (
    id_mecanica_sistema_atributo INTEGER PRIMARY KEY,
    id_mecanica INTEGER NOT NULL REFERENCES MECANICA_JOGO(id_mecanica) ON UPDATE RESTRICT ON DELETE RESTRICT,
    id_sistema_atributo INTEGER NOT NULL REFERENCES SISTEMA_ATRIBUTO(id_sistema_atributo) ON UPDATE RESTRICT ON DELETE RESTRICT,
    aplicabilidade TEXT NOT NULL DEFAULT 'nao_verificado' CHECK(aplicabilidade IN ('aplicavel','nao_aplicavel','nao_verificado')),
    unidade TEXT,
    valor_minimo INTEGER CHECK(valor_minimo>=0),
    valor_maximo_atributo INTEGER CHECK(valor_maximo_atributo>=valor_minimo),
    valor_maximo_total INTEGER CHECK(valor_maximo_total>=0),
    limite_total_status TEXT NOT NULL DEFAULT 'nao_verificado' CHECK(limite_total_status IN ('confirmado','nao_aplicavel','nao_verificado')),
    fonte_url TEXT,
    data_verificacao TEXT,
    UNIQUE(id_mecanica,id_sistema_atributo),
    CHECK((fonte_url IS NULL)=(data_verificacao IS NULL)),
    CHECK(data_verificacao IS NULL OR (date(data_verificacao,'+0 days') IS NOT NULL AND date(data_verificacao,'+0 days')=data_verificacao)),
    CHECK(aplicabilidade='aplicavel' OR (valor_minimo IS NULL AND valor_maximo_atributo IS NULL AND valor_maximo_total IS NULL AND limite_total_status='nao_verificado')),
    CHECK((limite_total_status='confirmado' AND valor_maximo_total IS NOT NULL) OR (limite_total_status!='confirmado' AND valor_maximo_total IS NULL)),
    CHECK(aplicabilidade='nao_verificado' OR (fonte_url IS NOT NULL AND length(trim(fonte_url))>0))
) STRICT;
-- Some mechanics do not have all globally named attributes. This records exact applicability.
CREATE TABLE MECANICA_ATRIBUTO (
    id_mecanica_sistema_atributo INTEGER NOT NULL REFERENCES MECANICA_SISTEMA_ATRIBUTO(id_mecanica_sistema_atributo) ON UPDATE RESTRICT ON DELETE CASCADE,
    id_atributo INTEGER NOT NULL REFERENCES ATRIBUTO_BATALHA(id_atributo) ON UPDATE RESTRICT ON DELETE RESTRICT,
    aplicabilidade TEXT NOT NULL CHECK(aplicabilidade IN ('aplicavel','nao_aplicavel','nao_verificado')),
    fonte_url TEXT,
    data_verificacao TEXT,
    PRIMARY KEY(id_mecanica_sistema_atributo,id_atributo),
    CHECK((fonte_url IS NULL)=(data_verificacao IS NULL)),
    CHECK(data_verificacao IS NULL OR (date(data_verificacao,'+0 days') IS NOT NULL AND date(data_verificacao,'+0 days')=data_verificacao)),
    CHECK(aplicabilidade='nao_verificado' OR (fonte_url IS NOT NULL AND length(trim(fonte_url))>0))
) STRICT;

CREATE TABLE POKEMON_COLECAO (
    id_pokemon_colecao INTEGER PRIMARY KEY,
    id_usuario INTEGER NOT NULL REFERENCES USUARIO(id_usuario) ON UPDATE RESTRICT ON DELETE CASCADE,
    id_dados_forma_atual INTEGER NOT NULL REFERENCES DADOS_FORMA_JOGO(id_dados_forma) ON UPDATE RESTRICT ON DELETE RESTRICT,
    id_mecanica INTEGER REFERENCES MECANICA_JOGO(id_mecanica) ON UPDATE RESTRICT ON DELETE RESTRICT,
    id_jogo_origem INTEGER REFERENCES JOGO(id_jogo) ON UPDATE RESTRICT ON DELETE RESTRICT,
    id_dados_forma_origem INTEGER REFERENCES DADOS_FORMA_JOGO(id_dados_forma) ON UPDATE RESTRICT ON DELETE RESTRICT,
    id_metodo_obtencao INTEGER REFERENCES METODO_OBTENCAO(id_metodo) ON UPDATE RESTRICT ON DELETE RESTRICT,
    id_natureza INTEGER REFERENCES NATUREZA(id_natureza) ON UPDATE RESTRICT ON DELETE RESTRICT,
    id_habilidade_forma INTEGER,
    apelido TEXT CHECK(length(apelido)<=40),
    nivel INTEGER CHECK(nivel>=0),
    data_registro TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    observacao TEXT CHECK(length(observacao)<=500),
    FOREIGN KEY(id_habilidade_forma,id_dados_forma_atual) REFERENCES HABILIDADE_FORMA_JOGO(id_habilidade_forma,id_dados_forma) ON UPDATE RESTRICT ON DELETE RESTRICT
) STRICT;

CREATE TABLE REGULAMENTO (
    id_regulamento INTEGER PRIMARY KEY,
    id_mecanica INTEGER NOT NULL REFERENCES MECANICA_JOGO(id_mecanica) ON UPDATE RESTRICT ON DELETE RESTRICT,
    codigo TEXT NOT NULL CHECK(length(trim(codigo))>0),
    versao TEXT NOT NULL CHECK(length(trim(versao))>0),
    nome TEXT NOT NULL CHECK(length(trim(nome))>0),
    formato TEXT NOT NULL CHECK(length(trim(formato))>0),
    temporada TEXT NOT NULL CHECK(length(trim(temporada))>0),
    data_inicio TEXT,
    data_fim TEXT,
    fonte_url TEXT NOT NULL CHECK(length(trim(fonte_url))>0),
    data_verificacao TEXT NOT NULL CHECK(date(data_verificacao,'+0 days') IS NOT NULL AND date(data_verificacao,'+0 days')=data_verificacao),
    UNIQUE(id_mecanica,codigo,versao,formato,temporada),
    CHECK(data_inicio IS NULL OR (date(data_inicio,'+0 days') IS NOT NULL AND date(data_inicio,'+0 days')=data_inicio)),
    CHECK(data_fim IS NULL OR (date(data_fim,'+0 days') IS NOT NULL AND date(data_fim,'+0 days')=data_fim)),
    CHECK(data_fim IS NULL OR data_inicio IS NULL OR data_fim>=data_inicio)
) STRICT;
CREATE TABLE PERFIL_ANALISE (
    id_perfil INTEGER PRIMARY KEY,
    id_dados_forma INTEGER NOT NULL REFERENCES DADOS_FORMA_JOGO(id_dados_forma) ON UPDATE RESTRICT ON DELETE RESTRICT,
    id_mecanica INTEGER NOT NULL REFERENCES MECANICA_JOGO(id_mecanica) ON UPDATE RESTRICT ON DELETE RESTRICT,
    id_usuario INTEGER REFERENCES USUARIO(id_usuario) ON UPDATE RESTRICT ON DELETE CASCADE,
    id_regulamento INTEGER REFERENCES REGULAMENTO(id_regulamento) ON UPDATE RESTRICT ON DELETE RESTRICT,
    nome_perfil TEXT NOT NULL CHECK(length(trim(nome_perfil))>0),
    descricao TEXT,
    tipo_perfil TEXT NOT NULL CHECK(tipo_perfil IN ('personalizado','referencia_competitiva')),
    fonte_url TEXT,
    data_verificacao TEXT,
    versao_fonte TEXT,
    CHECK((tipo_perfil='personalizado' AND id_usuario IS NOT NULL) OR (tipo_perfil='referencia_competitiva' AND id_usuario IS NULL)),
    CHECK((fonte_url IS NULL)=(data_verificacao IS NULL)),
    CHECK(data_verificacao IS NULL OR (date(data_verificacao,'+0 days') IS NOT NULL AND date(data_verificacao,'+0 days')=data_verificacao)),
    CHECK(tipo_perfil!='referencia_competitiva' OR (fonte_url IS NOT NULL AND length(trim(fonte_url))>0 AND versao_fonte IS NOT NULL AND length(trim(versao_fonte))>0))
) STRICT;
CREATE TABLE VALOR_ATRIBUTO_POKEMON (
    id_valor_atributo INTEGER PRIMARY KEY,
    id_pokemon_colecao INTEGER NOT NULL REFERENCES POKEMON_COLECAO(id_pokemon_colecao) ON UPDATE RESTRICT ON DELETE CASCADE,
    id_mecanica_sistema_atributo INTEGER NOT NULL REFERENCES MECANICA_SISTEMA_ATRIBUTO(id_mecanica_sistema_atributo) ON UPDATE RESTRICT ON DELETE RESTRICT,
    id_atributo INTEGER NOT NULL REFERENCES ATRIBUTO_BATALHA(id_atributo) ON UPDATE RESTRICT ON DELETE RESTRICT,
    estado TEXT NOT NULL DEFAULT 'conhecido' CHECK(estado IN ('conhecido','desconhecido','nao_aplicavel')),
    valor INTEGER,
    motivo TEXT,
    UNIQUE(id_pokemon_colecao,id_mecanica_sistema_atributo,id_atributo),
    CHECK((estado='conhecido' AND valor IS NOT NULL) OR (estado!='conhecido' AND valor IS NULL))
) STRICT;
CREATE TABLE VALOR_PERFIL_ANALISE (
    id_valor_perfil INTEGER PRIMARY KEY,
    id_perfil INTEGER NOT NULL REFERENCES PERFIL_ANALISE(id_perfil) ON UPDATE RESTRICT ON DELETE CASCADE,
    id_mecanica_sistema_atributo INTEGER NOT NULL REFERENCES MECANICA_SISTEMA_ATRIBUTO(id_mecanica_sistema_atributo) ON UPDATE RESTRICT ON DELETE RESTRICT,
    id_atributo INTEGER NOT NULL REFERENCES ATRIBUTO_BATALHA(id_atributo) ON UPDATE RESTRICT ON DELETE RESTRICT,
    estado TEXT NOT NULL DEFAULT 'conhecido' CHECK(estado IN ('conhecido','desconhecido','nao_aplicavel')),
    valor_alvo INTEGER,
    motivo TEXT,
    UNIQUE(id_perfil,id_mecanica_sistema_atributo,id_atributo),
    CHECK((estado='conhecido' AND valor_alvo IS NOT NULL) OR (estado!='conhecido' AND valor_alvo IS NULL))
) STRICT;
CREATE TABLE PERFIL_NATUREZA (
    id_perfil INTEGER NOT NULL REFERENCES PERFIL_ANALISE(id_perfil) ON UPDATE RESTRICT ON DELETE CASCADE,
    id_natureza INTEGER NOT NULL REFERENCES NATUREZA(id_natureza) ON UPDATE RESTRICT ON DELETE RESTRICT,
    PRIMARY KEY(id_perfil,id_natureza)
) STRICT;
CREATE TABLE PERFIL_HABILIDADE (
    id_perfil INTEGER NOT NULL REFERENCES PERFIL_ANALISE(id_perfil) ON UPDATE RESTRICT ON DELETE CASCADE,
    id_habilidade_forma INTEGER NOT NULL REFERENCES HABILIDADE_FORMA_JOGO(id_habilidade_forma) ON UPDATE RESTRICT ON DELETE RESTRICT,
    PRIMARY KEY(id_perfil,id_habilidade_forma)
) STRICT;
CREATE TABLE ELEGIBILIDADE_FORMA_REGULAMENTO (
    id_elegibilidade INTEGER PRIMARY KEY,
    id_regulamento INTEGER NOT NULL REFERENCES REGULAMENTO(id_regulamento) ON UPDATE RESTRICT ON DELETE RESTRICT,
    id_dados_forma INTEGER NOT NULL REFERENCES DADOS_FORMA_JOGO(id_dados_forma) ON UPDATE RESTRICT ON DELETE RESTRICT,
    status TEXT NOT NULL DEFAULT 'nao_verificado' CHECK(status IN ('permitido','restrito','proibido','condicional','nao_verificado')),
    condicao TEXT,
    fonte_url TEXT,
    data_verificacao TEXT,
    UNIQUE(id_regulamento,id_dados_forma),
    CHECK((fonte_url IS NULL)=(data_verificacao IS NULL)),
    CHECK(data_verificacao IS NULL OR (date(data_verificacao,'+0 days') IS NOT NULL AND date(data_verificacao,'+0 days')=data_verificacao)),
    CHECK(status='nao_verificado' OR (fonte_url IS NOT NULL AND length(trim(fonte_url))>0)),
    CHECK(status NOT IN ('restrito','condicional') OR (condicao IS NOT NULL AND length(trim(condicao))>0))
) STRICT;
CREATE TABLE TRANSFORMACAO_FORMA (
    id_transformacao INTEGER PRIMARY KEY,
    id_dados_forma_origem INTEGER NOT NULL REFERENCES DADOS_FORMA_JOGO(id_dados_forma) ON UPDATE RESTRICT ON DELETE RESTRICT,
    id_dados_forma_destino INTEGER NOT NULL REFERENCES DADOS_FORMA_JOGO(id_dados_forma) ON UPDATE RESTRICT ON DELETE RESTRICT,
    tipo_transformacao TEXT NOT NULL CHECK(length(trim(tipo_transformacao))>0),
    temporaria INTEGER NOT NULL CHECK(temporaria IN (0,1)),
    condicao TEXT NOT NULL CHECK(length(trim(condicao))>0),
    item_requerido TEXT,
    observacao TEXT,
    fonte_url TEXT NOT NULL CHECK(length(trim(fonte_url))>0),
    data_verificacao TEXT NOT NULL CHECK(date(data_verificacao,'+0 days') IS NOT NULL AND date(data_verificacao,'+0 days')=data_verificacao),
    UNIQUE(id_dados_forma_origem,id_dados_forma_destino,tipo_transformacao,condicao),
    CHECK(id_dados_forma_origem!=id_dados_forma_destino)
) STRICT;

CREATE INDEX ix_especie_nome_pt ON ESPECIE(nome_pt COLLATE NOCASE);
CREATE INDEX ix_especie_geracao ON ESPECIE(geracao_origem);
CREATE INDEX ix_forma_especie ON FORMA(id_especie);
CREATE INDEX ix_dados_forma_jogo ON DADOS_FORMA_JOGO(id_jogo,id_forma);
CREATE INDEX ix_tipo_contexto ON TIPO_FORMA_JOGO(id_tipo,id_dados_forma);
CREATE INDEX ix_colecao_usuario ON POKEMON_COLECAO(id_usuario,id_pokemon_colecao);
CREATE INDEX ix_colecao_contexto ON POKEMON_COLECAO(id_dados_forma_atual);
CREATE INDEX ix_colecao_mecanica ON POKEMON_COLECAO(id_mecanica);
CREATE INDEX ix_perfil_usuario ON PERFIL_ANALISE(id_usuario,id_perfil);
CREATE INDEX ix_perfil_contexto ON PERFIL_ANALISE(id_dados_forma,id_mecanica);
CREATE INDEX ix_elegibilidade_contexto ON ELEGIBILIDADE_FORMA_REGULAMENTO(id_dados_forma);
