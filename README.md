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

A carga verificada em banco vazio contém **1.025 espécies, 1.579 formas, 53 versões e 7.622 fichas**. Dessas, 7.454 são derivadas do snapshot, duas vêm de guia VGC, seis dos iniciais, oito de evento de 2024, dez de encontros em Poco Path, duas de parceiros e 140 documentam conteúdo contextual adicional de Let’s Go: disponibilidade das 153 espécies, 18 formas Alola e 15 formas Mega por versão. As 30 Mega estão marcadas como temporárias, ligadas à forma-base e não registráveis como exemplares. No subconjunto do snapshot, os métodos se sobrepõem: 6.965 fichas têm encontro selvagem, 667 presente e 36 ovo. Há 7.604 fichas com tipos e estatísticas com fonte (493 com Especial único da primeira geração) e 14.246 vínculos de habilidades potenciais. São 37 mecânicas selecionadas, onze parciais, inclusive IV/AV e natureza/nível documentados para Let’s Go; EV está explicitamente marcado como não aplicável nessa geração. Parceiros iniciais têm estatísticas próprias, separadas de Pikachu e Eevee comuns. Quatro regras históricas (Sword/Shield temporada 36 e Scarlet/Violet temporada 22) e 641 avaliações condicionais têm fonte, sem comprovar a legalidade completa; há dois perfis históricos de referência. Scarlet e Violet, por exemplo, têm três fichas de iniciais e quatro de evento encerrado e cinco de Poco Path por versão; presença e regulamentos de outros contextos ainda são parciais. A [cobertura](docs/project/coverage-final.json) e as [fontes](backend/data/README.md) detalham os limites. A demonstração contextual usa fatos sintéticos identificados como `FIXTURE`. Zero, ausência, desconhecimento e sistemas não aplicáveis permanecem distintos.

O documento do professor fixa Etapa 1 em 09/11, Etapa 2 em 13/11 e final em 17/11/2026. O usuário informou três dias para regularização; a diferença deve ser confirmada com o professor. Convite do colaborador e envio ao Classroom são ações manuais descritas no [roteiro](docs/stage2/README.md).
