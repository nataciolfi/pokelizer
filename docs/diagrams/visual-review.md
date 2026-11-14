# Revisão visual — 13/11/2026

Foram inspecionadas as 22 folhas ampliadas por pranchas de contato, com conferência detalhada das folhas conceitual 01 e lógico 01/06 em resolução nativa, incluindo DADOS_FORMA_JOGO (17 campos) e POKEMON_COLECAO (13 campos). As duas visões gerais também foram inspecionadas. Todos os 24 PNG são exportações do renderizador oficial. Texto nativo de 15 px (títulos conceituais 17 px), sem cortes de atributos nos painéis ampliados. Atributos conceituais e seus traços de ligação seguem os símbolos e a renderização do brModelo.

A inspeção revelou e corrigiu o limite de tela de 4096 px do brModelo: a visão geral usa cinco colunas e seis linhas, mantendo os objetos dentro da área editável. Os vínculos gerais passam por corredores entre entidades. Cardinalidades de vínculos que compartilham um participante podem se sobrepor na visão geral; cada vínculo tem sua folha ampliada sem essa ambiguidade, que deve acompanhar a apresentação/impressão. As folhas parciais preservam ícones FK de campos cujos outros vínculos aparecem em outra folha; os arquivos completos contêm todas as relações.

Verificação estrutural independente: `python docs/diagrams/tooling/check_models.py` → 26 entidades, 183 campos, 43 relações; todos os hashes conferem. Cada arquivo `.brM3` foi reaberto pelo carregador oficial, conforme `reopen-verification.txt`.

## Metadados do arquivo nativo

A revisão de publicação identificou os padrões de fábrica `autor` e `data` em `controlador.apoios.GuardaPadraoBrM`. São valores fixos sobre o autor da ferramenta e uma data histórica; não foram extraídos do usuário ou do sistema operacional. Os 24 invólucros foram atualizados pelos campos públicos para `autor=Pokelizer project` e `data=` (vazio), mantendo intacto o payload serializado do diagrama. O carregador oficial reabriu novamente os 24 arquivos. A varredura dos binários não encontrou o nome de autor anterior, a data padrão anterior, nome do usuário do sistema ou caminhos `/home/`. Os hashes de todos os XML e PNG permaneceram idênticos; não houve alteração visual. O manifest e o verificador incluem o novo estado.
