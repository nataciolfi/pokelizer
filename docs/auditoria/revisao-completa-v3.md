# Auditoria completa do PokéAnalyzer

**Data:** 03/11/2026  
**Versão auditada:** documentação e wireframes desktop existentes no repositório.  
**Versão corretiva proposta:** 3.0.  
**Escopo da auditoria:** coerência do produto, domínio Pokémon, modelo de dados, requisitos, arquitetura técnica, segurança, dados e interface.

## 1. Resultado executivo

A ideia do PokéAnalyzer é válida e tem uma boa separação inicial entre catálogo, jogo, coleção e regulamento. Entretanto, a versão 2.0 não estava pronta para virar SQL nem código. A documentação afirmava suportar casos que o modelo não conseguia representar sem perda ou ambiguidade.

**Diagnóstico:** especificação parcialmente consistente, arquitetura de dados insuficiente em pontos centrais e protótipo funcionalmente incompleto.

O repositório auditado contém documentos Markdown e a referência de um Figma. Não contém código-fonte de backend/frontend, arquivo SQLite, migrações, dados importados ou testes. Assim, não seria correto afirmar que bugs de implementação foram corrigidos ou que o sistema passou em testes executáveis.

## 2. Escala de severidade

- **Crítica:** pode corromper conceitos/dados ou produzir conclusões falsas.
- **Alta:** impede um requisito central ou torna o fluxo inconsistente.
- **Média:** causa ambiguidade, manutenção difícil ou experiência incompleta.
- **Baixa:** melhoria de clareza, apresentação ou conveniência.

## 3. Achados críticos

### C01 — O exemplar e o estado dele em um jogo estavam misturados
**Severidade:** crítica.

Na versão anterior, POKEMON_COLECAO apontava diretamente para DADOS_FORMA_JOGO. Isso fazia o exemplar existir dentro de um único contexto de jogo e misturava jogo de origem com jogo atual. A mesma criatura poderia passar por transferência e treinamento em um segundo jogo, mas o modelo não tinha uma entidade para guardar esse segundo estado sem duplicar ou sobrescrever informações.

**Correção v3:** POKEMON_COLECAO representa o exemplar do usuário. POKEMON_ESTADO_JOGO representa o exemplar em um contexto de jogo específico. O jogo de origem e o contexto de análise são separados. Cada estado possui sua forma, nível, natureza, habilidade e valores de treinamento daquele contexto.

### C02 — O modelo prometia Champions, mas só possuía colunas de IV/EV
**Severidade:** crítica.

MECANICA_JOGO tinha um campo textual de sistema de treinamento, mas POKEMON_COLECAO e PERFIL_ANALISE tinham apenas seis colunas de IV e seis de EV. Isso não representa um sistema de treinamento diferente. A documentação oficial de Champions confirma recrutamento próprio, visitantes via HOME e treinamento com Pontos de Vitória; o treinamento do Champions não é transferido como IV/EV para HOME.

**Correção v3:** ATRIBUTO_TREINAMENTO define os atributos e limites existentes em cada contexto. VALOR_TREINAMENTO_POKEMON e VALOR_TREINAMENTO_PERFIL armazenam os valores do exemplar e as referências do perfil. Um contexto só recebe atributos quando houver informação verificada. Não converter sistemas.

### C03 — Um método de obtenção único não representa os caminhos possíveis
**Severidade:** crítica.

O campo metodo_obtencao em DADOS_FORMA_JOGO permitia apenas um texto por forma/contexto. Uma mesma forma pode ter vários métodos, condições ou fontes de obtenção.

**Correção v3:** METODO_OBTENCAO é um catálogo e OBTENCAO_FORMA_JOGO registra múltiplos métodos, condições e fonte por contexto. O exemplar mantém seu método de origem individual.

### C04 — Elegibilidade da forma era apresentada como legalidade competitiva
**Severidade:** crítica.

A relação entre forma e regulamento não valida todos os dados de um exemplar. Uma validação competitiva integral pode depender de movimentos, itens, marca, origem, evento, nível, habilidade e outras condições. Parte desses dados nem existe no escopo inicial.

