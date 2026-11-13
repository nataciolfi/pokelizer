# Dicionário lógico/físico e relacionamentos

Gerado de `backend/schema.sql` por `python tools/document_model.py`. Não editar manualmente. Os desenhos brModelo são a representação visual complementar. O SQL e seus gatilhos definem restrições não expressáveis apenas pelas linhas do desenho.

## Convenções e cardinalidades condicionais

Cada linha da matriz é uma relação por FK, inclusive papéis diferentes entre as mesmas tabelas. Filho→pai indica quantos pais um filho referencia; pai→filho indica quantos filhos um pai pode ter. Mínimo zero no pai é permitido sem presumir que o catálogo/usuário esteja populado. Toda FK tem atualização RESTRICT; IDs são imutáveis. N significa muitos.

- ESPECIE rascunho pode ter 0..N formas; ESPECIE completa exige 1..N formas e exatamente uma padrão. A unicidade parcial e os gatilhos também protegem atualização/exclusão.
- DADOS_FORMA_JOGO pode ter 0..2 tipos no estado não verificado; quando status_tipos=aplicavel exige 1..2, incluindo posição primária; nao_aplicavel exige zero.
- PERFIL_ANALISE personalizado exige exatamente um USUARIO; referência exige zero usuários e evidência. REGULAMENTO é opcional no perfil.
- Origem de exemplar é opcional; quando id_dados_forma_origem é informado, id_jogo_origem é obrigatório e deve corresponder ao jogo daquela ficha.
- MECANICA_JOGO é opcional no exemplar sem valores contextuais conhecidos. Natureza, habilidade, nível e valores numéricos exigem mecânica confirmada compatível.
- Uma espécie/forma/jogo pode existir sem ficha, coleção, perfil, regulamento ou transformação. Não há participação mínima presumida nesses filhos.

## Matriz completa de relações

