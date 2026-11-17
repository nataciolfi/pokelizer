# Interface integrada — avanço após a Etapa 2

O Flask serve a página em `/`, o CSS em `/static/app.css` e o JavaScript em `/static/app.js`. Não há processo de build; imagens dos Pokémon são carregadas opcionalmente da PokéAPI Sprites, com símbolo neutro como alternativa quando indisponíveis. O novo design usa navegação de observatório, tipografia editorial, verde e coral sobre fundo claro; não depende dos wireframes antigos.

Implementado: busca/filtros/paginação de catálogo, detalhe global e fichas, conta/sessão, coleção privada com inclusão/consulta/edição/exclusão, origem, editor de valores com estados distintos, perfis e preferências, comparação por campo e consulta de elegibilidade. Todas as operações usam Fetch, cookie de sessão e CSRF. Mensagens e fontes mostram desconhecimento sem convertê-lo em zero ou proibição. Banco sem fichas apresenta o estado vazio explicativo; não permite fingir um cadastro contextual.

Arquivos:

- [HTML](../../backend/pokeanalyzer/templates/index.html)
- [CSS](../../backend/pokeanalyzer/static/app.css)
- [JavaScript](../../backend/pokeanalyzer/static/app.js)
- [Factory e rota inicial](../../backend/pokeanalyzer/__init__.py)

## Primeira tentativa de verificação — histórico

Rotas, operações e contratos são exercitados pelos testes de integração Flask. Há teste de renderização do template, entrega dos assets e cobertura. A demonstração contextual cria dados FIXTURE claramente identificados. O catálogo real offline foi carregado sem inventar fichas.

**Na primeira tentativa**, a verificação visual e ponta a ponta no navegador não foi concluída. O ambiente bloqueou a abertura de socket para o servidor local (`PermissionError: Operation not permitted`) e o navegador Brave encerrou por bloqueio de IPC/rede (`setsockopt: Operation not permitted`). As tentativas posteriores usaram permissão para um servidor local e estão registradas abaixo.

Para concluir em ambiente com navegador e servidor local:

1. Seguir instalação no backend e executar Flask em `127.0.0.1:5000`; abrir `/` em desktop e celular.
2. Conferir console, foco, teclado, diálogos, layout e rede Fetch. Testar filtros combinados, paginação e formas sem ficha com o snapshot real.
3. Usar banco separado com dados FIXTURE para exercitar criação de conta, coleção com zero/desconhecido, edição, perfil com alvo, comparação e exclusão; repetir em outra sessão para verificar isolamento.
4. Conferir rollback com limite inválido e mensagens de contexto incompatível. Não carregar fixtures em banco de uso pessoal.
5. Registrar resultados/imagens e corrigir qualquer problema antes de chamar a interface de finalizada.

A cobertura real por jogo/mecânica/regulamento também continua obrigatória; o relatório da Etapa 2 distingue esse trabalho da cobertura global do snapshot. Nenhuma hospedagem foi criada e o projeto não foi convertido para outra stack.


## Revisão parcial em navegador — 14/11/2026

Executado Brave headless contra Flask em 127.0.0.1, com banco temporário contendo catálogo real e fixture identificada. Fluxo automatizado: criação de conta, inclusão de exemplar com valor 0, criação de perfil com alvo 2 e análise com diferença -2; sem exceções JavaScript no roteiro. Tela de catálogo inspecionada em 1440×900 e 390×844; no celular, largura da página e viewport eram ambas 390 px. A primeira tentativa de automação acionou mudanças de contexto sobrepostas; o roteiro foi corrigido para aguardar cada resposta e a interface agora desabilita seletores durante o carregamento. Este resultado não cobre todos os fluxos, teclado, isolamento em duas sessões nem apresentação visual final.

Na continuação, outro banco temporário com migração 002 e catálogo real foi usado no Brave: consulta de Pikachu/Sword exibiu Electric, HP 35 e demais estatísticas, Static e Lightning Rod com fontes; uma conta criou exemplar de nível 50 com IV de HP 0, perfil com alvo 2 e comparação com diferença -2. Nenhuma exceção JavaScript foi registrada nesse roteiro. Uma primeira tentativa automatizada escolheu o atributo FIXTURE não aplicável e não salvou valor; foi corrigida para selecionar um atributo aplicável antes da repetição. Ainda faltam revisão de teclado, erros e isolamento entre sessões no navegador.

