# Escopo do projeto

## 1. Visão geral

O PokéAnalyzer será um website que reúne uma Pokédex Nacional completa, uma coleção pessoal por usuário e um analisador de Pokémon. O usuário poderá consultar espécies e formas, registrar seus próprios Pokémon e comparar seus IVs, EVs, natureza e habilidade com perfis de referência.

## 2. Objetivos

1. Disponibilizar consulta de espécies e formas oficiais.
2. Permitir contas e coleções individuais.
3. Registrar os dados de cada Pokémon capturado.
4. Comparar os dados cadastrados com perfis competitivos ou personalizados.
5. Explicar os pontos positivos e as oportunidades de melhoria de cada configuração.
6. Utilizar regras competitivas oficiais como referência de legalidade, sempre identificando jogo, formato, temporada e fonte.

## 3. Funcionalidades dentro do escopo

- Cadastro, login e saída de usuários.
- Pesquisa e filtros na Pokédex.
- Visualização dos dados de cada espécie e forma.
- Cadastro, edição, consulta e exclusão de Pokémon capturados.
- Registro de nível, natureza, habilidade, IVs e EVs.
- Criação e edição de perfis personalizados.
- Consulta de perfis competitivos de referência.
- Análise comparativa e apresentação de recomendações.
- Consulta de regulamentos oficiais e verificação de elegibilidade quando os dados necessários estiverem disponíveis.

## 4. Fora do escopo inicial

Para manter o projeto compreensível e viável, não serão implementados inicialmente:

- Simulador de batalhas.
- Calculadora completa de dano.
- Montagem e gerenciamento de equipes.
- Banco de golpes, itens segurados e estratégias completas.
- Integração com jogos ou leitura automática de arquivos de save.
- Marketplace, trocas ou funcionalidades sociais.
- Histórico detalhado de todas as análises.
- Aplicativo móvel nativo.

Essas ideias poderão ser avaliadas em versões futuras, mas não fazem parte da primeira entrega.

## 5. Catálogo completo e formas

O catálogo deverá contemplar a Pokédex Nacional e as formas oficiais que tenham relevância para identificação ou análise. Uma forma será registrada vinculada à espécie correspondente.

Formas puramente visuais poderão ser representadas no catálogo sem duplicar atributos de batalha quando não houver diferença. Mega Evoluções e outras transformações de batalha deverão ser identificadas como formas/estados especiais, sem tratá-las automaticamente como capturas independentes.

A contagem e a lista de espécies deverão acompanhar a referência oficial escolhida para a versão do catálogo. Não se deve fixar permanentemente um total no código.

## 6. Dois modos de análise

### Competitivo

Compara o Pokémon com perfis estratégicos de referência relacionados a um jogo, formato e regulamento oficial. O regulamento informa restrições e condições de uso; ele não determina, por si só, uma única distribuição ideal de IVs, EVs ou natureza para cada espécie.

### Personalizado

Permite que o usuário crie um perfil com os atributos, IVs, EVs e naturezas que deseja priorizar. O sistema compara o Pokémon registrado com esse objetivo pessoal.

## 7. Premissas

- O primeiro banco físico será simples e local, com SQLite.
- O website será servido por um backend Python/Flask.
- O usuário precisará estar autenticado para acessar e modificar sua coleção.
- A análise deverá explicar suas conclusões em regras legíveis, sem depender de inteligência artificial.
- Dados e regulamentos deverão manter referência de origem e versão.