| Filho e papel (campos) | Pai (campos) | Filho→pai | Pai→filho | Unicidade da relação | Exclusão do pai |
|---|---|---|---|---|---|
| DADOS_FORMA_JOGO (id_jogo) | JOGO (id_jogo) | 1..1 | 0..N | Campos podem repetir; combinação limitada pelas chaves da tabela | RESTRICT |
| DADOS_FORMA_JOGO (id_forma) | FORMA (id_forma) | 1..1 | 0..N | Campos podem repetir; combinação limitada pelas chaves da tabela | RESTRICT |
| ELEGIBILIDADE_FORMA_REGULAMENTO (id_dados_forma) | DADOS_FORMA_JOGO (id_dados_forma) | 1..1 | 0..N | Campos podem repetir; combinação limitada pelas chaves da tabela | RESTRICT |
| ELEGIBILIDADE_FORMA_REGULAMENTO (id_regulamento) | REGULAMENTO (id_regulamento) | 1..1 | 0..N | Campos podem repetir; combinação limitada pelas chaves da tabela | RESTRICT |
| FORMA (id_especie) | ESPECIE (id_especie) | 1..1 | 0..N | Campos podem repetir; combinação limitada pelas chaves da tabela | RESTRICT |
| HABILIDADE_FORMA_JOGO (id_habilidade) | HABILIDADE (id_habilidade) | 1..1 | 0..N | Campos podem repetir; combinação limitada pelas chaves da tabela | RESTRICT |
| HABILIDADE_FORMA_JOGO (id_dados_forma) | DADOS_FORMA_JOGO (id_dados_forma) | 1..1 | 0..N | Campos podem repetir; combinação limitada pelas chaves da tabela | CASCADE |
| MECANICA_ATRIBUTO (id_atributo) | ATRIBUTO_BATALHA (id_atributo) | 1..1 | 0..N | Campos podem repetir; combinação limitada pelas chaves da tabela | RESTRICT |
| MECANICA_ATRIBUTO (id_mecanica_sistema_atributo) | MECANICA_SISTEMA_ATRIBUTO (id_mecanica_sistema_atributo) | 1..1 | 0..N | Campos podem repetir; combinação limitada pelas chaves da tabela | CASCADE |
| MECANICA_JOGO (id_jogo) | JOGO (id_jogo) | 1..1 | 0..N | Campos podem repetir; combinação limitada pelas chaves da tabela | RESTRICT |
| MECANICA_SISTEMA_ATRIBUTO (id_sistema_atributo) | SISTEMA_ATRIBUTO (id_sistema_atributo) | 1..1 | 0..N | Campos podem repetir; combinação limitada pelas chaves da tabela | RESTRICT |
| MECANICA_SISTEMA_ATRIBUTO (id_mecanica) | MECANICA_JOGO (id_mecanica) | 1..1 | 0..N | Campos podem repetir; combinação limitada pelas chaves da tabela | RESTRICT |
| METODO_FORMA_JOGO (id_metodo) | METODO_OBTENCAO (id_metodo) | 1..1 | 0..N | Campos podem repetir; combinação limitada pelas chaves da tabela | RESTRICT |
| METODO_FORMA_JOGO (id_dados_forma) | DADOS_FORMA_JOGO (id_dados_forma) | 1..1 | 0..N | Campos podem repetir; combinação limitada pelas chaves da tabela | CASCADE |
| NATUREZA (atributo_reduzido) | ATRIBUTO_BATALHA (codigo) | 0..1 | 0..N | Campos podem repetir; combinação limitada pelas chaves da tabela | RESTRICT |
| NATUREZA (atributo_aumentado) | ATRIBUTO_BATALHA (codigo) | 0..1 | 0..N | Campos podem repetir; combinação limitada pelas chaves da tabela | RESTRICT |
| PERFIL_ANALISE (id_regulamento) | REGULAMENTO (id_regulamento) | 0..1 | 0..N | Campos podem repetir; combinação limitada pelas chaves da tabela | RESTRICT |
| PERFIL_ANALISE (id_usuario) | USUARIO (id_usuario) | 0..1 | 0..N | Campos podem repetir; combinação limitada pelas chaves da tabela | CASCADE |
| PERFIL_ANALISE (id_mecanica) | MECANICA_JOGO (id_mecanica) | 1..1 | 0..N | Campos podem repetir; combinação limitada pelas chaves da tabela | RESTRICT |
| PERFIL_ANALISE (id_dados_forma) | DADOS_FORMA_JOGO (id_dados_forma) | 1..1 | 0..N | Campos podem repetir; combinação limitada pelas chaves da tabela | RESTRICT |
| PERFIL_HABILIDADE (id_habilidade_forma) | HABILIDADE_FORMA_JOGO (id_habilidade_forma) | 1..1 | 0..N | Campos podem repetir; combinação limitada pelas chaves da tabela | RESTRICT |
| PERFIL_HABILIDADE (id_perfil) | PERFIL_ANALISE (id_perfil) | 1..1 | 0..N | Campos podem repetir; combinação limitada pelas chaves da tabela | CASCADE |
| PERFIL_NATUREZA (id_natureza) | NATUREZA (id_natureza) | 1..1 | 0..N | Campos podem repetir; combinação limitada pelas chaves da tabela | RESTRICT |
| PERFIL_NATUREZA (id_perfil) | PERFIL_ANALISE (id_perfil) | 1..1 | 0..N | Campos podem repetir; combinação limitada pelas chaves da tabela | CASCADE |
| POKEMON_COLECAO (id_habilidade_forma, id_dados_forma_atual) | HABILIDADE_FORMA_JOGO (id_habilidade_forma, id_dados_forma) | 0..1 | 0..N | Campos podem repetir; combinação limitada pelas chaves da tabela | RESTRICT |
| POKEMON_COLECAO (id_natureza) | NATUREZA (id_natureza) | 0..1 | 0..N | Campos podem repetir; combinação limitada pelas chaves da tabela | RESTRICT |
| POKEMON_COLECAO (id_metodo_obtencao) | METODO_OBTENCAO (id_metodo) | 0..1 | 0..N | Campos podem repetir; combinação limitada pelas chaves da tabela | RESTRICT |
| POKEMON_COLECAO (id_dados_forma_origem) | DADOS_FORMA_JOGO (id_dados_forma) | 0..1 | 0..N | Campos podem repetir; combinação limitada pelas chaves da tabela | RESTRICT |
| POKEMON_COLECAO (id_jogo_origem) | JOGO (id_jogo) | 0..1 | 0..N | Campos podem repetir; combinação limitada pelas chaves da tabela | RESTRICT |
| POKEMON_COLECAO (id_mecanica) | MECANICA_JOGO (id_mecanica) | 0..1 | 0..N | Campos podem repetir; combinação limitada pelas chaves da tabela | RESTRICT |
| POKEMON_COLECAO (id_dados_forma_atual) | DADOS_FORMA_JOGO (id_dados_forma) | 1..1 | 0..N | Campos podem repetir; combinação limitada pelas chaves da tabela | RESTRICT |
| POKEMON_COLECAO (id_usuario) | USUARIO (id_usuario) | 1..1 | 0..N | Campos podem repetir; combinação limitada pelas chaves da tabela | CASCADE |
| REGULAMENTO (id_mecanica) | MECANICA_JOGO (id_mecanica) | 1..1 | 0..N | Campos podem repetir; combinação limitada pelas chaves da tabela | RESTRICT |
| TIPO_FORMA_JOGO (id_tipo) | TIPO (id_tipo) | 1..1 | 0..N | Campos podem repetir; combinação limitada pelas chaves da tabela | RESTRICT |
| TIPO_FORMA_JOGO (id_dados_forma) | DADOS_FORMA_JOGO (id_dados_forma) | 1..1 | 0..N | Campos podem repetir; combinação limitada pelas chaves da tabela | CASCADE |
| TRANSFORMACAO_FORMA (id_dados_forma_destino) | DADOS_FORMA_JOGO (id_dados_forma) | 1..1 | 0..N | Campos podem repetir; combinação limitada pelas chaves da tabela | RESTRICT |
| TRANSFORMACAO_FORMA (id_dados_forma_origem) | DADOS_FORMA_JOGO (id_dados_forma) | 1..1 | 0..N | Campos podem repetir; combinação limitada pelas chaves da tabela | RESTRICT |
| VALOR_ATRIBUTO_POKEMON (id_atributo) | ATRIBUTO_BATALHA (id_atributo) | 1..1 | 0..N | Campos podem repetir; combinação limitada pelas chaves da tabela | RESTRICT |
| VALOR_ATRIBUTO_POKEMON (id_mecanica_sistema_atributo) | MECANICA_SISTEMA_ATRIBUTO (id_mecanica_sistema_atributo) | 1..1 | 0..N | Campos podem repetir; combinação limitada pelas chaves da tabela | RESTRICT |
| VALOR_ATRIBUTO_POKEMON (id_pokemon_colecao) | POKEMON_COLECAO (id_pokemon_colecao) | 1..1 | 0..N | Campos podem repetir; combinação limitada pelas chaves da tabela | CASCADE |
| VALOR_PERFIL_ANALISE (id_atributo) | ATRIBUTO_BATALHA (id_atributo) | 1..1 | 0..N | Campos podem repetir; combinação limitada pelas chaves da tabela | RESTRICT |
| VALOR_PERFIL_ANALISE (id_mecanica_sistema_atributo) | MECANICA_SISTEMA_ATRIBUTO (id_mecanica_sistema_atributo) | 1..1 | 0..N | Campos podem repetir; combinação limitada pelas chaves da tabela | RESTRICT |
| VALOR_PERFIL_ANALISE (id_perfil) | PERFIL_ANALISE (id_perfil) | 1..1 | 0..N | Campos podem repetir; combinação limitada pelas chaves da tabela | CASCADE |

