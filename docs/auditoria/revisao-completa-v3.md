# Auditoria completa do PokéAnalyzer

**Data:** 03/11/2026  
**Versão auditada:** documentação e wireframes desktop existentes no repositório.  
**Versão corretiva proposta:** 3.0.  
**Escopo:** produto, domínio Pokémon, modelo de dados, requisitos, arquitetura, segurança, dados e interface.

## 1. Resultado executivo

A ideia central é válida, mas o DER 2.0 não estava pronto para virar SQL ou código. Havia requisitos prometidos que o modelo não conseguia representar sem perda, duplicidade ou ambiguidade.

**Diagnóstico:** documentação inicial com boa direção, mas insuficiente para implementação segura. O problema não era só nomenclatura: eram relações que não representavam o ciclo de vida real de um Pokémon.

O repositório auditado contém documentação e referência de Figma. Não contém código de backend/frontend, arquivo SQLite, migrações, dados importados ou testes. Portanto, não seria correto afirmar que bugs de implementação foram corrigidos ou que o sistema passou em testes executáveis.

## 2. Severidade

- **Crítica:** pode corromper conceitos/dados ou produzir conclusões falsas.
- **Alta:** impede requisito central ou torna o fluxo inconsistente.
- **Média:** causa ambiguidade, manutenção difícil ou experiência incompleta.
- **Baixa:** melhoria de clareza ou apresentação.

## 3. Achados críticos

### C01 — Exemplar e estado em jogo estavam misturados
**Severidade:** crítica.

Na versão anterior, POKEMON_COLECAO apontava diretamente para DADOS_FORMA_JOGO. Isso prendia o exemplar a um único contexto e misturava jogo de origem com jogo atual. Transferências e treinamentos em um segundo jogo exigiriam duplicar ou sobrescrever dados.

**Correção v3:** POKEMON_COLECAO representa o indivíduo; POKEMON_ESTADO_JOGO representa o estado em cada mecânica. Um indivíduo pode ter estados separados por jogo.

### C02 — Champions era prometido, mas o modelo só guardava IV/EV
**Severidade:** crítica.

O modelo tinha um campo textual de sistema de treinamento, mas somente 6 colunas IV e 6 EV para Pokémon e perfil. Isso não modela um sistema próprio. A documentação oficial de Champions confirma recrutamento, visitantes via HOME e treinamento por Pontos de Vitória, com comportamento próprio e sem transferência dos ajustes de treinamento para HOME.

**Correção v3:** ATRIBUTO_TREINAMENTO define valores por mecânica; VALOR_TREINAMENTO_POKEMON e VALOR_TREINAMENTO_PERFIL armazenam valores e referências. Não há conversão entre jogos.

### C03 — Método de obtenção único não representava múltiplos caminhos
**Severidade:** crítica.

Um campo de texto em DADOS_FORMA_JOGO só permitia um método por forma/contexto.

**Correção v3:** METODO_OBTENCAO e OBTENCAO_FORMA_JOGO permitem vários métodos, condições e fontes. O exemplar guarda seu método original.

### C04 — Elegibilidade da forma era confundida com legalidade individual
**Severidade:** crítica.

A relação forma-regulamento não valida movimentos, itens, marca, origem, evento, nível e outras condições do exemplar.

**Correção v3:** ELEGIBILIDADE_REGULAMENTO informa apenas a elegibilidade catalogada da forma. Não pode afirmar “100% legal”.

### C05 — Perfil e regulamento estavam semanticamente próximos
**Severidade:** crítica.

Regulamento estabelece restrições. Perfil define objetivo/faixas de comparação. Um regulamento não determina uma única distribuição ideal.

**Correção v3:** PERFIL_ANALISE e REGULAMENTO são entidades separadas. Perfis de referência precisam de fonte e versão.

### C06 — Booleanos não representavam desconhecimento
**Severidade:** crítica.

A documentação dizia que booleanos poderiam ficar indefinidos sem detalhar como diferenciar “não usa” de “não sei”.

**Correção v3:** status controlados USA, NAO_USA e NAO_VERIFICADO.

### C07 — A espécie fixa no exemplar quebrava a evolução
**Severidade:** crítica.

O modelo anterior guardava id_especie diretamente em POKEMON_COLECAO. Um indivíduo que evolui de Bulbasaur para Ivysaur e Venusaur continuaria com a espécie inicial no registro global, criando conflito entre identidade e forma atual.

**Correção v3:** POKEMON_COLECAO identifica o indivíduo e guarda opcionalmente sua forma de origem. POKEMON_ESTADO_JOGO guarda a forma atual. A espécie atual é derivada da forma daquele estado.

### C08 — A tela de detalhes prometia evolução sem entidade de evolução
**Severidade:** alta.

O wireframe tinha seção/aba de evolução, mas o DER só possuía TRANSFORMACAO_FORMA. Evolução permanente e transformação temporária não são o mesmo relacionamento.

**Correção v3:** EVOLUCAO_FORMA_JOGO registra origem, destino, método e condição por jogo. TRANSFORMACAO_FORMA permanece para estados temporários/de batalha.

## 4. Achados de alta severidade

### A01 — Presença, obtenibilidade e registrabilidade misturadas
Foram separadas em status de presença, métodos de obtenção e registrabilidade independente/apenas por transformação.

### A02 — Relação de tipos não tinha slot
DADOS_FORMA_TIPO armazena tipo primário/secundário e o limite de dois.

### A03 — Habilidade sem garantia de contexto
A habilidade selecionada deve pertencer à mesma forma/mecânica do estado, com FK composta ou validação equivalente.

