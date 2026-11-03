# Decisões técnicas do PokéAnalyzer

**Versão:** 3.0

## DT01 — Python e Flask
Usar Python e Flask. Rotas pequenas chamam serviços de domínio; regras não ficam concentradas em funções HTTP.

## DT02 — SQLite
Usar SQLite no projeto escolar. Ativar PRAGMA foreign_keys = ON em toda conexão e usar transações para operações compostas.

## DT03 — HTML, CSS e JavaScript
Usar tecnologias web fundamentais e interface responsiva. O primeiro protótipo é desktop, não uma decisão de excluir mobile.

## DT04 — Catálogo global separado
ESPECIE e FORMA representam o catálogo. Dados por jogo ficam em DADOS_FORMA_JOGO. Existência no catálogo não implica disponibilidade.

## DT05 — Edição, mecânica e regulamento diferentes
JOGO identifica título/edição. MECANICA_JOGO descreve regras de atributos/treinamento. REGULAMENTO descreve regras de competição/temporada.

## DT06 — Dados de forma contextualizados
Tipos, habilidades, atributos-base, presença e registrabilidade são ligados ao contexto de jogo. Métodos de obtenção são relações múltiplas, não uma única string.

## DT07 — Exemplar e estado por jogo
POKEMON_COLECAO identifica o indivíduo e registra procedência opcional. Não armazena espécie atual fixa. POKEMON_ESTADO_JOGO armazena forma atual, nível, natureza, habilidade e treinamento daquele contexto. Forma de origem permanece como dado histórico.

## DT08 — Evolução e transformação distintas
EVOLUCAO_FORMA_JOGO representa uma mudança permanente. TRANSFORMACAO_FORMA representa mudança de estado, normalmente temporária. Evoluir atualiza o estado do mesmo exemplar; não cria outro POKEMON_COLECAO.

## DT09 — Treinamento extensível por contexto
ATRIBUTO_TREINAMENTO define valores existentes na mecânica. VALOR_TREINAMENTO_POKEMON e VALOR_TREINAMENTO_PERFIL registram valores do exemplar e referências. IV/EV não são campos universais.

## DT10 — Scarlet/Violet como primeiro contexto numérico
A primeira análise numérica será validada para Scarlet/Violet. Outros jogos só terão cálculo quando atributos, limites e fórmulas estiverem documentados.

## DT11 — Champions sem conversão
Champions possui recrutamento, visitantes via Pokémon HOME e treinamento próprio. Não converter treinamento em IV/EV de Scarlet/Violet. Cada estado mantém valores próprios.

## DT12 — Perfis não são regulamentos
PERFIL_ANALISE representa uma configuração de comparação. REGULAMENTO representa regras de competição. Um regulamento não determina automaticamente uma distribuição ideal.

## DT13 — Elegibilidade com escopo explícito
ELEGIBILIDADE_REGULAMENTO informa elegibilidade catalogada da forma. Não certifica legalidade completa do exemplar individual.

## DT14 — Análise explicável
Comparação determinística e verificável. Cada divergência aponta dado e regra. Nota global exige fórmula documentada e testes.

## DT15 — Nulo não é zero
Valor não informado, não aplicável e zero são estados distintos.

## DT16 — Fontes rastreáveis
Dados importados e regulamentos armazenam URL/referência, data de verificação e versão. Fontes de terceiros exigem avaliação de cobertura, licença e atribuição.

## DT17 — Segurança
Senhas usam hash adequado. Toda rota privada filtra pelo usuário autenticado. SQL parametrizado, CSRF em formulários de sessão e validação no servidor.

## DT18 — Implementação em fases
Primeiro implementar login, catálogo, coleção, estados por jogo e análise Scarlet/Violet. Outros jogos não recebem cálculo até que regras/dados estejam verificados.

## DT19 — Histórico de estados e análises
Histórico completo fica fora da primeira entrega. Por exemplar + mecânica há um estado atual. Evolução atualiza esse estado; no futuro, histórico poderá virar entidade própria.
