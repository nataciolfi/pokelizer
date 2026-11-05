# Plano de etapas — revisão após auditoria

## Etapa 0 — Fechamento da especificação
- [x] Auditar escopo, requisitos, documentos, DER textual e especificação dos wireframes.
- [x] Registrar contradições.
- [x] Propor modelo conceitual 3.0.
- [ ] Conferir visualmente as oito telas Figma.
- [ ] Aprovar critérios de inclusão das formas.
- [ ] Aprovar o limite do MVP.

## Etapa 1 — Modelo conceitual
- [x] Definir espécie, forma, jogo e mecânica como conceitos separados.
- [x] Separar jogo atual, origem e método de obtenção.
- [x] Separar sistemas de valores de atributo.
- [x] Separar perfil e regulamento.
- [x] Criar o primeiro diagrama do DER 3.0 no FigJam (catálogo e jogos).
- [x] Criar o segundo diagrama do DER 3.0 no FigJam (coleção e valores de atributos).
- [ ] Criar o terceiro diagrama do DER 3.0 no FigJam (análise e regulamentos).
- [ ] Conferir entidades associativas, cardinalidades e obrigatoriedade nos três diagramas.
- [ ] Testar exemplos de Pokémon transferido, recrutado e transformado.

## Etapa 2 — Modelo lógico
- [ ] Converter entidades em tabelas.
- [ ] Resolver N:N.
- [ ] Definir PK, FK, nulabilidade e unicidade.
- [ ] Definir CHECK constraints e índices.
- [ ] Definir regras que pertencem ao backend.
- [ ] Revisar 1FN, 2FN e 3FN.
- [ ] Criar dicionário de dados.

## Etapa 3 — Banco físico
- [ ] Criar SQLite e schema.sql.
- [ ] Ativar PRAGMA foreign_keys = ON em cada conexão.
- [ ] Criar restrições e índices.
- [ ] Popular tipos, naturezas, atributos e sistemas.
- [ ] Validar com catálogo pequeno antes da importação completa.
- [ ] Testar dados inválidos.

## Etapa 4 — Domínio e POO
- [ ] Criar classes de domínio para usuário, exemplar, jogo, mecânica e perfil.
- [ ] Criar DAO/repositórios.
- [ ] Criar serviço de coleção.
- [ ] Criar serviço de validação de treinamento.
- [ ] Criar serviço de análise com regras documentadas de comparação por atributo.
- [ ] Criar testes unitários.

## Etapa 5 — Backend Flask
- [ ] Criar configuração e estrutura.
- [ ] Implementar cadastro, login e logout.
- [ ] Implementar autorização por proprietário.
- [ ] Implementar CRUD da coleção.
- [ ] Implementar catálogo e filtros.
- [ ] Implementar perfis e elegibilidade limitada.
- [ ] Validar entradas e proteger formulários.

## Etapa 6 — Website
- [ ] Criar layout e navegação.
- [ ] Criar login/cadastro.
- [ ] Criar Pokédex/filtros.
- [ ] Criar detalhes de espécie/forma.
- [ ] Criar lista e detalhe de exemplar.
- [ ] Criar formulário de adição/edição.
- [ ] Criar lista/edição de perfis.
- [ ] Criar analisador e resultado.
- [ ] Criar estados de erro, vazio, carregamento e dados não verificados.
- [ ] Revisar responsividade e teclado.

## Etapa 7 — Dados e fontes
- [ ] Definir critérios de formas.
- [ ] Importar espécie/forma com identificadores estáveis.
- [ ] Registrar fonte e data.
- [ ] Registrar disponibilidade, tipos, habilidades e métodos por jogo.
- [ ] Registrar mecânicas e limites confirmados.
- [ ] Registrar regulamentos e elegibilidade com fontes.
- [ ] Marcar lacunas como não verificadas.

## Etapa 8 — Testes e entrega
- [ ] Testar isolamento entre usuários.
- [ ] Testar CRUD de exemplares.
- [ ] Testar compatibilidade forma/jogo/habilidade.
- [ ] Testar limites de treinamento.
- [ ] Testar ausência de conversão entre jogos.
- [ ] Testar perfis e regulamentos independentes.
- [ ] Testar resultado sem nota global arbitrária e tratamento de valores ausentes.
- [ ] Testar estados vazios e erros.
- [ ] Documentar instalação e execução.
- [ ] Preparar dados de demonstração.
- [ ] Preparar apresentação das três disciplinas.
- [ ] Registrar limitações.

**Regra:** não criar banco físico antes do modelo lógico. Não importar o catálogo completo antes de validar a estrutura com poucos registros. O MVP começa por Scarlet/Violet; outro jogo só habilita cálculo com regras confirmadas.
