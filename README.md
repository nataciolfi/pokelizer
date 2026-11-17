# Pokelizer

Catálogo Pokémon, coleção privada e comparação explicável de exemplares com perfis, em Python/POO, Flask e SQLite. A interface HTML/CSS/JavaScript usa Fetch; os fluxos verificados e os testes de navegador ainda pendentes estão em [frontend.md](docs/project/frontend.md). O projeto final continua em desenvolvimento, sobretudo na cobertura contextual de dados reais.

A entrega é desenvolvida na branch `final/complete-project`; a `main` ainda contém material antigo. Consulte o [relatório da Etapa 2](docs/stage2/README.md) e o [registro de continuidade](docs/project/progress.md) para distinguir implementado, verificado e pendente.

- [Instalação, banco, execução e API](backend/README.md)
- [Modelos nativos brModelo, imagens e pranchas](docs/diagrams/README.md)
- [SQL executável](backend/schema.sql) e [migração inicial](backend/migrations/001_stage1.sql)
- [UML atualizado](docs/uml/README.md)
- [Código Python](backend/pokeanalyzer/), [testes](backend/tests/) e [demonstração](tools/demonstrate_stage2.py)
- [Dados reais, fontes e licença](backend/data/README.md) e [cobertura executada](docs/project/coverage-final.json)
- [Requisitos do professor](docs/sources/teacher-requirements.md) e [reconciliação da Etapa 1](docs/stage1/decisions.md)

## Executar

Use Python 3.11+ e SQLite 3.37+. Em Debian/Ubuntu, instale também o pacote `python3-venv` se `python3 -m venv` informar que `ensurepip` não está disponível.

```bash
git clone --branch final/complete-project https://github.com/nataciolfi/pokelizer.git
cd pokelizer
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r backend/requirements.txt
export PYTHONPATH=backend
export POKEANALYZER_SECRET_KEY='troque-por-um-segredo-aleatorio-persistente'
python -m flask --app pokeanalyzer:create_app db-init
python -m flask --app pokeanalyzer:create_app catalog-import
python -m flask --app pokeanalyzer:create_app run
```

Startup não apaga nem recria banco existente. Leia as instruções de backup/migração antes de usar uma base anterior. `catalog-import` lê um snapshot real fixado com hashes; conflitos abortam sem sobrescrever curadoria prévia.

## Verificar a entrega

```bash
python tools/check_stage2.py
PYTHONPATH=backend python tools/demonstrate_stage2.py
```

O conjunto inclui as regressões da base, isolamento entre usuários, CRUD, transações e limites, análise, busca/catálogo, carga real, SQL e consistência dos modelos/UML. A revisão visual das imagens é registrada separadamente em [visual-review.md](docs/diagrams/visual-review.md).

A carga verificada em banco vazio contém **1.025 espécies, 1.579 formas, 53 versões e 7.472 fichas**. Dessas, 7.454 são derivadas de encontros, presentes ou ovos registrados no snapshot, duas vêm de um guia VGC, seis correspondem aos três iniciais de Scarlet e Violet, oito a um evento encerrado de 2024 e duas às formas de parceiros de Let’s Go. No subconjunto derivado da PokéAPI, os métodos se sobrepõem: 6.965 fichas têm encontro selvagem, 667 presente e 36 ovo. Há 7.454 fichas com tipos, 7.222 com estatísticas de fonte (493 com Especial único da primeira geração) e 14.220 vínculos de habilidades potenciais. São 37 mecânicas selecionadas, onze parciais, inclusive IV/AV e natureza/nível documentados para Let’s Go; EV está explicitamente marcado como não aplicável nessa geração. Parceiros iniciais têm estatísticas próprias, separadas de Pikachu e Eevee comuns. Duas regras da temporada 36 e 617 avaliações condicionais têm fonte, sem comprovar a legalidade completa; há dois perfis históricos de referência. Presença, tipos e mecânicas continuam parciais: Scarlet e Violet, por exemplo, têm três fichas de iniciais e quatro de um evento encerrado em cada versão. A [cobertura](docs/project/coverage-final.json) e as [fontes](backend/data/README.md) detalham os limites. A demonstração contextual usa fatos sintéticos identificados como `FIXTURE`. Zero, ausência, desconhecimento e sistemas não aplicáveis permanecem distintos.

O documento do professor fixa Etapa 1 em 09/11, Etapa 2 em 13/11 e final em 17/11/2026. O usuário informou três dias para regularização; a diferença deve ser confirmada com o professor. Convite do colaborador e envio ao Classroom são ações manuais descritas no [roteiro](docs/stage2/README.md).
