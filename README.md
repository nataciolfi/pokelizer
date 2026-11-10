# PokéAnalyzer

PokéAnalyzer é um projeto educacional com catálogo de espécies e formas Pokémon documentadas, coleção individual por usuário e analisador de atributos contextualizado por jogo.

## Objetivo acadêmico
- **Banco de Dados:** modelagem, relacionamentos, SQL e integridade.
- **Programação Orientada a Objetos:** classes, regras de domínio, serviços e persistência.
- **Desenvolvimento de Websites:** páginas, formulários, navegação e backend.

## Estado real

O repositório contém a documentação do projeto e uma primeira base de backend Flask/SQLite na pasta `backend/`. **O frontend, a importação do catálogo e o banco físico definitivo ainda não foram concluídos.** O schema do backend é provisório e deverá ser revisado após a construção do DER no brModelo.

## Escopo planejado

- Catálogo de espécies e formas oficiais documentadas.
- Dados e mecânicas separados por jogo.
- Contas e coleções individuais.
- Jogo atual, jogo de origem e método de obtenção separados.
- Treinamento registrado por sistema/atributo.
- Perfis personalizados e referências competitivas.
- Elegibilidade da espécie/forma por regulamento, sem prometer legalidade completa do exemplar.

## Contextos
- **Scarlet/Violet:** primeiro analisador completo de IV/EV/natureza.
- **Pokémon Champions:** treinamento separado, sem conversão para IV/EV.
- **Pokémon Legends: Z-A:** contexto próprio, com regras verificadas.
- **Pokémon Ventos e Ondas:** sem regras presumidas antes de documentação suficiente.

## Tecnologias planejadas

Python, Flask e SQLite já são usados na base inicial do backend. HTML, CSS e JavaScript permanecem planejados para a integração do frontend.

## Documentação

- [Auditoria técnica completa](docs/auditoria-completa.md)
- [Algoritmo de análise — versão inicial](docs/algoritmo-analise.md)
- [Decisões ainda em aberto](docs/decisoes-em-aberto.md)
- [Especificação das telas](docs/design/wireframes.md)
- [Escopo](docs/escopo.md)
- [Requisitos](docs/requisitos.md)
- [Modelo conceitual 3.0](docs/banco-de-dados/modelo-conceitual-v3.md)
- [DER 3.0 — documentação](docs/banco-de-dados/DER.md)
- [DER 3.0 — construção no brModelo](docs/design/der-brmodelo.md)
- [Relacionamentos 3.0](docs/banco-de-dados/relacionamentos.md)
- [Modelo conceitual 2.0 — histórico](docs/banco-de-dados/modelo-conceitual.md)
- [Decisões técnicas](docs/decisoes-tecnicas.md)
- [Plano de etapas](docs/plano-de-etapas.md)
- [Fontes oficiais](docs/fontes-oficiais.md)

## Backend — Etapa 2

- [Instruções para instalar, executar e testar a API](backend/README.md)
- [Código Python, DAOs, serviços, rotas Flask e schema provisório](backend/)

A implementação inicial permite cadastro de usuário, autenticação, consulta do catálogo e cadastro/consulta/exclusão de exemplares da coleção. Ela ainda não substitui a revisão do modelo lógico após o DER no brModelo.

## Fontes oficiais iniciais
- [Pokédex](https://www.pokemon.com/br/pokedex)
- [Pokémon Champions — treinamento](https://champions.pokemon.com/pt-br/pokemon/)
- [Pokémon Champions — mecânica](https://champions.pokemon.com/pt-br/gameplay/)
- [Pokémon Ventos e Ondas](https://windswaves.pokemon.com/pt-br/)

## Aviso
Projeto independente, sem afiliação à Nintendo, The Pokémon Company ou Game Freak. Pokémon e elementos relacionados pertencem aos respectivos titulares.
