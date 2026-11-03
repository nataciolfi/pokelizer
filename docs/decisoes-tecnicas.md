# Decisões técnicas do PokéAnalyzer

## DT01 — Python e Flask
Usar Python e Flask para o backend. A sintaxe facilita explicar rotas, classes, métodos e acesso ao banco.

## DT02 — SQLite
Usar SQLite no desenvolvimento escolar, sem exigir um servidor separado.

## DT03 — HTML, CSS e JavaScript
Usar tecnologias web fundamentais para manter o frontend fácil de compreender e apresentar.

## DT04 — Catálogo global separado dos dados por jogo
ESPECIE e FORMA representam o catálogo global. DADOS_FORMA_JOGO guarda estatísticas, tipos, habilidades e disponibilidade por contexto.

## DT05 — Mecânicas versionadas
JOGO e MECANICA_JOGO identificam o título e a versão de regras. Validações devem consultar o contexto correto.

## DT06 — Scarlet/Violet como referência principal da calculadora
A primeira calculadora de IV, EV e natureza utilizará as mecânicas da Geração IX de Pokémon Scarlet/Violet.

## DT07 — Champions separado
Pokémon Champions possui recrutamento, transferência por Pokémon HOME e treinamento com Pontos de Vitória. O projeto não converterá esse treinamento em IV/EV de Scarlet/Violet sem equivalência oficial confirmada.

## DT08 — Regulamentos versionados
REGULAMENTO terá código, formato, temporada, período e fonte. ELEGIBILIDADE_REGULAMENTO registra status, condição, fonte e data.

## DT09 — Análise explicável
O comparador utilizará regras e cálculos verificáveis, sem depender de inteligência artificial.

## DT10 — Nulo não é zero
Campos de IV/EV não aplicáveis ou não informados permanecem nulos.

## DT11 — Coleção em vez de captura
POKEMON_COLECAO representa capturas, transferências e recrutamentos.

## DT12 — Transformações separadas
TRANSFORMACAO_FORMA relaciona formas de origem e destino, sem criar capturas independentes automaticamente.

## DT13 — Fontes rastreáveis
Dados de formas, jogos e regulamentos devem registrar origem e data/versão.

## DT14 — Segurança
Senhas serão armazenadas com hash seguro e toda operação de coleção verificará o usuário proprietário.

## DT15 — Sem histórico de relatórios na primeira versão
A análise será calculada sob demanda. O histórico fica para uma versão futura.
