# Backend Pokelizer — Etapa 2

Python 3.11+, SQLite 3.37+ e Flask. Camadas: dataclasses em `models.py`, SQL/DAOs em `dao.py`, regras/transações em `services.py`, HTTP em `api.py`, conexão e migrações em `db.py`.

## Instalar e iniciar

Na raiz de um clone da branch `stage2/functional-delivery`:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r backend/requirements.txt
export PYTHONPATH=backend
export POKEANALYZER_DATABASE="$PWD/backend/instance/pokelizer.sqlite3"
export POKEANALYZER_SECRET_KEY='substitua-por-um-segredo-aleatorio-persistente'
python -m flask --app pokeanalyzer:create_app db-init
python -m flask --app pokeanalyzer:create_app catalog-import
python -m flask --app pokeanalyzer:create_app catalog-coverage
python -m flask --app pokeanalyzer:create_app run --host 127.0.0.1 --port 5000
```

`db-init` é explícito e não destrói tabelas. Startup não recria nem semeia o banco. Se o banco já é versionado, a mesma operação só aplica migrações pendentes. Para criar uma demonstração isolada, escolha outro arquivo em `POKEANALYZER_DATABASE`; nunca apague o banco anterior. A carga real e suas limitações estão em [data](data/README.md).

No ambiente da sessão, dependências e ferramentas portáteis foram usadas porque a rede do shell está sem DNS e a `.venv` herdada não tinha os pacotes disponíveis neste runtime; isso está registrado no [relatório](../docs/stage2/README.md). Em outra máquina, use a instalação convencional acima.

## Banco existente e preservação

```bash
python -m flask --app pokeanalyzer:create_app db-status
python -m flask --app pokeanalyzer:create_app db-backup /caminho/novo/backup.sqlite3
python -m flask --app pokeanalyzer:create_app db-upgrade
python -m flask --app pokeanalyzer:create_app db-import-legacy /caminho/antigo.sqlite3 /caminho/novo.sqlite3
```

Backup e importação recusam destinos existentes. A importação reconhece as 13 tabelas do backend antigo `5bd1357`, mantém IDs/hashes e valida tudo em arquivo novo. Origem aberta somente para leitura; linha incompatível ou coluna desconhecida interrompe sem destruir a origem. Mecânicas/fontes não são inventadas para tornar dados antigos válidos. Preserve backup, revise a cópia e repita para outro destino. Migrações aplicadas têm checksum; nunca edite `001_stage1.sql` em banco existente.

## Rotas

Todos os caminhos abaixo têm prefixo `/api`.

| Método/caminho | Uso |
|---|---|
| GET `/status`, `/csrf` | Saúde e token CSRF |
| POST `/auth/cadastro`, `/auth/login`, `/auth/logout` | Conta, sessão e saída |
| GET `/auth/me` | Conta atual sem hash |
| GET `/pokemon?busca=...&tipo=ID&geracao=N&jogo=ID` | Uma entrada por forma global, com fichas de jogo aninhadas; espécies sem forma/ficha preservadas |
| GET `/formas/ID` | Identidade global, espécie e fichas conhecidas |
| GET `/pokemon/ID` | Ficha identificada por `id_dados_forma`, opções contextuais, fontes e transformações |
| GET `/opcoes`, `/mecanicas/ID` | Jogos, tipos, métodos, naturezas; sistemas, atributos, limites e aplicabilidade da mecânica |
| GET/POST `/colecao` | Listar/incluir exemplares próprios |
| GET/PATCH/DELETE `/colecao/ID` | Consultar/editar/excluir exemplar próprio |
| GET/POST `/perfis` | Listar próprios/referências e criar personalizado |
| GET/PATCH/DELETE `/perfis/ID` | Ler visível; editar/excluir somente personalizado próprio |
| POST `/analises` | Comparar exemplar próprio com perfil autorizado e compatível |
| GET `/regulamentos` | Regulamentos versionados com fonte |
| GET `/regulamentos/ID/formas/FICHA` | Elegibilidade da ficha no regulamento, com estado e fonte |

Busca inclui nome português/inglês, nome e código de forma e número nacional exato. Geração é origem da espécie. Tipo/jogo se aplicam à mesma ficha antes do agrupamento. Uma forma aparece uma vez; os campos antigos de ficha no topo só ficam preenchidos quando há um único contexto no resultado. Para vários jogos, use `fichas[]`, sem escolher um jogo arbitrário. `/pokemon/ID` continua significando ID da ficha; `/formas/ID` é global.

Escritas exigem `X-CSRF-Token` de `/csrf`; cadastro/login devolvem token novo. Credenciais usam hash scrypt, sessão tem cookie HTTPOnly/SameSite. Dono vem exclusivamente da sessão. Perfil alheio/exemplar alheio retorna 404. Escrita sem sessão retorna 401; sem CSRF, 403; dados inválidos/incompatíveis, 400. Em produção, use segredo persistente, HTTPS e `POKEANALYZER_COOKIE_SECURE=1`; o servidor de desenvolvimento é local.

## Corpos de escrita

Cadastro aceita `nome_usuario`, `email`, `senha`. Login aceita `email`, `senha`. Campos desconhecidos, objetos JSON inválidos, números booleanos/fracionários e IDs fora de intervalo são rejeitados. Não há sucesso com campos ignorados. Logout e DELETE aceitam corpo vazio ou `{}`.

Coleção aceita `id_dados_forma_atual` (obrigatório na criação), `id_mecanica`, `id_jogo_origem`, `id_dados_forma_origem`, `id_metodo_obtencao`, `id_natureza`, `id_habilidade_forma`, `apelido`, `nivel`, `observacao`, `valores`.

```json
{
  "id_dados_forma_atual": 1,
  "id_mecanica": 1,
  "apelido": "FIXTURE exemplo — IDs dependem do banco",
  "valores": [
    {"id_mecanica_sistema_atributo": 1, "id_atributo": 1, "estado": "conhecido", "valor": 0},
    {"id_mecanica_sistema_atributo": 1, "id_atributo": 2, "estado": "desconhecido", "valor": null}
  ]
}
```

IDs acima são ilustrativos, não são IDs oficiais nem garantidos após carga real. Cada valor exige sistema da mecânica, atributo, estado (`conhecido`, `desconhecido`, `nao_aplicavel`), valor numérico ou nulo e `motivo` opcional. Número conhecido depende de aplicabilidade e limites individuais/totais confirmados. Zero permanece zero; ausência não vira zero. Inaplicabilidade exige regra confirmada. Valores duplicados e somas acima do limite falham. Pai e filhos são salvos/revertidos juntos.

PATCH preserva campos omitidos; `null` remove campo opcional. Se enviar `valores`, substitui a lista inteira; `[]` remove todos. Mudar ficha/mecânica com valores existentes exige lista explícita. Natureza/habilidade/nível preservados precisam continuar compatíveis ou ser removidos explicitamente. Origem não muda automaticamente e não exige método disponível no destino após transferência.

Perfil aceita `id_dados_forma`, `id_mecanica`, `id_regulamento`, `nome_perfil`, `descricao`, `valores`, `naturezas` e `habilidades`. Usa `valor_alvo` em vez de `valor`; preferências são listas de IDs. Contexto/nome são obrigatórios na criação. PATCH troca listas enviadas e preserva as omitidas; mudança de contexto exige todas as três listas explícitas para revalidação. Referências competitivas não são criadas pela API privada.

Análise aceita somente `id_pokemon_colecao` e `id_perfil`. Exige forma/jogo e versão de mecânica iguais. Retorna valores, alvos, diferença e estado (`igual`, `abaixo`, `acima`, `sem_dado`, `nao_comparado`, `nao_aplicavel`, `nao_verificado`) com regras e fontes. Preferências categóricas são explicadas à parte. Maior não é sempre melhor; nenhuma nota global é calculada. Elegibilidade de forma não comprova legalidade completa do indivíduo. Ausência de evidência retorna `nao_verificado`, sem inferir proibição.

## Testar e demonstrar

```bash
python tools/check_stage2.py
PYTHONPATH=backend python tools/demonstrate_stage2.py
```

O primeiro comando inclui testes existentes e regressões, SQL, dicionário, brModelo, UML e links. A revisão visual está documentada separadamente. A demonstração cria seu banco temporário, usa somente dados `FIXTURE`, chama as rotas e remove o banco ao terminar. [Resultados e roteiro para o professor](../docs/stage2/README.md).
