# DER 3.0 — quadro visual no Figma

**Quadro FigJam:** [PokéAnalyzer — DER 3.0](https://www.figma.com/board/2hpHQKy2zeoTFDFJX6EXQ9)  
**Modelo de referência:** [modelo conceitual 3.0](../banco-de-dados/modelo-conceitual-v3.md)  
**DER textual completo:** [DER.md](../banco-de-dados/DER.md)

## Estado do quadro

**Status: parcial.**

Dois diagramas foram gerados no mesmo quadro FigJam e são editáveis. O terceiro diagrama ainda não foi criado: uma nova tentativa foi bloqueada pelo limite de chamadas do Figma MCP no plano Starter. Portanto, o quadro atual **não deve ser considerado o DER visual completo**.

## Diagrama 1 — Catálogo e jogos

Entidades:
- ESPECIE
- FORMA
- JOGO
- DADOS_FORMA_JOGO
- MECANICA_JOGO
- TIPO
- TIPO_FORMA_JOGO
- HABILIDADE
- HABILIDADE_FORMA_JOGO
- METODO_OBTENCAO
- METODO_FORMA_JOGO
- TRANSFORMACAO_FORMA

Este domínio mostra catálogo global, presença por jogo, mecânicas versionadas, tipos ordenados, habilidades disponíveis, métodos possíveis e transformações.

## Diagrama 2 — Coleção e valores de atributos

**Status: criado no quadro FigJam em 05/11/2026.**

Entidades centrais:
- USUARIO
- POKEMON_COLECAO
- NATUREZA
- ATRIBUTO_BATALHA
- SISTEMA_ATRIBUTO
- MECANICA_SISTEMA_ATRIBUTO
- VALOR_ATRIBUTO_POKEMON

Entidades de contexto repetidas para leitura:
- JOGO
- DADOS_FORMA_JOGO
- METODO_OBTENCAO
- HABILIDADE_FORMA_JOGO
- MECANICA_JOGO

O diagrama representa a propriedade dos exemplares, o contexto atual e a origem, os dados opcionais do exemplar e os valores registrados por sistema, versão de mecânica e atributo. IV, EV e outros sistemas não são tratados como equivalentes.

## Diagrama 3 — Análise e regulamentos

**Status: pendente.**

Entidades centrais:
- PERFIL_ANALISE
- VALOR_PERFIL_ANALISE
- PERFIL_NATUREZA
- PERFIL_HABILIDADE
- REGULAMENTO
- ELEGIBILIDADE_FORMA_REGULAMENTO

Entidades de contexto previstas:
- USUARIO
- NATUREZA
- HABILIDADE_FORMA_JOGO
- DADOS_FORMA_JOGO
- MECANICA_JOGO
- MECANICA_SISTEMA_ATRIBUTO
- ATRIBUTO_BATALHA

Este domínio deve deixar explícito que perfil de análise e regulamento são entidades distintas. A elegibilidade verifica espécie/forma no contexto do regulamento; não declara a legalidade completa do exemplar.

## Regras de leitura

- PK: chave primária.
- FK: chave estrangeira.
- UK: valor único.
- Uma linha sólida representa relação identificadora no desenho.
- Símbolos de cardinalidade devem ser conferidos com as regras descritas em DER.md.
- As restrições que exigem regras adicionais (por exemplo, no máximo dois tipos) estão documentadas no DER textual e não podem ser inferidas só pelas linhas.
- Entidades repetidas em diagramas diferentes são referências do mesmo conceito, não novas entidades do modelo.

## Próximas revisões

1. Criar o diagrama 3 — análise e regulamentos — no mesmo quadro FigJam.
2. Conferir se cada FK tem sua relação correspondente nos três diagramas.
3. Revisar cardinalidades opcionais/obrigatórias.
4. Verificar que PERFIL_ANALISE não mistura perfil e regulamento.
5. Fazer uma checagem visual de legibilidade e conexões.
6. Marcar o DER como completo somente após essas verificações.

**Decisão de ferramenta:** o DER será mantido no Figma/FigJam. Não é necessário produzir uma cópia no brModelo.
