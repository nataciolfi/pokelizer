# Relatório de conclusão técnica da Etapa 1

Branch de revisão: `stage1/reconciled-architecture`. Não houve merge em main, force-push, remoção de branches ou alteração de outros projetos. A árvore inicial estava limpa. O histórico novo separa reconciliação de requisitos, implementação física/Python e entrega/verificação dos modelos.

## Implementado

- Especificação única para o produto completo, matriz de requisitos com estado real, decisões de branches, arquivos históricos explicitamente não normativos.
- 26 tabelas STRICT, 183 campos e 43 relações FK; PK, UNIQUE, CHECK, índices e ações referenciais explícitas. Uma tabela adicional formaliza atributos aplicáveis por sistema/versão. SQL e migração gerados de uma fonte revisável; deriva detectada sem reescrever artefatos.
- Invariantes de espécie completa/padrão, cobertura de tipos, contextos de habilidade/natureza/nível, sistemas e limites individuais/totais, perfil proprietário, regulamentos/elegibilidade, transformações e atualizações inversas protegidos no banco conforme matriz de enforcement.
- Conexões Python com FK/gatilhos ativos, teardown, transação/savepoints, comandos de inicialização/upgrade/backup/importação validada. Sem recriação destrutiva. Legacy importado somente em destino novo, sem inventar mecânica; origem e dados preservados ou operação recusada por inteiro.
- Backend existente preservado e adaptado: contas/scrypt/sessão/CSRF, catálogo global e filtros, coleção privada; criação/consulta privada de perfis na camada Python. Rotas sem SQL.
- Conceitual e lógico genuínos brModelo, nativos editáveis, exports e folhas legíveis; UML editável/exportado com classes reais separadas do comparador planejado.

## Decisões de arquitetura

DADOS_FORMA_JOGO é único por forma+jogo; a versão de mecânica permanece separada. Exemplar guarda contexto atual e origem opcional, sem misturar sistemas nem converter treinamento. Disponibilidade de método não determina a procedência real no jogo atual. Espécie/forma não exigem ficha de jogo. Publicar espécie completa exige exatamente uma padrão; publicar tipos aplicáveis exige cobertura primária. Perfis e regulamentos têm contexto/evidência. Comparação futura é explícita por campo e não pressupõe maior=melhor. Elegibilidade de forma não comprova legalidade individual. Veja [decisions.md](decisions.md) para justificativas e propostas divergentes rejeitadas.

## Caminhos obrigatórios

| Entrega | Nativo/editável ou código | Exportação/evidência |
|---|---|---|
| Conceitual | [docs/diagrams/conceitual.brM3](../diagrams/conceitual.brM3) | [conceitual.png](../diagrams/conceitual.png), [folhas ampliadas e XML](../diagrams/README.md) |
| Lógico | [docs/diagrams/logico.brM3](../diagrams/logico.brM3) | [logico.png](../diagrams/logico.png), [folhas ampliadas e XML](../diagrams/README.md) |
| Físico | [backend/schema.sql](../../backend/schema.sql) | [migração 001](../../backend/migrations/001_stage1.sql) e testes |
| UML | [docs/uml/classes.puml](../uml/classes.puml) | [classes.svg](../uml/classes.svg), [classes.png](../uml/classes.png) |
| Banco/conexão | [backend/pokeanalyzer/db.py](../../backend/pokeanalyzer/db.py) | [comandos reproduzíveis](../../backend/README.md), banco vazio criado localmente, testes de persistência/JOIN |
| Rastreabilidade | [requirements.md](requirements.md) | [cardinalidades/campos](data-model.md), [invariantes](integrity.md) |

## Verificação

Após instalar requirements em venv, executar `python tools/check_stage1.py`. Nesta máquina foi usado `PYTHONPATH=/home/Danilo/tools/python:backend python tools/check_stage1.py` para acessar dependências isoladas. Resultado: gerador/SQL/migração iguais; dicionário atualizado; modelos brModelo com 26 entidades, 183 campos e 43 relações; hashes nativos/exports intactos; UML com 11 classes reais consistente; links locais válidos; **45 testes aprovados**. Inicialização real aplicou [1], segundo upgrade não aplicou nada e db-status mostrou versão/checksum. Detalhes, limites do verificador e inspeção visual estão em [verification.md](verification.md).

## Pendências e limites

Não há bloqueio técnico obrigatório de brModelo/UML/SQL/conexão. O produto final continua incompleto por definição da etapa: falta carga oficial completa, analisador, edição HTTP completa, frontend e integração Fetch. As obrigações futuras permanecem mapeadas; não foram reclassificadas como opcionais. Dados legados incompatíveis precisam de curadoria explícita numa cópia antes da importação.

A publicação do Word original do professor foi recusada pela revisão automática pelo risco de informação pessoal/organizacional em repositório público. Foi usada alternativa segura: original mantido localmente, somente resumo dos requisitos sem contato publicado. Isso não bloqueia nenhum artefato obrigatório da etapa. A revisão automática também recusou um arquivo nativo pelo autor/data padrão da ferramenta; esses metadados foram retirados pelo gravador nativo, com reabertura e conferência dos modelos antes da publicação.

Ações manuais: confirmar/adicionar colaborador do professor com o contato do documento original; verificar aceitação; anexar nativos/exports/SQL/UML e link da branch/commit no Classroom e concluir envio. Não houve convite nem submissão nesta tarefa. Prazo escolar da Etapa 1 foi 09/11/2026; esta execução em 13/11/2026 não comprova entrega no prazo. [Instruções exatas](submission.md).
