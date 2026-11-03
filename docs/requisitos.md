# Requisitos do PokéAnalyzer

## Requisitos funcionais

| ID | Requisito |
|---|---|
| RF01 | Permitir criar conta de usuário. |
| RF02 | Permitir autenticar e encerrar sessão. |
| RF03 | Armazenar senhas em hash seguro, nunca em texto puro. |
| RF04 | Consultar o catálogo nacional de espécies. |
| RF05 | Pesquisar por número nacional e nome. |
| RF06 | Filtrar por tipo e geração. |
| RF07 | Exibir formas oficiais e suas espécies. |
| RF08 | Exibir dados de uma forma em um jogo específico. |
| RF09 | Registrar Pokémon na coleção de um usuário. |
| RF10 | Informar jogo/contexto e método de obtenção. |
| RF11 | Informar nível, natureza, habilidade, IVs e EVs quando aplicáveis. |
| RF12 | Consultar, editar e excluir somente registros da própria coleção. |
| RF13 | Selecionar perfis competitivos de referência. |
| RF14 | Criar, editar e excluir perfis personalizados. |
| RF15 | Comparar Pokémon com perfil compatível de forma e mecânicas. |
| RF16 | Apresentar pontos positivos, divergências e sugestões explicáveis. |
| RF17 | Consultar elegibilidade da forma no regulamento selecionado. |
| RF18 | Exibir fonte e data de verificação de regras e elegibilidade. |
| RF19 | Representar transformações sem tratá-las automaticamente como capturas. |
| RF20 | Ocultar ou desabilitar campos de IV/EV quando não forem aplicáveis ou confirmados. |

## Requisitos não funcionais

| ID | Requisito |
|---|---|
| RNF01 | Interface simples para usuários iniciantes. |
| RNF02 | Código legível e fácil de explicar academicamente. |
| RNF03 | Integridade referencial no banco. |
| RNF04 | Coleções privadas isoladas por usuário. |
| RNF05 | Senhas nunca armazenadas em texto puro. |
| RNF06 | Entradas numéricas validadas antes de salvar. |
| RNF07 | Recomendações explicam as regras utilizadas. |
| RNF08 | Dados de catálogo e regulamentos registram fonte e data/versão. |
| RNF09 | Execução local durante o desenvolvimento. |
| RNF10 | Atualizar dados de um jogo sem alterar o catálogo global de formas. |
| RNF11 | Não converter sistemas de treinamento sem equivalência oficial documentada. |

## Validações de domínio

- IV/EV só são exigidos nos contextos que os utilizam.
- Limites vêm de MECANICA_JOGO.
- Nulo significa não informado ou não aplicável; zero é um valor real.
- Habilidade selecionada deve estar disponível para a forma e jogo.
- Só formas registráveis podem entrar diretamente na coleção.
- Uma forma pode existir no catálogo sem estar disponível em um jogo.
- Legalidade vem de ELEGIBILIDADE_REGULAMENTO.
- Ausência de um dado não prova proibição.
- Perfil personalizado deve ter proprietário.
- Perfil competitivo específico deve apontar para seu regulamento.
- A análise não pode misturar dados de jogos diferentes.

## Critérios de aceitação

- Um usuário não acessa a coleção de outro usuário.
- Uma forma regional pode ter dados diferentes da forma padrão.
- A mesma forma pode ter dados diferentes em jogos distintos.
- Uma Mega Evolução aparece no catálogo sem ser tratada como captura independente.
- Um Pokémon de Champions pode ser registrado sem inventar IV/EV.
- Uma espécie não elegível continua visível na Pokédex.
- O analisador diferencia permitido, proibido, condicional e não verificado.
- Toda recomendação identifica o perfil, jogo e regulamento utilizados.
