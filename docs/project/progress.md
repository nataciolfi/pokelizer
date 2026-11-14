# Continuidade do Pokelizer

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
