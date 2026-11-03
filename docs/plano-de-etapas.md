# Plano de etapas

## Etapa 1 — Conceitual
- [x] Definir tema e objetivo.
- [x] Definir escopo e requisitos.
- [x] Identificar entidades e relacionamentos.
- [x] Separar dados globais e dados específicos por jogo.
- [x] Documentar regras de formas, treinamento e regulamentos.
- [ ] Conferir o DER visual no brModelo.

## Etapa 2 — Modelo lógico
- [ ] Converter entidades e relacionamentos em tabelas.
- [ ] Resolver relacionamentos N:N.
- [ ] Definir PK, FK, nulabilidade e unicidade.
- [ ] Definir restrições e índices.
- [ ] Revisar normalização.

## Etapa 3 — Banco físico
- [ ] Criar banco SQLite.
- [ ] Criar tabelas e restrições.
- [ ] Popular tipos e naturezas.
- [ ] Preparar importação do catálogo de espécies e formas.
- [ ] Testar consultas SQL.

## Etapa 4 — Backend e POO
- [ ] Criar estrutura Flask.
- [ ] Criar classes de domínio.
- [ ] Implementar acesso a dados.
- [ ] Implementar contas e autenticação.
- [ ] Implementar CRUD da coleção.
- [ ] Implementar comparador.

## Etapa 5 — Website
- [ ] Criar layout base.
- [ ] Criar Pokédex e pesquisa.
- [ ] Criar detalhes de espécie e forma.
- [ ] Criar login e cadastro.
- [ ] Criar formulário da coleção.
- [ ] Criar perfil e tela de análise.

## Etapa 6 — Dados e validação
- [ ] Importar dados oficiais com fonte registrada.
- [ ] Registrar contextos de jogo e mecânicas.
- [ ] Registrar regulamentos e elegibilidade.
- [ ] Testar limites IV/EV por mecânica.
- [ ] Testar isolamento entre usuários.
- [ ] Testar formas e transformações.

## Etapa 7 — Entrega
- [ ] Preparar dados de demonstração.
- [ ] Testar o fluxo completo.
- [ ] Documentar execução.
- [ ] Preparar apresentação das três disciplinas.
- [ ] Registrar limitações conhecidas.

## Regra de trabalho

Cada etapa deve gerar commits pequenos e mensagens claras. Não implementar o banco físico antes de revisar o modelo lógico.
