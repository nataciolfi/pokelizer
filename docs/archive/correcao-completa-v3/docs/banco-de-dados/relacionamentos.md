# Relacionamentos e cardinalidades — PokéAnalyzer

**Versão:** 3.0

| Entidade A | Relacionamento | Entidade B | Cardinalidade |
|---|---|---|---|
| USUARIO | possui | POKEMON_COLECAO | 1:N |
| FORMA | é forma de origem de | POKEMON_COLECAO | 1:N opcional no exemplar |
| JOGO | é jogo de origem de | POKEMON_COLECAO | 1:N opcional no exemplar |
| METODO_OBTENCAO | descreve origem de | POKEMON_COLECAO | 1:N opcional no exemplar |
| ESPECIE | possui | FORMA | 1:N |
| FORMA | possui dados em | DADOS_FORMA_JOGO | 1:N |
| JOGO | possui contextos | MECANICA_JOGO | 1:N |
| MECANICA_JOGO | contextualiza | DADOS_FORMA_JOGO | 1:N |
| DADOS_FORMA_JOGO | possui tipos | TIPO | N:N, por DADOS_FORMA_TIPO |
| DADOS_FORMA_JOGO | disponibiliza | HABILIDADE_FORMA_JOGO | 1:N |
| HABILIDADE | aparece em | HABILIDADE_FORMA_JOGO | 1:N |
| DADOS_FORMA_JOGO | permite métodos | METODO_OBTENCAO | N:N, por OBTENCAO_FORMA_JOGO |
| POKEMON_COLECAO | possui estados | POKEMON_ESTADO_JOGO | 1:N |
| MECANICA_JOGO | contextualiza | POKEMON_ESTADO_JOGO | 1:N |
| DADOS_FORMA_JOGO | define forma atual de | POKEMON_ESTADO_JOGO | 1:N |
| NATUREZA | caracteriza | POKEMON_ESTADO_JOGO | 1:N opcional |
| HABILIDADE_FORMA_JOGO | é selecionada em | POKEMON_ESTADO_JOGO | 1:N opcional |
| MECANICA_JOGO | define | GRUPO_LIMITE_TREINAMENTO | 1:N |
| GRUPO_LIMITE_TREINAMENTO | agrupa | ATRIBUTO_TREINAMENTO | 1:N opcional no atributo |
| MECANICA_JOGO | define | ATRIBUTO_TREINAMENTO | 1:N |
| POKEMON_ESTADO_JOGO | registra | VALOR_TREINAMENTO_POKEMON | 1:N |
| ATRIBUTO_TREINAMENTO | é medido em | VALOR_TREINAMENTO_POKEMON | 1:N |
| DADOS_FORMA_JOGO | recebe perfis | PERFIL_ANALISE | 1:N |
| USUARIO | cria | PERFIL_ANALISE | 1:N opcional |
| REGULAMENTO | contextualiza | PERFIL_ANALISE | 1:N opcional |
| PERFIL_ANALISE | define valores | VALOR_TREINAMENTO_PERFIL | 1:N |
| ATRIBUTO_TREINAMENTO | é referência de | VALOR_TREINAMENTO_PERFIL | 1:N |
| PERFIL_ANALISE | recomenda | NATUREZA | N:N, por PERFIL_NATUREZA |
| PERFIL_ANALISE | recomenda | HABILIDADE_FORMA_JOGO | N:N, por PERFIL_HABILIDADE |
| MECANICA_JOGO | recebe | REGULAMENTO | 1:N |
| REGULAMENTO | define | ELEGIBILIDADE_REGULAMENTO | 1:N |
| DADOS_FORMA_JOGO | é avaliada em | ELEGIBILIDADE_REGULAMENTO | 1:N |
| DADOS_FORMA_JOGO (origem) | inicia | EVOLUCAO_FORMA_JOGO | 1:N |
| DADOS_FORMA_JOGO (destino) | recebe | EVOLUCAO_FORMA_JOGO | 1:N |
| DADOS_FORMA_JOGO (origem) | inicia | TRANSFORMACAO_FORMA | 1:N |
| DADOS_FORMA_JOGO (destino) | recebe | TRANSFORMACAO_FORMA | 1:N |

## Explicação das relações principais

### Catálogo e contexto

**ESPECIE — FORMA (1:N)**  
Uma espécie possui uma ou mais formas. Cada forma pertence a exatamente uma espécie. O número nacional identifica a espécie, não cada forma.

**FORMA — DADOS_FORMA_JOGO (1:N)**  
Uma forma pode ter dados em vários contextos de jogo. Uma forma catalogada não precisa estar presente em todos os títulos.

