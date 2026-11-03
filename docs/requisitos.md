# Requisitos do PokéAnalyzer

## 1. Requisitos funcionais

| ID | Requisito |
|---|---|
| RF01 | O sistema deve permitir criar uma conta de usuário. |
| RF02 | O sistema deve permitir autenticar e encerrar uma sessão. |
| RF03 | O sistema deve armazenar senhas de forma segura, usando hash apropriado; nunca em texto puro. |
| RF04 | O usuário deve conseguir consultar a Pokédex Nacional. |
| RF05 | O usuário deve conseguir pesquisar Pokémon por nome e número nacional. |
| RF06 | O usuário deve conseguir filtrar Pokémon por tipo e geração. |
| RF07 | O sistema deve exibir espécies, formas, tipos, habilidades e atributos-base cadastrados. |
| RF08 | O usuário autenticado deve cadastrar um Pokémon em sua coleção. |
| RF09 | O usuário deve informar apelido opcional, nível, forma, natureza, habilidade, IVs e EVs. |
| RF10 | O usuário deve consultar, editar e excluir apenas os registros de sua própria coleção. |
| RF11 | O usuário deve conseguir selecionar um perfil competitivo de referência. |
| RF12 | O usuário deve conseguir criar, editar e excluir seus perfis personalizados. |
| RF13 | O sistema deve comparar os dados do Pokémon com o perfil escolhido. |
| RF14 | O sistema deve apresentar pontos adequados, divergências e sugestões de melhoria. |
| RF15 | O sistema deve identificar o jogo, formato, temporada e fonte do regulamento competitivo usado. |
| RF16 | O sistema deve verificar a elegibilidade de espécies/formas quando houver dados oficiais suficientes para o regulamento selecionado. |
| RF17 | O sistema deve comparar a habilidade selecionada com as habilidades recomendadas pelo perfil, quando o perfil especificar recomendações. |

## 2. Requisitos não funcionais

| ID | Requisito |
|---|---|
| RNF01 | A interface deve ser simples e adequada a usuários iniciantes. |
| RNF02 | O código deve privilegiar legibilidade e facilidade de explicação acadêmica. |
| RNF03 | O banco deve garantir integridade referencial entre entidades relacionadas. |
| RNF04 | Dados privados da coleção devem ser isolados por usuário. |
| RNF05 | Senhas nunca devem ser armazenadas em texto puro. |
| RNF06 | Entradas numéricas devem ser validadas antes de salvar. |
| RNF07 | A análise deve explicar as regras que produziram cada recomendação. |
| RNF08 | Os dados de catálogo e regulamentos devem registrar sua fonte e versão. |
| RNF09 | O projeto deve poder ser executado localmente durante o desenvolvimento. |
| RNF10 | A estrutura deve permitir atualizar o catálogo e os regulamentos sem reescrever as regras centrais do sistema. |

## 3. Validações de domínio previstas

Os limites exatos devem ser implementados de acordo com o jogo e a geração selecionados. Como referência para jogos principais modernos:

- IV: valor inteiro entre 0 e 31.
- EV: valor inteiro não negativo, com limites por atributo e limite total definidos pelas regras do jogo escolhido.
- Nível: valor inteiro válido para o jogo selecionado.
- Natureza e habilidade: devem existir no catálogo e ser compatíveis com a forma cadastrada.
- A forma cadastrada na coleção deve permitir captura direta; transformações temporárias de batalha não são capturas independentes.
- A soma e a distribuição de EVs devem ser verificadas conforme as regras aplicáveis, não apenas por uma regra genérica se houver diferenças entre títulos.

## 4. Critérios de aceitação iniciais

- Um usuário consegue criar conta e entrar.
- Um usuário não consegue visualizar ou alterar a coleção de outro usuário.
- Uma espécie pode possuir mais de uma forma.
- Uma forma pode possuir um ou dois tipos.
- Formas marcadas como não capturáveis diretamente não podem ser cadastradas como capturas independentes.
- Perfis podem recomendar habilidades; quando não houver recomendação, a habilidade não será julgada como inadequada por esse critério.
- Um Pokémon capturado não pode receber IVs fora do intervalo permitido.
- O analisador identifica o perfil selecionado e apresenta uma explicação para cada recomendação.
- Um perfil personalizado pertence ao usuário que o criou.
- Um perfil competitivo informa a referência de jogo/formato/regulamento utilizada.
