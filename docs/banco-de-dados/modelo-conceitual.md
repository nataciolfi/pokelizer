# Modelo conceitual do banco de dados

**Projeto:** PokéAnalyzer  
**Versão:** 3.0  
**Status:** modelo conceitual corrigido; ainda precisa ser desenhado e conferido no brModelo.

## 1. Princípio do modelo

O banco separa quatro áreas: catálogo global, dados por jogo, exemplares do usuário e estados desses exemplares em cada jogo.

**Um exemplar não é uma espécie fixa nem um registro preso a um único jogo.** O exemplar é a identidade individual pertencente ao usuário. A forma e a espécie atuais são obtidas a partir do estado do exemplar em um jogo. Isso permite que um Bulbasaur da coleção evolua para Ivysaur sem criar um indivíduo novo nem deixar a coleção presa à espécie inicial.

## 2. Conceitos

- **Espécie:** identidade da Pokédex Nacional.
- **Forma:** variante catalogada pertencente a uma espécie.
- **Jogo:** título/edição, como Pokémon Scarlet ou Pokémon Violet.
- **Mecânica de jogo:** conjunto documentado de regras de atributos e treinamento.
- **Dados da forma no jogo:** representação de uma forma naquele contexto.
- **Exemplar:** Pokémon individual registrado pelo usuário.
- **Estado em jogo:** forma atual, nível, habilidade, natureza e treinamento do exemplar em um contexto específico.
- **Evolução:** mudança permanente de uma forma/espécie para outra conforme regra de um jogo.
- **Transformação:** mudança de estado de batalha, normalmente temporária; não é evolução.
- **Perfil:** objetivo de comparação.
- **Regulamento:** regras de uma competição e período.
- **Elegibilidade da forma:** informação sobre a presença permitida/restrita da forma no regulamento; não certifica a legalidade completa do indivíduo.

## 3. Entidades

### USUARIO
- **id_usuario:** identificador.
- nome_usuario: nome público, único.
- email: e-mail de acesso, único sem distinção de maiúsculas/minúsculas.
- senha_hash: hash seguro da senha.
- data_cadastro: data/hora de criação.

### ESPECIE
- **id_especie:** identificador interno.
- numero_nacional: número nacional, único.
- nome_pt e nome_en: nomes de apresentação.
- geracao_origem: geração de introdução.
- codigo_catalogo: identificador estável da fonte, quando disponível.
- fonte_url e fonte_versao: origem dos dados.

### FORMA
- **id_forma:** identificador interno.
- id_especie: espécie à qual pertence.
- codigo_forma: código estável dentro da espécie.
- nome_forma: nome canônico.
- categoria: padrão, regional, alternativa, gênero, sazonal, cosmética, batalha ou outra categoria documentada.
- descricao: explicação da diferença.
- forma_padrao: indica a forma padrão.
- fonte_url e fonte_versao: referência que sustenta a forma.

Uma forma não recebe um novo número nacional. Shiny é uma característica visual do exemplar, não uma espécie ou forma nova por padrão. Formas temporárias de batalha podem existir no catálogo sem serem registráveis independentemente.

### JOGO
- **id_jogo:** identificador.
- nome: título oficial.
- edicao: edição específica.
- categoria: série principal, jogo de batalha, spin-off ou outra.
- geracao: geração associada, quando aplicável.
- plataforma: plataforma.
- data_lancamento: data confirmada.

Cada edição deve ter registro próprio quando disponibilidade ou regras puderem variar. Scarlet e Violet não serão fundidos.

### MECANICA_JOGO
- **id_mecanica:** identificador.
- id_jogo: título ao qual pertence.
- nome_contexto: nome do contexto.
- versao_referencia: versão ou conjunto de regras documentado.
- status_iv: USA, NAO_USA ou NAO_VERIFICADO.
- status_ev: USA, NAO_USA ou NAO_VERIFICADO.
- status_natureza: USA, NAO_USA ou NAO_VERIFICADO.
- iv_minimo e iv_maximo: limites de IV, quando aplicáveis.
- ev_maximo_atributo e ev_maximo_total: limites de EV, quando aplicáveis.
- sistema_treinamento: sistema próprio identificado.
- formula_atributos: versão/referência da fórmula de cálculo.
- vigencia_inicio e vigencia_fim: período, quando aplicável.
- fonte_regras e data_verificacao: evidência das regras.

