# Decisões em aberto — PokéAnalyzer

Este documento impede que decisões ainda não tomadas sejam escondidas dentro do código.

## Bloqueiam a aprovação final do modelo conceitual

### D01 — Definição de forma oficial
Aprovar uma política para variações regionais, gênero, sazonalidade, cosméticas, fusões, Gigantamax/Mega/estados de batalha e variações temporárias. Definir o que será catalogado como FORMA e o que será apenas transformação/estado visual. Para cada categoria, registrar exemplos incluídos e excluídos.

### D02 — Identificador estável de forma
Escolher um identificador interno estável e a estratégia de mapeamento para fontes externas. Não usar nome traduzido como chave, pois nomes podem mudar e colidir.

### D03 — Fonte primária do catálogo
Decidir quais fontes serão usadas para lista de espécies, formas, tipos, habilidades, atributos e disponibilidade. A Pokédex oficial é referência de consulta, mas não deve ser presumida como arquivo estruturado e completo de todas as formas. Registrar fonte, data, versão e divergências.

### D04 — Exemplar sem contexto atual
A versão 3.0 exige um contexto atual DADOS_FORMA_JOGO para registrar um exemplar. Confirmar se o MVP só permitirá registrar exemplares de jogos suportados e catalogados. Alternativa futura: permitir registro apenas da forma e deixar jogo atual pendente; isso exigiria alterar a nulabilidade e o fluxo da coleção.

### D05 — Histórico de transferência
O MVP mantém apenas jogo atual e jogo de origem. Confirmar que isso basta para a entrega escolar; histórico completo fica adiado.

### D06 — Conteúdo do perfil de referência
Definir se os perfis serão escritos manualmente, importados de fontes comunitárias ou baseados em materiais oficiais. Não chamar uma build comunitária de oficial. Toda referência externa precisa indicar fonte, data e termos relevantes.

## Bloqueiam funcionalidades específicas, mas não o modelo geral

### D07 — Fórmula de análise
A versão inicial compara por atributo com valor-alvo explícito e não dá nota global. Confirmar essa regra antes de criar qualquer pontuação agregada.

### D08 — Champions
A documentação oficial confirma recrutamento e treinamento com Pontos de Vitória, mas não se deve inventar escala, limites ou equivalência. Registrar o contexto sem análise numérica até os detalhes necessários serem confirmados por fonte oficial.

### D09 — Regulamentos cobertos
Definir os formatos e temporadas cobertos no MVP. Não assumir que a mesma lista de elegibilidade vale para todos os formatos, temporadas e jogos.

### D10 — Imagens
Escolher fonte e licença antes de incorporar imagens oficiais. O wireframe atual usa placeholders; isso é intencional até haver validação de uso.

### D11 — Privacidade e ciclo de vida da conta
Definir como exportar ou excluir conta e coleção, período de retenção e quais dados são indispensáveis. Mesmo sendo projeto local/escolar, não guardar senhas em texto puro nem publicar dados reais de usuários.

### D12 — Responsividade
Decidir se a entrega mínima será desktop e mobile web. A página Figma atual só documenta desktop e não deve ser chamada de responsiva até haver frames e inspeção em larguras menores.

## Critério de encerramento

Cada decisão deve receber: resposta escolhida, justificativa curta, impacto em entidades/requisitos/telas e data. Não converter uma pergunta em aberto em suposição silenciosa no código.