Em nova execução com perfis reais carregados, a referência Dragapult exibiu os três alvos e a fonte, e Escape fechou o diálogo. Uma tentativa de comparar Pikachu com o perfil de Dragapult mostrou erro de contexto; escolhendo o perfil de Pikachu a comparação passou. Uma segunda conta sintética não viu o exemplar nem o perfil privado da primeira; depois do retorno à primeira conta, ambos foram excluídos pela interface. Nenhuma exceção JavaScript foi registrada nesses roteiros. Uma primeira tentativa de teste usou a porta 5060, reservada pelo navegador, e foi repetida na 5056. Outra enviou Enter por automação sem fechar o diálogo; Escape foi comprovado, mas navegação completa e ativação por Enter ainda exigem revisão. Os nomes de perfil agora incluem contexto da ficha na listagem e seleção de análise.

A repetição com o evento de teclado completo (`text` e `unmodifiedText` no protocolo do navegador) confirmou que Enter também fecha o diálogo quando o botão está focado; a tentativa anterior não havia enviado o caractere. Ainda falta percorrer a aplicação inteira por teclado e conferir contraste de todos os estados.

## Fichas históricas — 15/11/2026

No Brave contra Flask e banco temporário com dados reais, a ficha de Magnemite em Yellow mostrou Electric, explicou o Especial único não representado e indicou que habilidades não se aplicam; a ficha Gold mostrou Electric/Steel, as seis estatísticas-base e o mesmo estado de habilidades. As fontes ficaram visíveis. Não houve exceções JavaScript nesse roteiro. A primeira execução de automação consultou a ficha antes da resposta Fetch terminar; a repetição aguardou o conteúdo detalhado. As fichas também mostram se o registro da forma está confirmado, negado ou não verificado. Em gerações com habilidades, a interface informa que a fonte lista possibilidades, sem comprovar o método de obtenção.

Em 15/11/2026, após a migração 003, Brave/Flask local com banco temporário mostrou as quatro opções distintas Red/Blue, inclusive versões japonesas, e a ficha Pikachu em `Red (red-japan)` com tipo Electric, Especial único e habilidade não aplicável; nenhuma exceção JavaScript. Isso não substitui a revisão completa de teclado e contraste ainda pendente.

Em 15/11/2026, o fluxo real em Ruby foi repetido com EV 255 e perfil com alvo 252; a análise relatou diferença 3 sem presumir melhora. A comparação agora filtra perfis pela ficha e mecânica do exemplar, avisa quando não há perfil e desabilita o envio. Em Brave, a mudança entre um Magnemite Yellow sem mecânica e o Pikachu Ruby confirmou os dois estados e a limpeza do resultado anterior. A primeira tentativa do roteiro escolheu Pikachu Yellow sem ficha no snapshot; foi repetida com Magnemite. Sem exceções JS nos testes bem-sucedidos; revisão integral de teclado/contraste permanece pendente.

Em 15/11/2026, Brave testou cadastro e análise de Magnemite Yellow em uma mecânica parcial: nível 50 foi salvo, natureza/habilidade apareceram como não aplicáveis e a interface informou que DV/Stat Experience ainda não estão disponíveis, sem tratar essa ausência como inexistência. O primeiro roteiro aguardou apenas o botão de conta e correu antes de terminar o carregamento inicial; a repetição aguardou o catálogo e passou sem exceções JS.

Em 15/11/2026, o fluxo Yellow passou novamente com quatro DVs, Stat Experience 65.535 e nível 50: a comparação explicou HP derivado 10 contra alvo 5. Ao editar o DV Especial do alvo para desconhecido, o HP derivado também apareceu desconhecido, sem exceções JS. O estado ausente ou desconhecido do alvo é apresentado ao lado do campo, e o Especial compartilhado não é duplicado em entradas independentes.

Em 16/11/2026, Brave com Flask e banco temporário mostrou as cinco estatísticas de Magnemite Yellow (HP 25, Especial 95, Velocidade 45) e Chansey Yellow (HP 250, Especial 105), com fontes e sem exibir os campos especiais modernos. Não houve exceções JavaScript. A primeira execução encerrou prematuramente a conexão do próprio roteiro por indentação; corrigida e repetida com sucesso.

Em 16/11/2026, Brave com servidor Flask e banco temporário também verificou os novos detalhes de obtenção: Pidgey em Let’s Go mostrou encontro selvagem e habilidades não aplicáveis; Pikachu em Yellow mostrou presente, sem indicação de encontro selvagem; Togepi em Gold mostrou ovo. As fontes estavam visíveis e não houve exceções JavaScript. Isso não substitui a revisão completa de teclado e contraste.

