# Relacionamentos e cardinalidades — PokéAnalyzer

| Entidade A | Relacionamento | Entidade B | Cardinalidade |
|---|---|---|---|
| ESPECIE | possui | FORMA | 1:N |
| FORMA | possui dados em | DADOS_FORMA_JOGO | 1:N |
| JOGO | possui versões de | MECANICA_JOGO | 1:N |
| MECANICA_JOGO | define | DADOS_FORMA_JOGO | 1:N |
| DADOS_FORMA_JOGO | possui | TIPO | N:N |
| DADOS_FORMA_JOGO | disponibiliza | HABILIDADE_FORMA_JOGO | 1:N |
| HABILIDADE | aparece em | HABILIDADE_FORMA_JOGO | 1:N |
| USUARIO | possui | POKEMON_COLECAO | 1:N |
| JOGO | é origem de | POKEMON_COLECAO | 1:N opcional no registro |
| DADOS_FORMA_JOGO | representa | POKEMON_COLECAO | 1:N |
| NATUREZA | caracteriza | POKEMON_COLECAO | 1:N opcional no registro |
| HABILIDADE_FORMA_JOGO | é selecionada em | POKEMON_COLECAO | 1:N opcional no registro |
| DADOS_FORMA_JOGO | é alvo de | PERFIL_ANALISE | 1:N |
| USUARIO | cria | PERFIL_ANALISE | 1:N opcional no perfil |
| MECANICA_JOGO | recebe | REGULAMENTO | 1:N |
| REGULAMENTO | define | ELEGIBILIDADE_REGULAMENTO | 1:N |
| DADOS_FORMA_JOGO | é avaliada em | ELEGIBILIDADE_REGULAMENTO | 1:N |
| PERFIL_ANALISE | recomenda | NATUREZA | N:N opcional |
| PERFIL_ANALISE | recomenda | HABILIDADE_FORMA_JOGO | N:N opcional |
| REGULAMENTO | contextualiza | PERFIL_ANALISE | 1:N opcional no perfil |
| DADOS_FORMA_JOGO (origem) | inicia | TRANSFORMACAO_FORMA | 1:N |
| DADOS_FORMA_JOGO (destino) | recebe | TRANSFORMACAO_FORMA | 1:N |

## Explicação das relações

### ESPECIE — FORMA (1:N)
Uma espécie possui uma ou mais formas. Cada forma pertence a uma única espécie.

### FORMA — DADOS_FORMA_JOGO (1:N)
Uma forma pode aparecer em vários jogos ou conjuntos de mecânicas. Cada registro guarda a representação da forma em um contexto específico.

### JOGO — MECANICA_JOGO (1:N)
Um jogo pode ter várias versões de mecânicas documentadas. Cada versão pertence a um jogo.

### MECANICA_JOGO — DADOS_FORMA_JOGO (1:N)
Uma versão de mecânicas pode descrever muitas formas. Cada registro de dados de forma utiliza uma versão específica.

### DADOS_FORMA_JOGO — TIPO (N:N)
Uma forma em um jogo possui um ou dois tipos. Um tipo pode aparecer em muitas formas. O limite de dois é uma regra de negócio adicional.

### DADOS_FORMA_JOGO — HABILIDADE_FORMA_JOGO (1:N)
Uma forma em um jogo disponibiliza uma ou mais opções de habilidade. Cada opção pertence a uma única forma/jogo.

### HABILIDADE — HABILIDADE_FORMA_JOGO (1:N)
Uma habilidade pode aparecer em muitas formas/jogos. Cada opção de habilidade aponta para uma habilidade.

### USUARIO — POKEMON_COLECAO (1:N)
Um usuário pode registrar nenhum, um ou muitos Pokémon. Cada registro pertence a exatamente um usuário.

### JOGO — POKEMON_COLECAO (1:N, opcional no registro)

