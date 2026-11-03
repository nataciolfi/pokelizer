# Relacionamentos e cardinalidades

Este documento explica as relações previstas no modelo conceitual e as regras que devem ser respeitadas.

## 1. Relacionamentos

| Entidade A | Relacionamento | Entidade B | Cardinalidade |
|---|---|---|---|
| ESPECIE | possui | FORMA | 1:N |
| FORMA | possui | TIPO | N:N |
| FORMA | disponibiliza | HABILIDADE | N:N |
| USUARIO | possui | POKEMON_CAPTURADO | 1:N |
| FORMA | representa | POKEMON_CAPTURADO | 1:N |
| NATUREZA | caracteriza | POKEMON_CAPTURADO | 1:N |
| HABILIDADE | é selecionada em | POKEMON_CAPTURADO | 1:N |
| FORMA | orienta | PERFIL_ANALISE | 1:N |
| USUARIO | cria | PERFIL_ANALISE | 1:N opcional no perfil |
| REGULAMENTO | contextualiza | PERFIL_ANALISE | 1:N opcional no perfil |
| PERFIL_ANALISE | recomenda | NATUREZA | N:N |
| PERFIL_ANALISE | recomenda | HABILIDADE | N:N opcional |
| REGULAMENTO | permite | FORMA | N:N |

## 2. Leitura das cardinalidades

### ESPECIE — FORMA (1:N)

Uma espécie possui uma ou mais formas catalogadas. Cada forma pertence a uma única espécie.

### FORMA — TIPO (N:N)

Uma forma possui um ou dois tipos. Um tipo pode estar associado a muitas formas.

A regra de máximo de dois tipos é uma restrição de domínio que será validada na implementação.

### FORMA — HABILIDADE (N:N)

Uma forma pode disponibilizar diferentes habilidades. Uma habilidade pode estar disponível para várias formas.

### USUARIO — POKEMON_CAPTURADO (1:N)

Um usuário pode cadastrar nenhum, um ou muitos Pokémon. Cada Pokémon capturado pertence obrigatoriamente a um único usuário.

### FORMA — POKEMON_CAPTURADO (1:N)

Uma forma pode aparecer em muitos registros de captura. Cada captura corresponde a uma forma específica.

### NATUREZA — POKEMON_CAPTURADO (1:N)

Uma natureza pode ser usada por muitos Pokémon capturados. Cada registro possui uma única natureza.

### HABILIDADE — POKEMON_CAPTURADO (1:N)

Uma habilidade pode ser selecionada em muitos registros. Cada registro de captura seleciona uma habilidade. A compatibilidade com a forma deve ser verificada pela regra de negócio.

### FORMA — PERFIL_ANALISE (1:N)

Uma forma pode ter vários perfis de análise. Cada perfil é feito para uma forma específica.

### USUARIO — PERFIL_ANALISE (1:N, opcional no perfil)

Um usuário pode criar vários perfis personalizados. Um perfil pode ter zero ou um usuário proprietário: zero para perfil de referência mantido pelo sistema e um para perfil personalizado.

### REGULAMENTO — PERFIL_ANALISE (1:N, opcional no perfil)

Um regulamento pode contextualizar vários perfis competitivos. Um perfil personalizado pode não estar associado a regulamento algum.

### PERFIL_ANALISE — NATUREZA (N:N)

Um perfil pode recomendar uma ou mais naturezas. Uma natureza pode ser recomendada por diversos perfis.

### PERFIL_ANALISE — HABILIDADE (N:N opcional)

Um perfil pode recomendar uma ou mais habilidades, mas também pode deixar a habilidade em aberto. Uma habilidade pode ser recomendada por vários perfis.

### REGULAMENTO — FORMA (N:N)

Um regulamento pode permitir várias formas, e uma forma pode aparecer em vários regulamentos. Essa relação deve refletir somente listas oficiais e precisa considerar as condições específicas do regulamento.

## 3. Restrições que não são resolvidas apenas pela cardinalidade

- A habilidade selecionada em POKEMON_CAPTURADO deve ser uma habilidade disponibilizada pela FORMA correspondente.
- A forma associada a POKEMON_CAPTURADO deve estar marcada como capturável diretamente; formas temporárias de batalha não podem ser registradas como captura independente.
- Se um perfil recomendar habilidades, a habilidade selecionada pelo usuário deve ser comparada com essa lista; ausência de recomendação não deve ser tratada automaticamente como erro.
- Um perfil personalizado deve possuir um usuário proprietário.
- Um perfil competitivo deve ser mantido pelo sistema e, quando depender de regras específicas, estar vinculado ao regulamento correspondente.
- A soma e os limites de EV devem obedecer ao jogo e à geração selecionados.
- A elegibilidade de uma forma deve ser validada de acordo com a fonte oficial e eventuais exceções do regulamento.

Essas condições deverão ser documentadas como regras de negócio e implementadas por validações no backend e/ou restrições no banco lógico.