Contagem: **26 tabelas de domínio**, **43 relações FK**. SCHEMA_MIGRATION é metadado operacional criado pelo executor Python, fora do modelo de domínio.

## ATRIBUTO_BATALHA

| Campo | Tipo SQLite | Nulo permitido | Chave | Default |
|---|---|---|---|---|
| id_atributo | INTEGER | não | PK | — |
| codigo | TEXT | não | — | — |
| nome | TEXT | não | — | — |

Chaves: PK(id_atributo); UNIQUE(codigo).

CHECKs, índices e gatilhos: consultar a definição desta tabela em [schema.sql](../../backend/schema.sql) e a [matriz de invariantes](integrity.md).

## DADOS_FORMA_JOGO

| Campo | Tipo SQLite | Nulo permitido | Chave | Default |
|---|---|---|---|---|
| id_dados_forma | INTEGER | não | PK | — |
| id_forma | INTEGER | não | FK | — |
| id_jogo | INTEGER | não | FK | — |
| status_presenca | TEXT | não | — | 'nao_verificada' |
| pode_ser_registrada | TEXT | sim | — | — |
| motivo_registro | TEXT | sim | — | — |
| status_tipos | TEXT | não | — | 'nao_verificado' |
| altura_m | REAL | sim | — | — |
| peso_kg | REAL | sim | — | — |
| hp_base | INTEGER | sim | — | — |
| ataque_base | INTEGER | sim | — | — |
| defesa_base | INTEGER | sim | — | — |
| ataque_especial_base | INTEGER | sim | — | — |
| defesa_especial_base | INTEGER | sim | — | — |
| velocidade_base | INTEGER | sim | — | — |
| fonte_url | TEXT | sim | — | — |
| data_verificacao | TEXT | sim | — | — |

