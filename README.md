# Pokelizer — Etapa 1

Catálogo Pokémon, coleção privada e analisador explicável com Python/POO, Flask, SQLite e futura interface HTML/CSS/JavaScript. Esta entrega contém a arquitetura para o produto completo, banco físico, conexão Python, modelos brModelo e UML. O analisador e a interface final continuam previstos para as etapas seguintes; não são apresentados como implementados.

O [relatório de entrega](docs/stage1/completion.md) reúne implementação, decisões, arquivos, testes e pendências. A autoridade atual é [docs/stage1](docs/stage1/README.md). [Decisões](docs/stage1/decisions.md) reconciliam as quatro branches e explicam os desvios; documentos antigos estão marcados como substituídos e preservados no arquivo histórico.

## Reproduzir

Clone a branch de entrega, sem substituir sua cópia de dados existente:

```sh
git clone --branch stage1/reconciled-architecture https://github.com/nataciolfi/pokelizer.git
cd pokelizer
python -m venv .venv
. .venv/bin/activate
python -m pip install -r backend/requirements.txt
export PYTHONPATH=backend
export POKEANALYZER_DATABASE="$PWD/backend/instance/pokelizer.sqlite3"
export POKEANALYZER_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
python -m flask --app pokeanalyzer:create_app db-init
python -m flask --app pokeanalyzer:create_app db-status
python -m flask --app pokeanalyzer:create_app db-upgrade
python backend/run.py
```

Requer Python 3.11+ e SQLite 3.37+ (`python -c 'import sqlite3; print(sqlite3.sqlite_version)'`). Windows PowerShell: ativar `.venv\Scripts\Activate.ps1` e definir variáveis com `$env:PYTHONPATH="backend"`, `$env:POKEANALYZER_DATABASE=...` e `$env:POKEANALYZER_SECRET_KEY=...`; os comandos Python são iguais. `.env.example` é referência, não um arquivo carregado automaticamente.

A API local estará em http://127.0.0.1:5000/api/status. O banco começa vazio, sem Pokémon fictícios ou fatos oficiais presumidos. Testes têm fixtures próprias e nunca devem ser executados como seed do catálogo real. A conexão é fechada no contexto Flask; FK e gatilhos recursivos são ativados em cada conexão.

`db-init`/`db-upgrade` aplicam migrações ordenadas com checksum e rollback. Iniciar o servidor não recria tabelas. Para dados do backend antigo, use o procedimento de backup e importação validada para **outro arquivo novo** no [backend/README.md](backend/README.md). Nenhum comando apaga/recria um banco existente. Banco local, segredos e dependências não são versionados.

## Entregáveis

| Entrega | Caminho |
|---|---|
| Conceitual brModelo nativo | [docs/diagrams/conceitual.brM3](docs/diagrams/conceitual.brM3) |
| Conceitual exportado | [docs/diagrams/conceitual.png](docs/diagrams/conceitual.png) + [pranchas legíveis](docs/diagrams/README.md) |
| Lógico brModelo nativo | [docs/diagrams/logico.brM3](docs/diagrams/logico.brM3) |
| Lógico exportado | [docs/diagrams/logico.png](docs/diagrams/logico.png) + [pranchas legíveis](docs/diagrams/README.md) |
| Modelo físico executável | [backend/schema.sql](backend/schema.sql) |
| Migração inicial | [backend/migrations/001_stage1.sql](backend/migrations/001_stage1.sql) |
| Conexão Python e comandos | [backend/pokeanalyzer/db.py](backend/pokeanalyzer/db.py), [instruções](backend/README.md) |
| UML editável/exportado | [classes.puml](docs/uml/classes.puml), [classes.svg](docs/uml/classes.svg), [classes.png](docs/uml/classes.png) |
| Matriz de requisitos/estado | [docs/stage1/requirements.md](docs/stage1/requirements.md) |
| Cardinalidades, campos e exclusões | [docs/stage1/data-model.md](docs/stage1/data-model.md) |
| Invariantes e enforcement | [docs/stage1/integrity.md](docs/stage1/integrity.md) |
| Verificação/limitações | [docs/stage1/verification.md](docs/stage1/verification.md) |

Os modelos foram criados, salvos, exportados e reabertos pelo brModelo 3.3.2; não são Mermaid/Figma. Pranchas ampliadas repetem referências às mesmas entidades para tornar todas as relações e campos legíveis. O índice de diagramas documenta a ferramenta, seus hashes, arquivos e reprodução. O UML identifica 11 classes implementadas e separa o serviço de comparação planejado das classes existentes.

## Verificar

```sh
python tools/check_stage1.py
```

O [roteiro de verificação](docs/stage1/verification.md) inclui também a consistência dos arquivos nativos/exports brModelo e a revisão visual. Resultado desta entrega: 45 testes de backend/banco aprovados, incluindo migração sem perda involuntária, rollback, isolamento e integridade contextual. Não usar essa contagem para inferir que todo o produto final está pronto.

## Estado e submissão

26 tabelas de domínio suportam os 25 conceitos exigidos mais aplicabilidade explícita por atributo. Uma ficha é única por forma+jogo; mecânicas são versões separadas. O exemplar mantém contexto atual e origem opcional; valores não são convertidos entre jogos. Tipagem e forma padrão têm mínimos verificados, além de unicidade. Perfis e elegibilidade guardam contexto e evidência; elegibilidade de forma não significa legalidade integral do exemplar.

Permanecem futuras a carga oficial completa, edição HTTP completa de coleção/perfis, comparação explicável, telas e integração Fetch. Os recursos obrigatórios estão mapeados sem serem rebaixados a opcionais. Não foram acrescentados simulador, equipes, marketplace ou funcionalidades sociais.

[Submissão manual](docs/stage1/submission.md): confirmar colaborador do professor usando o contato do Word original e anexar os artefatos ao Classroom. Nenhum convite ou envio foi feito. O original do professor foi mantido localmente após a revisão automática recusar sua publicação; o repositório contém apenas o [resumo de requisitos sem dados pessoais](docs/sources/teacher-requirements.md). A branch é para revisão e não foi mesclada automaticamente em main.
