# Auditoria técnica completa — PokéAnalyzer

**Auditoria:** 1.0 | **Data:** 04/11/2026 | **Base:** branch `audit/architecture-v3`

## 1. Veredito executivo

O PokéAnalyzer tem uma ideia consistente e algumas decisões corretas: separar espécie de forma, catálogo global de dados por jogo, coleção por usuário e regulamento de elegibilidade. Porém, a documentação 2.0 ainda promete mais do que o modelo consegue representar.

**O projeto não está pronto para implementação.** A árvore atual do GitHub contém documentação; não foram encontrados código Flask, frontend, banco SQLite, scripts de criação, dados importados, testes automatizados ou arquivo nativo de modelagem. O Figma contém oito wireframes, não uma aplicação funcional.

A versão 2.0 deve ser tratada como rascunho histórico. A versão 3.0 proposta corrige as principais inconsistências antes do modelo lógico.

## 2. Achados por severidade

| ID | Severidade | Área | Achado |
|---|---|---|---|
| A01 | Crítica | Estado do projeto | Não há software, banco físico, importador ou testes no repositório. |
| A02 | Crítica | Escopo | “Todas as formas oficiais” não possui critério de inclusão, identificador estável nem processo de verificação. |
| A03 | Crítica | Treinamento | Champions está no escopo, mas o banco só representa IV e EV em colunas fixas. |
| A04 | Crítica | Coleção | O modelo não define adequadamente jogo atual, jogo de origem e mudanças de contexto. |
| A05 | Alta | Disponibilidade | Presença, transferência, obtenção e registro independente estão misturados. |
| A06 | Alta | Dados por jogo | A ficha da forma está ligada à versão da mecânica, o que pode duplicar dados estáveis a cada revisão de regra. |
| A07 | Alta | Tipos | A relação N:N não registra tipo primário/secundário nem impede três tipos. |
| A08 | Alta | Habilidades | A compatibilidade entre exemplar, habilidade, forma e jogo não está garantida. |
| A09 | Alta | Regulamentos | “Legalidade” promete mais do que uma checagem de espécie/forma pode provar. |
| A10 | Alta | Perfis | Perfil de estratégia, perfil personalizado e regulamento estão acoplados. |
| A11 | Alta | Obtenção | Uma string em DADOS_FORMA_JOGO não representa vários métodos possíveis. |
| A12 | Média | Proveniência | Fonte e data de revisão não são obrigatórias em todos os dados mutáveis. |
| A13 | Média | Formas | Forma permanente, variação cosmética e transformação temporária não estão bem separadas. |
| A14 | Média | Interface | Os wireframes não especificam todos os estados nem todo o fluxo de manutenção da coleção. |
| A15 | Média | Segurança | Hash e isolamento são citados, mas sessão, autorização por registro, CSRF e validação ainda não viraram critérios completos. |
| A16 | Média | Acessibilidade | Não há critérios verificáveis de teclado, contraste, foco, rótulos ou responsividade. |
| A17 | Alta | Análise | O projeto promete pontos positivos e sugestões, mas não define a regra exata de comparação nem o significado de uma nota. |

## 3. Crítica detalhada

### A01 — Documentação não é implementação

O README informa que as tecnologias ainda são planejadas. Não há código executável para revisar, testar ou corrigir. A presença de entidades e wireframes não deve ser confundida com um sistema parcialmente implementado.

**Correção:** distinguir no status do projeto documentação, protótipo, software e testes. Não declarar nenhum formulário como funcional enquanto backend, validação e persistência não existirem.

### A02 — Catálogo completo sem definição de “forma”

A Pokédex oficial consultada apresenta a faixa nacional 1–1025 na data desta auditoria. Isso não equivale a um inventário único de todas as formas alternativas. É preciso decidir como o projeto tratará variações de gênero, região, estação, cosméticas, fusões e estados de batalha.

**Correção:** ESPECIE representa a entrada nacional; FORMA representa uma variação documentada com código estável, categoria, fonte e data. Toda espécie deve ter uma forma padrão. A contagem deve ser versionada por importação, nunca fixada no código. Fonte: https://www.pokemon.com/br/pokedex

### A03 — Champions não cabe em colunas IV/EV

O modelo 2.0 armazena seis IVs e seis EVs diretamente em POKEMON_COLECAO. Isso só representa jogos que usam esses sistemas. A documentação oficial de Champions descreve recrutamento próprio, visitantes vindos do Pokémon HOME e treinamento com Pontos de Vitória. Também informa que o treinamento feito em Champions não é levado de volta ao HOME e que a mudança de forma de um visitante pode apagar o treinamento anterior. Fontes: https://champions.pokemon.com/pt-br/pokemon/ e https://champions.pokemon.com/pt-br/gameplay/

**Correção:** separar o exemplar de seus valores de atributo. Cada valor deve apontar para um sistema de valores de atributo, atributo e versão da mecânica. IV, EV e treinamento próprio de Champions são sistemas diferentes, sem conversão automática. A fonte confirma o uso de PV, mas não autoriza inventar uma escala numérica de atributo: enquanto essa escala não estiver documentada, ela fica não verificada.

