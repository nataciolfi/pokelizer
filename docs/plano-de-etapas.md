# Plano de etapas

O projeto será desenvolvido em etapas pequenas. Uma etapa só será considerada concluída depois de sua documentação e dos testes correspondentes.

## Etapa 1 — Conceitual

- [x] Definir o tema e o objetivo do PokéAnalyzer.
- [x] Definir o escopo inicial.
- [x] Listar requisitos funcionais e não funcionais.
- [x] Propor entidades, atributos e relacionamentos.
- [ ] Revisar o DER e validar todas as cardinalidades.

## Etapa 2 — Modelo lógico

- [ ] Converter o DER para o modelo relacional.
- [ ] Definir chaves primárias e estrangeiras.
- [ ] Resolver relacionamentos N:N.
- [ ] Revisar normalização e restrições.
- [ ] Validar o modelo com exemplos de dados.

## Etapa 3 — Banco físico

- [ ] Criar o banco SQLite.
- [ ] Criar tabelas e restrições.
- [ ] Inserir dados iniciais de tipos e naturezas.
- [ ] Planejar importação do catálogo completo.
- [ ] Testar consultas SQL.

## Etapa 4 — Backend e POO

- [ ] Criar estrutura Flask.
- [ ] Criar classes de domínio.
- [ ] Criar camada de acesso a dados.
- [ ] Implementar cadastro e autenticação.
- [ ] Implementar CRUD da coleção.
- [ ] Implementar serviço de comparação.

## Etapa 5 — Website

- [ ] Criar layout base.
- [ ] Criar telas da Pokédex.
- [ ] Criar tela de detalhes da espécie/forma.
- [ ] Criar telas de login e cadastro.
- [ ] Criar formulário de Pokémon capturado.
- [ ] Criar tela de análise.
- [ ] Criar página da coleção.

## Etapa 6 — Dados e validação

- [ ] Carregar o catálogo completo de espécies e formas.
- [ ] Conferir fontes e qualidade dos dados.
- [ ] Carregar habilidades, tipos e naturezas.
- [ ] Registrar os regulamentos oficiais selecionados.
- [ ] Testar limites de IV, EV e compatibilidade.
- [ ] Testar isolamento de dados entre usuários.

## Etapa 7 — Entrega e apresentação

- [ ] Preparar dados de demonstração.
- [ ] Testar o fluxo completo.
- [ ] Documentar como executar o projeto.
- [ ] Preparar explicação de Banco de Dados, POO e Website.
- [ ] Registrar limitações conhecidas.

## Regra de trabalho

Cada etapa deve gerar commits pequenos e com mensagens descritivas. Não avançar para implementação antes de revisar e aprovar o modelo lógico.