**Correção v3:** a relação foi explicitamente nomeada ELEGIBILIDADE_REGULAMENTO e seu resultado se limita à espécie/forma. A interface não pode afirmar “100% legal”. A primeira versão mostra “elegibilidade da forma” e a condição conhecida.

### C05 — Perfil de análise e regulamento estavam semanticamente próximos
**Severidade:** crítica.

Regulamento estabelece restrições competitivas. Perfil define alvo ou preferências para comparar atributos. Um regulamento não define automaticamente uma única distribuição ideal.

**Correção v3:** PERFIL_ANALISE e REGULAMENTO continuam entidades separadas. Um perfil pode ser personalizado, estratégico ou uma referência competitiva; origem e versão precisam ser mostradas. Um regulamento só é associado quando a referência depende daquela competição.

### C06 — Status binário não representava desconhecimento
**Severidade:** crítica.

A documentação dizia que usa_iv, usa_ev e outros booleanos poderiam ficar sem definição, mas não especificava como diferenciar “não usa” de “não sei”. Booleano simples tem apenas dois estados.

**Correção v3:** estados controlados USA, NAO_USA e NAO_VERIFICADO. O mesmo princípio se aplica a presença e registrabilidade.

## 4. Achados de alta severidade

### A01 — Presença, obtenibilidade e registrabilidade estavam misturadas
Uma forma estar presente em um jogo não significa que possa ser capturada nele; pode depender de transferência, evento ou transformação. A versão v3 separa presença no jogo, métodos de obtenção e possibilidade de registro independente ou apenas como transformação.

### A02 — Tipo N:N não tinha posição
A relação DADOS_FORMA_JOGO–TIPO não registrava qual era o tipo primário ou secundário nem impedia duplicações. Foi criada DADOS_FORMA_TIPO com atributo slot e limite de no máximo dois tipos.

### A03 — Habilidade selecionada não tinha garantia de contexto
A coleção apontava para uma opção de habilidade, mas faltavam regras explícitas para impedir que ela pertencesse a outra forma ou outro jogo. A v3 exige chave estrangeira composta/validação que mantenha a habilidade no mesmo contexto.

### A04 — Transformações não tinham compatibilidade garantida
TRANSFORMACAO_FORMA ligava dados de origem e destino, mas não exigia que fossem contextos compatíveis. A v3 exige mesma mecânica/jogo e condição documentada; transformação não cria exemplar automaticamente.

### A05 — O comparador não tinha algoritmo especificado
“Pontos positivos” e “o que melhorar” eram descrições, não regras executáveis. Não havia definição de faixa desejada, prioridade, dados obrigatórios ou comportamento com valores ausentes.

**Correção:** perfis guardam valores/faixas por atributo, naturezas e habilidades preferidas. A comparação é campo a campo, determinística, contextual e explicável. Nota global só poderá existir com fórmula documentada e testes.

### A06 — IV alto era tratado implicitamente como melhor
Isso é falso como regra geral: alguns objetivos estratégicos podem preferir valores baixos em certos atributos. O perfil define o objetivo; o analisador não presume maximização universal.

### A07 — Uma forma podia ser cadastrada sem distinção clara entre forma real e estado temporário
A v3 classifica as formas e guarda a registrabilidade por jogo/contexto. Shiny é uma característica do exemplar, não uma espécie nova; estados temporários de batalha não geram captura independente por padrão.

### A08 — Jogo e mecânica não tinham definição operacional suficiente
JOGO deve representar o título/edição. MECANICA_JOGO representa o conjunto documentado de regras de atributos e treinamento. Regulamento de temporada não é versão de mecânica.

### A09 — Cobertura do catálogo não tinha critério verificável
A frase “Pokédex completa” não tinha lista de referência, versão nem relatório de cobertura. A v3 exige fonte, critério para formas, relatório de importação e documentação de lacunas antes de declarar cobertura completa.

## 5. Achados de média severidade

