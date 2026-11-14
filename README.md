# Pokelizer

Catálogo Pokémon, coleção privada e comparação explicável de exemplares com perfis, em Python/POO, Flask e SQLite. A Etapa 2 implementa o backend. A nova interface já está integrada no código, com [QA de navegador ainda pendente](docs/project/frontend.md); o projeto final mantém a obrigação de interface nova HTML/CSS/JavaScript com Fetch e catálogo contextual completo.

A entrega é desenvolvida na branch `stage2/functional-delivery`, sobre a reconciliação `91875bd`. A `main` ainda contém material antigo. Consulte o [relatório da Etapa 2](docs/stage2/README.md) e o [registro de continuidade](docs/project/progress.md) para distinguir implementado, verificado e pendente.

- [Instalação, banco, execução e API](backend/README.md)
- [Modelos nativos brModelo, imagens e pranchas](docs/diagrams/README.md)
- [SQL executável](backend/schema.sql) e [migração inicial](backend/migrations/001_stage1.sql)
- [UML atualizado](docs/uml/README.md)
- [Código Python](backend/pokeanalyzer/), [testes](backend/tests/) e [demonstração](tools/demonstrate_stage2.py)
- [Dados reais, fontes e licença](backend/data/README.md) e [cobertura executada](docs/stage2/coverage.json)
- [Requisitos do professor](docs/sources/teacher-requirements.md) e [reconciliação da Etapa 1](docs/stage1/decisions.md)

## Executar

```bash
git clone --branch stage2/functional-delivery https://github.com/nataciolfi/pokelizer.git
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

A carga global verificada contém **1.025 espécies, 1.579 formas e 51 jogos** do snapshot PokéAPI. Fichas e regras por jogo ainda precisam de fontes específicas; essa cobertura não é apresentada como concluída. A demonstração contextual usa fatos sintéticos identificados como `FIXTURE`. Zero, ausência, desconhecimento e sistemas não aplicáveis permanecem distintos. Elegibilidade de forma não comprova legalidade completa do exemplar.

O documento do professor fixa Etapa 1 em 09/11, Etapa 2 em 13/11 e final em 17/11/2026. O usuário informou três dias para regularização; a diferença deve ser confirmada com o professor. Convite do colaborador e envio ao Classroom são ações manuais descritas no [roteiro](docs/stage2/README.md).
