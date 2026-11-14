# Etapa 2 — backend e regularização da Etapa 1

Base auditada: `91875bd`, branch `stage1/reconciled-architecture`. A árvore estava limpa e as branches remotas não tinham avanços posteriores. A `main` continua histórica; esta entrega é desenvolvida em `stage2/functional-delivery`.

O documento do professor pede classes, DAOs, Flask e cadastro/consulta no banco, sem exigir frontend finalizado nesta etapa. Indica 13/11/2026 para Etapa 2 e 17/11 para a final. O pedido informa três dias para regularização: confirmar o prazo com o professor sem alterar o documento. O escopo final permanece integral.

## Implementação e evidência

| Requisito | Implementação | Evidência |
|---|---|---|
| Modelos conceitual/lógico nativos | 26 entidades, 183 campos, 43 relações; modelos integrais, visões por domínio e 22 pranchas | [Diagramas](../diagrams/README.md), [revisão visual](../diagrams/visual-review.md) |
| SQL e conexão Python | Esquema STRICT, FKs e gatilhos; migração versionada, backup e importação legada sem sobrescrita | [SQL](../../backend/schema.sql), [db.py](../../backend/pokeanalyzer/db.py), testes DB/schema |
| UML correspondente às classes reais | Modelos, DAOs, serviços e dependências, incluindo analisador implementado | [UML](../uml/README.md), AST + exportações revisadas |
| Coleção privada | Criar, listar, consultar, PATCH, excluir; dono vem da sessão | [Serviços](../../backend/pokeanalyzer/services.py), [rotas](../../backend/pokeanalyzer/api.py), testes de dois usuários |
| Atributos e perfis | Valores por mecânica/sistema/atributo; CRUD privado de perfis; preferências; gravação atômica de pai/filhos | Limites individuais e totais, rollback após filho inválido, mudança de contexto explícita |
| Catálogo | Nome/número/código, filtros de tipo/geração/jogo, uma identidade por forma e fichas aninhadas | Regressão de múltiplos jogos e formas sem ficha |
| Análise | Compatibilidade exata e estados por campo; ausência, zero, desconhecido e não aplicável separados | Testes de alvos menores, campos ausentes, mecânicas distintas; nenhuma nota global |
| Elegibilidade | Consulta contextual com fonte, condição e estado; sem alegar legalidade individual | Testes de regra/ficha ausente ou incompatível e evidência preservada |
| Validação | Corpos e campos desconhecidos rejeitados, listas e números estritos | HTTP 400 sem sucesso após ignorar campos; CSRF e autenticação mantidos |
| Dados reais reproduzíveis | Snapshot fixo com licença e hashes, carga atômica repetível, conflitos preservados | [Cobertura executada](coverage.json), [fontes](../../backend/data/README.md) |
| Demonstração | Cenário HTTP pelo cliente Flask, banco temporário e fatos explicitamente sintéticos | [Script](../../tools/demonstrate_stage2.py), [resultado](demo-result.txt) |

A carga real contém **1.025 espécies, 1.579 formas e 51 jogos**, cobrindo as identidades do snapshot da PokéAPI. **Não contém fichas por jogo, mecânicas, regulamentos ou referências competitivas confirmados.** As operações contextuais são demonstradas com fixtures identificadas, não apresentadas como fatos Pokémon. A cobertura factual por jogo continua uma pendência obrigatória do produto final. O backend recusa valores que dependam de limites não confirmados.

## Verificação

Com dependências instaladas, na raiz:

```bash
python tools/check_stage2.py
PYTHONPATH=backend python tools/demonstrate_stage2.py
```

No ambiente desta sessão foram usadas dependências locais previamente disponíveis: `PYTHONPATH=/home/Danilo/tools/python:backend`. O shell não tem DNS; o snapshot foi obtido pelo conector GitHub, nos URLs fixos do manifest, e a carga offline foi executada. O downloader de rede fica disponível para outro computador; sua transferência pelo shell **não foi confirmada aqui**. Todos os hashes e a leitura offline foram verificados.

O banco de teste limpo foi criado em `/tmp/pokelizer-stage2-clean.sqlite3`: `db-init` aplicou `[1]`; `db-upgrade` reaplicado não alterou nada; `catalog-import` gerou o relatório de cobertura. O banco local anterior em `backend/instance/` não foi modificado. Os testes existentes verificam backup, checksum, migração atômica, importação legada e preservação da origem.

## Apresentação e envio

1. Clonar a branch publicada, instalar dependências e criar um banco novo conforme o [backend](../../backend/README.md).
2. Mostrar as visões de catálogo, coleção, atributos, perfis e regulamentos. Abrir também os `.brM3` completos e uma prancha ampliada; apresentar SQL e UML.
3. Executar a demonstração FIXTURE e a suíte. Explicar onde ficam classes, DAOs, validações e transações.
4. Carregar o snapshot real e mostrar `catalog-coverage`. Distinguir identidade global das fichas ainda não verificadas.
5. No GitHub, Settings → Collaborators → Add people: buscar o e-mail do professor no documento original, confirmar a conta e verificar aceitação do convite. Esta sessão não enviou convite.
6. No Classroom, anexar `.brM3`, imagens de domínio/pranchas, SQL, UML, relatório e link da branch/commit. Abrir os anexos para conferir e clicar em entregar; guardar o comprovante. Nenhuma submissão foi feita automaticamente.

## Continuidade do projeto final

A interface definitiva deve ter novo design, HTML/CSS/JavaScript, Fetch e fluxos integrados de catálogo, coleção, perfis e análise. Continuam obrigatórios a cobertura contextual real, fontes verificadas, revisão visual/responsiva e testes no navegador. O prazo do backend determina a ordem; não reduz essas obrigações. Estado mais recente em [progress.md](../project/progress.md).
