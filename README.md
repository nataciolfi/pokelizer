# PokéAnalyzer

> Repositório: `pokelizer`

PokéAnalyzer é um projeto educacional que combina uma Pokédex Nacional completa com uma coleção pessoal de Pokémon e um analisador de atributos. O usuário poderá cadastrar os Pokémon que possui, informar IVs, EVs, natureza e habilidade, e comparar essas informações com perfis competitivos de referência ou perfis personalizados.

## Objetivo acadêmico

O projeto integra três disciplinas:

- **Banco de Dados:** modelagem conceitual e lógica, relacionamentos, SQL e persistência.
- **Programação Orientada a Objetos:** classes, objetos, atributos, métodos e separação de responsabilidades.
- **Desenvolvimento de Websites:** páginas, formulários, navegação e integração com o backend.

## Escopo definido

- Pokédex Nacional completa, incluindo as formas oficiais catalogadas.
- Contas de usuários e coleções individuais.
- Cadastro, consulta, edição e exclusão de Pokémon capturados.
- Registro de natureza, habilidade, nível, IVs e EVs.
- Comparação com perfis competitivos de referência e perfis personalizados.
- Consulta de regras competitivas oficiais por jogo, formato e temporada.
- Recomendações explicáveis: o sistema deverá mostrar quais dados motivaram cada sugestão.

## Tecnologias planejadas

| Tecnologia | Uso previsto |
|---|---|
| Python | Backend e regras de análise |
| Flask | Rotas e comunicação com o website |
| SQLite | Banco de dados inicial |
| SQL | Consultas e manipulação de dados |
| HTML | Estrutura das páginas |
| CSS | Estilo visual |
| JavaScript | Interações do frontend |

As tecnologias ainda são uma decisão de planejamento, não uma implementação concluída.

## Documentação

- [Escopo do projeto](docs/escopo.md)
- [Requisitos](docs/requisitos.md)
- [Modelo conceitual](docs/banco-de-dados/modelo-conceitual.md)
- [Relacionamentos e cardinalidades](docs/banco-de-dados/relacionamentos.md)
- [Diagrama Entidade-Relacionamento](docs/banco-de-dados/DER.md)
- [Decisões técnicas](docs/decisoes-tecnicas.md)
- [Plano de etapas](docs/plano-de-etapas.md)
- [Fontes oficiais e referência de regras](docs/fontes-oficiais.md)

## Situação atual

**Etapa:** planejamento conceitual.

Nenhum backend, frontend ou banco físico foi implementado ainda. O próximo objetivo é revisar e fechar o DER antes de convertê-lo em modelo lógico.

## Observações sobre dados e regras

- A Pokédex deve ser mantida como catálogo de espécies e formas, sem limitar o número de registros a uma lista inicial pequena.
- Dados de espécies, formas, tipos e habilidades deverão ter origem verificável.
- Regras competitivas devem ser vinculadas à publicação oficial correspondente e à sua vigência.
- Perfis competitivos do PokéAnalyzer são referências de análise. Eles não devem ser apresentados como builds obrigatórias oficialmente prescritas.
- Perfis personalizados pertencem ao usuário que os criou.
- O projeto é independente e não é afiliado à Nintendo, The Pokémon Company ou Game Freak. Pokémon e seus elementos relacionados são propriedade de seus respectivos titulares.
