# Continuidade do Pokelizer

## Estado atual — 17/11/2026

Pesquisa Scarlet/Violet: a [lista Bulbapedia, revisão 4595454](https://bulbapedia.bulbagarden.net/w/index.php?title=List_of_Pok%C3%A9mon_in_Pok%C3%A9mon_Scarlet_and_Violet&oldid=4595454), afirma 771 espécies compatíveis e indica versão de inclusão; a listagem trata o par de jogos em conjunto e não comprova método, exclusividade ou origem de cada exemplar. Extração preliminar de 733 linhas de formas sem nome explícito foi salva em `/tmp/pokelizer-sv-research/default-species.csv` para revisão, não integrada nem validada como catálogo completo. Identidades com variantes nomeadas exigem mapeamento manual, e lista por espécie não prova a forma padrão. O repositório público `Scotts-Thoughts/pokemon-data`, commit `96107bb60fc031b699602483ce67fe201443af1d`, foi clonado em `/tmp/pokelizer-source-pokemon-data`; seu README declara ausência de encontros selvagens para Scarlet/Violet e não apresenta licença para redistribuição. Nenhum dado dessa fonte foi incorporado. Próximo passo: confrontar formas e disponibilidade por versão com fontes específicas e fixar um extrato licenciado antes de habilitar registro.

O painel do catálogo foi verificado em Brave headless com Flask e banco descartável: `raichu-alola` exibiu Electric/Psychic, seis atributos, habilidades não aplicáveis e fonte GO Park; `charizard-mega-x` exibiu transformação temporária, condição e botão de registro desabilitado. A captura Mega foi aberta e inspecionada; em 390 px a página mediu `scrollWidth=390`. Os processos foram encerrados. A revisão integral por teclado/leitor de tela e a cobertura contextual dos demais jogos permanecem pendentes.

O fetch HTTPS funcionou com `GIT_EXEC_PATH=/home/Danilo/tools/git/usr/lib/git-core` fora da restrição de DNS. As árvores local e remota eram idênticas; a branch local foi alinhada a `8e7a233886bf1570a49ddbcaf708a7e48cd19bc0`, preservando a cadeia anterior na tag `final-session-history-2026-11-17-01`. Um clone limpo da branch em `/tmp/pokelizer-repro-20261117` executou `PYTHONPATH=/home/Danilo/tools/python:backend python tools/check_stage2.py`: 110 testes passaram em 161,15 s, além de SQL, dicionário, brModelo, UML, 257 links e demonstração. Usou dependências portáteis preexistentes; não comprova instalação nova das dependências. Próximo passo: ampliar cobertura de dados, completar QA do navegador e atualizar a documentação de entrega.

Auditoria da árvore remota identificou dois arquivos truncados durante a publicação pelo conector: `backend/tests/test_catalog_data.py` e este checkpoint. Foram reenviados em blocos completos e o commit remoto `d77e4b8d3c5a1e5282b3370dd6eb5ced56c9521c` restaurou a árvore `de337335a7086878085bc0ef10f417238a327891`, idêntica à árvore local do commit `88c5936`. A branch remota avançou sem force. Os commits locais e remotos têm históricos com SHAs distintos; não sincronizar refs sem reconstruir e conferir os objetos. Próximo passo: confirmar clone remoto, alinhar histórico local com segurança e continuar cobertura contextual e QA no navegador.

O marco Mega foi publicado na branch remota em `3022ab62e721201187652f995d0568104bf19d3e`; o commit local equivalente é `50d3134dcba80012f18d01de108536594aaa7d88`. Os hashes diferem porque o conector recriou os commits; as referências locais ainda não estão sincronizadas. Correção em andamento: a API agora informa habilidades como não aplicáveis também nas fichas Let’s Go de disponibilidade e Mega. Testes focados de formas comuns, Alola, Mega e parceiros: 2 passaram. Próximo passo: registrar a correção e publicar na branch remota, reconstruindo objetos locais ou usando Git com transporte HTTPS funcional; continuar QA visual e cobertura dos demais jogos.

Branch `final/complete-project`; o marco Alola está publicado no GitHub em `1a7f07166ef7883b7ed7e38e838191b49db60229` (cópia local equivalente `0c03fe662d323e1262212a75d00c4dc4d81f9caf`, diferente apenas nos metadados do conector). O objeto local e `origin/final/complete-project` precisam ser alinhados ao SHA remoto antes do próximo commit. O marco Mega de Let’s Go está em trabalho local. Não alterar `main`.

### Disponibilidade transferível em Let’s Go

A disponibilidade cobre 153 espécies padrão e 18 formas Alola via GO Park; o novo marco local registra ainda as 15 formas Mega por versão como transformações de batalha temporárias. As Mega têm fichas não registráveis e relações `TRANSFORMACAO_FORMA` com base, item e condição, sem virar exemplares da coleção. Tipos/estatísticas são do snapshot PokeAPI fixado e historicamente resolvidos para a geração VII. Três CSV curados validam hash e escopo; conflitos abortam em transação. A fonte Bulbapedia é dinâmica, sem revisão estável recuperável; data, atribuição e licença CC BY-NC-SA estão documentadas.

Banco vazio e importação repetível: 1.025 espécies, 1.579 formas, 53 jogos, 7.612 fichas, 37 mecânicas (11 parciais), 7.594 com tipos e estatísticas-base, 340 fichas/métodos GO Park, 2 Poké Ball Plus e 30 relações temporárias Mega. Cada Let’s Go contém 187 fichas, todas com tipos/estatísticas com fonte. `coverage-final.json` foi regenerado. Importação duas vezes: `integrity_check=ok`, zero FKs inválidas. A API da forma-base mostra destino, temporariedade e condição. Fonte/hash alterados abortam e preservam ficha e relação. `PYTHONPATH=/home/Danilo/tools/python:backend python tools/check_stage2.py`: 110 testes passaram; SQL/dicionário/brModelo/UML/links/demonstração passaram.

`PYTHONPATH=/home/Danilo/tools/python:backend python tools/check_stage2.py` passou 110 testes; SQL, dicionário, brModelo, UML, links e demonstração passaram. No Brave com banco limpo: conta, filtro Pikachu, exemplar do parceiro (IV HP 31, AV HP 0, seis EV não aplicáveis), perfil AV HP 200 e comparação -200; em 390 px, `scrollWidth=390`. A consulta detalhada do parceiro no card fez requisição API, mas o roteiro de extração de texto não confirmou a renderização da seção; esse detalhe permanece pendente de verificação visual/ajuste.

No navegador, o servidor iniciou e recebeu os assets e Fetch do catálogo. A primeira consulta DevTools por forma Alola falhou por sintaxe inválida no roteiro; a correção acionou um segundo pedido de escalonamento cuja revisão automática excedeu o prazo. Por isso, a renderização visual do detalhe Alola segue sem comprovação (a API e os testes passaram). As imagens antigas registram a tela de detalhe do Pikachu, mas não contam como validação Alola.

Próximo passo: publicar esse marco. A renderização visual de detalhes Mega/Alola segue sem comprovação. Depois ampliar Scarlet/Violet, regulamentos/perfis, outras versões com fichas zero e revisão completa de teclado/leitor de tela. Não declarar conclusão.

---

## Estado atual — 16/11/2026

Branch `final/complete-project`, commit atual publicado `0c1a59a7cd34510319f4f7a95e80ed2ffac1a467`, árvore `cd04c6dfea93f6a0ac4c8f5d81285f77c2b18c1f`. A tag `final-session-history-2026-11-16-09` preserva o commit local original `273e32e` antes do alinhamento de metadados do conector; árvores são idênticas. Não mexer em `main`. Continuação da auditoria: `AGENTS.md` ausente; os arquivos da Etapa 1 e as 73 provas anteriores foram preservados. As tarefas completas e pendências detalhadas continuam nos registros abaixo.

### Regras, estatísticas e valores de Let’s Go

Foram adicionadas mecânicas parciais independentes para `lets-go-pikachu` e `lets-go-eevee`: natureza, nível 1–100, IV 0–31 por atributo, AV (Awakening Values) 0–200 por atributo e EV marcado `nao_aplicavel`. A aplicação preserva zero, desconhecido e não aplicável. Os dois parceiros iniciais têm estatísticas-base próprias e ficha distinta; a importação confronta seus seis valores com a tabela histórica da Bulbapedia e mantém Pikachu/Eevee comuns distintos. A ficha comum usa estatísticas históricas PokéAPI, sem alegar que a disponibilidade de cada forma em Let’s Go foi completamente catalogada. Valores de IV conhecidos do parceiro documentado são validados como 31. Reimportação não sobrescreve curadoria conflitante.

Banco vazio aplicou migrações `[1, 2, 3, 4]`; duas importações mantiveram 1.025 espécies, 1.579 formas, 53 jogos, 7.472 fichas e 37 mecânicas; `integrity_check=ok`, `foreign_key_check=[]`. Cobertura: 7.454 tipos, 7.454 estatísticas com fonte, 493 fichas de Especial único, 14.220 vínculos de habilidade potencial e 11 mecânicas parciais. As duas versões Let’s Go têm 117 fichas cada com tipo e estatísticas-base, incluindo o parceiro; isso não significa disponibilidade total (há 1 ficha de parceiro documentada por versão, 116 formas padrão do conjunto de referência e alternativas ainda sem curadoria específica). `docs/project/coverage-final.json` foi regenerado.

`PYTHONPATH=/home/Danilo/tools/python:backend python tools/check_stage2.py`: 109 testes passaram; SQL, dicionário, modelo nativo brModelo, UML, links e demonstração passaram. Brave headless + Flask em banco temporário: conta, catálogo, exemplar do parceiro (IV HP 31, AV HP zero, EV não aplicável), perfil com AV HP 200 e análise -200. Foram inspecionadas imagens 1440 px e 390 px; a página móvel mediu 390 px sem overflow horizontal. O detalhe contextual dentro do painel do catálogo ainda não foi validado nessa execução automatizada; API e integração de dados são exercitadas em testes. Detalhe registrado em `docs/project/frontend.md`.

Próximo passo: continuar fonte/abrangência para outros contextos, melhorar revisão integral de acessibilidade do frontend e completar os dados por jogo/regulamentos/perfis. As alterações deste marco estão commitadas e publicadas na branch dedicada. Não declarar entrega final: cobertura contextual permanece parcial. Convite/aceitação do professor e submissão no Classroom são ações manuais autorizadas apenas pelo usuário.

---

## Base auditada em 13/11/2026

Branch de trabalho: `stage2/functional-delivery`, derivada de `stage1/reconciled-architecture` em `91875bd`. Árvore inicial limpa; nenhuma instrução AGENTS.md encontrada no repositório ou ancestrais. Remoto consultado pelo conector GitHub: não há commits posteriores; `main=f0e570b` está atrasada. Auditorias divergentes já reconciliadas na base; não fazer merge indiscriminado.

Documento local `Projeto_Integrado_Etapas_GitHub.docx` lido: Etapa 1 09/11, Etapa 2 13/11, final 17/11/2026. Usuário informou três dias para Etapa 2; divergência registrada, sem alterar datas do professor. Escopo completo mantido, sem tratar como MVP.

Baseline: 45 testes passaram (`PYTHONPATH=/home/Danilo/tools/python:backend python -m pytest backend/tests -q`). Ambiente tem ferramentas portáteis em `/home/Danilo/tools`: Git, Java, brModelo, PlantUML e dependências Python. `git` não está no PATH padrão; `.venv` herdada não contém as dependências neste runtime. Rede de shell sem DNS; conector GitHub funciona. Usar caminhos portáteis neste ambiente, instalação convencional documentada para outro computador.

Confirmado: coleção sem edição, atributos enviados ignorados, perfis sem HTTP CRUD, analisador ausente, busca sem codigo_forma, catálogo por ficha repete identidades. SQL/migrações e DAOs existentes serão preservados onde corretos. Imagens gerais abertas visualmente: muitos corredores sobrepostos, nomes genéricos e entidades distantes; precisa melhorar além da verificação estrutural.

## Em execução

1. CRUD transacional de coleção/atributos e perfis, validação estrita, comparação contextual e elegibilidade.
2. Catálogo global com fichas por jogo, códigos e filtros; carga real reproduzível com cobertura e fontes.
3. Diagramas nativos por domínio, UML atualizado, documentação e demonstração.
4. Após verificar Etapa 2: interface nova HTML/CSS/JS Fetch e integração; completar cobertura do catálogo.

## Pendências de entrega manual

Confirmar conta do professor usando o contato do documento original, convidar em Settings → Collaborators e verificar aceitação. Anexar arquivos ao Classroom e confirmar envio. Não houve convite nem submissão externa.

## Próximo passo

Implementar e testar serviços/DAOs/rotas da Etapa 2. Antes de retomar, ler este arquivo e conferir Git/árvore real. Nenhuma entrega foi declarada pronta.

## Implementado e testado nesta sessão

- Backend: PATCH privado da coleção; valores incluídos/consultados/substituídos na transação do exemplar; rollback de pai/filhos; mudança de contexto exige valores explícitos.
- CRUD de perfis personalizados, preferências de natureza/habilidade, alvos e autorização no DAO/serviço. Referências compartilhadas são somente leitura.
- Comparação com contexto exato, estados por campo, ausência/zero/desconhecido/não aplicável, diferenças sem pontuação; elegibilidade de forma com fonte e escopo limitado.
- Busca por codigo_forma/número/nome; listagem agrupada por identidade, fichas por jogo aninhadas e filtros no mesmo contexto; detalhe global e contextual.
- Corpos JSON e campos inválidos rejeitados; endpoints de opções e regras para clientes.
- Snapshot real PokéAPI fixado em `8a92bfa7dab2f12b84b5d151562f9857c133ff30`, fontes e SHA-256; importação transacional repetível sem sobrescrever conflitos, relatório de cobertura e downloader para novo destino.
- `PYTHONPATH=/home/Danilo/tools/python:backend python -m pytest backend/tests -q`: **69 passaram**. Inclui preservação de dados privados e conflitos na carga real. Esquema/migrações 001 não foram alterados.

Próximo passo em andamento: regenerar/revisar diagramas e UML. Depois documentar demonstração limpa e executar verificação completa. Interface Fetch e cobertura factual por jogo continuam obrigatórias. Não confundir cobertura global do snapshot com cobertura de fichas/mecânicas/regulamentos.

## Verificação consolidada da Etapa 2

`python tools/check_stage2.py` com PYTHONPATH portátil: **69 testes passaram** (7,60 s); SQL gerado, dicionário, 26 entidades/183 campos/43 relações brModelo, 15 classes UML e 245 links locais conferidos. Demonstração HTTP completa concluída em banco temporário. Saída em `docs/stage2/verification-result.txt`.

CLI em banco vazio: `db-init` → `[1]`, `db-upgrade` → nenhuma migração, carga offline → 1.025 espécies, 1.579 formas, 51 jogos. Fichas/mecânicas/regulamentos reais: **zero**, sem alegação de cobertura contextual. `docs/stage2/coverage.json` e `backend/data/README.md` detalham fontes e lacunas. Banco anterior preservado.

Revisão visual: abertas imagens integrais, dez visões por domínio, 22 pranchas por contato e amostras a 100%, além de UML. Recortes iniciais com sobreposição foram corrigidos; completos reordenados por domínio continuam densos e acompanham visões legíveis e pranchas. 34 brM3 reabertos oficialmente. Roteiro/instalação/API em `docs/stage2/README.md` e `backend/README.md`.

Próximo passo: interface nova HTML/CSS/JS com Fetch no Flask e QA de navegador. Skill Sites lida para fluxo local; nenhuma hospedagem criada. Permanecem curadoria contextual real, colaboração/aceite do professor e anexos Classroom. Commits locais serão publicados em branch dedicada pelo conector GitHub, pois o shell não resolve DNS.

## Interface após consolidação do backend

Nova interface em `backend/pokeanalyzer/templates/index.html` e `static/app.css`/`app.js`, servida na raiz do Flask. Fluxos Fetch implementados: catálogo/filtros/detalhes, conta, coleção/origem/valores, perfis/preferências, análise e elegibilidade. Sem dependências externas de UI; design novo, responsivo por CSS, acessibilidade básica de labels/foco/dialog/live regions. Há endpoint público de cobertura e teste de entrega do template/assets.

**Bloqueio de QA visual da interface:** abrir servidor local falhou por `PermissionError: Operation not permitted` em socket.bind; Brave headless encerrou com `setsockopt: Operation not permitted`. Os testes HTTP do Flask não equivalem a QA de navegador. Não declarar interface definitiva/ponta a ponta pronta. Roteiro para concluir em ambiente sem esse bloqueio: `docs/project/frontend.md`.

Próximo passo: repetir verificação consolidada, publicar commits/artefatos em branch dedicada sem alterar main, registrar hashes remotos. Cobertura factual por jogo e QA real no navegador permanecem pendentes, além de convite/aceitação do professor e anexos Classroom.

Verificação após interface: `python tools/check_stage2.py` passou integralmente: **70 testes**, SQL/dicionário/brModelo/UML, links locais e demonstração. `git diff --check` sem erros. Esse resultado comprova backend/entrega de assets, não a execução do JavaScript no navegador, que permanece bloqueada.

## Revisão final de evidência

Corrigida a projeção das fontes: a evidência global da forma não sobrescreve a evidência específica da ficha/jogo. Catálogo global, fichas aninhadas e detalhe mantêm ambas identificadas; regressão cobre fontes/datas diferentes. Token CSRF inválido com caracteres não ASCII agora retorna 403, sem TypeError. Verificação consolidada: **72 testes passaram**, diagramas/SQL/UML/links e demonstração também. Classes/métodos e estrutura SQL permanecem os mesmos; campos de fonte opcionais são projeções de colunas já existentes.

## Continuação em 14/11/2026

Revisão da carga: formas alternativas recebem categoria `nao_verificada`, em vez de herdar `padrao` do SQL sem evidência. Reimportação detecta divergência com categorias já curadas e aborta preservando a base, sem sobrescrever silenciosamente. Regressões verificam as categorias de todas as formas do snapshot e a preservação de curadoria. Verificação consolidada: **73 testes passaram**; demais checks e demonstração passaram. README agora aponta a interface já escrita e seu QA pendente.

## Publicação e ponto de retomada

Branch remota: `stage2/functional-delivery`, disponível no GitHub. O conector publicou a mesma árvore de cada commit local; cada blob binário e cada árvore foram comparados por SHA. O histórico remoto usa metadados do conector, por isso os hashes de commit diferem dos primeiros commits locais. Mapeamento em `docs/project/published-commits.json`; árvores e conteúdo são idênticos. O checkpoint de código/curadoria publicado é `5706f6c98edcc72f9b88900bd5a0b0fe07ef81bd`; esta nota de continuidade é um commit documental posterior.

Para evitar divergência na retomada, o checkout será alinhado ao histórico remoto conferido, preservando o histórico inicial sob a tag local `stage2-session-history-2026-11-14`. Ler o Git real e este arquivo antes de continuar. `main`, branches anteriores e banco pessoal não foram alterados. Os artefatos para Classroom são uma exportação dos arquivos versionados, fora do repositório, sem banco pessoal, .git ou .venv.

Estado final verificado: backend funcional com **73 testes**, checks de SQL/dicionário/brModelo/UML/links e demonstração passados. Não há migração nova: 001 permanece imutável. Diagramas nativos e pranchas revisados visualmente, UML com 15 classes reais. Dados reais: 1.025 espécies/1.579 formas/51 jogos do snapshot; fichas/mecânicas/regulamentos/referências competitivas reais permanecem pendentes de curadoria e fontes específicas. Interface Fetch já escrita, porém QA visual/ponta a ponta bloqueado pelas permissões de socket/IPC deste ambiente.

**Próximo trabalho obrigatório:** completar cobertura contextual com fontes e relatório; testar a interface em navegador num ambiente que permita servidor local e corrigir o que for encontrado. Roteiro em `docs/project/frontend.md`. A entrega final do projeto não foi declarada pronta. Confirmar prazo de regularização, conta/acesso/aceite do professor e envio/anexos Classroom manualmente, conforme `docs/stage2/README.md`. Nenhum convite, submissão Classroom, merge em main ou hospedagem foi realizado.

## Retomada do objetivo final

Branch `final/complete-project`, base remota conferida `1f5d84e`; árvore inicial limpa, sem AGENTS.md encontrado. O servidor local e o Brave headless foram executados com permissão apropriada em banco temporário sintético. O roteiro no navegador criou conta, exemplar com zero, perfil com alvo 2 e comparação com diferença -2; desktop e largura 390 px inspecionados, sem overflow horizontal ou exceções JS nessa execução. A primeira tentativa do roteiro fez duas alterações de contexto simultâneas e falhou por corrida; foi repetida aguardando cada carregamento. Persistem testes de teclado, erro, exclusão, isolamento e fluxos com dados reais, além de eventuais corridas com interações rápidas.

Importação contextual em implementação: encontros PokéAPI do commit fixo, compactados com hashes dos bytes originais e do gzip, somente Pokémon com uma única forma não temporária. Índices internos não foram aceitos como prova de presença. Red/Blue e suas versões japonesas foram excluídos pela colisão dos nomes de jogo no esquema herdado, até implementar identidade de versão sem ambiguidade. Contextos preexistentes não são sobrescritos. Fontes e limitações em `backend/data/README.md`. Tipos, habilidades, estatísticas por geração, mecânicas, regulamentos e perfis com fonte ainda precisam de curadoria. Não há conclusão do objetivo ainda.


### Marco: encontros reais e revisão inicial da interface

A importação em banco vazio agora gera **5.072 fichas** de encontros selvagens documentados, além de 1.025 espécies, 1.579 formas e 51 jogos. A fonte é o CSV de encontros fixado, cruzado com métodos e grupos de versão; presentes, trocas, eventos, linhas inconsistentes, formas ambíguas e versões com nomes Red/Blue duplicados foram excluídos. Fichas existentes são preservadas. A cobertura atual está em `docs/project/coverage-final.json`. Método disponível e fonte são gravados; tipos, atributos-base, habilidades, mecânicas e regulamentos reais continuam pendentes. Os sprites são referenciados somente quando há mapeamento inequívoco e sua situação de direitos está documentada.

O fluxo navegador sintético descrito em `docs/project/frontend.md` foi executado contra Flask/Brave local com permissão concedida; tela desktop e celular revisadas. Correção evita alteração de seletores enquanto o contexto é carregado. A verificação consolidada `python tools/check_stage2.py` passou **76 testes**, incluindo busca, inclusão de Pikachu/Gold e repetição da importação, além dos checks de modelos e demonstração.

Próximo passo: confirmar e carregar mecânicas reais com fontes, dados históricos de tipo/estatísticas e habilidades; ampliar cobertura de jogos sem mesclar versões homônimas; testar fluxo real e isolamento no navegador, atualizar os modelos e executar a suíte integral. O objetivo permanece ativo.

### Marco: regras reais de Sword e Shield

A carga agora cria duas mecânicas separadas para os jogos Sword e Shield, com as 25 naturezas da PokéAPI, nível de 1 a 100 e limites de IV (0–31) e EV (0–252 por atributo, 510 no total), com fontes e data registradas. O rótulo `regras-gerais-documentadas` não afirma número de patch ou equivalência com outros jogos. Teste com Pikachu/Sword cria exemplar e perfil reais, compara IV 0 e um alvo menor de EV, rejeita 32 IV, 253 EV e soma 511, e confirma rollback. A reimportação aborta ao detectar regra curada conflitante sem sobrescrevê-la. Mapeamento de sprite usa tanto número da espécie quanto código de forma, para não atribuir imagem de outra espécie com código coincidente.

Banco vazio: 1.025 espécies, 1.579 formas, 51 jogos, 5.072 fichas documentadas de encontro, **2 mecânicas**, zero regulamentos/elegibilidades. Suíte `python tools/check_stage2.py`: **78 testes passaram**; modelos/SQL/UML/links e demonstração passaram. Tipos, habilidades, estatísticas-base por jogo, outros contextos de mecânica, regras competitivas, acessibilidade por teclado, duas sessões no navegador e inspeção visual do modelo geral continuam pendentes. Próximo passo: importar tipagens históricas respaldadas pela PokéAPI para Sword/Shield e ampliar o fluxo real em navegador.

### Marco em andamento: fontes contextuais independentes

Branch `final/complete-project`, último commit publicado `9a00bed`. A migração 002 acrescenta fonte/data independentes para tipos e estatísticas, sem alterar 001 ou atribuir fonte aos dados antigos. A carga de Sword/Shield aplica alterações históricas por geração da PokéAPI às fichas de encontro já confirmadas e preserva valores previamente curados. Banco vazio: 5.072 fichas de encontro, das quais 364 têm tipos e estatísticas com fonte; 970 vínculos de habilidade com fonte. Reimportação e migração de base 001 testadas. A consulta de ficha na interface mostra tipos, estatísticas, habilidades e respectivas fontes. Relatório em `docs/project/coverage-final.json`.

`PYTHONPATH=/home/Danilo/tools/python:backend python tools/check_stage2.py`: **82 testes passaram**, além de SQL, dicionário, modelos, UML, links e demonstração. CLI de banco temporário aplicou `[1, 2]`, carregou o snapshot e repetiu upgrade sem alterações. Em Brave/Flask local com base temporária, Pikachu/Sword, conta, exemplar IV 0, perfil alvo 2 e comparação -2 passaram; detalhes em `frontend.md`. As duas imagens gerais e prancha conceitual 01 foram abertas; os campos novos aparecem, mas cardinalidades gerais continuam sobrepostas. Arquivos brModelo reabertos: 26 entidades, 187 campos, 43 relações.

Próximo passo: registrar e testar regulamentos reais e elegibilidade com fonte oficial, ampliar cobertura contextual, revisar legibilidade das imagens gerais e testar teclado/isolamento/erros no navegador. Permanecem zero regulamentos e perfis de referência reais neste marco; o objetivo não está concluído. Uma fonte oficial de Sword/Shield Season 36 / Series 14 foi localizada em https://www.pokemon.com/us/pokemon-news/pokemon-sword-and-pokemon-shield-ranked-battles-november-2022-season-season-36/; a elegibilidade depende também de condições de origem e a lista por espécie não deve ser confundida com prova para todas as formas.

### Regulamento real parcialmente coberto

O marco anterior foi publicado na branch `final/complete-project` como `12a97b2599f374e653b7741be5ff8d7b45e8322c`, com árvore conferida; histórico local original salvo na tag `final-session-history-2026-11-14-03`. A carga agora inclui dois registros da temporada 36 / Series 14, um por jogo, e 353 avaliações **condicionais** para formas padrão com encontro documentado e espécie nas faixas regionais da fonte oficial, cruzadas com dois CSVs PokéAPI fixados. Não determina legalidade completa; espécies suplementares e outras formas permanecem não verificadas. A reimportação detecta conflito sem sobrescrever, e o endpoint rejeita cruzar jogos. Em banco vazio, `db-init` aplicou `[1, 2]`; carga e repetição passaram. `python tools/check_stage2.py` passou **83 testes** e todos os checks/documentação/demonstração.

Próximo passo: preparar perfil de referência com distribuição explicitamente documentada (guia VGC em https://www.vgcguide.com/ev-training descreve Dragapult em Sword/Shield com EV de ataque 252, velocidade 252 e HP 4), sem inventar outros alvos, e obter evidência apropriada para a ficha contextual. Persistem cobertura por jogo, perfis adicionais, diagramas gerais sem sobreposição e testes de teclado/isolamento no navegador. Não declarar o projeto concluído.

### Perfil de referência e nova verificação em navegador

O marco do regulamento foi publicado em `791b2d352cd5e387d45644262fa6780ae1552998` na branch `final/complete-project`; árvore local alinhada, commit original preservado na tag `final-session-history-2026-11-14-04`. O guia VGC citado documenta criação de Dreepy para Dragapult em Sword/Shield e distribuição ofensiva; a carga adiciona duas fichas e dois perfis somente leitura com EVs ataque 252, velocidade 252 e HP 4, sem inventar natureza, habilidade ou outros alvos. Fontes da ficha, do perfil e das estatísticas são distintas. Banco vazio: 5.074 fichas (5.072 encontros + 2 do guia), 366 com tipos/estatísticas, 976 vínculos de habilidade, 2 mecânicas, 2 regulamentos, 355 elegibilidades condicionais, 2 perfis de referência. Reimportação é repetível; não adota automaticamente ficha existente de outra fonte.

`python tools/check_stage2.py` passou **84 testes**, mais modelos/SQL/UML/links e demonstração. Em Brave com dados reais e contas sintéticas, a referência mostra fonte e alvos; Escape fecha o diálogo. A tentativa de comparação incompatível mostrou erro, e a comparação compatível passou. Duas contas ficaram isoladas e a primeira excluiu seu exemplar e perfil pela interface, sem exceções JS. Uma tentativa inicial usou porta 5060 reservada; outra enviou Enter via automação sem fechar o diálogo: Escape foi confirmado, mas resta investigar Enter e revisar a navegação completa por teclado. O navegador e o banco usados são temporários.

Próximo passo: investigar ativação por Enter, melhorar as imagens gerais dos modelos, ampliar cobertura contextual e referências com fontes. A cobertura de encontros é parcial e os jogos Red/Blue homônimos seguem sem importação contextual; não declarar o projeto concluído.

Enter no botão focado foi repetido com o evento completo do navegador e fechou o diálogo; a tentativa anterior não enviava o caractere. Permanece pendente navegar por todos os fluxos usando apenas teclado e verificar contraste dos estados.

### Retomada em 15/11/2026 — modelos completos

Estado inicial da retomada: branch `final/complete-project` sincronizada com `origin` em `82415d9720a94d535be8b2b1822db52e52c22411`; a alteração local dos modelos lógicos era trabalho em andamento da sessão anterior. O relatório de cobertura continua registrando 5.074 fichas, 366 com tipos/estatísticas, 976 vínculos de habilidade, duas mecânicas, dois regulamentos, 355 elegibilidades condicionais e dois perfis de referência. Esses dados são parciais e o objetivo permanece ativo.

As duas visões completas do brModelo foram reorganizadas em uma cópia temporária antes de atualizar os arquivos nativos e as imagens. Cardinalidades foram distribuídas acima das entidades e conexões encaminhadas por corredores; as caixas ficaram mais estreitas para abrir espaço ao redor dos relacionamentos. As duas imagens e recortes a 100% foram inspecionados, e os modelos foram reabertos pelo carregador oficial. A leitura das cardinalidades melhorou; ainda há muitos corredores compartilhados e é difícil seguir determinados vínculos na visão geral. Pranchas R e visões por domínio continuam complementos necessários. O SQL e a implementação não foram alterados nesta revisão.

Próximo passo: executar as verificações de consistência, registrar/publicar o marco dos diagramas e ampliar dados reais para mais jogos, formas e perfis, com fontes e sem inferir disponibilidade a partir de índices internos. Também falta a revisão completa por teclado e contraste no navegador.

Verificação após reorganização: `PYTHONPATH=/home/Danilo/tools/python:backend python tools/check_stage2.py` passou com **84 testes**, conferência de 26 entidades/187 campos/43 relações, UML, links e demonstração; `git diff --check` passou. A inspeção visual e seus limites estão em `docs/diagrams/visual-review.md`.

### Dados históricos por geração — 15/11/2026

O marco dos modelos foi publicado na branch `final/complete-project` em `13b011271ebe5febe3ebbc834af5905430730fce`, com árvore remota conferida e histórico local anterior salvo na tag `final-session-history-2026-11-15-06`. A carga usa agora os históricos da PokéAPI nas fichas de encontro existentes, com geração proveniente do grupo de versão. Em banco temporário limpo: 5.074 fichas com tipo e fonte, 4.903 com as seis estatísticas e 9.956 vínculos de habilidade com fonte. As 171 fichas da primeira geração não recebem seis estatísticas indevidas; a interface explica que há Especial único ainda não representado. A API e a interface distinguem habilidades não aplicáveis nas gerações I e II das não verificadas; habilidades em outras gerações são apresentadas como potenciais, sem afirmar método de obtenção. O relatório `coverage-final.json` passou a detalhar cada jogo. Nenhuma ficha de presença foi criada a partir de índice interno.

Testes com dados reais conferem Clefairy Gold/X (Normal/Fairy), Magnemite Yellow/Gold (Electric/Electric-Steel), Pikachu Gold, habilidades históricas de Gengar, Pikachu e Poochyena, fonte, não aplicabilidade e preservação de histórico. CLI aplicou `[1, 2]` em banco temporário e duas cargas retornaram relatórios idênticos. No Brave, Magnemite Yellow e Gold mostraram tipos, estados e fontes esperados, sem exceções JavaScript; uma tentativa inicial foi repetida aguardando o Fetch. O objetivo permanece aberto: faltam identidade distinta para versões Red/Blue homônimas, ampliação de presença e dados além dos encontros, mecânicas de outros jogos, mais perfis/regulamentos e revisão completa por teclado/contraste.

A coleção passou a recusar com mensagem explícita contextos cuja presença ou registro independente não estejam confirmados, em conformidade com a regra SQL existente; a interface identifica esse estado e desabilita a inclusão. No navegador, uma ficha `FIXTURE` temporária não verificada exibiu o estado e o botão desabilitado. Um teste de reimportação sobre banco com exemplar e curadoria parcial preservou os dados anteriores sem completar a estatística parcialmente curada.

Verificação consolidada: `PYTHONPATH=/home/Danilo/tools/python:backend python tools/check_stage2.py` passou com **88 testes**, modelos/SQL/UML/links e demonstração. `git diff --check` passou.

### Identidade das versões Red/Blue — 15/11/2026

O marco de dados históricos foi publicado na branch `final/complete-project` em `14f5ead7f22166571cd4196c91de917c35ad9d88`. A migração 003 acrescenta o identificador de versão da PokéAPI sem alterar as migrações existentes, os IDs ou os vínculos anteriores. Red e Blue legados sem identificação permanecem ambíguos e são rotulados assim; quatro versões da fonte recebem identidades distintas. A importação e a seleção do grupo histórico usam o código, e não nomes repetidos. A base limpa passa a conter 53 versões, 5.330 fichas de encontro e duas do guia VGC; 5.332 com tipos, 4.903 com seis estatísticas, 9.956 vínculos de habilidades, duas mecânicas, dois regulamentos e 355 elegibilidades condicionais. Blue japonês não tem encontro cujo grupo de versão seja compatível no snapshot: ausência de ficha não prova ausência no jogo.

Em banco temporário, `db-init` aplicou `[1, 2, 3]`; duas cargas geraram relatórios idênticos e `db-upgrade` não reaplicou migrações. Teste da migração 002→003 preservou usuário, exemplar, ficha e jogo Red de identidade desconhecida; um código já utilizado não pode ser alterado e duplicatas diferindo apenas por caixa são rejeitadas. `integrity_check` retornou `ok` e `foreign_key_check` vazio. `PYTHONPATH=/home/Danilo/tools/python:backend python tools/check_stage2.py` passou **90 testes**, além de SQL, 26 entidades/188 campos/43 relações brModelo, UML, 255 links e demonstração FIXTURE. `git diff --check` passou. As imagens gerais foram abertas; o espaço entre linhas foi aumentado após identificar caixas sobrepostas. Os vínculos continuam densos e as pranchas ampliadas são necessárias.

No Brave, usando Flask em banco temporário limpo, o filtro exibiu quatro versões distintas e Pikachu em `Red (red-japan)` mostrou Electric, Especial único e habilidade não aplicável, sem exceções JavaScript. Uma primeira tentativa de servidor encontrou a porta 5055 ocupada; repetida com sucesso na 5057. As verificações completas por teclado/contraste ainda não foram concluídas. Próximo passo: publicar este marco; depois ampliar mecânicas e cobertura contextual com fontes específicas, contemplar Especial da geração I e concluir QA de acessibilidade. Não declarar o projeto final completo.

### Mecânicas históricas e comparação na interface — 15/11/2026

O marco de versões foi publicado em `c374e80539bb082df84f73e942942979071662bc` na branch `final/complete-project`, com árvore local e remota conferidas; histórico local anterior preservado na tag `final-session-history-2026-11-15-08`. A carga acrescenta regras para 22 versões explicitamente selecionadas das gerações III a VII, além das duas já existentes para Sword/Shield. Cada versão mantém mecânica separada e a geração é conferida no snapshot. Os sistemas registrados com fonte usam IV 0–31; EV 0–255 por atributo nas gerações III–V ou 0–252 nas gerações VI–VII, com total de 510. Let's Go, Legends, expansões e versões não selecionadas continuam sem inferência automática. A lista e as fontes estão em `backend/data/README.md`; o relatório detalha mecânicas por jogo. Reimportação é idempotente e uma regra Ruby divergente reverte a carga sem sobrescrever a curadoria.

`PYTHONPATH=/home/Danilo/tools/python:backend python tools/check_stage2.py` passou **92 testes**, além de SQL, dicionário, 26 entidades/188 campos/43 relações, UML, links e demonstração. Os testes cobrem Ruby EV 255 aceito/256 rejeitado, X 253 rejeitado, contexto incompatível, comparação de 255 com alvo 252 e conflito preservado; `integrity_check` retornou `ok` e não houve falhas de FK. Duas cargas sobre o banco temporário produziram relatórios idênticos. A execução consolidada ficou mais lenta (aproximadamente 10 minutos), sem falhas.

Em Brave/Flask local com conta sintética, um Pikachu em Ruby foi registrado com EV 255, um perfil com alvo 252 foi criado e a análise exibiu diferença 3 sem classificá-la como melhora. A primeira tentativa selecionou um perfil de referência de outro jogo e recebeu erro de incompatibilidade. A interface foi ajustada para listar somente perfis compatíveis com a forma/jogo e mecânica do exemplar; o fluxo passou sem seleção manual. Um exemplar de Magnemite em Yellow sem mecânica mostrou aviso, perfil e botão desativados; ao retornar ao exemplar Ruby, as opções compatíveis reapareceram e o resultado anterior foi apagado. Uma primeira tentativa com Pikachu Yellow falhou por não existir ficha de encontro correspondente no snapshot e foi repetida com Magnemite. Sem exceções JS nas verificações bem-sucedidas. Revisão completa de teclado e contraste continua pendente.

Próximo passo: publicar o marco e ampliar a representação das regras de gerações I/II e outras versões com fontes, sem representar DV/Stat Exp como sistemas modernos; expandir presença, regulamentos e perfis, e concluir QA de acessibilidade. A revisão automática expirou duas vezes quando solicitada a fechar abas locais de teste específicas; o servidor e o navegador temporários lançados nesta etapa foram encerrados e o bloqueio não afeta o projeto. Não declarar o objetivo concluído.

### Mecânicas parciais das gerações I–II — 15/11/2026

O marco anterior foi publicado em `5e40cd670a1f4739ff0f0a74063c1c0d40b80ce4`; árvore alinhada na branch `final/complete-project`, histórico local preservado na tag `final-session-history-2026-11-15-09`. A carga adiciona nove mecânicas explicitamente parciais para as versões identificadas de Red, Blue, Green, Yellow, Gold, Silver e Crystal: nível 1–100 e natureza/habilidade não aplicáveis, com fontes e data. Ainda não permite registrar DV ou Stat Experience: HP DV é derivado e os atributos especiais compartilham valores, portanto não podem ser tratados como seis IV/EV modernos independentes. A interface informa essa lacuna no cadastro e na análise, e indica naturezas/habilidades não aplicáveis. `coverage-final.json` distingue a contagem de mecânicas sem sistemas: 33 no total, das quais nove sem sistemas registrados. Os dados de presença continuam parciais.

Banco temporário vazio aplicou `[1, 2, 3]`; duas cargas geraram relatórios idênticos, `integrity_check` retornou `ok` e não houve falhas de FK. `PYTHONPATH=/home/Danilo/tools/python:backend python tools/check_stage2.py` passou **93 testes**, SQL, dicionário, brModelo, UML, 255 links e demonstração; `git diff --check` passou. Os testes incluem registro de nível, rejeição de natureza e nível inválido, comparação com estados não aplicáveis e ausência de IV/EV indevidos.

Em Brave com servidor e banco temporários, foi criado Magnemite Yellow nível 50, um perfil da mesma ficha e a comparação. Cadastro e análise indicaram a falta de sistemas para entrada e natureza/habilidade não aplicáveis, sem exceções JS. A primeira tentativa começou antes do carregamento inicial e foi repetida com espera; o servidor temporário foi encerrado. A lista conjunta da Pokédex Paldea consultada não distingue a disponibilidade de cada versão Scarlet/Violet, portanto não foi usada como prova de presença por jogo.

Próximo passo: publicar este marco; modelar DV/Stat Experience e Especial com relações corretas e fontes, ampliar presença por versão a partir de dados específicos, adicionar mecânicas e referências faltantes e terminar verificação completa de teclado/contraste. Não declarar o objetivo concluído.

### DV e Stat Experience — 15/11/2026

O marco anterior foi publicado em `f780ea6fb3e9559ad1bc6db703cbe7aeceef1445`; árvore local alinhada na branch `final/complete-project`, histórico local preservado na tag `final-session-history-2026-11-15-10`. A carga das nove mecânicas das gerações I–II agora inclui DV (quatro entradas independentes, 0–15) e Stat Experience (cinco entradas, 0–65.535, sem teto combinado). Especial é compartilhado; DV de HP não é aceito como entrada independente e é derivado na análise somente quando os quatro componentes são conhecidos. A resposta explica o cálculo, preserva ausência, desconhecimento e zero e não declara legalidade da combinação. Limites, dependências e fontes estão em `backend/data/README.md`. Uma colisão prévia do código `special` com outro significado interrompe a importação; dados existentes não são reinterpretados. A cobertura ainda marca as nove mecânicas como parciais por outras lacunas, embora agora tenham sistemas registrados.

Banco vazio aplicou `[1, 2, 3]`, duas importações geraram relatórios idênticos, `integrity_check` retornou `ok` e `foreign_key_check` vazio. `PYTHONPATH=/home/Danilo/tools/python:backend python tools/check_stage2.py` passou **95 testes**, SQL, modelos, UML, 255 links e demonstração. Depois da proteção adicional contra colisão de código, dois testes direcionados passaram, incluindo a nova colisão e a regressão dos DVs. Eles cobrem 15/16, 65.535/65.536, rollback, recusa de HP DV independente, Especial compartilhado, zero, alvo desconhecido, resultado HP derivado 10/5 e preservação de exemplar anterior à adição dos sistemas. A suíte consolidada anterior à última proteção levou cerca de quatro minutos.

Em Brave e Flask local com banco e contas sintéticos, Magnemite Yellow nível 50 foi registrado com quatro DVs e Stat Experience 65.535; um perfil compatível gerou HP derivado 10 contra alvo 5, com explicação. Após editar o DV Especial do perfil para desconhecido, o alvo de HP apareceu como desconhecido em vez de zero. Sem exceções JS; servidor temporário encerrado. A interface também passou a mostrar o estado do alvo ausente/desconhecido na tabela de comparação.

Próximo passo: publicar o marco, representar Especial base da geração I com fonte e migração segura, ampliar presença por versão e as mecânicas de jogos atuais com fontes, e concluir teclado/contraste. Não declarar o objetivo concluído.

### Especial base da geração I — 16/11/2026

O marco de DV foi publicado em `93adb0bbe70ddcd221be3fdfd192791e179a5e84` na branch `final/complete-project`; histórico local anterior preservado na tag `final-session-history-2026-11-15-11`. A migração 004 adiciona `especial_base` opcional sem modificar as anteriores. O snapshot inclui `stats.csv` com hash verificado e o importador cruza o identificador `special` com os valores históricos de geração I; grava cinco estatísticas com fonte apenas quando não há curadoria parcial anterior. A carga de seis estatísticas também se abstém de preencher uma ficha que já tenha `especial_base`. O relatório identifica conjuntos com Especial único e eventuais dados misturados, sem alterá-los.

Banco vazio aplicou `[1, 2, 3, 4]`; duas importações geraram relatórios idênticos. A carga contém 5.332 fichas com estatísticas e fonte, das quais 429 com cinco valores e Especial único e 4.903 com seis valores modernos; nenhuma combinação de sistemas foi detectada. `integrity_check` retornou `ok` e `foreign_key_check` vazio. A migração 003→004 preservou usuário, exemplar, valores existentes e checksums; curadoria parcial não foi sobrescrita. `PYTHONPATH=/home/Danilo/tools/python:backend python tools/check_stage2.py` passou **99 testes**, SQL, dicionário, 26 entidades/189 campos/43 relações brModelo, UML, 255 links e demonstração. Um teste direcionado também confirmou preservação e detecção de dados estatísticos misturados; `git diff --check` passou.

Os modelos nativos foram reabertos e as imagens completas e prancha lógica 01 inspecionadas. A primeira exportação encostava a ficha na próxima tabela e no rodapé da prancha; a altura das caixas lógicas foi ajustada, e as imagens reabertas mostram os campos e o rodapé separados. As visões completas ainda são densas e as pranchas R continuam necessárias. Em Brave com Flask e banco temporário, Magnemite Yellow exibiu HP 25 e Especial 95, e Chansey Yellow HP 250 e Especial 105, com fontes e sem atributos especiais modernos. A primeira tentativa do roteiro fechou sua conexão por erro de indentação; a repetição passou sem exceções JS.

Próximo passo: publicar o marco, ampliar a cobertura de presença e dados por versão com fontes específicas, completar mecânicas/regulamentos e referências ainda ausentes e verificar integralmente teclado e contraste. Não declarar o objetivo completo.

### Métodos de obtenção e presença ampliada — 16/11/2026

O marco anterior foi publicado em `8583432025f7214c8042cd02c4dab2c4867080a0` na branch `final/complete-project`. A carga agora interpreta métodos selecionados de mundo aberto, hordas e outros encontros selvagens, além de presentes e ovos como categorias separadas, usando descrições inglesas do snapshot PokéAPI fixado. Raids, trocas e distribuições especiais continuam fora dessa curadoria. Cada ficha nova traz método, fonte e aviso de que condições detalhadas não foram importadas. Fichas e métodos existentes são preservados sem enriquecimento automático; ausência não comprova indisponibilidade. Habilidades em Let’s Go são marcadas como não aplicáveis com fonte.

Em banco vazio, migrações `[1, 2, 3, 4]`, duas cargas idênticas, `integrity_check=ok` e `foreign_key_check` vazio. A cobertura registrada inclui 7.456 fichas: 7.454 do snapshot e duas do guia VGC; 6.965 com encontro selvagem, 669 com presente e 36 com ovo, com interseções. Há 7.206 fichas com tipos/estatísticas, 33 mecânicas e 617 elegibilidades condicionais. As fichas de Scarlet/Violet seguem ausentes e as de Let’s Go não têm tipos ou estatísticas importados. `PYTHONPATH=/home/Danilo/tools/python:backend python tools/check_stage2.py` passou 101 testes, conferências de SQL, dicionário, 26 entidades/189 campos/43 relações brModelo, UML, 257 links e demonstração. Os testes verificam métodos reais, preservação de exemplar e curadoria; a expectativa antiga de zero fichas em Blue japonesa foi corrigida, pois há seis presentes no cruzamento da fonte.

Em Brave e Flask locais, com banco temporário, Pidgey de Let’s Go exibiu encontro selvagem e habilidades não aplicáveis, Pikachu de Yellow exibiu presente sem classificá-lo como selvagem e Togepi de Gold exibiu ovo; as fontes estavam visíveis e não houve exceções JavaScript. Servidor e navegador temporários foram encerrados. Revisão completa de teclado e contraste continua pendente.

Próximo passo: validar integralmente, publicar este marco, importar fatos específicos e rastreáveis dos contextos ainda incompletos, revisar acessibilidade e completar regulamentos/perfis. Não declarar o objetivo concluído.

### Acessibilidade parcial — 16/11/2026

O marco de obtenção foi publicado em `a37d6449c8e7d67d2c722de9cdde7be16f3ad109`; a árvore local corresponde à remota e a tag local `final-session-history-2026-11-16-02` preserva o commit anterior à sincronização. Corrigidos contrastes detectados em textos de navegação, cartões e etiquetas, nomes acessíveis dos botões de catálogo e ciclo de foco nos diálogos. Em Brave foram executados Tab/Enter/Escape para conta e detalhe de Bulbasaur, incluindo retorno do foco; a medição dos textos visíveis nas telas públicas examinadas não encontrou falhas após o ajuste. Imagens de 1440×900 e 390×844 foram abertas e não havia transbordamento horizontal da página. Sem exceções JS. `PYTHONPATH=/home/Danilo/tools/python:backend python -m pytest backend/tests/test_stage2.py::test_application_serves_integrated_interface_and_coverage -q` passou (1 teste); `git diff --check` passou. A medição não cobre todos os estados/transparências e não substitui auditoria com leitor de tela; falta percorrer formulários privados por teclado.

Uma possível fonte comunitária adicional, PokeDB, descreve exportações de encontros para Scarlet/Violet; o acesso à página retornou 403 e seus termos proíbem coleta por scripts. Nenhum dado foi incorporado. Pode ser avaliada uma exportação manual autorizada, com licença, versões, mapeamento de formas e fonte por versão conferidos; não presumir que uma lista conjunta comprove presença nos dois jogos. Próximo passo: testar e publicar o marco de acessibilidade, avançar nas fontes e nos fluxos privados ainda pendentes.

### Iniciais de Scarlet e Violet — 16/11/2026

O marco de acessibilidade foi publicado em `b1d686c8748d412046e6e7ac122f53944835fcd6`, com árvore local e remota idênticas; a tag local `final-session-history-2026-11-16-03` conserva o commit local anterior à sincronização. A fonte oficial da Pokémon Company confirma Sprigatito, Fuecoco e Quaxly como primeiros parceiros de Scarlet e Violet. Foram incluídas seis fichas com método de presente e fontes independentes para presença, tipos, estatísticas e habilidades potenciais. As duas versões recebem regras independentes de nível, natureza, habilidade, IV e EV com limites documentados. A escolha de um inicial não prova outros métodos nem legalidade completa. Curadoria preexistente permanece intacta.

Banco vazio aplicou `[1, 2, 3, 4]`; duas cargas produziram relatórios idênticos, `integrity_check=ok` e `foreign_key_check` vazio. A carga tem 7.462 fichas e 35 mecânicas, das quais nove parciais; Scarlet e Violet possuem apenas três fichas por versão. O novo teste criou exemplar e perfil Scarlet, comparou EV 252 com alvo 4, rejeitou EV 253 e perfil de Violet, e confirmou reimportação e preservação. A primeira suíte consolidada apontou expectativa antiga da contagem total de mecânicas; ela foi atualizada. `PYTHONPATH=/home/Danilo/tools/python:backend python tools/check_stage2.py` passou 102 testes e todas as verificações de SQL, modelos, UML, links e demonstração. Um teste adicional, executado separadamente, comprovou preservação de contexto curado. `git diff --check` passou.

No Brave com Flask e banco temporário, Sprigatito Scarlet e Fuecoco Violet exibiram tipo, estatísticas, método de presente e fontes, sem exceções JS. Servidor e navegador temporários foram encerrados. A disponibilidade das demais espécies em cada versão continua desconhecida; uma fonte conjunta sem distinção por versão não é suficiente.

Próximo passo: publicar este marco e seguir com cobertura contextual específica e acessibilidade dos formulários privados. Não declarar o projeto concluído.

### Evento histórico Scarlet/Violet — 16/11/2026

O marco dos iniciais foi publicado em `6f8869f9776e749fab40d7981b15b6cbafb2313a`, com árvore local e remota idênticas; a tag local `final-session-history-2026-11-16-04` preserva o commit anterior à sincronização. Fonte oficial do Poké Portal registra Stonjourner, Eiscue, Armarouge e Ceruledge nas duas versões em incursões Teracristal de cinco estrelas entre 18/10/2024 00:00 e 20/10/2024 23:59 UTC. Foram criadas oito fichas com método e período explícitos: o evento está encerrado e não comprova disponibilidade atual ou legalidade completa. A forma temporária `eiscue-noice` não recebe ficha; tipos e estatísticas vêm separadamente do snapshot PokéAPI. Fichas preexistentes não são substituídas.

Banco vazio aplicou `[1, 2, 3, 4]`; duas cargas geraram relatórios idênticos, `integrity_check=ok` e `foreign_key_check` vazio. São 7.470 fichas, 35 mecânicas e 617 avaliações condicionais. Scarlet e Violet têm sete fichas por versão, quatro delas do evento encerrado. `PYTHONPATH=/home/Danilo/tools/python:backend python tools/check_stage2.py` passou 104 testes, SQL, modelos, UML, links e demonstração. Após acrescentar a contagem por jogo ao relatório, o teste direcionado do evento passou novamente: ele verifica versões, forma padrão, não inclusão da forma de batalha, fontes, datas e repetição. No Brave com Flask e banco temporário, Stonjourner Scarlet e Ceruledge Violet mostraram o método, aviso de encerramento, período e fonte, sem exceções JS. Servidor e navegador temporários foram encerrados.

Próximo passo: publicar; ampliar contextos por versão a partir de fontes reproduzíveis e verificadas, completar regulamentos/perfis e terminar revisão dos formulários privados por teclado. Não declarar o projeto concluído.

### Reprodução em clone limpo — 16/11/2026

O marco do evento foi publicado em `037bc111a7bc32cb5650e388efe5c2951b872f75`, com árvore local e remota idênticas; o histórico local anterior foi preservado na tag `final-session-history-2026-11-16-05`. Um clone público `--single-branch --branch final/complete-project` foi criado em `/tmp`, no mesmo commit. Neste sistema a primeira tentativa de `python3 -m venv .venv` falhou porque o pacote de ambiente virtual/`ensurepip` não estava instalado. Sem alterar pacotes do sistema, foi criado um ambiente isolado com `python3 -m venv --without-pip .venv` e as dependências foram instaladas nele usando `python3 -m pip --python .venv/bin/python install -r backend/requirements.txt`. Os READMEs passaram a mencionar o pré-requisito `python3-venv` em Debian/Ubuntu e a branch atual.

No clone, `db-init` aplicou `[1, 2, 3, 4]` e `catalog-import` reproduziu 1.025 espécies, 1.579 formas, 53 versões, 7.470 fichas, 35 mecânicas e 617 avaliações condicionais. No ambiente isolado, `.venv/bin/python tools/check_stage2.py` passou 104 testes, SQL, dicionário, 26 entidades/189 campos/43 relações brModelo, UML, 257 links e demonstração. Não houve modificação da base pessoal.

Próximo passo: publicar as correções de documentação e ampliar tipos em Let’s Go apenas nas fichas já comprovadas: a comparação da lista específica desses jogos com a PokéAPI fixada concordou nas 153 espécies listadas. Permanecem pendentes outras fontes, regulamentos/perfis e revisão de formulários privados por teclado.

### Tipagem em Let’s Go — 16/11/2026

A verificação de clone limpo foi publicada em `2e72741e8e3a7fe7b8d86874d40833534566c666`, com árvore local e remota idênticas; a tag local `final-session-history-2026-11-16-06` preserva o commit anterior à sincronização. As 153 tipagens de formas padrão na lista específica da Bulbapedia, revisão 4566084, foram comparadas às tipagens históricas da PokéAPI fixada e coincidiram. A extração versionada em `backend/data/curated/` informa fonte, alteração, atribuição e licença CC BY-NC-SA 2.5. O importador valida o hash e a cobertura da extração e verifica cada ficha antes de gravar o tipo; divergências revertem a transação. Apenas fichas existentes de formas padrão são enriquecidas, sem criar presença ou inferir estatísticas.

Banco vazio aplicou `[1, 2, 3, 4]`; duas cargas idênticas, `integrity_check=ok` e `foreign_key_check` vazio. A cobertura tem 7.452 fichas com tipos e 7.220 com estatísticas; em cada versão Let’s Go há 116 fichas comuns com tipos e uma ficha de parceiro distinta; as 117 estão sem estatísticas-base verificadas. Os testes direcionados passaram para busca com filtro por tipo/jogo, ausência de estatísticas inventadas, habilidades não aplicáveis e rollback por alteração da referência. Em Brave e Flask com banco temporário, o filtro Electric/Let’s Go, Pikachu! retornou Pikachu, cujo detalhe exibiu tipo, estatísticas desconhecidas e fonte, sem exceções JS. Servidor e navegador temporários foram encerrados.

Próximo passo: concluir a suíte consolidada, publicar e continuar ampliando dados contextuais com fontes por versão, regulamentos/perfis e revisão dos formulários privados por teclado. Não declarar o objetivo concluído.

### Parceiros e vínculos legados — 16/11/2026

Durante a revisão das fontes, foi identificada uma ambiguidade no snapshot de encontros: os presentes dos parceiros iniciais usam os IDs de Pikachu/Eevee comuns, apesar de serem formas distintas. A carga não associa mais esses presentes às formas comuns e cria as fichas `pikachu-starter` e `eevee-starter` nas versões correspondentes, com fonte e restrições documentadas. Vínculos antigos não são apagados: a API e a interface os identificam como associação não verificada e a cobertura os conta para revisão. Um teste preservou tanto um vínculo previamente curado como um exemplar e seu método declarado ao reimportar.

Em banco vazio, duas cargas foram idênticas e geraram 7.472 fichas, incluindo dois parceiros, sem vínculos antigos a revisar; integridade e FKs passaram. Um banco temporário criado pela versão anterior foi reimportado: os dois vínculos ambíguos foram preservados e sinalizados. No Brave, Pikachu comum exibiu o aviso e a ficha separada do parceiro exibiu restrições e fonte, sem exceções JS. `PYTHONPATH=/home/Danilo/tools/python:backend python tools/check_stage2.py` passou 107 testes, SQL, modelos brModelo, UML, links e demonstração; `python tools/check_links.py` e `git diff --check` também passaram.

Próximo passo: publicar o marco de tipos/parceiros; depois, seguir com estatísticas e mecânicas de Let’s Go, demais dados por versão, regulamentos/perfis e revisão dos formulários privados por teclado. Não declarar o objetivo concluído.
