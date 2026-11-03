# Modelo conceitual do banco de dados

**Projeto:** PokéAnalyzer  
**Versão:** 2.0  
**Etapa:** revisão do modelo conceitual

## 1. Objetivo

O banco sustenta três partes do sistema:

1. **Pokédex global:** espécies e todas as formas oficiais catalogadas.
2. **Dados por jogo:** estatísticas, tipos, habilidades, disponibilidade e mecânicas específicas de cada jogo.
3. **Coleção e análise:** Pokémon registrados por usuários, perfis de comparação e regulamentos competitivos.

A separação evita assumir que uma forma existe em todos os jogos, que seus atributos são sempre iguais ou que toda espécie é permitida em qualquer competição.

## 2. Contexto adotado

A referência principal para IV, EV e natureza será Pokémon Scarlet e Pokémon Violet, da Geração IX. Pokémon Champions será registrado como jogo de batalha separado, com recrutamento e treinamento próprios. Pokémon Legends: Z-A também terá seu próprio contexto de mecânicas.

Winds e Waves estão previstos para 2027 e não terão regras cadastradas até que sejam lançados e documentados oficialmente.

**Regra central:** nunca converter os valores de treinamento de um jogo para IV/EV de outro sem equivalência oficial documentada.

## 3. Entidades

### USUARIO
- **id_usuario:** identificador.
- nome_usuario: nome público.
- email: e-mail de acesso, único.
- senha_hash: hash seguro da senha.
- data_cadastro: data de criação.

### ESPECIE
- **numero_nacional:** número nacional da espécie.
- nome_pt: nome em português.
- nome_en: nome em inglês.
- geracao_origem: geração em que foi introduzida.

Uma espécie é distinta de suas formas. Formas regionais ou de batalha não recebem novo número nacional.

### FORMA
- **id_forma:** identificador.
- nome_forma: nome ou identificação da forma.
- categoria: padrão, regional, gênero, sazonal, cosmética, batalha ou outra categoria documentada.
- descricao: explicação da diferença.
- forma_padrao: indica a forma padrão.
- referencia_visual: referência visual, quando disponível.

Todas as formas oficiais entram no catálogo global. Estatísticas, tipos, habilidades e disponibilidade ficam em DADOS_FORMA_JOGO, pois podem variar entre jogos.

### JOGO
- **id_jogo:** identificador.
- nome: título oficial.
- categoria: série principal, jogo de batalha ou spin-off.
- geracao: geração associada, quando aplicável.
- plataforma: plataforma oficial.
- data_lancamento: data de lançamento, quando disponível.

### MECANICA_JOGO
- **id_mecanica:** identificador.
- versao: nome ou versão das regras.
- usa_iv: indica se o contexto utiliza IV; pode ficar não definido enquanto não houver confirmação.
- usa_ev: indica se o contexto utiliza EV; pode ficar não definido enquanto não houver confirmação.
- usa_natureza: indica se o contexto utiliza natureza; pode ficar não definido enquanto não houver confirmação.
- iv_minimo e iv_maximo: limites aplicáveis, quando existentes.
- ev_maximo_atributo: limite individual, quando existente.
- ev_maximo_total: limite total, quando existente.
- sistema_treinamento: descrição do sistema de treinamento do jogo.
- fonte_regras: URL ou referência oficial.
- data_inicio e data_fim: período de validade, quando aplicável.

Cada versão de mecânicas pertence a um jogo. Um jogo pode ter mais de uma versão documentada ao longo do tempo.

### DADOS_FORMA_JOGO
Representa como uma forma aparece em um contexto específico de mecânicas.
- **id_dados_forma:** identificador.
- status_disponibilidade: disponível, transferível, indisponível ou não verificado.
- metodo_obtencao: captura, evolução, transferência, recrutamento, transformação ou outro método documentado.
- pode_ser_registrada: indica se pode ser registrada como exemplar independente.
- altura e peso: valores do contexto do jogo.
- hp_base, ataque_base, defesa_base, ataque_especial_base, defesa_especial_base e velocidade_base: atributos-base.
- fonte_dados: referência da origem dos dados.

