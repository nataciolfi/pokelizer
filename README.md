# PokéAnalyzer

O **PokéAnalyzer** é um projeto educacional de Pokédex, coleção individual e análise comparativa de Pokémon. O sistema separa o catálogo global das espécies e formas, os dados de cada jogo, os exemplares pertencentes aos usuários e o estado de cada exemplar em um contexto de jogo.

O objetivo não é declarar genericamente que um Pokémon é “bom” ou “legal”. O sistema deve explicar **o que está comparando, em qual jogo, com quais regras, com quais dados e com qual fonte**.

## Objetivo acadêmico

O projeto integra três disciplinas:

- **Banco de Dados:** modelagem conceitual e lógica, integridade, relacionamentos, SQL e persistência.
- **Programação Orientada a Objetos:** classes de domínio, serviços, repositórios, validações e separação de responsabilidades.
- **Desenvolvimento de Websites:** páginas, formulários, navegação, acessibilidade e integração com o backend.

## Escopo da primeira versão

1. Pokédex Nacional com espécies e formas oficialmente documentadas segundo a política de catalogação do projeto.
2. Consulta por número, nome, tipo, geração, forma e contexto de jogo.
3. Cadastro e autenticação de usuários.
4. Coleções individuais, com vários exemplares da mesma espécie.
5. Registro separado da origem do exemplar e do estado dele em cada jogo.
6. Analisador inicial de atributos com contexto de Scarlet/Violet.
7. Perfis personalizados e perfis de referência, claramente identificados por fonte.
8. Consulta da elegibilidade da espécie/forma em regulamentos versionados, sem prometer uma verificação completa de legalidade individual.

## Contextos de jogo

- **Pokémon Scarlet e Pokémon Violet:** tratados como edições distintas. A primeira calculadora de atributos será validada para o contexto da Geração IX.
- **Pokémon Champions:** contexto próprio. Recrutamento, Pokémon visitantes e treinamento do Champions não serão convertidos em IV/EV de Scarlet/Violet. A estrutura prevê valores de treinamento específicos por contexto, que só serão cadastrados quando documentados.
- **Pokémon Legends: Z-A:** contexto separado. Não herda automaticamente regras de outros jogos.
- **Pokémon Winds e Pokémon Waves:** ainda não terão regras cadastradas antes de lançamento e documentação verificável.

## Tecnologias planejadas

| Tecnologia | Responsabilidade |
|---|---|
| Python | Regras de domínio e backend |
| Flask | Rotas HTTP e sessões |
| SQLite | Persistência inicial |
| SQL | Consultas, transações e restrições |
| HTML | Estrutura das páginas |
| CSS | Layout e responsividade |
| JavaScript | Interações do frontend |

Nenhuma dessas partes está implementada ainda. O repositório atualmente contém documentação e especificações; não há aplicação, banco físico ou testes automatizados.

## Documentação

- [Auditoria completa e decisões corretivas](docs/auditoria/revisao-completa-v3.md)
- [Escopo do projeto](docs/escopo.md)
- [Requisitos](docs/requisitos.md)
- [Matriz de casos de teste](docs/testes/casos-de-teste.md)
- [Modelo conceitual v3](docs/banco-de-dados/modelo-conceitual.md)
- [DER v3](docs/banco-de-dados/DER.md)
- [Relacionamentos e cardinalidades](docs/banco-de-dados/relacionamentos.md)
- [Regras de integridade e validação](docs/banco-de-dados/regras-integridade.md)
- [Revisão do DER](docs/banco-de-dados/revisao-der.md)
- [Wireframes e correções propostas](docs/design/wireframes.md)
- [Decisões técnicas](docs/decisoes-tecnicas.md)
- [Fontes e política de dados](docs/fontes-oficiais.md)
- [Plano de etapas](docs/plano-de-etapas.md)

## Situação atual

**Versão documental proposta:** 3.0.

A revisão v3 corrige a separação entre exemplar e estado por jogo, a modelagem de treinamento, a disponibilidade, os métodos de obtenção, os perfis e a elegibilidade competitiva.

**Ainda pendente:** conferir e atualizar o DER visual no brModelo e revisar visualmente os frames do Figma. As alterações desta revisão estão documentadas, mas não devem ser confundidas com mudanças já aplicadas nos arquivos visuais.

## Limites importantes

- Estar na Pokédex não significa estar presente em todos os jogos.
- Estar presente em um jogo não significa que o Pokémon possa ser obtido nele.
- Poder ser obtido não significa estar permitido em qualquer regulamento.
- Uma forma permitida não torna automaticamente um exemplar individual legal: movimentos, itens, origem, marca e outras condições podem ser necessários.
- IV, EV, natureza e treinamentos específicos dependem do contexto de jogo.
- Um IV 31 não é universalmente melhor; o valor desejado depende do objetivo do perfil.
- Dados desconhecidos permanecem desconhecidos, não são preenchidos com zero.
- Builds estratégicas de referência não são regras oficiais e devem ter fonte e versão.
- O projeto é independente e não é afiliado à Nintendo, The Pokémon Company ou Game Freak. Pokémon e seus elementos relacionados pertencem aos respectivos titulares.
