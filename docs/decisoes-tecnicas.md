# Decisões técnicas iniciais

Este documento registra decisões de planejamento. Elas poderão ser revisadas antes da implementação, mas mudanças devem ser justificadas.

## DT01 — Backend em Python com Flask

**Decisão:** usar Python e Flask para o backend.

**Motivo:** a sintaxe é acessível para iniciantes e permite demonstrar rotas, classes, métodos e operações com o banco.

## DT02 — SQLite como banco inicial

**Decisão:** usar SQLite durante o desenvolvimento e a apresentação escolar.

**Motivo:** não exige servidor de banco separado e permite trabalhar com SQL e relacionamentos.

## DT03 — HTML, CSS e JavaScript no frontend

**Decisão:** construir a interface com tecnologias web fundamentais.

**Motivo:** facilita demonstrar a disciplina de Desenvolvimento de Websites sem introduzir um framework frontend adicional.

## DT04 — Catálogo separado de coleção

**Decisão:** separar ESPECIE/FORMA dos registros POKEMON_CAPTURADO.

**Motivo:** os dados gerais de uma espécie são compartilhados por todos os usuários; dados de captura pertencem a cada usuário.

## DT05 — Perfil competitivo separado de perfil personalizado

**Decisão:** usar PERFIL_ANALISE com tipo de perfil e proprietário opcional.

**Motivo:** perfis mantidos pelo sistema e perfis criados por usuários compartilham uma estrutura de comparação, mas têm regras de propriedade diferentes.

## DT06 — Regulamento versionado

**Decisão:** manter REGULAMENTO como entidade própria, com jogo, formato, temporada, período e fonte oficial.

**Motivo:** as regras competitivas podem mudar. O programa não deve presumir que um regulamento antigo continua vigente.

## DT07 — Análise baseada em regras explícitas

**Decisão:** o comparador usará condições e cálculos compreensíveis, com resultados explicáveis.

**Motivo:** é importante que o aluno consiga explicar por que uma recomendação foi feita. O projeto não depende de inteligência artificial.

## DT08 — Valores de IV e EV em atributos separados na primeira versão

**Decisão:** armazenar os seis valores de IV e os seis valores de EV como atributos do registro de captura e do perfil.

**Motivo:** simplificar o modelo conceitual e facilitar a explicação. A normalização será reavaliada no modelo lógico.

## DT09 — Formas como registros distintos de catálogo

**Decisão:** cada forma tem seu próprio identificador e pertence a uma espécie.

**Motivo:** formas regionais e formas que alteram atributos ou tipos precisam ser diferenciadas. Variações cosméticas não devem causar duplicação desnecessária de estatísticas.

## DT10 — Dados oficiais com rastreabilidade

**Decisão:** dados de catálogo e regulamentos devem registrar fonte, versão ou data de atualização.

**Motivo:** evitar informações desatualizadas e permitir conferir a origem dos dados.

## DT11 — Segurança de contas

**Decisão:** senhas devem ser armazenadas com hash seguro e operações de coleção devem verificar o usuário autenticado.

**Motivo:** impedir exposição de senha e acesso à coleção de outra pessoa.

## DT12 — Sem persistência de relatórios na primeira versão

**Decisão:** calcular a análise quando o usuário solicitar, sem criar uma entidade de histórico inicialmente.

**Motivo:** manter o escopo reduzido. O histórico poderá ser adicionado posteriormente se houver necessidade.

## DT13 — Fontes oficiais e regras separadas por contexto

**Decisão:** usar fontes oficiais para dados de catálogo e regulamentos. Separar mecânicas do jogo/geração, regulamento competitivo e perfil estratégico.

**Motivo:** a Pokédex completa não é a mesma coisa que a lista de Pokémon permitidos em um campeonato. A elegibilidade muda por regulamento, e perfis estratégicos do projeto não são builds obrigatórias oficiais.

**Registro de referência:** consultar [fontes oficiais e referência de regras](fontes-oficiais.md). A documentação registra que o Regulation Set M-C de Pokémon Champions foi anunciado com vigência de 9 de setembro a 2 de dezembro de 2026 (UTC). Essa informação deve ser atualizada quando o projeto for implementado ou apresentado após o período.
