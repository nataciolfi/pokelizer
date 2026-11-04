# DER 3.0 — quadro visual no Figma

**Quadro FigJam:** [PokéAnalyzer — DER 3.0 | Catálogo e jogos](https://www.figma.com/board/2hpHQKy2zeoTFDFJX6EXQ9)  
**Modelo de referência:** [modelo conceitual 3.0](../banco-de-dados/modelo-conceitual-v3.md)  
**DER textual completo:** [DER.md](../banco-de-dados/DER.md)

## Estado do quadro

<badge>Parcial</badge>

O primeiro diagrama foi gerado no FigJam e é editável. Ele cobre o domínio de catálogo e contexto de jogo. O limite de chamadas do Figma MCP no plano Starter impediu acrescentar os outros dois diagramas nesta execução. Portanto, o quadro atual **não deve ser considerado o DER visual completo**.

## Diagrama 1 — Catálogo e jogos

Entidades presentes:
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

Ainda precisa ser acrescentado ao mesmo quadro:
- USUARIO
- POKEMON_COLECAO
- NATUREZA
- ATRIBUTO_BATALHA
- SISTEMA_ATRIBUTO
- MECANICA_SISTEMA_ATRIBUTO
- VALOR_ATRIBUTO_POKEMON

As entidades JOGO, DADOS_FORMA_JOGO, METODO_OBTENCAO, HABILIDADE_FORMA_JOGO e MECANICA_JOGO aparecem novamente como referências de contexto para manter o diagrama compreensível.

## Diagrama 3 — Análise e regulamentos

Ainda precisa ser acrescentado:
- PERFIL_ANALISE
- VALOR_PERFIL_ANALISE
- PERFIL_NATUREZA
- PERFIL_HABILIDADE
- REGULAMENTO
- ELEGIBILIDADE_FORMA_REGULAMENTO

As entidades NATUREZA, HABILIDADE_FORMA_JOGO, DADOS_FORMA_JOGO, MECANICA_JOGO, MECANICA_SISTEMA_ATRIBUTO e ATRIBUTO_BATALHA aparecem novamente como referências.

## Regras de leitura

- PK: chave primária.
- FK: chave estrangeira.
- UK: valor único.
- Uma linha sólida representa relação identificadora no desenho.
- Símbolos de cardinalidade devem ser conferidos com as regras descritas em DER.md.
- As restrições que exigem regras adicionais (por exemplo, no máximo dois tipos) estão documentadas no DER textual e não podem ser inferidas só pelas linhas.

## Próximas revisões

1. Acrescentar os diagramas 2 e 3 no mesmo quadro FigJam.
2. Conferir se cada FK tem sua relação correspondente.
3. Revisar cardinalidades opcionais/obrigatórias.
4. Verificar que PERFIL_ANALISE não mistura perfil e regulamento.
5. Fazer uma checagem visual de legibilidade e conexões.
6. Marcar o DER como completo somente após essas verificações.

**Decisão de ferramenta:** o DER será mantido no Figma/FigJam. Não é necessário produzir uma cópia no brModelo.
