# Escopo do projeto

## 1. Visão geral

O PokéAnalyzer será um website com Pokédex Nacional completa, incluindo formas oficiais, coleção individual por usuário e analisador de Pokémon. O catálogo global será separado dos dados específicos de cada jogo.

O usuário poderá consultar espécies e formas, registrar Pokémon capturados, transferidos ou recrutados e comparar dados com perfis compatíveis com o jogo e as mecânicas selecionadas.

## 2. Objetivos

1. Disponibilizar consulta de espécies e todas as formas oficiais catalogadas.
2. Separar dados globais da Pokédex dos atributos, tipos, habilidades e disponibilidade por jogo.
3. Permitir contas e coleções individuais.
4. Registrar método de obtenção, jogo de origem, natureza, habilidade, nível, IVs e EVs quando aplicáveis.
5. Comparar dados com perfis competitivos de referência ou perfis personalizados.
6. Explicar pontos positivos e oportunidades de melhoria.
7. Consultar regulamentos oficiais, sempre identificando jogo, formato, temporada, vigência e fonte.
8. Distinguir a presença de uma forma na Pokédex da disponibilidade dela em um jogo e da elegibilidade em um regulamento.

## 3. Contexto de jogos

- **Pokémon Scarlet e Pokémon Violet (Geração IX):** referência principal da calculadora de IVs, EVs e naturezas.
- **Pokémon Champions:** contexto competitivo separado, com recrutamento, transferência e treinamento próprio por Pontos de Vitória. Os valores desse treinamento não serão convertidos em IV/EV de Scarlet/Violet sem equivalência oficial documentada.
- **Pokémon Legends: Z-A:** contexto próprio de catálogo e mecânicas; não herdar automaticamente regras de Scarlet/Violet.
- **Outros jogos oficiais:** poderão ser acrescentados com seus próprios registros de jogo e mecânicas.

A próxima geração principal ainda não terá regras cadastradas antes de seu lançamento e da publicação de informações oficiais.

## 4. Funcionalidades dentro do escopo

- Cadastro, login e saída de usuários.
- Pesquisa e filtros na Pokédex.
- Visualização de espécies e formas oficiais.
- Consulta de dados da forma por jogo.
- Cadastro, edição, consulta e exclusão de Pokémon na coleção.
- Registro de método de obtenção e jogo de origem, quando conhecido.
- Registro de nível, natureza, habilidade, IVs e EVs quando aplicáveis.
- Criação e edição de perfis personalizados.
- Consulta de perfis competitivos de referência.
- Análise comparativa com recomendações explicáveis.
- Consulta de regulamentos e verificação da elegibilidade por forma e jogo, quando houver fonte oficial suficiente.

## 5. Catálogo completo e formas

O catálogo global deverá contemplar a Pokédex Nacional e todas as formas oficiais documentadas. Cada forma pertence a uma espécie.

Estatísticas-base, tipos, habilidades e disponibilidade serão registrados por contexto de jogo. Uma forma pode existir no catálogo sem estar presente ou ser obtenível em todos os jogos.

Formas puramente visuais também poderão ser catalogadas. Mega Evoluções e outras transformações de batalha serão identificadas como estados/transformações, sem tratá-las automaticamente como capturas independentes.

A lista e a contagem do catálogo deverão acompanhar a fonte oficial e a versão dos dados, sem fixar permanentemente um total no código.

## 6. Modos de análise

### Atributos por mecânica de jogo

A primeira calculadora utilizará as mecânicas da Geração IX de Scarlet/Violet para IVs, EVs e natureza. O sistema deve validar limites a partir do contexto de mecânicas selecionado.

Quando um jogo não utilizar ou não tiver confirmado um desses sistemas, o campo correspondente ficará indisponível ou não informado. O programa não deve preencher ausência com zero nem converter sistemas de treinamento diferentes.

### Competitivo

Compara a forma com um regulamento oficial específico de jogo, formato e temporada. O regulamento informa restrições e elegibilidade; não determina por si só uma única distribuição ideal de IVs, EVs ou natureza.

### Personalizado

Permite que o usuário crie um perfil com valores e prioridades que deseja comparar. O perfil pertence ao usuário e pode existir sem regulamento competitivo.

## 7. Fora do escopo inicial

- Simulador de batalhas.
- Calculadora completa de dano.
- Montagem e gerenciamento de equipes.
- Banco completo de golpes e itens segurados.
- Integração com jogos ou leitura automática de arquivos de save.
- Marketplace, trocas ou funcionalidades sociais.
- Histórico detalhado de todas as análises.
- Aplicativo móvel nativo.
- Conversão automática entre sistemas de treinamento de jogos diferentes.

Essas ideias poderão ser avaliadas em versões futuras, mas não fazem parte da primeira entrega.

## 8. Premissas

- O primeiro banco físico será local, usando SQLite.
- O website será servido por Python/Flask.
- O usuário precisará estar autenticado para acessar e modificar sua coleção.
- A análise deverá explicar suas conclusões por regras legíveis.
- Dados de jogos, formas e regulamentos deverão manter referência de origem e versão.
- Dados desconhecidos serão marcados como não verificados, e não presumidos.
