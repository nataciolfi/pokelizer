# Modelo conceitual do banco de dados

**Projeto:** PokéAnalyzer  
**Versão:** 3.0  
**Status:** modelo conceitual corrigido; ainda precisa ser desenhado e conferido no brModelo.

## 1. Objetivo e princípio de modelagem

O banco sustenta quatro áreas:
1. catálogo global de espécies e formas;
2. dados da forma em cada jogo/contexto de mecânicas;
3. exemplares pertencentes a usuários e estados desses exemplares em cada jogo;
4. perfis de comparação e regulamentos competitivos.

A regra principal da v3 é: **um exemplar não é o mesmo que o estado dele em um jogo**. O Pokémon individual pertence à coleção do usuário. Nível, forma, habilidade, natureza e treinamento podem depender do jogo e são registrados no estado por jogo.

## 2. Conceitos que precisam permanecer separados

- **Espécie:** identidade da Pokédex Nacional.
- **Forma:** variante catalogada pertencente à espécie.
- **Jogo:** título/edição, como Pokémon Scarlet ou Pokémon Violet.
- **Mecânica de jogo:** conjunto de regras documentadas de atributos e treinamento.
- **Dados da forma no jogo:** como aquela forma é representada no contexto selecionado.
- **Exemplar:** Pokémon individual registrado pelo usuário.
- **Estado em jogo:** representação daquele exemplar dentro de um contexto de jogo.
- **Perfil:** objetivo de comparação.
- **Regulamento:** regras de uma competição e período.
- **Elegibilidade da forma:** registro de permissão/restrição de uma forma no regulamento. Não é uma certificação completa de legalidade individual.

## 3. Entidades

### USUARIO
- **id_usuario:** identificador.
- nome_usuario: nome público, único.
- email: e-mail de acesso, único sem distinção de maiúsculas/minúsculas.
- senha_hash: hash seguro da senha.
- data_cadastro: data/hora de criação.

### ESPECIE
- **id_especie:** identificador interno.
- numero_nacional: número da Pokédex Nacional, único.
- nome_pt e nome_en: nomes de apresentação.
- geracao_origem: geração de introdução.
- codigo_catalogo: identificador estável da fonte, quando disponível.
- fonte_url e fonte_versao: referência de origem.

### FORMA
- **id_forma:** identificador interno.
- id_especie: espécie à qual pertence.
- codigo_forma: código estável dentro da espécie.
- nome_forma: nome canônico da forma.
- categoria: padrão, regional, alternativa, gênero, sazonal, cosmética, batalha ou outra categoria documentada.
- descricao: explicação da diferença.
- forma_padrao: indica a forma padrão da espécie.
- fonte_url e fonte_versao: referência que sustenta a forma.

Uma forma não recebe um novo número nacional. Shiny não será uma nova espécie/forma por padrão: será uma característica visual do exemplar. Formas de batalha podem existir no catálogo sem serem registráveis independentemente.

### JOGO
- **id_jogo:** identificador.
- nome: título oficial.
- edicao: edição específica, quando aplicável.
- categoria: série principal, batalha, spin-off ou outra.
- geracao: geração associada, quando aplicável.
- plataforma: plataforma.
- data_lancamento: data, quando confirmada.

Cada edição deve ter seu próprio registro quando disponibilidade ou regras puderem variar. Scarlet e Violet não serão fundidos.

### MECANICA_JOGO
- **id_mecanica:** identificador.
- id_jogo: título ao qual pertence.
- nome_contexto: nome compreensível do contexto.
- versao_referencia: versão ou conjunto de regras documentado.
- status_iv: USA, NAO_USA ou NAO_VERIFICADO.
- status_ev: USA, NAO_USA ou NAO_VERIFICADO.
- status_natureza: USA, NAO_USA ou NAO_VERIFICADO.
- iv_minimo e iv_maximo: limites de IV, quando aplicáveis.
- ev_maximo_atributo e ev_maximo_total: limites de EV, quando aplicáveis.
- sistema_treinamento: identificador/descrição do sistema próprio.
- formula_atributos: versão ou referência da fórmula de cálculo.
- vigencia_inicio e vigencia_fim: período, quando aplicável.
- fonte_regras e data_verificacao: evidência das regras.