Chaves: PK(id_dados_forma); UNIQUE(id_forma, id_jogo).

CHECKs, índices e gatilhos: consultar a definição desta tabela em [schema.sql](../../backend/schema.sql) e a [matriz de invariantes](integrity.md).

## ELEGIBILIDADE_FORMA_REGULAMENTO

| Campo | Tipo SQLite | Nulo permitido | Chave | Default |
|---|---|---|---|---|
| id_elegibilidade | INTEGER | não | PK | — |
| id_regulamento | INTEGER | não | FK | — |
| id_dados_forma | INTEGER | não | FK | — |
| status | TEXT | não | — | 'nao_verificado' |
| condicao | TEXT | sim | — | — |
| fonte_url | TEXT | sim | — | — |
| data_verificacao | TEXT | sim | — | — |

Chaves: PK(id_elegibilidade); UNIQUE(id_regulamento, id_dados_forma).

CHECKs, índices e gatilhos: consultar a definição desta tabela em [schema.sql](../../backend/schema.sql) e a [matriz de invariantes](integrity.md).

## ESPECIE

| Campo | Tipo SQLite | Nulo permitido | Chave | Default |
|---|---|---|---|---|
| id_especie | INTEGER | não | PK | — |
| numero_nacional | INTEGER | não | — | — |
| nome_pt | TEXT | não | — | — |
| nome_en | TEXT | sim | — | — |
| geracao_origem | INTEGER | sim | — | — |
| status_catalogo | TEXT | não | — | 'rascunho' |
| fonte_url | TEXT | sim | — | — |
| data_verificacao | TEXT | sim | — | — |

Chaves: PK(id_especie); UNIQUE(numero_nacional).

CHECKs, índices e gatilhos: consultar a definição desta tabela em [schema.sql](../../backend/schema.sql) e a [matriz de invariantes](integrity.md).

## FORMA

| Campo | Tipo SQLite | Nulo permitido | Chave | Default |
|---|---|---|---|---|
| id_forma | INTEGER | não | PK | — |
| id_especie | INTEGER | não | FK | — |
| codigo_forma | TEXT | não | — | — |
| nome_forma | TEXT | não | — | — |
| categoria | TEXT | não | — | 'padrao' |
| estado_forma | TEXT | sim | — | — |
| descricao | TEXT | sim | — | — |
| forma_padrao | INTEGER | não | — | 0 |
| fonte_url | TEXT | sim | — | — |
| data_verificacao | TEXT | sim | — | — |

