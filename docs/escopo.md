# Escopo do projeto

**Versão:** 3.0  
**Status:** especificação revisada; implementação ainda não iniciada.

## 1. Visão geral

O PokéAnalyzer será um website com catálogo de espécies e formas, coleção individual por usuário e analisador comparativo. O catálogo global não será confundido com os dados de um jogo, e um exemplar individual não será confundido com o estado dele em um jogo específico.

O exemplar é a identidade individual. A espécie/forma atual é derivada do estado do exemplar no contexto de jogo. Assim, um Pokémon pode evoluir e manter o mesmo registro de coleção.

## 2. Objetivos

1. Manter catálogo nacional de espécies e formas oficiais documentadas.
2. Consultar formas sem presumir disponibilidade em todos os jogos.
3. Guardar tipos, habilidades, atributos-base e métodos de obtenção por contexto de jogo.
4. Permitir contas e coleções isoladas por usuário.
5. Registrar exemplares individuais, inclusive vários da mesma espécie.
6. Separar forma/jogo de origem dos estados do exemplar em outros jogos.
7. Representar evoluções permanentes e transformações de batalha separadamente.
8. Comparar atributos com perfis personalizados ou de referência.
9. Consultar elegibilidade de espécies/formas em regulamentos versionados.
10. Identificar fonte, versão e data de verificação.
11. Exibir limitações e dados faltantes sem inventar valores.

## 3. Política de catálogo

A unidade central é a espécie. Cada espécie pode ter uma ou mais formas catalogadas. Uma forma possui identificador interno estável, nome canônico, categoria e fonte verificável.

Serão incluídas formas oficialmente documentadas como variantes de jogo, incluindo, quando aplicável, formas regionais, alternativas, sazonais, de gênero, cosméticas e de batalha. A classificação precisa ser registrada.

- Shiny é característica visual do exemplar, não espécie/forma nova por padrão.
- Estados temporários de batalha podem constar no catálogo, mas não são automaticamente exemplares independentes.
- Variações cosméticas com catálogo oficial próprio podem ser formas quando houver fonte e identificador inequívocos.
- Forma catalogada pode não possuir dados em determinado jogo.
- A contagem do catálogo fica associada à versão da fonte, não fixada no código.

“Pokédex completa” só pode ser critério de aceitação quando existir lista de referência versionada e relatório de cobertura com inclusões, exclusões e lacunas.

## 4. Contextos de jogo

### Scarlet e Violet
São registros de jogo distintos. A primeira calculadora de IV, EV e natureza será validada para a Geração IX. Limites vêm do contexto de mecânicas, não de constantes espalhadas no código.

### Pokémon Champions
Contexto próprio, com Pokémon visitantes via HOME, recrutamento dentro do jogo e treinamento próprio. O treinamento realizado em Champions não será convertido para IV/EV de outro jogo. A estrutura prevê estados separados e atributos de treinamento configuráveis.

O cálculo numérico só será habilitado quando atributos, limites, regras de persistência e fonte estiverem documentados. Até lá, o sistema poderá registrar o contexto sem apresentar análise incompleta.

### Pokémon Legends: Z-A
Contexto separado. Disponibilidade, formas, habilidades e mecânicas precisam de dados próprios. Não herdar regras de outro jogo.

### Pokémon Winds e Pokémon Waves
Anunciados para 2027. Não criar disponibilidade ou regras presumidas antes do lançamento e de fontes oficiais suficientes.

## 5. Funcionalidades da primeira versão

- Cadastro, login e encerramento de sessão.
- Pesquisa e filtros do catálogo.
- Consulta de espécie, formas, evolução e transformação por jogo.
- Coleção privada com vários exemplares da mesma espécie.
- Registro da forma/jogo de origem e método de obtenção.
- Registro de estados de um exemplar em diferentes contextos de jogo.
- Evoluir um exemplar atualizando seu estado, sem duplicar o indivíduo.
- Atributos de treinamento definidos por contexto.
- Perfis personalizados e estratégicos de referência.
- Comparação explicável e tratamento de dados ausentes.
- Consulta de elegibilidade da forma em regulamento.
- Fonte, versão e data de verificação visíveis.

## 6. O que o analisador promete

O analisador compara um estado de exemplar com um perfil compatível de mesma forma e contexto de mecânicas.

Deve validar jogo/contexto, forma, natureza, habilidade, aplicabilidade e completude dos dados. Compara cada atributo com a faixa/preferência do perfil e explica divergências. Deve diferenciar dado desconhecido de não aplicável e indicar quando uma característica pode ser alterada, se houver fonte.

Não reduzir tudo a uma nota única sem fórmula. IV alto não é automaticamente desejável. A primeira versão não é simulador, calculadora de dano nem montador completo de equipes.

## 7. Elegibilidade competitiva

A primeira versão verifica elegibilidade catalogada da espécie/forma no regulamento. Não certifica legalidade completa do exemplar. Validação individual pode depender de movimentos, itens, origem, marca, evento, nível e outras condições fora do escopo.

A interface usará “elegibilidade da forma” ou “compatibilidade com o regulamento”, nunca “Pokémon 100% legal” sem verificar todos os requisitos.

## 8. Fora do escopo inicial

- Simulador de batalhas e calculadora completa de dano.
- Montagem automática de equipes.
- Catálogo completo de golpes, itens e combinações legais.
- Verificação integral de legitimidade/origem do exemplar.
- Integração automática com saves ou Pokémon HOME.
- Marketplace, trocas e funcionalidades sociais.
- Aplicativo móvel nativo.
- Histórico detalhado de estados e relatórios.
- Importação de dados sem fonte/licença verificáveis.

## 9. Premissas técnicas

- SQLite, Python, Flask, HTML, CSS e JavaScript.
- Regras de domínio fora das rotas Flask.
- Consultas SQL parametrizadas.
- Toda operação privada valida o usuário proprietário no backend.
- Chaves estrangeiras, CHECKs, índices e transações.
- Regras agregadas são validadas no serviço e cobertas por testes.
- Dados importados têm origem, versão e data de verificação.