MECANICA_JOGO não é um regulamento competitivo. Os estados de IV/EV/natureza são trivalorados para não confundir “não usa” com “não verificado”.

### DADOS_FORMA_JOGO
Representa como uma forma existe em um contexto específico.
- **id_dados_forma:** identificador.
- id_forma: forma do catálogo.
- id_mecanica: contexto de mecânicas.
- status_presenca: PRESENTE, AUSENTE ou NAO_VERIFICADO.
- status_registrabilidade: INDEPENDENTE, APENAS_TRANSFORMACAO, NAO_REGISTRAVEL ou NAO_VERIFICADO.
- altura e peso: valores e unidades documentadas.
- hp_base, ataque_base, defesa_base, ataque_especial_base, defesa_especial_base e velocidade_base.
- fonte_dados, versao_dados e data_verificacao.

A combinação forma + mecânica deve ser única. Presença no jogo, obtenibilidade e registrabilidade são informações diferentes.

### TIPO
- **id_tipo:** identificador.
- nome_tipo: nome canônico.

### DADOS_FORMA_TIPO
Entidade associativa entre DADOS_FORMA_JOGO e TIPO.
- **id_dados_forma:** contexto de forma.
- **id_tipo:** tipo.
- slot: PRIMARIO ou SECUNDARIO.

A combinação contexto + slot é única e um contexto possui no máximo dois tipos.

### HABILIDADE
- **id_habilidade:** identificador.
- nome: nome canônico.
- codigo_catalogo: código estável, quando disponível.

Descrição e condições podem variar por jogo; não devem ser tratadas como texto universal imutável.

### HABILIDADE_FORMA_JOGO
Associa uma habilidade disponível a um contexto de forma.
- **id_habilidade_forma:** identificador.
- id_dados_forma: contexto exato.
- id_habilidade: habilidade.
- slot: normal, oculta, especial ou outro slot documentado.
- condicao: condição de disponibilidade.
- fonte_url e data_verificacao.

A combinação contexto + habilidade deve ser única. A habilidade escolhida em um estado do exemplar deve pertencer ao mesmo contexto.

### NATUREZA
- **id_natureza:** identificador.
- nome: nome canônico.
- atributo_aumentado: atributo ou NENHUM.
- atributo_reduzido: atributo ou NENHUM.

Naturezas neutras não devem ser representadas com atributos inventados. Uma natureza só pode ser usada quando a mecânica a confirmar como aplicável.

### METODO_OBTENCAO
- **id_metodo:** identificador.
- codigo: identificador estável.
- nome: captura, ovo, presente, recrutamento, transferência, troca, evolução ou outro método documentado.

### OBTENCAO_FORMA_JOGO
Associação que registra os métodos possíveis para uma forma em um contexto.
- **id_obtencao:** identificador.
- id_dados_forma: forma/contexto.
- id_metodo: método.
- condicao: condição necessária.
- fonte_url e data_verificacao.

Uma forma pode ter vários métodos em um mesmo jogo. Método não é um único atributo em DADOS_FORMA_JOGO.

### POKEMON_COLECAO
Representa o exemplar individual de um usuário, independentemente do contexto em que será analisado.
- **id_pokemon_colecao:** identificador.
- id_usuario: proprietário.
- id_especie: espécie do exemplar.
- apelido: apelido opcional.
- id_jogo_origem: jogo em que foi obtido originalmente, opcional se desconhecido.
- id_metodo_origem: método real de obtenção, opcional se desconhecido.
- data_obtencao: data aproximada/opcional.
- data_registro: data/hora em que entrou na coleção.
- observacao: anotação opcional.

Dois exemplares da mesma espécie podem existir na mesma coleção. Origem e método descrevem a história do exemplar, não o jogo atual.

### POKEMON_ESTADO_JOGO
Representa o estado de um exemplar em um contexto de jogo.
- **id_estado_jogo:** identificador.
- id_pokemon_colecao: exemplar.
- id_dados_forma: forma e mecânica em que o exemplar está registrado.
- id_natureza: natureza, quando aplicável e conhecida.
- id_habilidade_forma: habilidade escolhida, quando aplicável e conhecida.
- nivel: nível naquele jogo, quando aplicável.
- observacao: informação contextual.
- data_atualizacao: última alteração do estado.