MECANICA_JOGO não é regulamento competitivo. Estados trivalorados distinguem “não usa” de “não verificado”.

### DADOS_FORMA_JOGO
Representa uma forma em um contexto de mecânicas.
- **id_dados_forma:** identificador.
- id_forma: forma do catálogo.
- id_mecanica: contexto de mecânicas.
- status_presenca: PRESENTE, AUSENTE ou NAO_VERIFICADO.
- status_registrabilidade: INDEPENDENTE, APENAS_TRANSFORMACAO, NAO_REGISTRAVEL ou NAO_VERIFICADO.
- altura e peso: valores/unidades documentadas.
- hp_base, ataque_base, defesa_base, ataque_especial_base, defesa_especial_base e velocidade_base.
- fonte_dados, versao_dados e data_verificacao.

A combinação forma + mecânica é única. Presença, obtenibilidade e registrabilidade são conceitos distintos.

### TIPO
- **id_tipo:** identificador.
- nome_tipo: nome canônico.

### DADOS_FORMA_TIPO
Associação entre DADOS_FORMA_JOGO e TIPO.
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
Associa habilidade disponível a um contexto de forma.
- **id_habilidade_forma:** identificador.
- id_dados_forma: contexto exato.
- id_habilidade: habilidade.
- slot: normal, oculta, especial ou outro slot documentado.
- condicao: condição de disponibilidade.
- fonte_url e data_verificacao.

A combinação contexto + habilidade é única. A habilidade escolhida em um estado deve pertencer ao mesmo contexto.

### NATUREZA
- **id_natureza:** identificador.
- nome: nome canônico.
- atributo_aumentado: atributo ou NENHUM.
- atributo_reduzido: atributo ou NENHUM.

Naturezas neutras usam NENHUM. Uma natureza só pode ser selecionada quando a mecânica a utilizar.

### METODO_OBTENCAO
- **id_metodo:** identificador.
- codigo: identificador estável.
- nome: captura, ovo, presente, recrutamento, transferência, troca, evolução ou outro método documentado.

### OBTENCAO_FORMA_JOGO
Associa métodos possíveis a uma forma/contexto.
- **id_obtencao:** identificador.
- id_dados_forma: forma/contexto.
- id_metodo: método.
- condicao: condição necessária.
- fonte_url e data_verificacao.

Uma forma pode ter vários métodos no mesmo jogo. Método não é um único texto em DADOS_FORMA_JOGO.

### POKEMON_COLECAO
Representa a identidade individual do exemplar pertencente ao usuário.
- **id_pokemon_colecao:** identificador.
- id_usuario: proprietário.
- id_forma_origem: forma no momento da obtenção, opcional quando desconhecida.
- id_jogo_origem: jogo de obtenção original, opcional quando desconhecido.
- id_metodo_origem: método real de obtenção, opcional quando desconhecido.
- apelido: apelido opcional.
- data_obtencao: data aproximada/opcional.
- data_registro: data/hora de inclusão.
- observacao: anotação opcional.

**Não armazenar uma espécie atual fixa nesta entidade.** A espécie/forma atual vem de POKEMON_ESTADO_JOGO. A forma de origem é apenas procedência e não muda quando o exemplar evolui.

### POKEMON_ESTADO_JOGO
Representa o estado atual de um exemplar em um contexto específico.
- **id_estado_jogo:** identificador.
- id_pokemon_colecao: exemplar.
- id_mecanica: contexto de mecânicas.
- id_dados_forma: forma atual naquele contexto.
- id_natureza: natureza, quando aplicável e conhecida.
- id_habilidade_forma: habilidade selecionada, quando aplicável e conhecida.
- nivel: nível naquele jogo, quando aplicável.
- observacao: informação contextual.
- data_atualizacao: última alteração.

Um exemplar pode possuir estados em vários jogos. Deve existir no máximo um estado atual por combinação exemplar + mecânica. Quando evolui dentro daquele jogo, o registro do estado é atualizado para a forma de destino; não se cria um novo exemplar. Histórico de estados fica fora da primeira versão.