**JOGO — MECANICA_JOGO (1:N)**  
Cada jogo pode ter um ou mais contextos documentados de mecânicas. JOGO identifica a edição; MECANICA_JOGO guarda regras de atributos e treinamento. Regulamento competitivo não é uma mecânica.

### Tipos, habilidades e obtenção

**DADOS_FORMA_JOGO — TIPO (N:N)**  
DADOS_FORMA_TIPO guarda slot primário/secundário e limita a dois tipos.

**DADOS_FORMA_JOGO — HABILIDADE_FORMA_JOGO (1:N)**  
Uma forma/contexto pode oferecer várias opções de habilidade. Cada opção pertence a um contexto específico.

**DADOS_FORMA_JOGO — METODO_OBTENCAO (N:N)**  
OBTENCAO_FORMA_JOGO permite vários métodos e condições para a mesma forma no mesmo jogo.

### Exemplar, evolução e estado

**USUARIO — POKEMON_COLECAO (1:N)**  
Um usuário pode registrar muitos exemplares, inclusive vários da mesma espécie. Cada exemplar pertence a um único usuário.

**FORMA — POKEMON_COLECAO (1:N opcional)**  
A forma de origem é um dado de procedência. Ela não é a forma atual obrigatória do Pokémon e não muda quando ele evolui.

**POKEMON_COLECAO — POKEMON_ESTADO_JOGO (1:N)**  
Um exemplar individual pode ter estados em vários jogos. O registro global não guarda espécie atual, nível ou treinamento universal.

**DADOS_FORMA_JOGO — POKEMON_ESTADO_JOGO (1:N)**  
O estado aponta para a forma atual em um contexto de jogo. A espécie atual é derivada da forma associada ao estado.

**DADOS_FORMA_JOGO — EVOLUCAO_FORMA_JOGO**  
A evolução é uma transição permanente, com origem, destino, método e condição específicos do jogo. Ao evoluir, o sistema atualiza a forma do estado do mesmo exemplar. Não cria um novo exemplar.

**DADOS_FORMA_JOGO — TRANSFORMACAO_FORMA**  
Transformação de batalha é registrada separadamente. Mega Evolução e estados temporários não são tratados como evolução permanente nem como nova captura.

### Treinamento e perfil

**MECANICA_JOGO — ATRIBUTO_TREINAMENTO (1:N)**  
Cada mecânica define os atributos de treinamento existentes. Isso impede assumir IV/EV em todos os títulos.

**POKEMON_ESTADO_JOGO — VALOR_TREINAMENTO_POKEMON (1:N)**  
Cada estado armazena valores por atributo de treinamento. O mesmo exemplar em outro jogo tem valores separados.

**PERFIL_ANALISE — VALOR_TREINAMENTO_PERFIL (1:N)**  
Cada perfil define faixas ou valores desejados. Os atributos precisam pertencer à mecânica do perfil.

**PERFIL_ANALISE — NATUREZA/HABILIDADE (N:N)**  
Associações registram preferências e prioridades. Preferência não é sinônimo de obrigação.

### Regulamentos

**MECANICA_JOGO — REGULAMENTO (1:N)**  
Um contexto de jogo pode receber vários regulamentos/temporadas.

**REGULAMENTO — ELEGIBILIDADE_REGULAMENTO (1:N)**  
Sem linha verificada, a elegibilidade fica não verificada, nunca proibida por inferência.

**DADOS_FORMA_JOGO — ELEGIBILIDADE_REGULAMENTO (1:N)**  
A relação informa a elegibilidade catalogada da forma, não a legalidade completa de um exemplar individual.

## Restrições para o modelo lógico

- Número nacional único por espécie.
- Código de forma único dentro da espécie.
- Forma + mecânica única em DADOS_FORMA_JOGO.
- A coleção não possui uma espécie atual fixa; o estado aponta para a forma atual.
- Forma de origem é opcional e não muda após evolução.
- Um estado atual por exemplar + mecânica.
- Evolução atualiza o estado do mesmo exemplar.
- Transformação temporária não cria captura.
- No máximo dois tipos por contexto e slots distintos.
- Habilidade selecionada compatível com o contexto do estado.
- Valores de treinamento vinculados à mesma mecânica do estado.
- Limites individuais e incrementos definidos por atributo; limites agregados definidos uma única vez por grupo.
- Limites individuais e agregados de treinamento respeitados.
- Perfil, regulamento, evolução e transformação contextualmente compatíveis.
- Perfil personalizado com proprietário; perfil de sistema sem proprietário.
- Ausência de elegibilidade = não verificado.
- Toda consulta/alteração privada filtra o usuário autenticado.

Ver [regras-integridade.md](regras-integridade.md) para as regras e testes mínimos.