Um exemplar pode ter estados separados em vários jogos. A mesma criatura pode, por exemplo, ter um estado no jogo de origem e outro estado em Champions. Os dados de treinamento ficam ligados ao estado, nunca ao exemplar global.

### ATRIBUTO_TREINAMENTO
Define quais valores de treinamento existem em um contexto de mecânicas.
- **id_atributo_treinamento:** identificador.
- id_mecanica: contexto de mecânicas.
- codigo: código estável do atributo.
- categoria: IV, EV, TREINAMENTO_PROPRIO ou outra categoria documentada.
- atributo: HP, ataque, defesa, ataque especial, defesa especial, velocidade ou outro atributo documentado.
- nome_exibicao: rótulo para a interface.
- unidade: unidade/escala.
- valor_minimo e valor_maximo: limites individuais, quando conhecidos.
- grupo_validacao e limite_grupo: grupo e limite agregado, quando aplicável.
- fonte_url e data_verificacao.

Não criar atributos de treinamento antes de conhecer sua definição, escala e limites. Isso permite modelar sistemas distintos sem converter automaticamente um no outro.

### VALOR_TREINAMENTO_POKEMON
Registra o valor de treinamento de um estado do exemplar.
- **id_estado_jogo:** estado do exemplar.
- **id_atributo_treinamento:** atributo definido na mecânica.
- valor: valor numérico.
- observacao: opcional.

A combinação estado + atributo é única. O atributo deve pertencer à mesma mecânica do estado.

### PERFIL_ANALISE
Representa o objetivo de comparação.
- **id_perfil:** identificador.
- id_dados_forma: forma/contexto ao qual o perfil se aplica.
- id_usuario: proprietário, nulo somente para perfil mantido pelo sistema.
- id_regulamento: regulamento relacionado, opcional.
- nome_perfil: nome.
- descricao: objetivo.
- tipo_perfil: PERSONALIZADO, REFERENCIA_ESTRATEGICA ou REFERENCIA_COMPETITIVA.
- fonte_perfil e versao_perfil: origem/versionamento, obrigatórios para perfis de referência.
- data_criacao: data de criação.

Perfil é objetivo de comparação, não regulamento nem promessa de build oficial.

### VALOR_TREINAMENTO_PERFIL
Define o intervalo ou valor esperado de um atributo no perfil.
- **id_perfil:** perfil.
- **id_atributo_treinamento:** atributo da mesma mecânica.
- valor_minimo_desejado: limite inferior, quando usado.
- valor_maximo_desejado: limite superior, quando usado.
- peso_prioridade: importância relativa, se houver método de pontuação documentado.

Faixa exata pode ser representada com mínimo igual ao máximo. A aplicação deve validar se pelo menos uma referência foi definida e se os limites fazem sentido.

### PERFIL_NATUREZA
Associa naturezas a um perfil.
- **id_perfil:** perfil.
- **id_natureza:** natureza.
- preferencia: PREFERIDA, ACEITAVEL ou EVITAR.
- prioridade: ordem ou importância, quando usada.

### PERFIL_HABILIDADE
Associa opções de habilidade a um perfil.
- **id_perfil:** perfil.
- **id_habilidade_forma:** opção de habilidade do contexto.
- preferencia: PREFERIDA, ACEITAVEL ou EVITAR.
- prioridade: ordem ou importância, quando usada.

### REGULAMENTO
Representa regras de uma competição.
- **id_regulamento:** identificador.
- id_mecanica: jogo/contexto ao qual pertence.
- codigo: código oficial, quando existir.
- nome: nome.
- formato: individual, duplas ou outro formato.
- temporada: temporada/série.
- data_inicio e data_fim: vigência.
- fonte_oficial: URL.
- data_verificacao: última conferência.

### ELEGIBILIDADE_REGULAMENTO
Registra a elegibilidade catalogada de uma forma em um regulamento.
- **id_elegibilidade:** identificador.
- id_regulamento: regulamento.
- id_dados_forma: forma/contexto avaliado.
- status: PERMITIDO, RESTRITO, PROIBIDO, CONDICIONAL ou NAO_VERIFICADO.
- condicao: condição ou restrição.
- fonte_verificacao: referência.
- data_verificacao: data.

