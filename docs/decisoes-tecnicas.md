# Decisões técnicas do PokéAnalyzer

**Versão:** 3.0

## DT01 — Python e Flask
Usar Python e Flask para o backend. As rotas devem ser pequenas e chamar serviços de domínio, sem concentrar regras de negócio dentro das funções HTTP.

## DT02 — SQLite
Usar SQLite no desenvolvimento escolar. Ativar PRAGMA foreign_keys = ON em toda conexão e usar transações para operações compostas.

## DT03 — HTML, CSS e JavaScript
Usar tecnologias web fundamentais. A interface deve ser responsiva; o primeiro protótipo de baixa fidelidade é desktop, não uma decisão de excluir mobile.

## DT04 — Catálogo global separado
ESPECIE e FORMA descrevem o catálogo. Os dados por jogo ficam em DADOS_FORMA_JOGO. A disponibilidade nunca é inferida apenas pela existência da forma.

## DT05 — Edição e mecânica são diferentes
JOGO identifica um título/edição. MECANICA_JOGO descreve um conjunto documentado de regras de atributos/treinamento daquele jogo. Uma temporada competitiva pertence a REGULAMENTO, não a MECANICA_JOGO.

## DT06 — Dados de forma contextualizados
Tipos, habilidades, estatísticas-base, presença, registrabilidade e métodos de obtenção serão ligados ao contexto de jogo. Uma forma pode ter vários métodos de obtenção; por isso, método não será uma única string em DADOS_FORMA_JOGO.

## DT07 — Exemplar separado do estado por jogo
POKEMON_COLECAO representa o exemplar do usuário, com espécie e origem. POKEMON_ESTADO_JOGO representa aquele exemplar em um contexto específico de jogo. O jogo de origem e o jogo em que ocorre a análise são separados.

## DT08 — Treinamento extensível por contexto
ATRIBUTO_TREINAMENTO define os valores que existem em cada contexto de mecânicas. VALOR_TREINAMENTO_POKEMON armazena o valor daquele atributo para o estado do exemplar. Assim, IV/EV são definidos no contexto que os usa, sem inventar equivalência para sistemas diferentes.

## DT09 — Scarlet/Violet como primeiro contexto numérico
A primeira análise numérica será validada para Scarlet/Violet. Outros jogos poderão ser cadastrados separadamente; só terão análise quando seus atributos, limites e fórmulas estiverem documentados.

## DT10 — Champions sem conversão
Pokémon Champions possui recrutamento, visitantes via Pokémon HOME e treinamento próprio. Treinamento de Champions não será convertido em IV/EV de Scarlet/Violet. Cada estado de jogo mantém seus valores próprios.

## DT11 — Perfis não são regulamentos
PERFIL_ANALISE representa uma configuração de comparação. REGULAMENTO representa regras de uma competição. Um regulamento pode restringir uso, mas não determina automaticamente uma única build ou distribuição ideal.

## DT12 — Elegibilidade com escopo explícito
ELEGIBILIDADE_REGULAMENTO informa a elegibilidade catalogada da espécie/forma. Não certifica a legalidade completa de um exemplar individual, pois o sistema inicial não valida todos os movimentos, itens, origens e demais condições.

## DT13 — Análise explicável
A análise será determinística e baseada em regras/cálculos verificáveis. Não usar IA para inventar notas ou recomendações. Cada divergência deve apontar o dado comparado e a regra aplicada.

## DT14 — Nulo não é zero
Valor não informado, não aplicável e zero são estados distintos. Não converter ausência de dados em número durante importação ou cálculo.

## DT15 — Fontes rastreáveis
Registros importados e regulamentos devem armazenar URL/referência, data de verificação e versão da fonte/dado. Dados de terceiros exigem avaliação de cobertura, licença e atribuição.

## DT16 — Segurança e privacidade
Senhas armazenadas com hash adequado. Toda rota de coleção e perfil filtra por usuário autenticado no backend. Usar SQL parametrizado, proteção CSRF em formulários de sessão e validação do lado do servidor.

## DT17 — Escopo de implementação
Primeiro implementar o fluxo essencial: login, catálogo, coleção, estado por jogo e analisador de Scarlet/Violet. A estrutura comporta outros contextos, mas a aplicação não deve anunciar análise numérica de um jogo antes de os dados daquele jogo serem verificados.

## DT18 — Histórico de análises
O histórico de relatórios fica fora da primeira entrega. Os dados de entrada e a versão do perfil/mecânica utilizados precisam ser identificáveis para reproduzir uma análise enquanto ela estiver aberta, mas não será armazenado relatório histórico completo.
