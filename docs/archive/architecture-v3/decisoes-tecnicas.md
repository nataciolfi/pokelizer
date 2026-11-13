# Decisões técnicas — revisão 2.0

## DT01 — Python e Flask
Backend em Python/Flask, com estrutura pequena e legível para a apresentação escolar.

## DT02 — SQLite
Banco inicial SQLite. Ativar chaves estrangeiras em cada conexão e usar transações para escrita.

## DT03 — HTML, CSS e JavaScript
Frontend com tecnologias web fundamentais e templates Jinja2. JavaScript limitado a interações de interface.

## DT04 — Catálogo separado dos dados por jogo
ESPECIE e FORMA são globais. DADOS_FORMA_JOGO registra a forma dentro de um título.

## DT05 — Dados e mecânicas versionados separadamente
DADOS_FORMA_JOGO aponta para JOGO. MECANICA_JOGO também aponta para JOGO, mas possui sua versão. O backend exige que forma/jogo e mecânica pertençam ao mesmo título.

## DT06 — Scarlet/Violet primeiro
Primeira análise numérica para IV, EV e natureza de Scarlet/Violet. Limites vêm do banco, não de condicionais espalhadas pelo código.

## DT07 — Sistemas de valores de atributos separados
Valores pertencem a um sistema, atributo e versão de mecânica. IV não é treinamento; EV representa esforço; sistemas próprios de outros jogos têm semântica separada. Não há conversão automática entre eles.

## DT08 — Champions em contexto próprio
Recrutamento, visitantes via HOME e treinamento por PV são tratados separadamente. O cálculo fica bloqueado até existir escala e limites documentados. Fontes: https://champions.pokemon.com/pt-br/pokemon/ e https://champions.pokemon.com/pt-br/gameplay/

## DT09 — Perfil e regulamento separados
REGULAMENTO guarda restrições. PERFIL_ANALISE guarda valores de comparação. Perfil não torna recomendação uma regra oficial.

## DT10 — Elegibilidade limitada
Verificar elegibilidade de espécie/forma. Não prometer legalidade completa sem dados de golpes, itens, origem, evento e outras restrições.

## DT11 — Coleção individual
Um registro representa um exemplar. Jogo atual, jogo de origem e método real ficam separados. Sem histórico completo de transferências no MVP.

## DT12 — Forma e transformação
FORMA é variação catalogada. TRANSFORMACAO_FORMA registra a transição contextual. Transformação temporária não cria captura automaticamente.

## DT13 — Tipos ordenados
TIPO_FORMA_JOGO mantém posições 1 e 2, sem duplicação ou terceiro tipo.

## DT14 — Proveniência
Dados de forma, mecânicas, regulamentos e perfis de referência guardam URL e data de verificação.

## DT15 — Segurança
Hash de senha por biblioteca reconhecida, SQL parametrizado, sessão segura, proteção CSRF e autorização por proprietário em toda rota de coleção. Não versionar segredos.

## DT16 — Análise explicável
Cálculos determinísticos em Python, com jogo, mecânica, sistema de atributos, perfil e fonte apresentados no resultado. A primeira versão compara cada atributo com o valor-alvo explícito e classifica igual/abaixo/acima/sem dado. Não gera nota global nem presume que valor maior é melhor. Natureza e habilidade são verificadas separadamente como opções categóricas compatíveis. Consulte [algoritmo de análise](algoritmo-analise.md).

## DT17 — Histórico fora do MVP
Sem histórico de relatórios ou de todas as transferências na primeira entrega.

## DT18 — Estrutura modular
Separar rotas, domínio, serviços, acesso a dados e templates. Evitar concentrar tudo em app.py.
