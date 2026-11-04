# Relacionamentos e cardinalidades — PokéAnalyzer 3.0

Este arquivo acompanha o [modelo conceitual 3.0](modelo-conceitual-v3.md) e o [DER 3.0](DER.md). A versão 2.0 foi substituída porque misturava dados de jogo, regras, obtenção e treinamento.

| Entidade A | Relacionamento | Entidade B | Cardinalidade |
|---|---|---|---|
| ESPECIE | possui | FORMA | 1:N |
| FORMA | aparece em | DADOS_FORMA_JOGO | 1:N |
| JOGO | descreve | DADOS_FORMA_JOGO | 1:N |
| JOGO | possui versões de | MECANICA_JOGO | 1:N |
| DADOS_FORMA_JOGO | tem tipos | TIPO | N:N via TIPO_FORMA_JOGO |
| DADOS_FORMA_JOGO | disponibiliza | HABILIDADE | N:N via HABILIDADE_FORMA_JOGO |
| DADOS_FORMA_JOGO | admite métodos | METODO_OBTENCAO | N:N via METODO_FORMA_JOGO |
| USUARIO | possui | POKEMON_COLECAO | 1:N |
| DADOS_FORMA_JOGO | é o contexto atual de | POKEMON_COLECAO | 1:N |
| JOGO | é origem de | POKEMON_COLECAO | 1:N, opcional no exemplar |
| METODO_OBTENCAO | foi usado em | POKEMON_COLECAO | 1:N, opcional no exemplar |
| NATUREZA | caracteriza | POKEMON_COLECAO | 1:N, opcional |
| HABILIDADE_FORMA_JOGO | é selecionada em | POKEMON_COLECAO | 1:N, opcional |
| MECANICA_JOGO | oferece sistemas de treinamento | SISTEMA_ATRIBUTO | N:N via MECANICA_SISTEMA_ATRIBUTO |
| POKEMON_COLECAO | possui valores | VALOR_ATRIBUTO_POKEMON | 1:N |
| MECANICA_SISTEMA_ATRIBUTO | valida valores | VALOR_ATRIBUTO_POKEMON | 1:N |
| ATRIBUTO_BATALHA | recebe valor | VALOR_ATRIBUTO_POKEMON | 1:N |
| DADOS_FORMA_JOGO | é alvo de | PERFIL_ANALISE | 1:N |
| MECANICA_JOGO | é usada por | PERFIL_ANALISE | 1:N |
| USUARIO | cria | PERFIL_ANALISE | 1:N, opcional no perfil |
| REGULAMENTO | contextualiza | PERFIL_ANALISE | 1:N, opcional no perfil |
| PERFIL_ANALISE | define valores | VALOR_PERFIL_ANALISE | 1:N |
| MECANICA_SISTEMA_ATRIBUTO | define valores de perfil | VALOR_PERFIL_ANALISE | 1:N |
| ATRIBUTO_BATALHA | recebe valor-alvo | VALOR_PERFIL_ANALISE | 1:N |
| PERFIL_ANALISE | recomenda | NATUREZA | N:N via PERFIL_NATUREZA |
| PERFIL_ANALISE | recomenda | HABILIDADE_FORMA_JOGO | N:N via PERFIL_HABILIDADE |
| MECANICA_JOGO | recebe | REGULAMENTO | 1:N |
| REGULAMENTO | define elegibilidade | DADOS_FORMA_JOGO | N:N via ELEGIBILIDADE_FORMA_REGULAMENTO |
| DADOS_FORMA_JOGO (origem) | inicia | TRANSFORMACAO_FORMA | 1:N |
| DADOS_FORMA_JOGO (destino) | recebe | TRANSFORMACAO_FORMA | 1:N |

## Explicação das relações críticas

### Espécie, forma e dados por jogo
Uma espécie tem uma ou mais formas catalogadas. A forma pode aparecer em vários jogos. A ausência de uma linha de dados não remove a forma da Pokédex; significa apenas que o contexto ainda não foi documentado.

### Dados de forma e mecânicas
DADOS_FORMA_JOGO depende do jogo. MECANICA_JOGO também depende do jogo, mas representa uma versão de regras. Uma análise combina os dois registros e o backend verifica que pertencem ao mesmo jogo. Atualizar um regulamento não duplica a ficha da forma.

### Tipos
TIPO_FORMA_JOGO armazena a posição 1 ou 2. Não basta saber que uma forma é Água e Voador; a interface precisa saber a ordem de apresentação. O modelo lógico deverá impedir mais de dois tipos.

### Habilidades
HABILIDADE_FORMA_JOGO guarda opções disponíveis para aquela forma naquele jogo. POKEMON_COLECAO aponta para a opção selecionada, e o backend confere que ela pertence ao contexto atual do exemplar.

### Métodos de obtenção
METODO_FORMA_JOGO lista o que é possível em determinado jogo. POKEMON_COLECAO guarda o método efetivamente usado. Assim, uma forma pode ter diversos métodos possíveis sem que o sistema escolha um método arbitrário para todos os exemplares.

### Coleção, jogo atual e jogo de origem
Cada exemplar pertence a um usuário e tem um contexto atual por meio de DADOS_FORMA_JOGO. O jogo de origem é opcional e separado. A primeira versão não armazena o histórico inteiro de transferências; esse limite precisa ser informado na interface.

### Sistemas de treinamento
MECANICA_SISTEMA_ATRIBUTO informa quais sistemas existem em uma versão de mecânicas, sua aplicabilidade, unidade e limites conhecidos. VALOR_ATRIBUTO_POKEMON guarda um valor por exemplar, sistema e atributo. IV, EV e treinamento próprio de outro jogo não podem ser misturados.

### Perfil de análise
PERFIL_ANALISE define o alvo e a mecânica. VALOR_PERFIL_ANALISE guarda os valores que o exemplar será comparado. Naturezas e habilidades recomendadas ficam em associações próprias. Perfil competitivo não é o mesmo que regulamento.

### Regulamento e elegibilidade
REGULAMENTO está ligado a uma versão de mecânicas. ELEGIBILIDADE_FORMA_REGULAMENTO classifica a espécie/forma no regulamento. Essa relação não comprova a legalidade completa de um exemplar individual.

## Restrições para o modelo lógico

- E-mail e nome de usuário únicos sem distinção de maiúsculas/minúsculas.
- Código de forma único dentro da espécie.
- Uma forma padrão por espécie.
- Forma + jogo únicos em DADOS_FORMA_JOGO.
- Posição de tipo restrita a 1 ou 2; sem duplicação.
- Habilidade e método únicos por ficha e opção/slot.
- Jogo + versão únicos em MECANICA_JOGO.
- Mecânica + tipo de treinamento únicos.
- Exemplar + sistema + atributo únicos nos valores de treinamento.
- Perfil + sistema + atributo únicos nos valores de perfil.
- Perfil personalizado exige proprietário.
- Habilidade selecionada deve pertencer ao contexto atual.
- Forma e mecânica de perfil devem apontar para o mesmo jogo.
- Elegibilidade única por regulamento + forma/jogo.
- Origem e destino de transformação devem pertencer ao mesmo jogo.
- Toda operação de coleção verifica o proprietário no servidor.
- Limites de treinamento desconhecidos não podem ser substituídos por valores presumidos.
