# Modelo conceitual — PokéAnalyzer 3.0

**Status:** referência corrigida para o próximo DER e modelo lógico.  
**Data:** 04/11/2026.

## 1. Separações obrigatórias

1. Catálogo: espécies e formas oficiais.
2. Contexto de jogo: presença e dados de uma forma em cada jogo.
3. Mecânicas: versões de regras de um jogo.
4. Coleção: exemplares individuais, com origem e contexto atual.
5. Análise: perfil de comparação separado de regulamento.

Espécie não é forma; forma não é exemplar; ficha de forma/jogo não é versão de regras; recomendação não é regulamento.

## 2. Entidades

### USUARIO
- **id_usuario:** PK.
- nome_usuario: nome público, único.
- email: e-mail único, sem diferença por maiúsculas/minúsculas.
- senha_hash: hash de biblioteca reconhecida.
- data_cadastro: data de criação.

### ESPECIE
- **id_especie:** PK.
- numero_nacional: número oficial, único.
- nome_pt, nome_en.
- geracao_origem.

Número nacional identifica a espécie, não cada forma.

### FORMA
- **id_forma:** PK.
- id_especie: FK.
- codigo_forma: identificador estável, único dentro da espécie.
- nome_forma.
- categoria: padrão, regional, gênero, sazonal, cosmética, fusão, batalha ou outra documentada.
- estado_forma: permanente, condicional ou temporário, quando conhecido.
- descricao, forma_padrao.
- fonte_url, data_verificacao.

Deve existir exatamente uma forma padrão por espécie. Categoria não determina, sozinha, se pode ser armazenada em um jogo.

### JOGO
- **id_jogo:** PK.
- nome: título/edição oficial, único.
- categoria: série principal, batalha ou spin-off.
- geracao, plataforma, data_lancamento.

Scarlet e Violet são jogos distintos para compatibilidade específica.

### MECANICA_JOGO
- **id_mecanica:** PK.
- id_jogo: FK.
- versao: versão ou conjunto de regras.
- usa_natureza: sim, não ou NULL enquanto não verificado.
- data_inicio, data_fim.
- fonte_url, data_verificacao.

A mecânica é versionada, mas fica separada dos dados da forma.

### DADOS_FORMA_JOGO
- **id_dados_forma:** PK.
- id_forma: FK.
- id_jogo: FK.
- status_presenca: nativa, transferível, ausente ou não verificada.
- pode_ser_registrada: sim, não ou NULL se desconhecido.
- altura_m, peso_kg: decimal.
- hp_base, ataque_base, defesa_base, ataque_especial_base, defesa_especial_base, velocidade_base: inteiros quando esse conceito existir no contexto.
- fonte_url, data_verificacao.

A combinação forma + jogo é única. DADOS_FORMA_JOGO não depende de uma versão de regulamento.

### TIPO
- **id_tipo:** PK.
- nome_tipo: único.

### TIPO_FORMA_JOGO
Associação de DADOS_FORMA_JOGO e TIPO.
- id_dados_forma, id_tipo.
- posicao: 1 (primário) ou 2 (secundário).

Não repetir tipo nem posição; máximo de duas linhas por ficha.

### HABILIDADE
- **id_habilidade:** PK.
- nome: único.
- descricao.

### HABILIDADE_FORMA_JOGO
Associação de DADOS_FORMA_JOGO e HABILIDADE.
- **id_habilidade_forma:** PK.
- id_dados_forma, id_habilidade.
- slot: normal, oculta ou outra posição documentada.
- condicao.

A combinação ficha + habilidade + slot é única.

### METODO_OBTENCAO
- **id_metodo:** PK.
- nome: captura, presente, evolução, troca, transferência, recrutamento etc.
- descricao.

### METODO_FORMA_JOGO
Associação entre DADOS_FORMA_JOGO e METODO_OBTENCAO.
- id_dados_forma, id_metodo.
- condicao.

Lista métodos possíveis; não determina o método usado por um exemplar.

### NATUREZA
- **id_natureza:** PK.
- nome.
- atributo_aumentado, atributo_reduzido.

Natureza é opcional quando não se aplica ou não é conhecida. A mecânica informa se o sistema está confirmado.