Chaves: PK(id_forma); UNIQUE parcial(id_especie); UNIQUE(id_especie, codigo_forma).

CHECKs, índices e gatilhos: consultar a definição desta tabela em [schema.sql](../../backend/schema.sql) e a [matriz de invariantes](integrity.md).

## HABILIDADE

| Campo | Tipo SQLite | Nulo permitido | Chave | Default |
|---|---|---|---|---|
| id_habilidade | INTEGER | não | PK | — |
| nome | TEXT | não | — | — |
| descricao | TEXT | sim | — | — |

Chaves: PK(id_habilidade); UNIQUE(nome).

CHECKs, índices e gatilhos: consultar a definição desta tabela em [schema.sql](../../backend/schema.sql) e a [matriz de invariantes](integrity.md).

## HABILIDADE_FORMA_JOGO

| Campo | Tipo SQLite | Nulo permitido | Chave | Default |
|---|---|---|---|---|
| id_habilidade_forma | INTEGER | não | PK | — |
| id_dados_forma | INTEGER | não | FK | — |
| id_habilidade | INTEGER | não | FK | — |
| slot | TEXT | não | — | — |
| condicao | TEXT | sim | — | — |
| fonte_url | TEXT | não | — | — |
| data_verificacao | TEXT | não | — | — |

Chaves: PK(id_habilidade_forma); UNIQUE(id_habilidade_forma, id_dados_forma); UNIQUE(id_dados_forma, slot); UNIQUE(id_dados_forma, id_habilidade, slot).

CHECKs, índices e gatilhos: consultar a definição desta tabela em [schema.sql](../../backend/schema.sql) e a [matriz de invariantes](integrity.md).

## JOGO

| Campo | Tipo SQLite | Nulo permitido | Chave | Default |
|---|---|---|---|---|
| id_jogo | INTEGER | não | PK | — |
| nome | TEXT | não | — | — |
| categoria | TEXT | sim | — | — |
| geracao | INTEGER | sim | — | — |
| plataforma | TEXT | sim | — | — |
| data_lancamento | TEXT | sim | — | — |
| fonte_url | TEXT | sim | — | — |
| data_verificacao | TEXT | sim | — | — |

Chaves: PK(id_jogo); UNIQUE(nome).

CHECKs, índices e gatilhos: consultar a definição desta tabela em [schema.sql](../../backend/schema.sql) e a [matriz de invariantes](integrity.md).

## MECANICA_ATRIBUTO

| Campo | Tipo SQLite | Nulo permitido | Chave | Default |
|---|---|---|---|---|
| id_mecanica_sistema_atributo | INTEGER | não | PK, FK | — |
| id_atributo | INTEGER | não | PK, FK | — |
| aplicabilidade | TEXT | não | — | — |
| fonte_url | TEXT | sim | — | — |
| data_verificacao | TEXT | sim | — | — |

Chaves: PK(id_mecanica_sistema_atributo, id_atributo).

CHECKs, índices e gatilhos: consultar a definição desta tabela em [schema.sql](../../backend/schema.sql) e a [matriz de invariantes](integrity.md).

## MECANICA_JOGO

| Campo | Tipo SQLite | Nulo permitido | Chave | Default |
|---|---|---|---|---|
| id_mecanica | INTEGER | não | PK | — |
| id_jogo | INTEGER | não | FK | — |
| versao | TEXT | não | — | — |
| usa_natureza | TEXT | não | — | 'nao_verificado' |
| usa_habilidade | TEXT | não | — | 'nao_verificado' |
| usa_nivel | TEXT | não | — | 'nao_verificado' |
| nivel_minimo | INTEGER | sim | — | — |
| nivel_maximo | INTEGER | sim | — | — |
| data_inicio | TEXT | sim | — | — |
| data_fim | TEXT | sim | — | — |
| fonte_url | TEXT | sim | — | — |
| data_verificacao | TEXT | sim | — | — |

Chaves: PK(id_mecanica); UNIQUE(id_jogo, versao).

