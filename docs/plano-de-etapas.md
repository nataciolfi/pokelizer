# Plano de etapas

**Versão:** 3.0  
**Regra:** não avançar para banco físico e implementação enquanto as decisões conceituais e lógicas ainda estiverem contraditórias.

## Etapa 0 — Auditoria e correção da especificação
- [x] Inspecionar todos os documentos existentes do repositório.
- [x] Identificar contradições entre escopo, requisitos, DER, decisões técnicas e wireframes documentados.
- [x] Definir separação entre exemplar individual e estado por jogo.
- [x] Definir treinamento configurável por contexto.
- [x] Diferenciar presença, obtenibilidade, registrabilidade e elegibilidade.
- [x] Documentar limitações da verificação competitiva.
- [x] Especificar correções para as oito telas.
- [ ] Obter aprovação do modelo conceitual v3.

## Etapa 1 — Modelo conceitual
- [x] Definir objetivo, escopo e funcionalidades revisadas.
- [x] Definir entidades, relacionamentos e regras de negócio v3.
- [x] Separar espécie, forma e transformação.
- [x] Separar catálogo global e dados específicos por jogo.
- [x] Separar exemplar e estado do exemplar em jogo.
- [x] Separar perfil de análise e regulamento.
- [ ] Conferir o DER v3 visualmente no brModelo.
- [ ] Aprovar cardinalidades e regras com casos de teste.

## Etapa 2 — Modelo lógico
- [ ] Converter entidades e associações em tabelas.
- [ ] Definir PK, FK e chaves únicas.
- [ ] Definir FKs compostas para garantir compatibilidade entre jogo, mecânica, forma e habilidade.
- [ ] Definir nulabilidade e valores controlados.
- [ ] Definir CHECKs, índices e gatilhos estritamente necessários.
- [ ] Verificar normalização.
- [ ] Revisar o modelo com exemplos concretos de Scarlet/Violet e Champions.

## Etapa 3 — Banco físico SQLite
- [ ] Criar banco e tabelas.
- [ ] Ativar foreign keys em toda conexão.
- [ ] Criar índices e restrições.
- [ ] Popular tipos, naturezas e dados iniciais confiáveis.
- [ ] Criar processo de importação versionado.
- [ ] Validar inserções, atualizações e exclusões.
- [ ] Testar limites de treinamento e integridade de contextos.

## Etapa 4 — Backend e POO
- [ ] Criar estrutura Flask.
- [ ] Separar modelos de domínio, repositórios e serviços.
- [ ] Implementar autenticação e sessão.
- [ ] Implementar isolamento de coleção e perfil por usuário.
- [ ] Implementar cadastro e atualização de estados por jogo.
- [ ] Implementar serviço de comparação.
- [ ] Implementar consulta de elegibilidade de forma.
- [ ] Implementar validações no servidor e tratamento de erros.

## Etapa 5 — Website
- [ ] Revisar e aprovar wireframes.
- [ ] Criar layout base e navegação.
- [ ] Criar login e cadastro.
- [ ] Criar Pokédex e pesquisa/filtros.
- [ ] Criar detalhes de espécie e forma.
- [ ] Criar coleção e cadastro de exemplar/estado.
- [ ] Criar perfis.
- [ ] Criar tela do analisador.
- [ ] Criar estados vazio, carregamento, erro e dados não verificados.
- [ ] Verificar responsividade.

## Etapa 6 — Dados e validação
- [ ] Definir fonte/licença de cada conjunto importado.
- [ ] Importar espécies e formas com relatório de cobertura.
- [ ] Importar dados por jogo e registrar versão.
- [ ] Validar Scarlet/Violet com casos conhecidos.
- [ ] Acrescentar dados de Champions só quando regras específicas estiverem verificadas.
- [ ] Acrescentar Legends: Z-A em etapa própria, sem herdar regras.
- [ ] Atualizar regulamentos e registrar vigência/fonte.
- [ ] Testar isolamento entre usuários e segurança de rotas.
- [ ] Testar formas, transformações e métodos de obtenção.

## Etapa 7 — Testes e entrega
- [ ] Testar unidade dos cálculos e validadores.
- [ ] Testar integração banco/backend.
- [ ] Testar fluxo completo no navegador.
- [ ] Testar usuário A contra registros de usuário B.
- [ ] Testar dados ausentes e não aplicáveis.
- [ ] Preparar conjunto de demonstração rastreável.
- [ ] Documentar instalação, execução e limitações.
- [ ] Preparar apresentação das três disciplinas.
- [ ] Registrar versão entregue e commits.

## Critério de avanço

Uma etapa só é considerada concluída quando seus artefatos existem e foram verificados. Uma tarefa documentada não equivale a uma funcionalidade implementada. Um diagrama textual não equivale a um DER visual conferido.