Um jogo pode ser a origem de muitos registros da coleção. Um registro pode informar zero ou um jogo de origem, pois a origem pode ser desconhecida ou o registro pode representar um Pokémon recrutado no contexto atual.

### DADOS_FORMA_JOGO — POKEMON_COLECAO (1:N)
Um contexto de forma/jogo pode ser usado por muitos exemplares. Cada exemplar está vinculado a exatamente um contexto. O método de obtenção distingue captura, transferência ou recrutamento.

### NATUREZA — POKEMON_COLECAO (1:N, opcional no registro)
Uma natureza pode aparecer em muitos exemplares. Um exemplar pode ter uma natureza registrada ou não, dependendo do contexto e dos dados disponíveis.

### HABILIDADE_FORMA_JOGO — POKEMON_COLECAO (1:N, opcional no registro)
Uma opção de habilidade pode ser selecionada por muitos exemplares. Cada exemplar seleciona zero ou uma opção, conforme o jogo. A relação evita selecionar uma habilidade inexistente naquele contexto.

### DADOS_FORMA_JOGO — PERFIL_ANALISE (1:N)
Uma forma em determinado jogo pode ter vários perfis de análise. Cada perfil é elaborado para um único contexto de forma e mecânicas.

### USUARIO — PERFIL_ANALISE (1:N, opcional no perfil)
Um usuário pode criar vários perfis personalizados. Um perfil pode ter zero proprietário se for mantido pelo sistema, ou um proprietário se for personalizado.

### MECANICA_JOGO — REGULAMENTO (1:N)
Uma versão de mecânicas pode receber vários regulamentos. Cada regulamento se refere a uma versão específica.

### REGULAMENTO — ELEGIBILIDADE_REGULAMENTO (1:N)
Um regulamento possui registros de elegibilidade para as formas verificadas. Cada registro pertence a um regulamento.

### DADOS_FORMA_JOGO — ELEGIBILIDADE_REGULAMENTO (1:N)
Uma forma em determinado jogo pode ser avaliada em vários regulamentos. Cada registro de elegibilidade avalia uma forma/jogo em um regulamento específico.

### PERFIL_ANALISE — NATUREZA (N:N opcional)
Um perfil pode recomendar uma ou várias naturezas, ou não especificar nenhuma. Uma natureza pode ser recomendada por vários perfis.

### PERFIL_ANALISE — HABILIDADE_FORMA_JOGO (N:N opcional)
Um perfil pode recomendar uma ou várias opções de habilidade. A ausência de recomendação não significa que a habilidade seja inválida.

### REGULAMENTO — PERFIL_ANALISE (1:N, opcional no perfil)
Um regulamento pode contextualizar vários perfis. Um perfil pode estar ligado a um regulamento ou não. Perfil competitivo específico de torneio deve apontar para o regulamento; perfil personalizado pode não apontar.

### DADOS_FORMA_JOGO — TRANSFORMACAO_FORMA
Cada transformação possui exatamente uma forma de origem e uma forma de destino. Uma forma pode participar de várias transformações.

## Restrições para o modelo lógico e backend

- E-mail único por usuário.
- Cada FORMA pertence a uma ESPECIE.
- A combinação FORMA + MECANICA_JOGO deve ser única em DADOS_FORMA_JOGO.
- Uma forma pode ter no máximo dois tipos em cada contexto.
- Habilidade selecionada deve pertencer às opções daquela forma/jogo.
- Um Pokémon da coleção só pode usar DADOS_FORMA_JOGO marcado como registrável.
- Limites de IV/EV vêm de MECANICA_JOGO.
- Campos não aplicáveis ficam nulos, não zero.
- Perfil personalizado deve ter proprietário.
- Perfil competitivo específico deve apontar para o regulamento.
- Ausência de elegibilidade verificada não significa proibição.
- Transformação deve ligar contextos compatíveis e ter condição documentada.
- Nenhuma análise pode misturar dados de jogos diferentes.