- O protótipo não especifica estados vazio, carregamento, erro, dado ausente e perfil incompatível.
- A coleção foi descrita como tabela, mas não explicitava que cada linha representa um exemplar individual; espécies repetidas precisam ser permitidas.
- A tela de cadastro não separava com clareza origem, método de obtenção e estado em jogo.
- A Pokédex precisava distinguir filtros globais e contextuais.
- Detalhes de Pokémon misturavam evolução, forma e transformação.
- Não havia política de fonte/licença para conjuntos de dados secundários.
- Não havia critérios técnicos explícitos para chave estrangeira composta, transações, parametrização SQL e autorização por proprietário.
- A responsividade não estava especificada; o protótipo desktop não deve ser confundido com decisão de construir apenas desktop.

## 6. Riscos de segurança e integridade a impedir na implementação

1. A rota de um registro não pode confiar apenas no ID recebido; deve filtrar pelo usuário da sessão.
2. A senha nunca deve ser armazenada em texto puro ou hash rápido sem função apropriada para senhas.
3. SQL deve ser parametrizado.
4. Operações de atualização/exclusão devem verificar proprietário e usar transação quando necessário.
5. Formulários autenticados devem ter proteção CSRF.
6. Limites de atributos precisam ser verificados no backend, não apenas no JavaScript.
7. Chaves estrangeiras do SQLite precisam ser ativadas em toda conexão.
8. A interface não pode transformar dado ausente em zero, “permitido” ou “proibido”.
9. Fontes e datas de verificação não podem ser removidas durante atualização de catálogo.
10. Erros internos não devem revelar senha, hash ou detalhes privados.

## 7. Auditoria das oito telas

A especificação corrigida está em [wireframes.md](../design/wireframes.md). Resumo:
- Entrar: validação, sessão expirada e erro.
- Criar conta: política de senha, e-mail único e feedback.
- Pokédex: filtro global separado de disponibilidade e tipo por jogo.
- Detalhes: separar espécie, forma, evolução e transformação.
- Coleção: cada item é exemplar individual com múltiplos estados por jogo.
- Adicionar: dividir exemplar/origem e estado em jogo.
- Analisador: selecionar estado, perfil e regulamento separadamente.
- Perfil: nome, objetivo, contexto, faixas e preferências.

**Limitação:** a cota do Figma Starter bloqueou a leitura visual adicional. A auditoria das telas é funcional/documental; espaçamentos, colisões, alinhamento e tipografia continuam pendentes de inspeção visual. Nenhum frame foi declarado corrigido visualmente nesta revisão.

## 8. Decisões da versão 3.0

- Separar exemplar e estado por jogo.
- Modelar atributos de treinamento por mecânica.
- Separar método de obtenção e contexto atual.
- Separar presença, obtenibilidade e registrabilidade.
- Normalizar tipos por slot.
- Restringir habilidade ao contexto correto.
- Separar perfil de análise e regulamento.
- Limitar alegações de elegibilidade.
- Registrar fonte e verificação.
- Fazer primeira análise numérica com contexto de Scarlet/Violet, sem simular suporte de outros jogos não verificados.

## 9. O que não foi alterado nem alegado

- Não existe backend a corrigir.
- Não existe frontend implementado.
- Não existe banco SQLite físico.
- Não existem testes executáveis.
- O DER visual do brModelo não foi atualizado.
- Os frames do Figma não foram modificados.
- A importação completa da Pokédex não foi executada.

A auditoria corrige a especificação documental e define o trabalho seguinte. Ela não substitui a implementação e os testes.

## 10. Portões de aprovação antes do código

- [ ] Usuário aprova a separação entre exemplar e estado por jogo.
- [ ] DER v3 visual confere com o Mermaid e as cardinalidades.
- [ ] Modelo lógico possui chaves e restrições compatíveis.
- [ ] Cada regra de negócio tem pelo menos um caso de teste.
- [ ] Fonte e política de dados foram escolhidas.
- [ ] Wireframes foram atualizados e inspecionados visualmente.
- [ ] Escopo inicial de cálculo e jogos foi aceito.
