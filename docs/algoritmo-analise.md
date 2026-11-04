# Algoritmo de análise — versão inicial

**Status:** regra proposta para o MVP, antes da implementação.

## 1. Objetivo

Comparar um exemplar da coleção com um perfil explícito e mostrar diferenças rastreáveis. O analisador não inventa uma “build perfeita” nem converte valores entre jogos.

## 2. Pré-condições

A análise só pode executar quando:
1. O exemplar pertence ao usuário autenticado.
2. O exemplar possui contexto atual conhecido.
3. O perfil selecionado é compatível com a forma e o jogo do exemplar.
4. A versão de mecânicas pertence ao mesmo jogo.
5. O sistema de valores de atributo está marcado como aplicável e verificado.
6. Os limites necessários para validação são conhecidos.

Caso alguma condição falhe, o sistema explica por que não analisou em vez de improvisar.

## 3. Comparação de valores

Cada linha do perfil representa um atributo e um sistema (por exemplo IV ou EV), com um valor-alvo explícito.

O resultado para cada linha é um destes estados:
- **Igual ao alvo:** o valor registrado corresponde ao alvo do perfil.
- **Abaixo do alvo:** valor registrado menor que o alvo.
- **Acima do alvo:** valor registrado maior que o alvo.
- **Sem dado:** o exemplar não tem valor registrado.
- **Não aplicável:** a mecânica confirma que o sistema não existe naquele contexto.
- **Não verificado:** a mecânica ou seus limites ainda não estão confirmados.
- **Não comparado:** o perfil não definiu um alvo para esse atributo.

“Acima” e “abaixo” são descrições matemáticas, não avaliações automáticas de qualidade. Em estratégias específicas, um IV menor pode ser intencional.

## 4. Natureza e habilidade

Natureza e habilidade não são valores numéricos de atributo:
- Natureza: verificar se corresponde a uma das naturezas selecionadas pelo perfil e se a mecânica utiliza esse sistema.
- Habilidade: verificar se a habilidade escolhida existe para a forma no jogo atual e se está entre as opções do perfil, quando o perfil especificar preferência.

A análise não deve chamar uma habilidade válida de inválida apenas porque não foi preferida pelo perfil.

## 5. Elegibilidade

A elegibilidade da espécie/forma no regulamento é um painel separado da comparação de atributos. Seus estados são:
- permitido;
- restrito;
- proibido;
- condicional;
- não verificado.

Esse resultado não prova a legalidade completa do exemplar. Golpes, itens, origem, evento e demais dados não fazem parte do MVP.

## 6. Recomendação e linguagem

A versão inicial não gera nota total, ranking automático ou rótulo “competitivo/não competitivo”. Mostra:
- quais valores coincidem com o alvo;
- quais diferem;
- quais estão ausentes;
- quais sistemas não se aplicam ou não foram verificados;
- quais preferências de natureza/habilidade correspondem ao perfil.

Não inferir que um valor acima do alvo é melhor. Não chamar atributo sem dado de incompatível. Toda sugestão identifica perfil, jogo, mecânica e fonte quando houver.

## 7. Exemplo de saída

Para um alvo de 31 IV em Velocidade:
- valor 31: “Igual ao alvo”.
- valor 0: “Abaixo do alvo”.
- valor não informado: “Sem dado”.

O sistema não diz que 31 é melhor que 0 sem considerar o perfil. Um perfil pode deliberadamente recomendar 0.

## 8. Testes de aceitação

- Perfil sem alvo de velocidade não gera comparação de velocidade.
- Valor real maior que o alvo aparece como “acima”, sem juízo automático.
- Valor ausente não é tratado como zero.
- Sistema não aplicável não é tratado como sistema com valor zero.
- Mecânica não verificada bloqueia análise numérica.
- Perfil e exemplar de jogos diferentes não podem ser comparados.
- Elegibilidade é apresentada separadamente da comparação de atributos.