Esta entidade liga FORMA a MECANICA_JOGO. Se os dados não estiverem verificados, o sistema não inventará estatísticas nem concluirá automaticamente que a forma é proibida.

### TIPO
- **id_tipo:** identificador.
- nome_tipo: nome do tipo.

### HABILIDADE
- **id_habilidade:** identificador.
- nome: nome oficial.
- descricao: descrição resumida.

### HABILIDADE_FORMA_JOGO
Entidade associativa entre DADOS_FORMA_JOGO e HABILIDADE.
- **id_habilidade_forma:** identificador.
- slot: habilidade normal, oculta ou outra posição documentada.
- condicao: condição de obtenção ou uso, quando aplicável.

Isso impede que o usuário selecione uma habilidade que não esteja disponível naquela forma e naquele jogo.

### NATUREZA
- **id_natureza:** identificador.
- nome: nome da natureza.
- atributo_aumentado: atributo favorecido, quando aplicável.
- atributo_reduzido: atributo prejudicado, quando aplicável.

Naturezas neutras não aumentam nem reduzem atributos. Os efeitos devem respeitar MECANICA_JOGO.

### POKEMON_COLECAO
Representa um exemplar registrado por um usuário. O nome é mais abrangente que POKEMON_CAPTURADO porque alguns jogos usam transferência ou recrutamento.
- **id_pokemon_colecao:** identificador.
- apelido: apelido opcional.
- nivel: nível, quando aplicável.
- metodo_obtencao: capturado, transferido, recrutado ou outro método documentado.
- jogo_origem: jogo em que foi obtido originalmente, quando conhecido.
- data_registro: data do registro.
- iv_hp, iv_ataque, iv_defesa, iv_atq_especial, iv_def_especial e iv_velocidade: valores individuais, quando o jogo utilizar IV.
- ev_hp, ev_ataque, ev_defesa, ev_atq_especial, ev_def_especial e ev_velocidade: valores de esforço, quando o jogo utilizar EV.

Cada registro pertence a um usuário e a um DADOS_FORMA_JOGO, que identifica o contexto atual de jogo. O jogo de origem é opcional, pois um Pokémon pode ter sido transferido. Natureza e habilidade selecionada são opcionais quando não se aplicarem ao contexto.

**Nulo não é zero:** nulo significa não aplicável ou não informado; zero é um valor real.

### PERFIL_ANALISE
Representa uma configuração usada como objetivo de comparação.
- **id_perfil:** identificador.
- nome_perfil: nome.
- descricao: finalidade.
- tipo_perfil: competitivo ou personalizado.
- iv_hp_ideal, iv_ataque_ideal, iv_defesa_ideal, iv_atq_especial_ideal, iv_def_especial_ideal e iv_velocidade_ideal: referências opcionais.
- ev_hp, ev_ataque, ev_defesa, ev_atq_especial, ev_def_especial e ev_velocidade: distribuição de referência opcional.

Cada perfil aponta para um DADOS_FORMA_JOGO específico. Perfil personalizado pertence a um usuário. Perfil competitivo mantido pelo sistema não tem proprietário e deve indicar o regulamento quando for específico de uma competição. Naturezas e habilidades recomendadas são relacionamentos opcionais.

### REGULAMENTO
- **id_regulamento:** identificador.
- codigo: código oficial.
- nome: nome.
- formato: individual, duplas ou outro formato documentado.
- temporada: temporada ou série.
- data_inicio e data_fim: período de vigência.
- fonte_oficial: URL ou referência oficial.
- data_consulta: data da última verificação.

Cada regulamento pertence a uma MECANICA_JOGO específica.

### ELEGIBILIDADE_REGULAMENTO
Entidade associativa entre REGULAMENTO e DADOS_FORMA_JOGO.
- **id_elegibilidade:** identificador.
- status: permitido, restrito, proibido, condicional ou não verificado.
- condicao: restrição ou condição aplicável.
- fonte_verificacao: referência que sustenta a classificação.
- data_verificacao: data da verificação.

