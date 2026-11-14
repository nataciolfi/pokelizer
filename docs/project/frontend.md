# Interface integrada — avanço após a Etapa 2

O Flask serve a página em `/`, o CSS em `/static/app.css` e o JavaScript em `/static/app.js`. Não há processo de build; imagens dos Pokémon são carregadas opcionalmente da PokéAPI Sprites, com símbolo neutro como alternativa quando indisponíveis. O novo design usa navegação de observatório, tipografia editorial, verde e coral sobre fundo claro; não depende dos wireframes antigos.

Implementado: busca/filtros/paginação de catálogo, detalhe global e fichas, conta/sessão, coleção privada com inclusão/consulta/edição/exclusão, origem, editor de valores com estados distintos, perfis e preferências, comparação por campo e consulta de elegibilidade. Todas as operações usam Fetch, cookie de sessão e CSRF. Mensagens e fontes mostram desconhecimento sem convertê-lo em zero ou proibição. Banco sem fichas apresenta o estado vazio explicativo; não permite fingir um cadastro contextual.

Arquivos:

- [HTML](../../backend/pokeanalyzer/templates/index.html)
- [CSS](../../backend/pokeanalyzer/static/app.css)
- [JavaScript](../../backend/pokeanalyzer/static/app.js)
- [Factory e rota inicial](../../backend/pokeanalyzer/__init__.py)

## Verificação e limite atual

Rotas, operações e contratos são exercitados pelos testes de integração Flask. Há teste de renderização do template, entrega dos assets e cobertura. A demonstração contextual cria dados FIXTURE claramente identificados. O catálogo real offline foi carregado sem inventar fichas.

**A verificação visual e ponta a ponta no navegador não foi concluída.** O ambiente bloqueou a abertura de socket para o servidor local (`PermissionError: Operation not permitted`) e o navegador Brave encerrou por bloqueio de IPC/rede (`setsockopt: Operation not permitted`). Não foi solicitado relaxamento das permissões. Nenhum screenshot ou teste de navegador é alegado como evidência.

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
