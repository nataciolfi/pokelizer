# Wireframes de baixa fidelidade — revisão de conteúdo

**Wireframes:** [PokéAnalyzer — Wireframes](https://www.figma.com/design/ElwmtWufS0oyS2KNwLsHFD)

**DER:** [PokéAnalyzer — DER 3.0 (FigJam)](https://www.figma.com/board/2hpHQKy2zeoTFDFJX6EXQ9)  
**Escopo existente:** oito telas desktop, 1440 × 1000.  
**Status:** estrutura criada; auditoria visual detalhada e alterações no Figma pendentes por limite de chamadas do plano Starter.

## Diagnóstico

As telas formam um ponto de partida, não um fluxo fechado. O conteúdo deve seguir o modelo conceitual 3.0. Textos e dados de exemplo são placeholders, não dados oficiais nem funcionalidades implementadas.

## Correções por tela

### 01 — Entrar
- Incluir mensagens de erro e estado de carregamento.
- Não revelar se um e-mail existe por mensagens específicas.
- Manter acesso a criar conta.

### 02 — Criar conta
- Mostrar regras mínimas de senha.
- Validar confirmação no frontend e backend.
- Associar mensagens de erro aos campos.
- Impedir duplicidade de e-mail e nome de usuário.

### 03 — Pokédex
- Filtrar por tipo, geração e jogo.
- Distinguir presença no jogo de transferência, obtenção e elegibilidade.
- Mostrar espécies mesmo sem dados do jogo.
- Indicar dados não verificados.
- Criar estado vazio e opção de limpar filtros.

### 04 — Detalhes do Pokémon
- Separar espécie, forma e evolução.
- Mostrar formas alternativas da mesma espécie.
- Mostrar jogo, fonte e estado de verificação.
- Distinguir forma registrável de transformação temporária.
- Não mostrar estatísticas de um jogo como universais.

### 05 — Minha coleção
- Cada linha/card representa um exemplar.
- Mostrar apelido, espécie/forma, jogo atual e jogo de origem, quando conhecido.
- Permitir abrir, editar e excluir um exemplar.
- Mostrar coleção vazia.
- Permitir vários exemplares da mesma forma.

### 06 — Adicionar Pokémon
Separar identidade, contexto atual, origem, método real, características e treinamento. IV/EV não podem ser campos universais. Para Champions, não mostrar IV/EV por padrão; só apresentar treinamento específico quando a escala estiver confirmada.

### 07 — Analisador
- Selecionar exemplar.
- Selecionar mecânica compatível com o jogo atual.
- Selecionar perfil e regulamento separadamente.
- Mostrar sistema de treinamento comparado.
- Exibir valores ausentes e limites não verificados.
- Separar comparação de atributos da elegibilidade da espécie/forma.
- Não declarar legalidade completa do exemplar.

### 08 — Perfil personalizado
- Adicionar nome, descrição e salvar.
- Exibir jogo, forma e mecânica-alvo.
- Organizar valores por sistema e atributo.
- Mostrar natureza/habilidade somente quando aplicáveis.
- Validar limites e soma segundo a mecânica.
- Criar lista de perfis, editar e excluir.

## Fluxo necessário

Entrar/criar conta → Pokédex ou coleção → detalhe da forma/exemplar → adicionar/editar → analisador → resultado. O usuário também deve acessar uma lista de perfis, criar/editar perfil e voltar à análise sem perder o exemplar.

## Telas e estados ainda necessários

- Detalhe de exemplar individual.
- Confirmação de exclusão.
- Lista/gerenciamento de perfis.
- Pokédex sem resultados.
- Coleção vazia.
- Formulário inválido.
- Dados de jogo não verificados.
- Mecânica sem treinamento confirmado.
- Nenhum perfil compatível.
- Elegibilidade não verificada.

## Critérios de inspeção visual

Hierarquia consistente, rótulos próximos aos campos, navegação uniforme, espaçamento/alinhamento, contraste, foco de teclado, responsividade e ausência de campos de treinamento incompatíveis. A inspeção pixel a pixel do Figma ainda não foi realizada devido ao limite de chamadas.

## Disciplinas

- Websites: páginas, formulários, navegação e acessibilidade.
- Banco de Dados: os formulários refletem espécie, forma, jogo, exemplar, perfil e regulamento.
- POO: validações e cálculos ficam em classes/serviços no backend.