CHECKs, índices e gatilhos: consultar a definição desta tabela em [schema.sql](../../backend/schema.sql) e a [matriz de invariantes](integrity.md).

## MECANICA_SISTEMA_ATRIBUTO

| Campo | Tipo SQLite | Nulo permitido | Chave | Default |
|---|---|---|---|---|
| id_mecanica_sistema_atributo | INTEGER | não | PK | — |
| id_mecanica | INTEGER | não | FK | — |
| id_sistema_atributo | INTEGER | não | FK | — |
| aplicabilidade | TEXT | não | — | 'nao_verificado' |
| unidade | TEXT | sim | — | — |
| valor_minimo | INTEGER | sim | — | — |
| valor_maximo_atributo | INTEGER | sim | — | — |
| valor_maximo_total | INTEGER | sim | — | — |
| limite_total_status | TEXT | não | — | 'nao_verificado' |
| fonte_url | TEXT | sim | — | — |
| data_verificacao | TEXT | sim | — | — |

Chaves: PK(id_mecanica_sistema_atributo); UNIQUE(id_mecanica, id_sistema_atributo).

CHECKs, índices e gatilhos: consultar a definição desta tabela em [schema.sql](../../backend/schema.sql) e a [matriz de invariantes](integrity.md).

## METODO_FORMA_JOGO

| Campo | Tipo SQLite | Nulo permitido | Chave | Default |
|---|---|---|---|---|
| id_dados_forma | INTEGER | não | PK, FK | — |
| id_metodo | INTEGER | não | PK, FK | — |
| condicao | TEXT | sim | — | — |
| fonte_url | TEXT | não | — | — |
| data_verificacao | TEXT | não | — | — |

Chaves: PK(id_dados_forma, id_metodo).

CHECKs, índices e gatilhos: consultar a definição desta tabela em [schema.sql](../../backend/schema.sql) e a [matriz de invariantes](integrity.md).

## METODO_OBTENCAO

| Campo | Tipo SQLite | Nulo permitido | Chave | Default |
|---|---|---|---|---|
| id_metodo | INTEGER | não | PK | — |
| nome | TEXT | não | — | — |
| descricao | TEXT | sim | — | — |

Chaves: PK(id_metodo); UNIQUE(nome).

CHECKs, índices e gatilhos: consultar a definição desta tabela em [schema.sql](../../backend/schema.sql) e a [matriz de invariantes](integrity.md).

## NATUREZA

| Campo | Tipo SQLite | Nulo permitido | Chave | Default |
|---|---|---|---|---|
| id_natureza | INTEGER | não | PK | — |
| nome | TEXT | não | — | — |
| atributo_aumentado | TEXT | sim | FK | — |
| atributo_reduzido | TEXT | sim | FK | — |
| estado_efeito | TEXT | não | — | 'nao_verificado' |
| fonte_url | TEXT | sim | — | — |
| data_verificacao | TEXT | sim | — | — |

Chaves: PK(id_natureza); UNIQUE(nome).

CHECKs, índices e gatilhos: consultar a definição desta tabela em [schema.sql](../../backend/schema.sql) e a [matriz de invariantes](integrity.md).

## PERFIL_ANALISE

| Campo | Tipo SQLite | Nulo permitido | Chave | Default |
|---|---|---|---|---|
| id_perfil | INTEGER | não | PK | — |
| id_dados_forma | INTEGER | não | FK | — |
| id_mecanica | INTEGER | não | FK | — |
| id_usuario | INTEGER | sim | FK | — |
| id_regulamento | INTEGER | sim | FK | — |
| nome_perfil | TEXT | não | — | — |
| descricao | TEXT | sim | — | — |
| tipo_perfil | TEXT | não | — | — |
| fonte_url | TEXT | sim | — | — |
| data_verificacao | TEXT | sim | — | — |
| versao_fonte | TEXT | sim | — | — |

Chaves: PK(id_perfil).

CHECKs, índices e gatilhos: consultar a definição desta tabela em [schema.sql](../../backend/schema.sql) e a [matriz de invariantes](integrity.md).

