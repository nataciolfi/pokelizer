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
| RF06 | Filtrar por tipo, geração, categoria de forma e jogo sem confundir filtros globais com filtros específicos. |
| RF07 | Exibir as formas oficiais catalogadas e indicar a fonte dos dados. |
| RF08 | Exibir atributos, tipos, habilidades e disponibilidade em contexto de jogo selecionado. |
| RF09 | Diferenciar presença no jogo, obtenibilidade e elegibilidade competitiva. |
| RF10 | Permitir registrar vários exemplares da mesma espécie na coleção do usuário. |
| RF11 | Registrar jogo de origem e método de obtenção separadamente do contexto atual. |
| RF12 | Registrar o estado de um exemplar em contextos de jogo diferentes, sem misturar dados de treinamento. |
| RF13 | Exibir somente atributos de treinamento definidos para as mecânicas selecionadas. |
| RF14 | Consultar, editar e excluir somente exemplares e estados pertencentes ao usuário autenticado. |
| RF15 | Criar, editar e excluir perfis personalizados pertencentes ao usuário. |
| RF16 | Consultar perfis estratégicos de referência com fonte, versão e contexto identificados. |
| RF17 | Exigir compatibilidade entre forma, jogo, mecânicas e perfil antes da análise. |
| RF18 | Comparar atributos por campo e explicar divergências e preferências. |
| RF19 | Diferenciar valor zero, valor não informado e atributo não aplicável. |
| RF20 | Consultar elegibilidade de forma em um regulamento específico. |
| RF21 | Exibir status de elegibilidade, condição, fonte e data de verificação. |
| RF22 | Exibir “não verificado” quando a fonte não for suficiente; ausência de registro não significa proibição. |
| RF23 | Representar transformações como relações entre formas/contextos, sem criar automaticamente um exemplar novo. |
| RF24 | Registrar múltiplos métodos de obtenção possíveis por forma e contexto. |
| RF25 | Exibir mensagens de carregamento, vazio, erro e ausência de dados. |
| RF26 | Permitir que o usuário veja a origem e a versão dos dados usados na análise. |

## 2. Requisitos não funcionais

| ID | Requisito |
|---|---|
| RNF01 | Interface compreensível para usuários iniciantes. |
| RNF02 | Código legível, modular e explicável academicamente. |
| RNF03 | Integridade referencial no banco. |
| RNF04 | Coleções e perfis privados isolados por usuário. |
| RNF05 | Senhas nunca armazenadas em texto puro. |
| RNF06 | Entradas numéricas validadas no backend. |
| RNF07 | Consultas SQL parametrizadas. |
| RNF08 | Rotas de alteração devem aplicar autorização por proprietário. |
| RNF09 | Interface responsiva em largura desktop e mobile, ainda que o primeiro wireframe seja desktop. |
| RNF10 | Dados de catálogo e regulamentos registram fonte, versão e data de verificação. |
| RNF11 | Regras de um jogo não podem ser usadas silenciosamente em outro. |
| RNF12 | Falha ou ausência de fonte não pode ser convertida em permissão, proibição ou valor numérico presumido. |
| RNF13 | Banco SQLite deve ativar chaves estrangeiras em cada conexão. |
| RNF14 | Operações que alterem várias tabelas devem usar transações. |
| RNF15 | A aplicação deve fornecer instruções reproduzíveis de instalação e execução local. |

## 3. Regras de domínio

- Espécie e forma são conceitos diferentes.
- Uma forma pertence a uma espécie; formas não recebem automaticamente um novo número nacional.
- O catálogo global não representa disponibilidade em todos os jogos.
- Presença, obtenibilidade e elegibilidade são estados diferentes.
- Um jogo representa um título/edição; Scarlet e Violet são registros separados.
- MECANICA_JOGO representa um conjunto documentado de regras de atributos e treinamento.
- Um exemplar pertence a um usuário e a uma espécie.
- O estado de um exemplar em um jogo guarda forma, nível, habilidade, natureza e treinamento daquele contexto.
- O mesmo exemplar pode possuir estados em mais de um jogo.
- Método de obtenção não pertence ao registro global de forma; uma forma pode ter vários métodos no mesmo jogo.
- Os atributos de treinamento são definidos por contexto. IV e EV não são campos universais.
- Um perfil só pode comparar com um contexto de forma/mecânicas compatível.
- Perfil personalizado deve ter proprietário.
- Perfil de referência deve identificar origem e versão; não deve ser apresentado como build oficial quando não for.
- Regulamento não define por si só uma única distribuição ideal de atributos.
- Elegibilidade da forma não é uma verificação completa da legalidade do exemplar.
- Transformações temporárias não criam capturas independentes automaticamente.
- Nulo significa desconhecido ou não aplicável conforme o estado do campo; zero é valor real.
- Toda recomendação deve explicar sua regra e seus dados de entrada.

## 4. Critérios de aceitação

1. Dois exemplares da mesma espécie podem existir na coleção com apelidos e atributos diferentes.
2. O mesmo exemplar pode ter estados separados em Scarlet/Violet e Champions sem converter valores de treinamento entre eles.
3. Um Pokémon transferido mantém seu jogo de origem separado do jogo em que está sendo analisado.
4. Uma forma regional pode ter tipos, habilidades e estatísticas diferentes da forma padrão.
5. Uma forma catalogada pode aparecer mesmo sem dados de disponibilidade no jogo selecionado.
6. Um Pokémon ausente de um regulamento continua visível na Pokédex.
7. Uma ausência de registro de elegibilidade gera “não verificado”, não “proibido”.
8. Um perfil personalizado não precisa de regulamento.
9. Um perfil de referência informa sua origem, versão e contexto.
10. Uma natureza ou habilidade incompatível com o contexto não pode ser salva.
11. A soma e os limites dos valores de treinamento são validados conforme a mecânica selecionada.
12. Nulo não é convertido em zero durante cálculos.
13. Usuário A não consegue ler, atualizar ou excluir registro de usuário B alterando o ID na URL ou requisição.
14. Análises com dados insuficientes informam quais dados faltam e não produzem uma nota enganosa.
15. A interface nunca chama a elegibilidade de forma de “legalidade completa” do exemplar.

## 5. Fora dos critérios iniciais

Não é critério da primeira versão validar movimentos, itens, origem integral, marca, evento, legitimidade ou todos os requisitos individuais de torneio. Esse recurso exigiria um módulo e dados adicionais.