### POKEMON_COLECAO
Um exemplar individual, nunca um agrupamento por espécie.
- **id_pokemon_colecao:** PK.
- id_usuario: FK obrigatório.
- id_dados_forma_atual: FK obrigatório no MVP.
- id_jogo_origem: FK opcional.
- id_metodo_obtencao: FK opcional.
- id_natureza: FK opcional.
- id_habilidade_forma: FK opcional.
- apelido, nivel, data_registro, observacao.

O jogo atual é derivado de DADOS_FORMA_JOGO. Jogo de origem é independente. O MVP mantém um contexto atual e não guarda histórico completo de transferências. Habilidade deve ser compatível com o contexto atual.

### ATRIBUTO_BATALHA
- **id_atributo:** PK.
- codigo único: HP, ATK, DEF, SP_ATK, SP_DEF, SPEED.
- nome.

### TIPO_TREINAMENTO
- **id_tipo_treinamento:** PK.
- codigo único: IV, EV, CHAMPIONS_TRAINING ou outro sistema documentado.
- nome, descricao.

CHAMPIONS_TRAINING identifica um sistema separado; não implica que sua escala numérica esteja conhecida.

### MECANICA_TREINAMENTO
Associação entre MECANICA_JOGO e TIPO_TREINAMENTO.
- **id_mecanica_treinamento:** PK.
- id_mecanica, id_tipo_treinamento.
- aplicabilidade: aplicável, não aplicável ou não verificado.
- unidade.
- valor_minimo, valor_maximo_atributo, valor_maximo_total.
- fonte_url, data_verificacao.

Mecânica + tipo de treinamento é único. Limites desconhecidos ficam NULL e bloqueiam cálculo automático.

### VALOR_TREINAMENTO_POKEMON
Valor de treinamento aplicado a um exemplar.
- **id_valor_treinamento:** PK.
- id_pokemon_colecao.
- id_mecanica_treinamento.
- id_atributo.
- valor.

Exemplar + sistema/versão + atributo é único. Substitui as colunas fixas de IV/EV da versão 2.0.

### PERFIL_ANALISE
- **id_perfil:** PK.
- id_dados_forma: alvo forma/jogo.
- id_mecanica: versão de regras.
- id_usuario: proprietário; obrigatório para perfil personalizado, NULL para perfil mantido pelo sistema.
- id_regulamento: opcional; obrigatório apenas quando o perfil é explicitamente específico de um regulamento.
- nome_perfil, descricao.
- tipo_perfil: personalizado ou referência competitiva.
- fonte_url, data_verificacao para perfis de referência externos.

Forma e mecânica devem pertencer ao mesmo jogo. Perfil é referência de comparação; não é automaticamente regra oficial.

### VALOR_PERFIL_ANALISE
- **id_valor_perfil:** PK.
- id_perfil.
- id_mecanica_treinamento.
- id_atributo.
- valor_alvo.

Perfil + sistema/versão + atributo é único.

### PERFIL_NATUREZA
Associação N:N entre PERFIL_ANALISE e NATUREZA.

### PERFIL_HABILIDADE
Associação N:N entre PERFIL_ANALISE e HABILIDADE_FORMA_JOGO. A habilidade precisa ser válida para o alvo do perfil.

### REGULAMENTO
- **id_regulamento:** PK.
- id_mecanica.
- codigo, nome, formato, temporada.
- data_inicio, data_fim.
- fonte_url, data_verificacao.

### ELEGIBILIDADE_FORMA_REGULAMENTO
Associação entre REGULAMENTO e DADOS_FORMA_JOGO.
- **id_elegibilidade:** PK.
- id_regulamento, id_dados_forma.
- status: permitido, restrito, proibido, condicional ou não verificado.
- condicao, fonte_url, data_verificacao.

Regulamento + ficha da forma é único. A entidade verifica apenas elegibilidade da espécie/forma, não a legalidade completa do exemplar.

### TRANSFORMACAO_FORMA
- **id_transformacao:** PK.
- id_dados_forma_origem, id_dados_forma_destino.
- tipo_transformacao.
- condicao, item_requerido, observacao.

Origem e destino devem pertencer ao mesmo jogo. Transformação temporária não gera captura independente.

## 3. Relacionamentos