## PERFIL_HABILIDADE

| Campo | Tipo SQLite | Nulo permitido | Chave | Default |
|---|---|---|---|---|
| id_perfil | INTEGER | não | PK, FK | — |
| id_habilidade_forma | INTEGER | não | PK, FK | — |

Chaves: PK(id_perfil, id_habilidade_forma).

CHECKs, índices e gatilhos: consultar a definição desta tabela em [schema.sql](../../backend/schema.sql) e a [matriz de invariantes](integrity.md).

## PERFIL_NATUREZA

| Campo | Tipo SQLite | Nulo permitido | Chave | Default |
|---|---|---|---|---|
| id_perfil | INTEGER | não | PK, FK | — |
| id_natureza | INTEGER | não | PK, FK | — |

Chaves: PK(id_perfil, id_natureza).

CHECKs, índices e gatilhos: consultar a definição desta tabela em [schema.sql](../../backend/schema.sql) e a [matriz de invariantes](integrity.md).

## POKEMON_COLECAO

| Campo | Tipo SQLite | Nulo permitido | Chave | Default |
|---|---|---|---|---|
| id_pokemon_colecao | INTEGER | não | PK | — |
| id_usuario | INTEGER | não | FK | — |
| id_dados_forma_atual | INTEGER | não | FK | — |
| id_mecanica | INTEGER | sim | FK | — |
| id_jogo_origem | INTEGER | sim | FK | — |
| id_dados_forma_origem | INTEGER | sim | FK | — |
| id_metodo_obtencao | INTEGER | sim | FK | — |
| id_natureza | INTEGER | sim | FK | — |
| id_habilidade_forma | INTEGER | sim | FK | — |
| apelido | TEXT | sim | — | — |
| nivel | INTEGER | sim | — | — |
| data_registro | TEXT | não | — | CURRENT_TIMESTAMP |
| observacao | TEXT | sim | — | — |

Chaves: PK(id_pokemon_colecao).

CHECKs, índices e gatilhos: consultar a definição desta tabela em [schema.sql](../../backend/schema.sql) e a [matriz de invariantes](integrity.md).

## REGULAMENTO

| Campo | Tipo SQLite | Nulo permitido | Chave | Default |
|---|---|---|---|---|
| id_regulamento | INTEGER | não | PK | — |
| id_mecanica | INTEGER | não | FK | — |
| codigo | TEXT | não | — | — |
| versao | TEXT | não | — | — |
| nome | TEXT | não | — | — |
| formato | TEXT | não | — | — |
| temporada | TEXT | não | — | — |
| data_inicio | TEXT | sim | — | — |
| data_fim | TEXT | sim | — | — |
| fonte_url | TEXT | não | — | — |
| data_verificacao | TEXT | não | — | — |

Chaves: PK(id_regulamento); UNIQUE(id_mecanica, codigo, versao, formato, temporada).

CHECKs, índices e gatilhos: consultar a definição desta tabela em [schema.sql](../../backend/schema.sql) e a [matriz de invariantes](integrity.md).

## SISTEMA_ATRIBUTO

| Campo | Tipo SQLite | Nulo permitido | Chave | Default |
|---|---|---|---|---|
| id_sistema_atributo | INTEGER | não | PK | — |
| codigo | TEXT | não | — | — |
| nome | TEXT | não | — | — |
| descricao | TEXT | sim | — | — |

Chaves: PK(id_sistema_atributo); UNIQUE(codigo).

CHECKs, índices e gatilhos: consultar a definição desta tabela em [schema.sql](../../backend/schema.sql) e a [matriz de invariantes](integrity.md).

## TIPO

| Campo | Tipo SQLite | Nulo permitido | Chave | Default |
|---|---|---|---|---|
| id_tipo | INTEGER | não | PK | — |
| nome_tipo | TEXT | não | — | — |

Chaves: PK(id_tipo); UNIQUE(nome_tipo).

