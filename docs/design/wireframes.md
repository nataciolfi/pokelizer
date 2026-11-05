# Wireframes de baixa fidelidade

**Escopo documentado:** oito telas desktop, 1440 × 1000.  
**Status:** estrutura especificada; revisão visual detalhada e complementação dos estados ainda pendentes.

## Objetivo

Definir a estrutura, navegação e campos principais do website antes da implementação em HTML, CSS e Flask. O protótipo usa componentes, textos, formas e placeholders.

## Telas criadas

| Nº | Tela | Objetivo |
|---:|---|---|
| 01 | Entrar | Permitir autenticação e acesso à coleção pessoal. |
| 02 | Criar conta | Registrar usuário e credenciais. |
| 03 | Pokédex | Pesquisar espécies e filtrar por tipo, geração e jogo. |
| 04 | Detalhes do Pokémon | Consultar uma espécie, suas formas e dados no contexto de um jogo. |
| 05 | Minha coleção | Consultar os Pokémon registrados pelo usuário. |
| 06 | Adicionar Pokémon | Registrar espécie/forma, jogo, método de obtenção, natureza, habilidade, IVs e EVs quando aplicáveis. |
| 07 | Analisador | Comparar um exemplar com um perfil competitivo ou personalizado. |
| 08 | Perfil personalizado | Definir EVs, naturezas e habilidades preferidas para comparação. |

## Convenções visuais

- Wireframe desktop com frames de 1440 × 1000.
- Paleta neutra e em tons de cinza, para priorizar hierarquia e fluxo.
- Campos e botões baseados em componentes editáveis do sistema visual Simple Design System.
- Imagens de Pokémon aparecem como placeholders para não antecipar a decisão sobre fontes e licenças de imagens.
- O conteúdo de exemplo é ilustrativo e não representa dados oficiais definitivos ou uma análise real.

## Regras funcionais refletidas no protótipo

1. As coleções pertencem ao usuário autenticado.
2. A Pokédex consulta espécies e formas; disponibilidade de cada forma deve ser contextualizada pelo jogo.
3. A tela de cadastro inclui jogo/contexto e método de obtenção.
4. IVs e EVs só são exibidos quando aplicáveis às mecânicas selecionadas.
5. O analisador distingue perfis competitivos e personalizados.
6. O resultado deverá mostrar o jogo, o contexto de mecânicas, o perfil e a fonte/regulamento utilizados.
7. As telas são wireframes; ainda não existe implementação funcional.

## Revisão pendente

- [ ] Revisar visualmente as oito telas especificadas.
- [ ] Conferir textos, espaçamentos e alinhamentos.
- [ ] Decidir se é necessário acrescentar telas mobile/responsivas.
- [ ] Validar o fluxo de navegação antes da implementação do frontend.
- [ ] Depois da revisão, registrar a versão aprovada no projeto.

## Relação com as disciplinas

- **Desenvolvimento de Websites:** define páginas, campos, navegação e hierarquia.
- **Banco de Dados:** os formulários refletem os dados de usuário, espécie/forma, coleção, perfil e regulamento previstos no modelo.
- **POO:** a tela do analisador antecipa as operações que serão separadas em classes e métodos no backend.