## Acessibilidade e apresentação — 16/11/2026

No Brave com Flask e banco temporário, foram inspecionadas imagens em 1440×900 e 390×844; o catálogo não apresentou transbordamento horizontal da página nessas dimensões. A primeira medição de contraste dos textos visíveis identificou falhas em navegação, metadados de cartões e etiquetas; as cores foram ajustadas e a repetição, assim como as telas públicas de coleção, perfis, análise, regulamentos e o diálogo de conta, não apontou falhas entre os textos examinados. A medição usa estilos computados e fundos opacos; não cobre todas as combinações de imagem, transparência, foco, erro ou dados privados e não equivale a uma auditoria WCAG completa.

Com eventos reais de teclado, Tab alcançou navegação, conta, filtros e cartões; Enter abriu a conta e os detalhes de Bulbasaur; Escape fechou os diálogos e devolveu o foco ao controle de origem. O foco agora circula dentro do diálogo ao chegar ao primeiro/último controle. Os botões de catálogo têm nomes acessíveis com espécie e código da forma. O roteiro não percorreu todos os formulários privados por teclado; essa verificação e uma revisão com leitor de tela continuam pendentes. Não houve exceções JavaScript nas verificações.

Em 16/11/2026, a consulta no Brave de Sprigatito em Scarlet e Fuecoco em Violet exibiu tipos, estatísticas, presente e fontes, sem exceções JavaScript. Outros registros dessas versões ainda necessitam de fontes específicas.

Em 16/11/2026, o Brave exibiu nas fichas Stonjourner Scarlet e Ceruledge Violet o método de incursão, o aviso de evento encerrado, período em UTC e fonte, sem exceções JavaScript.

Em 16/11/2026, Brave com banco temporário filtrou o catálogo por Electric e Let’s Go, Pikachu!, retornou Pikachu e exibiu seu tipo com fonte, mantendo estatísticas-base como não verificadas. Nenhuma exceção JavaScript foi registrada nesse roteiro.

Em 16/11/2026, um banco temporário anterior foi reimportado e o Brave mostrou no Pikachu comum que um vínculo de presente legado exige revisão; a ficha separada do parceiro mostrou suas restrições e fonte. Não houve exceções JavaScript.


Em 16/11/2026, no Brave headless contra Flask e SQLite limpo, a conta de demonstração criou um exemplar Pikachu parceiro de Let’s Go pelo formulário da coleção. A ficha selecionada e sua mecânica foram conferidas no seletor: natureza e nível, IV, AV e EV não aplicável; o editor exibiu limites 31 e 200 e estados distintos. A interface salvou IV HP 31, AV HP 0 e seis EV não aplicáveis. Um perfil da mesma forma/jogo salvou AV HP alvo 200; a análise exibiu diferença -200, desconhecidos como “Não informado” e EV como “Não aplicável”, com fonte e explicação de que abaixo não significa pior. O roteiro exercitou Fetch e fluxo conta → coleção → perfil → análise; o teste automatizado também cobre limite AV 201, IV de parceiro 30, estado EV conhecido inválido e rollback transacional. A página não teve overflow em 390 px; o screenshot mobile mostra a tabela de comparação rolável dentro do cartão. A captura desktop de 1440 px e a mobile foram abertas e inspecionadas. O detalhe contextual de estatísticas no catálogo não foi confirmado nesse roteiro automatizado; dados e fonte estão conferidos em API/testes. Formulários privados por teclado e leitor de tela seguem pendentes.


Em 17/11/2026, contra o banco limpo com as 153 espécies compatíveis por versão, o Brave completou: conta nova → filtro Pikachu → coleção do Pikachu parceiro → perfil AV → análise. O exemplar salvou IV HP 31, AV HP 0 e seis EV `nao_aplicavel`; o perfil salvou AV HP 200. A tabela exibiu -200, valores ausentes como “Não informado” e EV como “Não aplicável”, com explicação de distância sem hierarquia melhor/pior. Limites 31/200 ficaram visíveis; `scrollWidth=390`. O card abriu consulta Fetch para a ficha do parceiro, mas a automação não obteve o texto renderizado do bloco de detalhes; não considero comprovada essa parte visual. As imagens desktop/mobile foram capturadas em `/tmp` e abertas.