### A04 — Exemplar não é ficha de catálogo

DADOS_FORMA_JOGO descreve uma forma dentro de um jogo; POKEMON_COLECAO descreve um exemplar individual. Um usuário pode ter vários exemplares idênticos com valores diferentes e ter obtido um deles num jogo e estar usando em outro.

**Correção:** um exemplar tem contexto atual, jogo de origem e método real de obtenção separados. O MVP guarda um contexto atual por exemplar; histórico completo de transferências fica fora do escopo inicial.

### A05 — Disponibilidade, obtenção e elegibilidade são dimensões diferentes

Uma forma pode aparecer nativamente, ser transferível, estar ausente ou não verificada. Pode ter vários métodos de obtenção. Pode não ser registrável independentemente. Pode ser permitida ou proibida em um regulamento específico. Um único campo não representa isso.

**Correção:** status de presença fica em DADOS_FORMA_JOGO; métodos possíveis ficam em uma associação; o método realmente usado fica no exemplar; elegibilidade fica ligada ao regulamento.

### A06 — Dados de jogo e versões de regras não devem ser a mesma coisa

DADOS_FORMA_JOGO ligado a MECANICA_JOGO pode duplicar tipos, habilidades, medidas e atributos-base sempre que uma versão de regra mudar.

**Correção:** DADOS_FORMA_JOGO aponta para JOGO. MECANICA_JOGO também aponta para JOGO, mas guarda versão e vigência. O analisador combina os dois e valida que são do mesmo título.

### A07 — Tipos precisam de posição

A associação simples N:N diz quais tipos aparecem, mas não qual é o primário ou secundário. Também não impede repetição ou um terceiro tipo.

**Correção:** TIPO_FORMA_JOGO registra posição 1 ou 2, com unicidade por posição e por tipo, e limite máximo de duas linhas.

### A08 — Habilidades têm contexto

A habilidade precisa estar disponível para aquela forma naquele jogo e naquele slot. Não basta existir no catálogo global.

**Correção:** a coleção aponta para HABILIDADE_FORMA_JOGO. O backend verifica se a habilidade selecionada pertence ao contexto atual do exemplar.

### A09 — Elegibilidade não é legalidade completa

A elegibilidade da espécie/forma não valida golpes, itens, habilidade, origem, evento, nível ou todas as demais restrições de um exemplar individual.

**Correção:** chamar a funcionalidade de **elegibilidade da espécie/forma no regulamento**. Não exibir “Pokémon legal” ou “Pokémon ilegal” como conclusão total.

### A10 — Perfil competitivo não é regulamento

O regulamento define regras e restrições. O perfil define valores e preferências de comparação. Uma distribuição recomendada não se torna oficial só por estar associada a um regulamento.

**Correção:** selecionar perfil e regulamento separadamente. Perfis de referência guardam fonte, data de revisão e aviso sobre seu caráter de referência.

### A11 — Método de obtenção precisa ser multivalorado

Uma forma pode ter captura, presente, evolução, evento, troca, transferência ou recrutamento como métodos possíveis.

**Correção:** METODO_OBTENCAO + METODO_FORMA_JOGO listam opções; POKEMON_COLECAO guarda o método realmente usado.

### A12 — Proveniência é requisito, não observação

Dados sem fonte/data de revisão não sustentam recomendações confiáveis.

**Correção:** dados de forma, mecânicas, regulamentos e perfis de referência guardam URL e data de verificação. Dados desconhecidos permanecem “não verificados”.

### A13 — Forma e transformação são diferentes

Forma regional ou sazonal pode ser uma forma catalogável. Mega Evolução e outros estados de batalha podem depender de transformação temporária.

**Correção:** classificar a forma e indicar se ela pode ser registrada independentemente em cada jogo. TRANSFORMACAO_FORMA descreve origem, destino e condição; não cria captura automática.

### A14 — Os oito wireframes não fecham o fluxo

As telas cobrem login, cadastro, Pokédex, detalhes, coleção, adição, análise e perfil. Ainda faltam estados e especificações para detalhe/edição do exemplar, confirmação de exclusão, lista de perfis, resultados vazios, campos indisponíveis e dados não verificados.

**Correção:** revisar conteúdo e navegação antes do frontend. A inspeção visual de alinhamento, sobreposição e espaçamento do Figma não foi concluída porque o MCP bloqueou novas chamadas pelo limite do plano Starter. Não declarar essa revisão visual concluída.

### A15 — Segurança precisa ser testável

Hash não basta. Cada operação da coleção precisa confirmar o proprietário na sessão. Consultas devem ser parametrizadas. Segredos não podem ir para o Git. Formulários de alteração precisam de proteção CSRF e validação no servidor.

**Correção:** escrever testes de autorização, autenticação, sessão e validação. O frontend nunca é a fronteira de segurança.

### A16 — Acessibilidade precisa ter critérios