CHECKs, índices e gatilhos: consultar a definição desta tabela em [schema.sql](../../backend/schema.sql) e a [matriz de invariantes](integrity.md).

## TIPO_FORMA_JOGO

| Campo | Tipo SQLite | Nulo permitido | Chave | Default |
|---|---|---|---|---|
| id_dados_forma | INTEGER | não | PK, FK | — |
| id_tipo | INTEGER | não | PK, FK | — |
| posicao | INTEGER | não | — | — |

Chaves: PK(id_dados_forma, id_tipo); UNIQUE(id_dados_forma, posicao).

CHECKs, índices e gatilhos: consultar a definição desta tabela em [schema.sql](../../backend/schema.sql) e a [matriz de invariantes](integrity.md).

## TRANSFORMACAO_FORMA

| Campo | Tipo SQLite | Nulo permitido | Chave | Default |
|---|---|---|---|---|
| id_transformacao | INTEGER | não | PK | — |
| id_dados_forma_origem | INTEGER | não | FK | — |
| id_dados_forma_destino | INTEGER | não | FK | — |
| tipo_transformacao | TEXT | não | — | — |
| temporaria | INTEGER | não | — | — |
| condicao | TEXT | não | — | — |
| item_requerido | TEXT | sim | — | — |
| observacao | TEXT | sim | — | — |
| fonte_url | TEXT | não | — | — |
| data_verificacao | TEXT | não | — | — |

Chaves: PK(id_transformacao); UNIQUE(id_dados_forma_origem, id_dados_forma_destino, tipo_transformacao, condicao).

CHECKs, índices e gatilhos: consultar a definição desta tabela em [schema.sql](../../backend/schema.sql) e a [matriz de invariantes](integrity.md).

## USUARIO

| Campo | Tipo SQLite | Nulo permitido | Chave | Default |
|---|---|---|---|---|
| id_usuario | INTEGER | não | PK | — |
| nome_usuario | TEXT | não | — | — |
| email | TEXT | não | — | — |
| senha_hash | TEXT | não | — | — |
| data_cadastro | TEXT | não | — | CURRENT_TIMESTAMP |

Chaves: PK(id_usuario); UNIQUE(email); UNIQUE(nome_usuario).

CHECKs, índices e gatilhos: consultar a definição desta tabela em [schema.sql](../../backend/schema.sql) e a [matriz de invariantes](integrity.md).

## VALOR_ATRIBUTO_POKEMON

| Campo | Tipo SQLite | Nulo permitido | Chave | Default |
|---|---|---|---|---|
| id_valor_atributo | INTEGER | não | PK | — |
| id_pokemon_colecao | INTEGER | não | FK | — |
| id_mecanica_sistema_atributo | INTEGER | não | FK | — |
| id_atributo | INTEGER | não | FK | — |
| estado | TEXT | não | — | 'conhecido' |
| valor | INTEGER | sim | — | — |
| motivo | TEXT | sim | — | — |

Chaves: PK(id_valor_atributo); UNIQUE(id_pokemon_colecao, id_mecanica_sistema_atributo, id_atributo).

CHECKs, índices e gatilhos: consultar a definição desta tabela em [schema.sql](../../backend/schema.sql) e a [matriz de invariantes](integrity.md).

## VALOR_PERFIL_ANALISE

| Campo | Tipo SQLite | Nulo permitido | Chave | Default |
|---|---|---|---|---|
| id_valor_perfil | INTEGER | não | PK | — |
| id_perfil | INTEGER | não | FK | — |
| id_mecanica_sistema_atributo | INTEGER | não | FK | — |
| id_atributo | INTEGER | não | FK | — |
| estado | TEXT | não | — | 'conhecido' |
| valor_alvo | INTEGER | sim | — | — |
| motivo | TEXT | sim | — | — |

Chaves: PK(id_valor_perfil); UNIQUE(id_perfil, id_mecanica_sistema_atributo, id_atributo).

CHECKs, índices e gatilhos: consultar a definição desta tabela em [schema.sql](../../backend/schema.sql) e a [matriz de invariantes](integrity.md).