### ATRIBUTO_TREINAMENTO
Define valores de treinamento existentes em uma mecânica.
- **id_atributo_treinamento:** identificador.
- id_mecanica: contexto.
- codigo: código estável.
- categoria: IV, EV, TREINAMENTO_PROPRIO ou outra categoria documentada.
- atributo: HP, ataque, defesa, ataque especial, defesa especial, velocidade ou outro atributo.
- nome_exibicao: rótulo da interface.
- unidade: unidade/escala.
- valor_minimo e valor_maximo: limites individuais.
- grupo_validacao e limite_grupo: agrupamento/limite agregado, quando aplicável.
- fonte_url e data_verificacao.

Não criar atributos antes de conhecer sua definição, escala e limites. Isso permite contextos de treinamento distintos sem conversão implícita.

### VALOR_TREINAMENTO_POKEMON
Registra o valor de treinamento de um estado.
- **id_estado_jogo:** estado.
- **id_atributo_treinamento:** atributo da mecânica.
- valor: valor numérico.
- observacao: opcional.

A combinação estado + atributo é única e o atributo precisa pertencer à mesma mecânica do estado.

### PERFIL_ANALISE
Representa o objetivo de comparação.
- **id_perfil:** identificador.
- id_dados_forma: forma/contexto alvo.
- id_usuario: proprietário, nulo apenas para perfil mantido pelo sistema.
- id_regulamento: regulamento relacionado, opcional.
- nome_perfil: nome.
- descricao: objetivo.
- tipo_perfil: PERSONALIZADO, REFERENCIA_ESTRATEGICA ou REFERENCIA_COMPETITIVA.
- fonte_perfil e versao_perfil: origem/versionamento para perfis de referência.
- data_criacao: data de criação.

Perfil é objetivo de comparação, não regulamento nem promessa de build oficial.

### VALOR_TREINAMENTO_PERFIL
Define faixa desejada por atributo.
- **id_perfil:** perfil.
- **id_atributo_treinamento:** atributo da mesma mecânica.
- valor_minimo_desejado: limite inferior opcional.
- valor_maximo_desejado: limite superior opcional.
- peso_prioridade: importância relativa, se houver fórmula documentada.

Faixa exata pode ser representada com mínimo igual ao máximo.

### PERFIL_NATUREZA
Associa naturezas a perfil.
- **id_perfil:** perfil.
- **id_natureza:** natureza.
- preferencia: PREFERIDA, ACEITAVEL ou EVITAR.
- prioridade: importância/ordem, quando usada.

### PERFIL_HABILIDADE
Associa opções de habilidade a perfil.
- **id_perfil:** perfil.
- **id_habilidade_forma:** opção de habilidade do contexto.
- preferencia: PREFERIDA, ACEITAVEL ou EVITAR.
- prioridade: importância/ordem, quando usada.

### REGULAMENTO
Representa regras de uma competição.
- **id_regulamento:** identificador.
- id_mecanica: contexto ao qual pertence.
- codigo: código oficial, quando existir.
- nome: nome.
- formato: individual, duplas ou outro.
- temporada: temporada/série.
- data_inicio e data_fim: vigência.
- fonte_oficial: URL.
- data_verificacao: última conferência.

### ELEGIBILIDADE_REGULAMENTO
Registra a elegibilidade de uma forma em regulamento.
- **id_elegibilidade:** identificador.
- id_regulamento: regulamento.
- id_dados_forma: forma/contexto avaliado.
- status: PERMITIDO, RESTRITO, PROIBIDO, CONDICIONAL ou NAO_VERIFICADO.
- condicao: condição/restrição.
- fonte_verificacao: referência.
- data_verificacao: data.

A combinação regulamento + contexto de forma é única. Não certifica legalidade integral de exemplar individual.

