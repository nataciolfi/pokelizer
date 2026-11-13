# Especificação autoritativa — Pokelizer Etapa 1

Esta é a especificação reconciliada do produto completo. A Etapa 1 implementa banco, conexão, arquitetura e documentação; a interface final e o analisador completo são trabalho posterior obrigatório. Não há entrega MVP nem redução do produto a uma demonstração.

## Produto acordado

Catálogo completo de espécies e formas oficiais, contas e coleções privadas de exemplares, filtros por número/nome/tipo/geração/jogo, perfis pessoais e referências competitivas com evidência, comparação explicável e elegibilidade de formas por regulamentos versionados. Identidade global, ficha por jogo, versão de mecânica, procedência e estado atual são conceitos distintos. Sistemas não confirmados permanecem desconhecidos; transformação não gera exemplar independente automaticamente. HTML/CSS/JavaScript consumirão a API Flask em etapa posterior, sem obrigação de seguir wireframes antigos.

Não inclui simulador de batalhas, equipes, marketplace, rede social ou certificação de legalidade completa de indivíduos.

## Leitura e entregáveis

1. [Decisões e evidência de branches](decisions.md).
2. [Matriz de requisitos, critérios e estado real](requirements.md).
3. [Dicionário e todas as cardinalidades/ações de exclusão](data-model.md).
4. [Invariantes e fronteiras entre SQL, serviço e importação](integrity.md).
5. [Modelos genuínos brModelo e exportações](../diagrams/README.md).
6. [Modelo físico executável](../../backend/schema.sql), [migrações](../../backend/migrations/) e [conexão/comandos Python](../../backend/README.md).
7. [UML de classes implementadas](../uml/README.md).
8. [Contrato futuro do analisador](analysis.md) e [fontes/estados desconhecidos](sources.md).
9. [Verificação reproduzível e limitações](verification.md) e [submissão manual](submission.md).

Os textos em [archive](../archive/) preservam as propostas anteriores, inclusive a branch divergente de correção. Não são especificação vigente. Os caminhos de documentos antigos apontam para este índice para evitar versões concorrentes.

## Autoridade do SQL

As definições revisáveis estão em backend/tools/schema_base.sql e backend/tools/build_schema.py (gatilhos). O gerador produz backend/schema.sql e a migração inicial como artefatos idênticos; não existem duas versões independentes do esquema. Testes comparam a saída e a estrutura criada. Uma migração já distribuída/aplicada não deve ser editada; novas mudanças posteriores a esta entrega recebem 002, 003 etc., e o checksum detecta edição de histórico.

Os 26 conceitos de domínio incluem os 25 exigidos e MECANICA_ATRIBUTO, associação que torna explícita a aplicabilidade de cada atributo no sistema/versão. SCHEMA_MIGRATION é metadado técnico do executor, fora do domínio. Veja a matriz para não confundir entidades persistidas com classes Python implementadas.
