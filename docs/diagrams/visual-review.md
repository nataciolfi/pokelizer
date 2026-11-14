# Revisão visual — 13/11/2026

Foram inspecionadas as 22 folhas ampliadas por pranchas de contato, com conferência detalhada das folhas conceitual 01 e lógico 01/06 em resolução nativa, incluindo DADOS_FORMA_JOGO (17 campos) e POKEMON_COLECAO (13 campos). As duas visões gerais também foram inspecionadas. Todos os 24 PNG são exportações do renderizador oficial. Texto nativo de 15 px (títulos conceituais 17 px), sem cortes de atributos nos painéis ampliados. Atributos conceituais e seus traços de ligação seguem os símbolos e a renderização do brModelo.

A inspeção revelou e corrigiu o limite de tela de 4096 px do brModelo: a visão geral usa cinco colunas e seis linhas, mantendo os objetos dentro da área editável. Os vínculos gerais passam por corredores entre entidades. Cardinalidades de vínculos que compartilham um participante podem se sobrepor na visão geral; cada vínculo tem sua folha ampliada sem essa ambiguidade, que deve acompanhar a apresentação/impressão. As folhas parciais preservam ícones FK de campos cujos outros vínculos aparecem em outra folha; os arquivos completos contêm todas as relações.

Verificação estrutural independente: `python docs/diagrams/tooling/check_models.py` → 26 entidades, 183 campos, 43 relações; todos os hashes conferem. Cada arquivo `.brM3` foi reaberto pelo carregador oficial, conforme `reopen-verification.txt`.

## Metadados do arquivo nativo

A revisão de publicação identificou os padrões de fábrica `autor` e `data` em `controlador.apoios.GuardaPadraoBrM`. São valores fixos sobre o autor da ferramenta e uma data histórica; não foram extraídos do usuário ou do sistema operacional. Os 24 invólucros foram atualizados pelos campos públicos para `autor=Pokelizer project` e `data=` (vazio), mantendo intacto o payload serializado do diagrama. O carregador oficial reabriu novamente os 24 arquivos. A varredura dos binários não encontrou o nome de autor anterior, a data padrão anterior, nome do usuário do sistema ou caminhos `/home/`. Os hashes de todos os XML e PNG permaneceram idênticos; não houve alteração visual. O manifest e o verificador incluem o novo estado.

## Revisão da Etapa 2 — 13/11/2026

Foram abertas novamente as duas imagens integrais, as 22 pranchas por contato e amostras de campos a 100% (conceitual 01 e lógico 06), as dez novas visões de domínio e o PNG de UML. A primeira versão dos recortes tinha relações sobre caixas em atributos/perfis; foi rejeitada visualmente e regenerada com posições explícitas. A versão revisada aproxima conceitos por domínio, usa nomes por papel e elimina cruzamentos de linhas entre relações nas cinco visões conceituais. Em coleção, origem e contexto atual têm caminhos separados. Nas visões lógicas, cardinalidades nativas e legendas identificam o papel; mostram somente identidades, não a lista integral de campos.

Os completos foram reordenados por domínio e seus corredores separados. Ainda são densos, com cardinalidades próximas em entidades muito conectadas. Não são a única evidência de legibilidade: para a apresentação, as visões de domínio são a entrada principal e as pranchas R trazem todos os atributos e cada relação isolada. Essa limitação visual permanece explícita; consistência automática não é prova de legibilidade.

O SQL não mudou: 26 entidades, 183 campos, 43 FKs. Os 34 `.brM3` foram reabertos pelo carregador oficial após gravação e limpeza de metadados. Os arquivos nativos/XML completos e as pranchas ampliadas foram preservados e atualizados. As visões extras são recortes com os mesmos nomes de entidades, sem novas tabelas. O UML mostra 15 classes efetivamente implementadas, com métodos conferidos por AST; fonte, PNG e SVG foram regenerados. Revisão visual: textos e caixas completos, sem sobreposição de métodos ou corte de campos selecionados.