- ESPECIE 1:N FORMA.
- FORMA 1:N DADOS_FORMA_JOGO.
- JOGO 1:N DADOS_FORMA_JOGO.
- JOGO 1:N MECANICA_JOGO.
- DADOS_FORMA_JOGO N:N TIPO via TIPO_FORMA_JOGO.
- DADOS_FORMA_JOGO N:N HABILIDADE via HABILIDADE_FORMA_JOGO.
- DADOS_FORMA_JOGO N:N METODO_OBTENCAO via METODO_FORMA_JOGO.
- USUARIO 1:N POKEMON_COLECAO.
- DADOS_FORMA_JOGO 1:N POKEMON_COLECAO.
- JOGO 1:N POKEMON_COLECAO como origem (opcional no exemplar).
- METODO_OBTENCAO 1:N POKEMON_COLECAO como método real (opcional).
- NATUREZA 1:N POKEMON_COLECAO (opcional).
- HABILIDADE_FORMA_JOGO 1:N POKEMON_COLECAO (opcional).
- MECANICA_JOGO N:N TIPO_TREINAMENTO via MECANICA_TREINAMENTO.
- POKEMON_COLECAO 1:N VALOR_TREINAMENTO_POKEMON.
- MECANICA_TREINAMENTO 1:N VALOR_TREINAMENTO_POKEMON.
- ATRIBUTO_BATALHA 1:N VALOR_TREINAMENTO_POKEMON.
- DADOS_FORMA_JOGO 1:N PERFIL_ANALISE.
- MECANICA_JOGO 1:N PERFIL_ANALISE.
- USUARIO 1:N PERFIL_ANALISE (opcional no perfil).
- REGULAMENTO 1:N PERFIL_ANALISE (opcional no perfil).
- PERFIL_ANALISE 1:N VALOR_PERFIL_ANALISE.
- MECANICA_TREINAMENTO 1:N VALOR_PERFIL_ANALISE.
- ATRIBUTO_BATALHA 1:N VALOR_PERFIL_ANALISE.
- PERFIL_ANALISE N:N NATUREZA via PERFIL_NATUREZA.
- PERFIL_ANALISE N:N HABILIDADE_FORMA_JOGO via PERFIL_HABILIDADE.
- MECANICA_JOGO 1:N REGULAMENTO.
- REGULAMENTO N:N DADOS_FORMA_JOGO via ELEGIBILIDADE_FORMA_REGULAMENTO.
- DADOS_FORMA_JOGO 1:N TRANSFORMACAO_FORMA como origem e como destino.

## 4. Restrições

- Nome de usuário e e-mail únicos, sem diferença por maiúsculas/minúsculas.
- Código da forma único dentro da espécie; uma forma padrão por espécie.
- Forma + jogo únicos em DADOS_FORMA_JOGO.
- Tipos com posição 1 ou 2; sem duplicação; máximo de dois.
- Habilidade/slot e método únicos por ficha.
- Jogo + versão únicos em MECANICA_JOGO.
- Mecânica + tipo de treinamento únicos.
- Exemplar + sistema + atributo únicos.
- Perfil + sistema + atributo únicos.
- Perfil personalizado exige proprietário.
- Forma e mecânica do perfil pertencem ao mesmo jogo.
- Elegibilidade única por regulamento + forma/jogo.
- Transformação liga fichas do mesmo jogo.
- Toda operação da coleção verifica o proprietário no backend.
- Limites não confirmados não podem ser presumidos.

## 5. Limites do MVP

- Um contexto atual por exemplar, além do jogo de origem.
- Sem histórico completo de transferências.
- Sem movesets, itens, equipes ou cálculo de dano.
- Análise somente para sistemas de treinamento documentados.
- O catálogo pode conter dados não verificados sem inventá-los.

## 6. Migração em relação à versão 2.0

- DADOS_FORMA_JOGO passa a referenciar JOGO, não MECANICA_JOGO.
- Tipos migram para TIPO_FORMA_JOGO com posição.
- Métodos possíveis migram para METODO_FORMA_JOGO.
- Jogo de origem continua separado do contexto atual.
- Colunas fixas IV/EV são substituídas por VALOR_TREINAMENTO_POKEMON.
- Valores dos perfis passam para VALOR_PERFIL_ANALISE.
- “Legalidade” passa a significar elegibilidade da espécie/forma.

**Não iniciar o modelo lógico sem desenhar este DER no brModelo e revisar as cardinalidades.**