A combinação regulamento + dados da forma é única. Esta entidade não certifica a legalidade completa de um exemplar individual.

### TRANSFORMACAO_FORMA
Registra transformação entre duas formas em um contexto.
- **id_transformacao:** identificador.
- id_dados_forma_origem: forma/contexto de origem.
- id_dados_forma_destino: forma/contexto de destino.
- tipo_transformacao: Mega Evolução ou outra transformação.
- condicao: condição necessária.
- item_requerido: item, quando aplicável.
- observacao: detalhes.
- fonte_url e data_verificacao.

Origem e destino devem pertencer ao mesmo contexto de mecânica, salvo exceção documentada. Transformação não cria automaticamente uma nova captura.

## 4. Relacionamentos e cardinalidades

- USUARIO 1:N POKEMON_COLECAO.
- ESPECIE 1:N FORMA.
- FORMA 1:N DADOS_FORMA_JOGO.
- JOGO 1:N MECANICA_JOGO.
- MECANICA_JOGO 1:N DADOS_FORMA_JOGO.
- DADOS_FORMA_JOGO N:N TIPO, resolvido por DADOS_FORMA_TIPO.
- DADOS_FORMA_JOGO 1:N HABILIDADE_FORMA_JOGO.
- HABILIDADE 1:N HABILIDADE_FORMA_JOGO.
- DADOS_FORMA_JOGO N:N METODO_OBTENCAO, resolvido por OBTENCAO_FORMA_JOGO.
- POKEMON_COLECAO 0:N POKEMON_ESTADO_JOGO.
- DADOS_FORMA_JOGO 1:N POKEMON_ESTADO_JOGO.
- NATUREZA 0:N POKEMON_ESTADO_JOGO.
- HABILIDADE_FORMA_JOGO 0:N POKEMON_ESTADO_JOGO.
- MECANICA_JOGO 1:N ATRIBUTO_TREINAMENTO.
- POKEMON_ESTADO_JOGO 1:N VALOR_TREINAMENTO_POKEMON.
- ATRIBUTO_TREINAMENTO 1:N VALOR_TREINAMENTO_POKEMON.
- DADOS_FORMA_JOGO 1:N PERFIL_ANALISE.
- USUARIO 0:N PERFIL_ANALISE.
- REGULAMENTO 0:N PERFIL_ANALISE.
- PERFIL_ANALISE 1:N VALOR_TREINAMENTO_PERFIL.
- ATRIBUTO_TREINAMENTO 1:N VALOR_TREINAMENTO_PERFIL.
- PERFIL_ANALISE N:N NATUREZA, resolvido por PERFIL_NATUREZA.
- PERFIL_ANALISE N:N HABILIDADE_FORMA_JOGO, resolvido por PERFIL_HABILIDADE.
- MECANICA_JOGO 1:N REGULAMENTO.
- REGULAMENTO 1:N ELEGIBILIDADE_REGULAMENTO.
- DADOS_FORMA_JOGO 1:N ELEGIBILIDADE_REGULAMENTO.
- DADOS_FORMA_JOGO 1:N TRANSFORMACAO_FORMA como origem e 1:N como destino.

## 5. Regras que exigem validação adicional

Algumas regras não são resolvidas por uma FK simples:
- total de EV ou outro grupo de treinamento;
- no máximo dois tipos por contexto;
- habilidade selecionada pertencente ao mesmo contexto do estado;
- atributo de treinamento pertencente à mecânica do estado;
- regulamento e forma pertencentes ao mesmo contexto de jogo;
- origem e destino de transformação pertencentes ao mesmo contexto;
- perfil e exemplar com mesma forma/mecânica;
- estado só criado quando a forma puder ser registrada independentemente.

No modelo lógico, usar FKs compostas quando aplicável. No backend, validar regras agregadas em serviços e transações. Criar testes para todos os casos.

## 6. Decisões de escopo

- A primeira análise numérica será implementada para Scarlet/Violet.
- Champions será modelado em contexto próprio e só terá cálculo quando os atributos de treinamento específicos estiverem documentados.
- Legends: Z-A terá dados e mecânicas independentes.
- Winds/Waves não receberá regras antes de documentação oficial.
- Movimentos, itens e validação integral de legalidade individual estão fora da primeira versão.
- O histórico completo de relatórios está fora da primeira versão.
