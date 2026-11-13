# Wireframes de baixa fidelidade

**Arquivo Figma:** [PokéAnalyzer — Wireframes](https://www.figma.com/design/ElwmtWufS0oyS2KNwLsHFD)  
**Tipo:** Figma Design  
**Escopo existente:** oito telas desktop de baixa fidelidade, frames 1440 × 1000.  
**Status:** telas existentes; correções funcionais especificadas abaixo, ainda não aplicadas visualmente.

## 1. Objetivo

Definir a estrutura do website antes da implementação. O Figma não é uma versão funcional do produto: botões, filtros e formulários são demonstrativos e não estão conectados a backend ou banco.

## 2. Auditoria das telas existentes

| Tela | Problema identificado na especificação | Correção necessária |
|---|---|---|
| 01 — Entrar | Não documenta estados de erro, sessão expirada ou recuperação de senha. | Prever validação, credenciais incorretas e retorno após autenticação. |
| 02 — Criar conta | Não deixa explícitas regras de senha, e-mail único e feedback de validação. | Incluir confirmação, mensagens por campo e aviso de conta criada. |
| 03 — Pokédex | Filtros globais e filtros de jogo podem ser confundidos. Tipo pode variar por forma/contexto. | Separar busca global dos filtros contextuais; exibir categoria e disponibilidade da forma. |
| 04 — Detalhes | Espécie, forma, evolução e transformação não são a mesma coisa. | Separar identidade da espécie, seletor de forma, relações evolutivas e transformações; mostrar fonte e estado de disponibilidade. |
| 05 — Minha coleção | Uma linha por espécie não representa vários exemplares iguais. | Cada linha deve representar um exemplar; exibir apelido, origem e estados de jogo. |
| 06 — Adicionar Pokémon | Origem, método de obtenção e jogo em que o exemplar será analisado podem parecer um único campo. | Separar origem/método do exemplar e criação do estado em um jogo; campos dependem das mecânicas. |
| 07 — Analisador | Perfil competitivo, regulamento e jogo estão conceitualmente próximos demais. | Selecionar exemplar/estado, perfil compatível e regulamento separadamente; explicar que elegibilidade da forma não é legalidade integral do exemplar. |
| 08 — Perfil personalizado | Falta tornar explícitos nome, contexto, preferências e critérios de treinamento. | Incluir nome, objetivo, espécie/forma, jogo/mecânica, faixas/valores de treinamento, naturezas, habilidades e salvamento. |

## 3. Especificação corrigida de cada tela

### 01 — Entrar
- E-mail ou identificador de usuário.
- Senha.
- Ação de entrar.
- Link para criar conta.
- Estado de credenciais inválidas.
- Estado de campo obrigatório.
- Estado de sessão expirada.
- Não exibir detalhes técnicos de autenticação.

### 02 — Criar conta
- Nome de usuário.
- E-mail.
- Senha.
- Confirmação de senha.
- Regras de validação próximas dos campos.
- Aviso de e-mail já utilizado.
- Confirmação de criação.

### 03 — Pokédex
- Pesquisa por número, nome ou forma.
- Filtros de catálogo: geração e categoria de forma.
- Filtros contextuais: jogo, tipo no jogo, presença e obtenibilidade.
- Não ocultar uma espécie do catálogo global porque está ausente no jogo selecionado.
- Distinguir ausência de dados e ausência confirmada no jogo.
- Cards devem identificar espécie e forma sem sugerir que cada forma é espécie separada.

### 04 — Detalhes do Pokémon
- Número nacional e espécie.
- Seletor/lista de formas.
- Categoria da forma.
- Tipos e estatísticas no contexto selecionado.
- Habilidades disponíveis naquele contexto.
- Status de presença e obtenibilidade.
- Relações de evolução em seção própria.
- Transformações em seção própria, com condição e indicação de que não criam automaticamente novo exemplar.
- Fonte e data de verificação.

### 05 — Minha coleção
- Cada item é um exemplar individual, não um agrupamento por espécie.
- Apelido e espécie.
- Forma do estado selecionado.
- Jogo de origem e método de obtenção.
- Estados de jogo cadastrados.
- Ações para abrir, editar e excluir.
- Estado vazio para usuário sem registros.
- Filtros por nome, forma, jogo de origem e jogo do estado.

### 06 — Adicionar Pokémon
Dividir visualmente em duas etapas:
1. **Exemplar:** espécie, apelido opcional, jogo de origem opcional, método de obtenção e data aproximada, quando conhecida.
2. **Estado em jogo:** jogo/contexto, forma, nível, natureza, habilidade e atributos de treinamento definidos para esse contexto.

Não mostrar IV/EV por padrão. Os campos devem vir do catálogo de atributos de treinamento da mecânica selecionada. Permitir salvar o exemplar sem inventar valores quando alguns dados forem desconhecidos.

### 07 — Analisador
- Selecionar um exemplar e um estado em jogo já registrado.
- Mostrar o jogo e o contexto de mecânicas de forma visível.
- Selecionar perfil compatível.
- Selecionar regulamento separadamente, quando for verificar elegibilidade.
- Resultado por atributo: valor atual, preferência/faixa do perfil, divergência e explicação.
- Alertar sobre dados insuficientes.
- Não apresentar nota global sem explicar o cálculo.
- Usar “elegibilidade da forma no regulamento”, não “Pokémon totalmente legal”.

### 08 — Perfil personalizado
- Nome e descrição/objetivo.
- Espécie e forma alvo.
- Jogo e mecânica.
- Faixas ou valores esperados para atributos de treinamento.
- Naturezas preferidas/aceitáveis/evitadas.
- Habilidades preferidas/aceitáveis.
- Salvar, editar e excluir.
- Mostrar que o perfil pertence ao usuário.

## 4. Fluxo de navegação recomendado

1. Usuário entra ou cria conta.
2. Acessa Pokédex ou Minha coleção.
3. Na Pokédex, abre detalhes e pode iniciar cadastro de exemplar.
4. Na coleção, abre um exemplar e escolhe/edita um estado em jogo.
5. No estado, inicia análise e seleciona perfil compatível.
6. Opcionalmente consulta elegibilidade da forma em um regulamento.
7. Pode criar/editar um perfil personalizado.

As telas existentes não comprovam que esse fluxo esteja conectado. É necessário acrescentar conectores/anotações de navegação e confirmar o retorno entre telas.

## 5. Estados que ainda precisam ser desenhados

- Carregando dados.
- Nenhum resultado na busca.
- Coleção vazia.
- Nenhum estado em jogo cadastrado.
- Cadastro com dados inválidos.
- Erro de autenticação.
- Forma sem dados verificados no jogo.
- Atributo não aplicável.
- Análise impedida por dados ausentes.
- Perfil incompatível com o jogo/forma.
- Elegibilidade não verificada.
- Regulamento expirado ou sem fonte atual.

## 6. Revisão visual pendente

- [ ] Aplicar as correções funcionais descritas nas oito telas.
- [ ] Verificar alinhamento, sobreposição, espaçamento, hierarquia e legibilidade em cada frame.
- [ ] Verificar consistência de cabeçalho, navegação e ações.
- [ ] Criar pelo menos uma tela/variante de estado vazio e de erro.
- [ ] Criar versão responsiva ou documentar claramente a adaptação mobile.
- [ ] Conferir fluxo com conectores entre as telas.
- [ ] Fazer revisão visual final e registrar a data de aprovação.

**Limitação desta revisão:** a cota de leitura do Figma no plano Starter bloqueou novas inspeções visuais. Portanto, esta documentação corrige a especificação funcional e registra o que deve mudar, mas não afirma que os frames do Figma já foram editados ou visualmente aprovados.
