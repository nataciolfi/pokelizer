# Decisões em aberto — PokéAnalyzer

Este documento impede que decisões ainda não tomadas sejam escondidas dentro do código.

## Bloqueiam a aprovação final do modelo conceitual

### D01 — Definição de forma oficial
Aprovar política para variações regionais, gênero, sazonalidade, cosméticas, fusões, Mega/Gigantamax/estados de batalha e variações temporárias. Definir o que será catalogado como FORMA e o que será apenas transformação/estado visual. Registrar exemplos incluídos e excluídos.

### D02 — Identificador estável de forma
Escolher identificador interno estável e mapeamento para fontes externas. Não usar nome traduzido como chave, pois nomes podem mudar e colidir.

### D03 — Fonte primária do catálogo
Decidir fontes para espécies, formas, tipos, habilidades, atributos e disponibilidade. A Pokédex oficial é referência de consulta, mas não deve ser presumida como arquivo estruturado e completo de todas as formas. Registrar fonte, data, versão e divergências.

### D04 — Exemplar sem contexto atual
A versão 3.0 exige contexto atual DADOS_FORMA_JOGO para registrar exemplar. Confirmar se o MVP só permitirá exemplares de jogos suportados e catalogados. Alternativa futura: permitir registrar apenas a forma e deixar jogo atual pendente; isso exige rever nulabilidade e fluxo.

### D05 — Histórico de transferência
O MVP mantém apenas jogo atual e jogo de origem. Confirmar que basta para a entrega escolar; histórico completo fica adiado.

### D06 — Conteúdo do perfil de referência
Definir se perfis serão escritos manualmente, importados de fontes comunitárias ou baseados em materiais oficiais. Não chamar build comunitária de oficial. Referência externa precisa de fonte e data.

## Bloqueiam funcionalidades específicas, mas não o modelo geral

### D07 — Fórmula de análise
A versão inicial compara por atributo com valor-alvo explícito e não dá nota global. Confirmar antes de criar pontuação agregada.

### D08 — Champions
Fontes oficiais confirmam recrutamento e treinamento com Pontos de Vitória, mas não se deve inventar escala, limites ou equivalência. Registrar contexto sem análise numérica até confirmação.

### D09 — Regulamentos cobertos
Definir formatos e temporadas cobertos no MVP. Não assumir a mesma elegibilidade em todos os formatos, temporadas e jogos.

### D10 — Imagens
Escolher fonte e licença antes de incorporar imagens oficiais. O wireframe usa placeholders intencionalmente.

### D11 — Privacidade e ciclo de vida da conta
Definir exportação/exclusão, retenção e dados indispensáveis. Não guardar senhas em texto puro nem publicar dados reais.

### D12 — Responsividade
Decidir se a entrega mínima será desktop e mobile web. A página Figma atual só documenta desktop e não deve ser chamada de responsiva antes de desenhar e inspecionar larguras menores.

## Critério de encerramento
Cada decisão deve ter resposta escolhida, justificativa curta, impacto em entidades/requisitos/telas e data. Não converter pergunta em aberto em suposição silenciosa no código.
