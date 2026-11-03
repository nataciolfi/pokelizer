# PokéAnalyzer

PokéAnalyzer é um projeto educacional que combina uma Pokédex Nacional completa com uma coleção pessoal e um analisador de atributos. O catálogo mantém espécies e formas oficiais; os dados de estatísticas, tipos, habilidades e disponibilidade são contextualizados por jogo.

## Objetivo acadêmico

O projeto integra três disciplinas:

- **Banco de Dados:** modelagem conceitual e lógica, relacionamentos, SQL e persistência.
- **Programação Orientada a Objetos:** classes, objetos, atributos, métodos e separação de responsabilidades.
- **Desenvolvimento de Websites:** páginas, formulários, navegação e integração com o backend.

## Escopo definido

- Pokédex Nacional completa, incluindo formas oficiais catalogadas.
- Dados de formas, tipos, habilidades e atributos por jogo.
- Contas de usuários e coleções individuais.
- Registro de Pokémon capturados, transferidos ou recrutados.
- Registro de natureza, habilidade, nível, IVs e EVs quando aplicáveis ao jogo.
- Comparação com perfis competitivos de referência e perfis personalizados.
- Verificação de elegibilidade por regulamento oficial.
- Recomendações explicáveis, com indicação do jogo e perfil utilizados.

## Contextos de jogo

- **Pokémon Scarlet/Violet (Geração IX):** referência principal da calculadora de IV, EV e natureza.
- **Pokémon Champions:** contexto competitivo separado, com recrutamento, transferência e sistema próprio de treinamento. Não converter treinamento de Champions em IV/EV de Scarlet/Violet.
- **Pokémon Legends: Z-A:** contexto próprio; não herdar automaticamente as regras de Scarlet/Violet.
- **Outros jogos oficiais:** poderão ser acrescentados por meio de novos registros de jogo e mecânica.

## Tecnologias planejadas

| Tecnologia | Uso previsto |
|---|---|
| Python | Backend e regras de análise |
| Flask | Rotas e comunicação com o website |
| SQLite | Banco de dados inicial |
| SQL | Consultas e manipulação dos dados |
| HTML | Estrutura das páginas |
| CSS | Estilo visual |
| JavaScript | Interações do frontend |

As tecnologias ainda são decisões de planejamento; a implementação não começou.

## Documentação

- [Escopo do projeto](docs/escopo.md)
- [Requisitos](docs/requisitos.md)
- [Modelo conceitual](docs/banco-de-dados/modelo-conceitual.md)
- [Revisão e fechamento do DER](docs/banco-de-dados/revisao-der.md)
- [Relacionamentos e cardinalidades](docs/banco-de-dados/relacionamentos.md)
- [Diagrama Entidade-Relacionamento](docs/banco-de-dados/DER.md)
- [Decisões técnicas](docs/decisoes-tecnicas.md)
- [Plano de etapas](docs/plano-de-etapas.md)
- [Fontes oficiais e referência de regras](docs/fontes-oficiais.md)

## Situação atual

**Etapa:** revisão conceitual, versão 2.0.

A documentação e o DER textual foram atualizados para separar catálogo global, dados específicos por jogo, coleção e elegibilidade competitiva. Falta conferir o diagrama visual no brModelo antes de considerar a etapa conceitual completamente encerrada.

Nenhum backend, frontend ou banco físico foi implementado ainda.

## Observações sobre dados e regras

- A presença na Pokédex não significa disponibilidade em todos os jogos.
- A presença no jogo não significa elegibilidade em qualquer regulamento.
- Perfis competitivos do PokéAnalyzer são referências de análise, não builds obrigatórias publicadas oficialmente.
- Campos não aplicáveis devem permanecer nulos; zero é um valor real.
- Dados de espécies, formas, tipos, habilidades e regulamentos devem ter origem verificável.
- O projeto é independente e não é afiliado à Nintendo, The Pokémon Company ou Game Freak. Pokémon e seus elementos relacionados são propriedade de seus respectivos titulares.
