# Requisitos do PokéAnalyzer

**Versão:** 3.0  
**Status:** requisitos revisados; implementação ainda não iniciada.

## 1. Requisitos funcionais

| ID | Requisito |
|---|---|
| RF01 | Permitir criar conta de usuário com validação dos campos. |
| RF02 | Permitir autenticar, encerrar sessão e impedir acesso à área privada sem autenticação. |
| RF03 | Armazenar senhas somente em hash seguro. |
| RF04 | Consultar o catálogo global de espécies e formas. |
| RF05 | Pesquisar por número nacional, nome e identificador da forma. |
| RF06 | Filtrar por tipo, geração, categoria de forma e jogo sem confundir filtros globais e específicos. |
| RF07 | Exibir formas oficiais catalogadas e indicar a fonte dos dados. |
| RF08 | Exibir atributos, tipos, habilidades e disponibilidade em contexto de jogo. |
| RF09 | Diferenciar presença, obtenibilidade, registrabilidade e elegibilidade. |
| RF10 | Permitir registrar vários exemplares individuais, inclusive da mesma espécie. |
| RF11 | Registrar forma de origem, jogo de origem e método de obtenção separadamente do estado atual. |
| RF12 | Registrar estados de um exemplar em contextos de jogo diferentes, sem misturar treinamentos. |
| RF13 | Exibir somente atributos de treinamento definidos para as mecânicas selecionadas. |
| RF14 | Consultar, editar e excluir somente exemplares/estados pertencentes ao usuário autenticado. |
| RF15 | Criar, editar e excluir perfis personalizados pertencentes ao usuário. |
| RF16 | Consultar perfis de referência com fonte, versão e contexto identificados. |
| RF17 | Exigir compatibilidade de forma, jogo, mecânica e perfil antes da análise. |
| RF18 | Comparar atributos por campo e explicar divergências e preferências. |
| RF19 | Diferenciar zero, valor não informado e atributo não aplicável. |
| RF20 | Consultar elegibilidade da forma em regulamento específico. |
| RF21 | Exibir status, condição, fonte e data de verificação. |
| RF22 | Exibir não verificado quando a fonte for insuficiente; ausência não significa proibição. |
| RF23 | Representar transformações sem criar automaticamente novo exemplar. |
| RF24 | Registrar múltiplos métodos de obtenção possíveis por forma/contexto. |
| RF25 | Exibir mensagens de carregamento, vazio, erro e ausência de dados. |
| RF26 | Permitir consultar fonte e versão dos dados usados na análise. |
| RF27 | Consultar relações evolutivas, métodos e condições no contexto de jogo selecionado. |
| RF28 | Atualizar a forma atual do estado do mesmo exemplar quando ele evoluir, sem duplicar o indivíduo. |

## 2. Requisitos não funcionais

| ID | Requisito |
|---|---|
| RNF01 | Interface compreensível para iniciantes. |
| RNF02 | Código legível, modular e explicável academicamente. |
| RNF03 | Integridade referencial no banco. |
| RNF04 | Coleções e perfis isolados por usuário. |
| RNF05 | Senhas nunca armazenadas em texto puro. |
| RNF06 | Entradas numéricas validadas no backend. |
| RNF07 | Consultas SQL parametrizadas. |
| RNF08 | Rotas de alteração aplicam autorização por proprietário. |
| RNF09 | Interface responsiva em desktop e mobile. |
| RNF10 | Dados e regulamentos registram fonte, versão e data de verificação. |
| RNF11 | Regras de um jogo não são usadas silenciosamente em outro. |
| RNF12 | Ausência de fonte não vira permissão, proibição ou valor presumido. |
| RNF13 | SQLite ativa chaves estrangeiras em cada conexão. |
| RNF14 | Operações que alteram várias tabelas usam transações. |
| RNF15 | Instalação e execução local são reproduzíveis. |

## 3. Regras de domínio

- Espécie e forma são diferentes.
- Uma forma pertence a uma espécie; não recebe automaticamente outro número nacional.
- O catálogo global não representa disponibilidade em todos os jogos.
- JOGO representa título/edição; Scarlet e Violet são registros distintos.
- MECANICA_JOGO representa regras de atributos/treinamento.
- O exemplar individual não guarda uma espécie atual fixa: ela é derivada do estado por jogo.
- A forma de origem é opcional e não muda após evolução.
- Cada exemplar pertence a um usuário e pode ter vários estados por jogo.
- Cada estado tem no máximo uma forma atual por contexto de mecânicas.
- Evolução altera a forma do estado existente; não cria outro exemplar.
- Transformação temporária não é evolução.
- Método de obtenção é separado da origem e do estado atual.
- IV/EV não são campos universais.
- Perfil só compara com contexto compatível.
- Perfil personalizado tem proprietário.
- Perfil de referência identifica fonte e versão.
- Regulamento não determina sozinho uma distribuição ideal.
- Elegibilidade da forma não é validação integral de legalidade individual.
- Nulo, zero, não aplicável e desconhecido são situações distintas.
- Recomendações explicam regra e dados usados.

## 4. Critérios de aceitação

1. Dois exemplares da mesma espécie podem existir com apelidos e estados diferentes.
2. Um exemplar pode ter estados separados em Scarlet/Violet e Champions sem conversão de treinamento.
3. Jogo de origem é separado do jogo em que o exemplar está sendo analisado.
4. Bulbasaur pode evoluir no estado para Ivysaur e depois Venusaur mantendo o mesmo id_pokemon_colecao.
5. A forma de origem permanece como procedência depois da evolução.
6. Uma forma regional pode ter tipos, habilidades e atributos próprios.
7. Forma catalogada pode aparecer mesmo sem dados de disponibilidade no jogo selecionado.
8. Ausência de registro de elegibilidade gera não verificado, não proibido.
9. Perfil personalizado não precisa de regulamento.
10. Perfil de referência informa fonte, versão e contexto.
11. Natureza/habilidade incompatível não pode ser salva.
12. Limites individuais e agregados de treinamento são validados conforme mecânica.
13. Nulo não é convertido em zero.
14. Usuário A não acessa registros de usuário B alterando IDs na URL/requisição.
15. Análise com dados insuficientes explica o que falta e não produz nota enganosa.
16. Interface não chama elegibilidade da forma de legalidade completa do exemplar.
17. Evolução e transformação são apresentadas em relações distintas.

## 5. Fora dos critérios iniciais

Não é critério da primeira versão validar todos os movimentos, itens, origem integral, marca, evento, legitimidade ou requisitos individuais de torneio. Isso exigiria dados e módulo adicionais.