A elegibilidade é específica para um regulamento. A presença na Pokédex não implica permissão competitiva.

### TRANSFORMACAO_FORMA
Representa uma transformação de uma forma de origem em uma forma de destino.
- **id_transformacao:** identificador.
- tipo_transformacao: Mega Evolução ou outro estado especial.
- condicao: condição necessária.
- item_requerido: item necessário, quando aplicável.
- observacao: detalhes adicionais.

A transformação liga dois registros de DADOS_FORMA_JOGO. Isso permite catalogar formas de batalha sem tratá-las automaticamente como capturas independentes.

## 4. Relacionamentos principais

- ESPECIE 1:N FORMA.
- FORMA 1:N DADOS_FORMA_JOGO.
- JOGO 1:N MECANICA_JOGO.
- MECANICA_JOGO 1:N DADOS_FORMA_JOGO.
- DADOS_FORMA_JOGO N:N TIPO.
- DADOS_FORMA_JOGO 1:N HABILIDADE_FORMA_JOGO.
- HABILIDADE 1:N HABILIDADE_FORMA_JOGO.
- USUARIO 1:N POKEMON_COLECAO.
- JOGO 1:N POKEMON_COLECAO, opcional no registro, como jogo de origem.
- DADOS_FORMA_JOGO 1:N POKEMON_COLECAO.
- NATUREZA 1:N POKEMON_COLECAO, opcional no registro.
- HABILIDADE_FORMA_JOGO 1:N POKEMON_COLECAO, opcional no registro.
- DADOS_FORMA_JOGO 1:N PERFIL_ANALISE.
- USUARIO 1:N PERFIL_ANALISE, opcional no perfil.
- MECANICA_JOGO 1:N REGULAMENTO.
- REGULAMENTO 1:N ELEGIBILIDADE_REGULAMENTO.
- DADOS_FORMA_JOGO 1:N ELEGIBILIDADE_REGULAMENTO.
- PERFIL_ANALISE N:N NATUREZA, opcional.
- PERFIL_ANALISE N:N HABILIDADE_FORMA_JOGO, opcional.
- REGULAMENTO 1:N PERFIL_ANALISE, opcional no perfil.
- DADOS_FORMA_JOGO 1:N TRANSFORMACAO_FORMA como origem e 1:N como destino.

## 5. Regras de negócio

1. Uma espécie possui uma ou mais formas; cada forma pertence a uma espécie.
2. Uma forma pode ter dados em vários jogos.
3. A disponibilidade é específica do jogo.
4. Uma forma possui um ou dois tipos no contexto aplicável.
5. As habilidades disponíveis dependem da forma e do jogo.
6. Cada Pokémon da coleção pertence a um usuário.
7. Cada registro de coleção representa uma forma em um contexto de jogo.
8. Um perfil de análise deve apontar para a forma e as mecânicas que avalia.
9. Perfil personalizado deve ter proprietário.
10. Perfil competitivo específico deve apontar para o regulamento correspondente.
11. A mesma forma pode ser permitida em um regulamento e proibida em outro.
12. Elegibilidade deve ter fonte e data de verificação.
13. Transformação temporária não é automaticamente uma captura independente.
14. IV/EV só são exigidos se as mecânicas selecionadas os utilizarem.
15. Habilidade selecionada deve ser compatível com a forma e o jogo.
16. Dados desconhecidos permanecem desconhecidos; nunca preencher com valores presumidos.

## 6. Decisões de simplificação controlada

- Os seis IVs e seis EVs permanecem como atributos separados para facilitar a explicação escolar.
- Tipos, habilidades e disponibilidade ficam ligados a DADOS_FORMA_JOGO, não à FORMA global.
- Relações N:N serão convertidas em tabelas associativas no modelo lógico.
- A análise será calculada quando solicitada; o histórico de relatórios fica fora da primeira versão.
- O treinamento próprio de Champions não será convertido em IV/EV sem equivalência oficial confirmada.
