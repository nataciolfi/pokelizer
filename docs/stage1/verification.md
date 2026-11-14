# Verificação da entrega

> Registro histórico da Etapa 1 em `91875bd`. Implementações e verificações posteriores estão em [Etapa 2](../stage2/README.md) e [progress.md](../project/progress.md). Estados “futuro/pendente” abaixo descrevem aquela entrega.


Ambiente da execução em 2026-11-13: Python 3.13, SQLite 3.46.1. Instalação isolada nesta máquina em /home/Danilo/tools/python; em um clone normal instalar backend/requirements.txt em venv e usar somente PYTHONPATH=backend.

## Comandos executados

```sh
PYTHONPATH=/home/Danilo/tools/python:backend python -m pytest backend/tests -q
python backend/tools/build_schema.py --check
python tools/document_model.py --check
python docs/uml/check_uml.py
python docs/diagrams/tooling/check_models.py
python tools/check_links.py
# Ou executar todos em um comando:
PYTHONPATH=/home/Danilo/tools/python:backend python tools/check_stage1.py
```

Resultado: **45 passed**. O gerador --check confere bytes sem escrever arquivos; teste de deriva comprova que ele falha quando a fonte muda e preserva a saída anterior. O dicionário compara todas as tabelas/campos/FKs do SQL. O UML confere 11 classes reais, campos/métodos, infraestrutura sem SQL em rotas e hashes das exportações revisadas.

Foi criado e mantido localmente um banco vazio funcionando em backend/instance/pokelizer.sqlite3, ignorado pelo Git. Os seguintes comandos reais retornaram:

```text
db-init:    Migrações aplicadas: [1]
db-upgrade: Migrações aplicadas: nenhuma (atualizado)
db-status:  1: 001_stage1.sql 54ca87ef7693f498639d12338e48c0e11c846f960964ca2c2e16cb184f8f8b2e
```

O comando completo usa `PYTHONPATH=backend python -m flask --app pokeanalyzer:create_app` antes de db-init/db-upgrade/db-status; nesta máquina foi acrescentado /home/Danilo/tools/python ao PYTHONPATH. O banco começa sem dados de catálogo; as provas de persistência com dados estão em bancos temporários dos testes, separados do arquivo real.

## O que cada teste prova

| Arquivo | Verificação exercitada |
|---|---|
| backend/tests/test_schema.py | Criação STRICT; FK; unicidade de número/forma/ficha; mínimo/máximo padrão; publicação e exclusão/alteração da padrão; tipos duplicados/slots/cobertura; habilidade/mecânica incompatíveis; origem separada; perfil dono/opções/contexto; limite individual e combinado para exemplar/perfil; desconhecido/não aplicável/zero; elegibilidade com fonte/condição e jogo correto; transformação compatível; atualização inversa; deletes; REPLACE; gerador --check sem escrita |
| backend/tests/test_db.py | Repetição de upgrade e persistência; nova migração preservando dados; falha DDL+DML reverte; checksum alterado rejeitado; savepoints; connection reuse/close e rollback no teardown; importação legada com IDs/hash/apelido/relações preservados e fonte SHA-256 intacta, inclusive nomes de arquivo com ?/#; cópia inválida removida sem alterar fonte; backup sem sobrescrita; FK/gatilhos ativados em conexão crua |
| backend/tests/test_api.py | Cadastro/hash/login/logout/CSRF; privacidade com dois usuários; consulta/inclusão/exclusão; validação de IDs e nível; contexto proibido/habilidade incompatível; número/nome/código e filtros; identidades sem ficha; procedência diferente do atual; rollback; fixture carregada repetidamente sem duplicar; criação/consulta de perfil privado Python e contexto incompatível |

Nenhum teste é usado como evidência de correção de fatos oficiais ou completude da Pokédex. As fixtures são sintéticas identificadas como FIXTURE e vivem somente em tests/fixtures; o antigo seed de demonstração foi desativado para evitar contaminar o catálogo.

## Modelos nativos e inspeção visual

O [índice brModelo](../diagrams/README.md) contém os arquivos nativos, exportações, metodologia e comando de conferência de consistência. Conferir o esquema, os campos, chaves e as 43 relações, os hashes dos nativos/exports e a reabertura real no brModelo. Os detalhes de execução e limitações da inspeção ficam naquele índice.

Para repetir a revisão humana: abrir as duas visões gerais e todas as pranchas ampliadas em 100%/zoom, verificar todas as margens e textos, ler as 43 relações no manifesto e comparar com [data-model.md](data-model.md). Abrir o .brM3 no brModelo, editar em uma cópia e exportar para comprovar editabilidade. Conferir o UML vetorial e PNG, com atenção às 11 classes implementadas e à classe planejada separada. Não substituir essa etapa por um hash: o hash só detecta mudança posterior à inspeção.

## Checklist repetível de consistência

- [x] Conceitual e lógico têm as mesmas 26 entidades/tabelas e 183 atributos/campos do domínio; chaves e nulabilidade conferidas no modelo lógico.
- [x] As 43 FKs têm relações correspondentes, inclusive dois papéis de origem/destino e FK composta de habilidade; mínimos condicionais estão anotados, não escondidos em cardinalidade genérica.
- [x] SQL direto e migração inicial têm os mesmos bytes; o runner acrescenta somente metadados SCHEMA_MIGRATION.
- [x] Dicionário é gerado por introspecção do SQL e todas as relações têm mínimos/máximos/ações de exclusão.
- [x] UML usa nomes e métodos reais, com referências a objetos separadas das relações de tabelas.
- [x] Conexão e DAOs consultam colunas existentes; testes API e consultas JOIN exercitam essa compatibilidade.
- [x] Fontes não confirmadas, zero, desconhecido e não aplicável permanecem distintos; sem seed oficial inventado.
- [x] Migração e importação preservam banco anterior e não inferem mecânicas; dados incompatíveis exigem curadoria explícita.
- [x] Nenhuma etapa foi enviada ao Classroom nem convite a colaborador foi emitido.

## Limitações que permanecem

A Etapa 1 não entrega aplicação final: carga oficial completa, comparação, edição completa e frontend permanecem no plano obrigatório. A validação estrutural não substitui verificação de fatos, fontes/licenças ou interpretação de um regulamento. Migração de dados legados incoerentes recusa a cópia inteira e exige curadoria em cópia separada, sem apagar/inventar valores para passar nas restrições.

A aceitação escolar e submissão no prazo não podem ser comprovadas por testes de software. A Etapa 1 venceu em 09/11/2026 segundo o documento recebido. Conferir acesso do professor e concluir Classroom manualmente, conforme [submission.md](submission.md).