**Correção:** rótulos de campos, foco visível, navegação por teclado, contraste, mensagens de erro associadas, ordem de tabulação e layout responsivo.

### A17 — O analisador ainda não tem uma definição objetiva de resultado

O escopo promete mostrar pontos positivos e oportunidades de melhoria, mas não define como o sistema compara valores, quando algo é considerado melhor, como trata dados ausentes nem de onde viria uma pontuação geral. Um IV acima do alvo pode ser indesejado em uma configuração específica; logo, “maior” não significa automaticamente “melhor”.

**Correção:** a primeira versão não atribui uma nota global. Ela compara atributo por atributo contra um alvo explícito do perfil: igual ao alvo, abaixo, acima ou sem dado comparável. Natureza e habilidade são verificações categóricas de compatibilidade/preferência. O texto não chama algo de positivo ou negativo sem regra explicável. Uma métrica agregada só poderá ser adicionada com fórmula, pesos e validação documentados.

## 4. Correções estruturais adotadas na versão 3.0

1. DADOS_FORMA_JOGO passa a depender de FORMA + JOGO, não de uma versão de mecânica.
2. MECANICA_JOGO permanece versionada por jogo.
3. Tipos passam por TIPO_FORMA_JOGO com posição primária/secundária.
4. Métodos possíveis passam por METODO_FORMA_JOGO.
5. Jogo atual, jogo de origem e método real ficam separados.
6. Valores de treinamento passam a ser genéricos por sistema, atributo e mecânica.
7. Perfil de análise fica separado de regulamento.
8. Elegibilidade fica explicitamente limitada à espécie/forma.
9. Fonte e data de verificação passam a ser parte do modelo.
10. Formas temporárias não são tratadas como captura automática.

A referência completa é [modelo conceitual 3.0](banco-de-dados/modelo-conceitual-v3.md).

## 5. Escopo recomendado

### Núcleo do primeiro produto
- Autenticação e coleção privada.
- Catálogo de espécies/formas com critérios e fontes.
- Pesquisa e filtros.
- Detalhe de forma por jogo.
- CRUD de exemplares.
- Perfis personalizados.
- Analisador IV/EV/natureza para Scarlet/Violet.
- Elegibilidade de espécie/forma quando houver regulamento verificado.
- Estados vazios, erros e validações.

### Extensões condicionadas à documentação
- Champions: contexto de visitante/recrutado e sistema de valores separado, sem conversão. Cálculo numérico só quando escala e limites forem comprovados.
- Legends: Z-A: dados e regras próprios, sem herdar fórmulas de Scarlet/Violet.
- Outros títulos: novos registros de jogo, dados e mecânicas verificados.

### Fora do primeiro produto
Legalidade completa de cada exemplar, simulador/cálculo de dano, movesets e itens completos, gerenciamento de equipes, sincronização com HOME, leitura de save e histórico completo de transferências.

## 6. Matriz mínima de testes

| Caso | Resultado esperado |
|---|---|
| Usuário A abre exemplar de B | Acesso negado. |
| Dois exemplares da mesma forma | Dois registros independentes. |
| Origem diferente do contexto atual | Campos distintos. |
| Forma sem disponibilidade confirmada | Não inventar presença. |
| Forma com dois tipos | Posições 1 e 2; sem terceiro tipo. |
| Habilidade de outro contexto | Rejeitar. |
| Mecânica sem IV/EV | Não exibir nem exigir esses campos. |
| Valor excede limite documentado | Rejeitar. |
| Limite desconhecido | Não calcular. |
| Perfil de outro jogo | Rejeitar. |
| Perfil personalizado sem proprietário | Rejeitar. |
| Elegibilidade não verificada | Mostrar não verificado, nunca proibido. |
| Transformação temporária | Não criar exemplar independente. |
| Busca sem resultados | Estado vazio e limpeza de filtros. |
| Dado sem fonte | Não apresentar como confirmado. |
| IV real maior que valor-alvo | Mostrar “acima do alvo”; não presumir melhor ou pior. |
| Valor necessário não informado | Mostrar “sem dados”; não classificar como incompatível. |
| Perfil não define um atributo | Não comparar esse atributo. |

## 7. Ordem de execução

1. Aprovar critérios do catálogo e modelo v3.
2. Completar e conferir o DER no Figma/FigJam.
3. Criar modelo lógico e dicionário de dados.
4. Revisar normalização e restrições.
5. Criar SQLite e testes de integridade.
6. Implementar domínio, DAO e serviços.
7. Implementar autenticação e CRUD.
8. Integrar frontend.
9. Importar dados com fonte.
10. Habilitar análises somente para contextos confirmados.

## 8. Limitações desta auditoria

A árvore completa do repositório foi inspecionada. Como não havia código ou banco físico, não foi possível executar análise estática, consultas ou testes de vulnerabilidade. A inspeção visual detalhada do Figma também foi bloqueada pelo limite do plano. As conclusões são sobre os documentos e as funcionalidades especificadas, não bugs de código inexistente.