### A04 — Transformação sem compatibilidade
Origem e destino precisam pertencer ao mesmo contexto de mecânicas, salvo exceção oficial documentada.

### A05 — Comparador sem algoritmo
“Pontos positivos” e “melhorias” não tinham faixa desejada, prioridade, campos obrigatórios ou comportamento com dados ausentes. A v3 define comparação campo a campo, com faixas, preferências e explicações. Nota global só existe com fórmula e testes.

### A06 — IV alto implicitamente tratado como sempre melhor
Alguns objetivos podem preferir IV baixo em atributos específicos. O perfil define o objetivo; o analisador não presume maximização universal.

### A07 — Formas e estados de batalha sem distinção
A v3 classifica formas e registra se uma forma é independente ou apenas transformação. Shiny é característica visual do exemplar por padrão.

### A08 — Jogo, mecânica e regulamento não estavam operacionalmente definidos
JOGO é título/edição; MECANICA_JOGO é conjunto de regras de atributos/treinamento; REGULAMENTO é regra de uma competição/período.

### A09 — “Pokédex completa” sem critério mensurável
Não existia lista de referência, versão, política de formas nem relatório de cobertura. A v3 exige fonte versionada e relatório de importação antes de declarar completude.

## 5. Achados de média severidade

- Ausência de estados vazio, carregamento, erro e dados insuficientes no wireframe.
- Coleção não enfatizava múltiplos exemplares da mesma espécie.
- Cadastro não separava origem, método e estado em jogo.
- Filtros da Pokédex misturavam catálogo e contexto.
- Detalhes misturavam forma, evolução e transformação.
- Política de fonte/licença de dados secundários era insuficiente.
- Segurança não especificava FK, transações, SQL parametrizado e autorização por proprietário.
- Responsividade não estava especificada.

## 6. Riscos de segurança e integridade

1. Consultas privadas filtram pelo usuário da sessão, não por ID enviado pelo cliente.
2. Senhas nunca ficam em texto puro.
3. SQL parametrizado.
4. Atualização/exclusão validam proprietário.
5. Formulários autenticados têm proteção CSRF.
6. Limites são validados no backend.
7. Chaves estrangeiras SQLite são ativadas em toda conexão.
8. Ausência de dado não vira zero, permitido ou proibido.
9. Fonte e data de verificação são preservadas.
10. Erros não revelam hash ou dados privados.

## 7. Auditoria das oito telas

A especificação corrigida está em [wireframes.md](../design/wireframes.md). O resumo:
- Entrar: validação, sessão expirada e erros.
- Criar conta: política de senha, e-mail único e feedback.
- Pokédex: filtros globais separados de disponibilidade e tipo por jogo.
- Detalhes: espécie, forma, evolução e transformação em seções distintas.
- Coleção: cada item é exemplar individual; um exemplar evolui sem virar outro.
- Adicionar: dividir exemplar/origem e estado em jogo.
- Analisador: selecionar estado, perfil e regulamento separadamente.
- Perfil: nome, objetivo, contexto, faixas e preferências.

**Limitação visual:** a cota Figma Starter bloqueou novas leituras. A auditoria das telas é funcional/documental. Espaçamento, sobreposição, alinhamento e tipografia ainda precisam de inspeção visual. Os frames não foram declarados corrigidos.

## 8. Decisões corretivas v3

- Separar exemplar e estado por jogo.
- A espécie atual vem do estado, não do registro global do exemplar.
- Guardar forma de origem separadamente.
- Modelar evolução permanente e transformação temporária em entidades distintas.
- Modelar treinamento por mecânica.
- Separar obtenibilidade, presença e registrabilidade.
- Normalizar tipos por slot e habilidade por contexto.
- Separar perfil de regulamento.
- Limitar alegações de elegibilidade.
- Registrar fontes e datas.
- Implementar primeiro cálculo validado para Scarlet/Violet.

## 9. Verificação de normalização do treinamento

Na checagem final da própria proposta v3, foi identificada uma duplicação potencial: armazenar limites IV/EV em MECANICA_JOGO e repetir limites individuais/agregados em ATRIBUTO_TREINAMENTO criaria fontes de verdade concorrentes. Essa duplicação foi removida antes da publicação da revisão.

- Limites individuais, unidade, tipo numérico e incremento ficam em ATRIBUTO_TREINAMENTO.
- Limites agregados ficam uma única vez em GRUPO_LIMITE_TREINAMENTO.
- Cada atributo pode referenciar um grupo da mesma mecânica.
- O serviço valida a soma do grupo dentro de uma transação.

## 10. O que não foi alterado nem alegado

- Não existe backend implementado.
- Não existe frontend implementado.
- Não existe SQLite físico.
- Não existem testes executáveis.
- O DER visual do brModelo não foi atualizado.
- Os frames do Figma não foram modificados.
- A importação completa do catálogo não foi executada.

A matriz com cenários concretos para catálogo, contexto de jogo, coleção, evolução, análise, regulamentos, segurança e importação está em [casos-de-teste.md](../testes/casos-de-teste.md). Esses cenários ainda não foram executados; são especificações para a futura implementação.

## 10. Portões antes do código

- [ ] Aprovar separação exemplar/estado por jogo.
- [ ] Conferir DER v3 no brModelo.
- [ ] Definir chaves/restrições no modelo lógico.
- [ ] Criar casos de teste para cada regra de negócio.
- [ ] Escolher e documentar fontes/licenças de dados.
- [ ] Atualizar e inspecionar visualmente wireframes.
- [ ] Aprovar escopo inicial dos jogos e cálculos.