### EVOLUCAO_FORMA_JOGO
Registra uma evolução permanente permitida em um contexto de jogo.
- **id_evolucao:** identificador.
- id_dados_forma_origem: forma/contexto antes da evolução.
- id_dados_forma_destino: forma/contexto depois da evolução.
- metodo_evolucao: nível, troca, item ou outro método.
- condicao: requisitos completos e legíveis.
- item_requerido: item, quando aplicável.
- fonte_url e data_verificacao.

Origem e destino pertencem ao mesmo contexto de mecânicas. Uma espécie pode ter várias evoluções possíveis; as condições distinguem os caminhos.

### TRANSFORMACAO_FORMA
Registra uma transformação de estado, como forma de batalha temporária.
- **id_transformacao:** identificador.
- id_dados_forma_origem: forma/contexto original.
- id_dados_forma_destino: forma/contexto transformada.
- tipo_transformacao: Mega Evolução ou outra transformação.
- condicao: condição necessária.
- item_requerido: item, quando aplicável.
- observacao: detalhes.
- fonte_url e data_verificacao.

Transformação e evolução são relações distintas. Transformação não cria automaticamente novo exemplar.

## 4. Relacionamentos e cardinalidades

- USUARIO 1:N POKEMON_COLECAO.
- FORMA 0:N POKEMON_COLECAO como forma de origem.
- JOGO 0:N POKEMON_COLECAO como jogo de origem.
- METODO_OBTENCAO 0:N POKEMON_COLECAO como método original.
- ESPECIE 1:N FORMA.
- FORMA 1:N DADOS_FORMA_JOGO.
- JOGO 1:N MECANICA_JOGO.
- MECANICA_JOGO 1:N DADOS_FORMA_JOGO.
- DADOS_FORMA_JOGO N:N TIPO, por DADOS_FORMA_TIPO.
- DADOS_FORMA_JOGO 1:N HABILIDADE_FORMA_JOGO.
- HABILIDADE 1:N HABILIDADE_FORMA_JOGO.
- DADOS_FORMA_JOGO N:N METODO_OBTENCAO, por OBTENCAO_FORMA_JOGO.
- POKEMON_COLECAO 0:N POKEMON_ESTADO_JOGO.
- MECANICA_JOGO 1:N POKEMON_ESTADO_JOGO.
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
- PERFIL_ANALISE N:N NATUREZA, por PERFIL_NATUREZA.
- PERFIL_ANALISE N:N HABILIDADE_FORMA_JOGO, por PERFIL_HABILIDADE.
- MECANICA_JOGO 1:N REGULAMENTO.
- REGULAMENTO 1:N ELEGIBILIDADE_REGULAMENTO.
- DADOS_FORMA_JOGO 1:N ELEGIBILIDADE_REGULAMENTO.
- DADOS_FORMA_JOGO 1:N EVOLUCAO_FORMA_JOGO como origem e 1:N como destino.
- DADOS_FORMA_JOGO 1:N TRANSFORMACAO_FORMA como origem e 1:N como destino.

## 5. Regras que exigem validação adicional

- Um estado pertence ao mesmo contexto de mecânicas de DADOS_FORMA_JOGO.
- Um exemplar pode ter no máximo um estado atual por mecânica; ao evoluir, atualiza-se a forma no estado.
- A forma atual do exemplar deve pertencer à espécie consistente com a sua cadeia de evolução.
- A habilidade do estado pertence à mesma forma/contexto.
- O atributo de treinamento pertence à mesma mecânica do estado.
- Perfis, regulamentos, evoluções e transformações precisam usar contextos compatíveis.
- Limites agregados de treinamento e limite de dois tipos exigem validação transacional.
- Estado não deve ser criado para uma forma não registrável independentemente; transformação temporária não cria exemplar.
- A ausência de registro competitivo significa não verificado, não proibido.

As regras detalhadas estão em [regras-integridade.md](regras-integridade.md).

## 6. Decisões de escopo

- A primeira análise numérica será implementada para Scarlet/Violet.
- Champions terá estados e atributos de treinamento próprios, sem conversão em IV/EV.
- Legends: Z-A terá dados e mecânicas independentes.
- Winds/Waves não receberá regras antes de documentação oficial.
- Movimentos, itens e validação integral de legalidade individual estão fora da primeira versão.
- Histórico completo de estados e relatórios fica fora da primeira versão.
