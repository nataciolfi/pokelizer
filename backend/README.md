# Backend — Etapa 1

A estrutura completa do produto está no SQLite. Esta etapa implementa conexão, migrações, persistência inicial e preserva cadastro/login/logout, consultas de catálogo e coleção privada existentes. Edição HTTP de perfis e o comparador explicável continuam planejados. `PerfilService`/`PerfilDAO` já demonstram persistência e leitura privada; não existe endpoint de comparação.

## Instalação e banco vazio

Python 3.11+ e SQLite 3.37+ são necessários. A partir da raiz do repositório:

```sh
python -m venv .venv
. .venv/bin/activate
pip install -r backend/requirements.txt
export PYTHONPATH=backend
export POKEANALYZER_DATABASE="$PWD/backend/instance/pokelizer.sqlite3"
export POKEANALYZER_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
python -m flask --app pokeanalyzer:create_app db-init
python -m flask --app pokeanalyzer:create_app db-status
python backend/run.py
```

O app não cria tabelas ao iniciar. `db-init` e `db-upgrade` aplicam arquivos numerados consecutivamente em `migrations/`, verificam SHA-256 das migrações já aplicadas e executam todas as pendências numa transação. Repetir o comando num banco atualizado preserva os dados. A tabela `SCHEMA_MIGRATION` registra versão, arquivo, checksum e data. `schema.sql` é o modelo físico gerado para inspeção/execução num banco vazio; o runner usa as migrações. A fonte do gerador e a verificação de correspondência estão em `tools/build_schema.py`.

Todas as conexões da aplicação ativam `foreign_keys` e `recursive_triggers`. O contexto Flask reutiliza uma conexão por requisição e fecha-a no teardown; alterações não confirmadas são revertidas. DAOs usam `transaction()`, com savepoints quando chamados dentro de outra transação. Rotas não contêm SQL.

Não existe comando de reset destrutivo. `db-init` recusa um banco legado sem histórico; não usa `CREATE TABLE IF NOT EXISTS` para alterar sua estrutura. Novas versões exigem nova migração, nunca alteração silenciosa de uma migração aplicada.

## Backup e atualização do backend antigo

```sh
python -m flask --app pokeanalyzer:create_app db-backup /caminho/novo/backup.sqlite3
python -m flask --app pokeanalyzer:create_app db-upgrade
python -m flask --app pokeanalyzer:create_app db-import-legacy /caminho/antigo.sqlite3 /caminho/novo.sqlite3
```

Backup e importação recusam destinos existentes. `db-import-legacy` reconhece as 13 tabelas do backend `5bd1357`, mantém IDs, hashes de senha, dados e relacionamentos e valida a cópia inteira num arquivo novo. A origem é aberta apenas para leitura em snapshot consistente. Uma linha incompatível com as regras revisadas interrompe a operação, informa tabela/chave e elimina apenas o destino parcial recém-criado; a origem permanece intacta. O teste preserva conta, espécie, forma, jogo, contexto e exemplar e compara o SHA-256 do arquivo original antes/depois.

Dados antigos podem exigir curadoria: presença/registro conhecidos sem fonte e data, valores de nível/natureza/habilidade sem mecânica confirmada, efeitos de natureza sem atributo reconhecido ou habilidade de outro contexto. Nenhuma mecânica/fonte é inferida. Nesse caso, mantenha origem e backup, trabalhe numa cópia separada, verifique fontes, corrija os registros indicados e repita a importação para outro destino novo. Compare contagens/IDs e consultas antes de apontar `POKEANALYZER_DATABASE` para a cópia validada. Bancos com tabelas/colunas desconhecidas são recusados para impedir perda silenciosa de dados.

## API preservada

| Método e caminho | Uso |
|---|---|
| GET `/api/status`, `/api/csrf` | Status e token CSRF |
| POST `/api/auth/cadastro`, `/api/auth/login`, `/api/auth/logout` | Conta, sessão e saída |
| GET `/api/auth/me` | Usuário autenticado; nunca retorna hash |
| GET `/api/pokemon?busca=...&tipo=ID&geracao=N&jogo=ID` | Nome/número nacional e filtros combináveis |
| GET `/api/pokemon/ID` | Contexto forma/jogo pelo `id_dados_forma` |
| GET/POST `/api/colecao` | Listar e registrar exemplares do usuário da sessão |
| GET/DELETE `/api/colecao/ID` | Consultar/excluir somente exemplar próprio |

Busca de geração usa a geração de origem da espécie. Tipo/jogo são filtros dos contextos por jogo. Espécies e formas sem contexto continuam na listagem sem esses filtros, com IDs/contexto nulos e tipos vazios; ausência de dado não é ausência confirmada. Uma forma pode produzir várias linhas, uma por jogo; a identidade global é `id_especie`/`id_forma`.

Requisições de escrita exigem `X-CSRF-Token`, obtido em `/api/csrf` e renovado ao autenticar. Coleções sempre usam o usuário da sessão, sem aceitar proprietário do corpo JSON. Cadastro usa scrypt do Werkzeug. Configure segredo persistente e cookies seguros antes de publicar com HTTPS; o servidor `run.py` é apenas desenvolvimento local.

Na coleção, `id_mecanica` é opcional quando natureza, habilidade e nível são desconhecidos. Valores conhecidos exigem mecânica compatível e limites confirmados no banco. `id_dados_forma_origem` opcional exige `id_jogo_origem` correspondente. `id_metodo_obtencao` descreve história real e não é restringido pela disponibilidade no jogo atual após uma transferência. Não é uma prova automática de legalidade competitiva.

## Verificação reproduzível

```sh
PYTHONPATH=backend python -m pytest backend/tests -q
python backend/tools/build_schema.py --check
python docs/uml/check_uml.py
```

Fixtures em `tests/fixtures/catalog.sql` usam exclusivamente nomes, URLs e limites sintéticos e bancos temporários do pytest. O loader é repetível. `tests/fixtures/legacy_v0.sql` é o esquema histórico usado apenas para testar importação. O antigo `scripts/seed_demo.py` agora recusa execução para impedir inserção de demonstrações no catálogo real. Inicialização não carrega fatos Pokémon nem fixtures.

Os testes exercitam conexão/reabertura/fechamento, rollback/savepoints, criação limpa, migração repetida, falha atômica, checksum alterado, preservação legada, backup sem sobrescrita, busca/filtros, isolamento entre usuários, autenticação, CSRF, inteiros estritos, história de aquisição e privacidade dos perfis. Os testes de esquema verificam as invariantes do modelo; veja [verificação da etapa](../docs/stage1/verification.md).
