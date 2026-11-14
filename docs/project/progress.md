# Continuidade do Pokelizer

## Base auditada em 13/11/2026

Branch de trabalho: `stage2/functional-delivery`, derivada de `stage1/reconciled-architecture` em `91875bd`. Árvore inicial limpa; nenhuma instrução AGENTS.md encontrada no repositório ou ancestrais. Remoto consultado pelo conector GitHub: não há commits posteriores; `main=f0e570b` está atrasada. Auditorias divergentes já reconciliadas na base; não fazer merge indiscriminado.

Documento local `Projeto_Integrado_Etapas_GitHub.docx` lido: Etapa 1 09/11, Etapa 2 13/11, final 17/11/2026. Usuário informou três dias para Etapa 2; divergência registrada, sem alterar datas do professor. Escopo completo mantido, sem tratar como MVP.

Baseline: 45 testes passaram (`PYTHONPATH=/home/Danilo/tools/python:backend python -m pytest backend/tests -q`). Ambiente tem ferramentas portáteis em `/home/Danilo/tools`: Git, Java, brModelo, PlantUML e dependências Python. `git` não está no PATH padrão; `.venv` herdada não contém as dependências neste runtime. Rede de shell sem DNS; conector GitHub funciona. Usar caminhos portáteis neste ambiente, instalação convencional documentada para outro computador.

Confirmado: coleção sem edição, atributos enviados ignorados, perfis sem HTTP CRUD, analisador ausente, busca sem codigo_forma, catálogo por ficha repete identidades. SQL/migrações e DAOs existentes serão preservados onde corretos. Imagens gerais abertas visualmente: muitos corredores sobrepostos, nomes genéricos e entidades distantes; precisa melhorar além da verificação estrutural.

## Em execução

1. CRUD transacional de coleção/atributos e perfis, validação estrita, comparação contextual e elegibilidade.
2. Catálogo global com fichas por jogo, códigos e filtros; carga real reproduzível com cobertura e fontes.
3. Diagramas nativos por domínio, UML atualizado, documentação e demonstração.
4. Após verificar Etapa 2: interface nova HTML/CSS/JS Fetch e integração; completar cobertura do catálogo.

## Pendências de entrega manual

Confirmar conta do professor usando o contato do documento original, convidar em Settings → Collaborators e verificar aceitação. Anexar arquivos ao Classroom e confirmar envio. Não houve convite nem submissão externa.

## Próximo passo

Implementar e testar serviços/DAOs/rotas da Etapa 2. Antes de retomar, ler este arquivo e conferir Git/árvore real. Nenhuma entrega foi declarada pronta.

## Implementado e testado nesta sessão

- Backend: PATCH privado da coleção; valores incluídos/consultados/substituídos na transação do exemplar; rollback de pai/filhos; mudança de contexto exige valores explícitos.
- CRUD de perfis personalizados, preferências de natureza/habilidade, alvos e autorização no DAO/serviço. Referências compartilhadas são somente leitura.
- Comparação com contexto exato, estados por campo, ausência/zero/desconhecido/não aplicável, diferenças sem pontuação; elegibilidade de forma com fonte e escopo limitado.
- Busca por codigo_forma/número/nome; listagem agrupada por identidade, fichas por jogo aninhadas e filtros no mesmo contexto; detalhe global e contextual.
- Corpos JSON e campos inválidos rejeitados; endpoints de opções e regras para clientes.
- Snapshot real PokéAPI fixado em `8a92bfa7dab2f12b84b5d151562f9857c133ff30`, fontes e SHA-256; importação transacional repetível sem sobrescrever conflitos, relatório de cobertura e downloader para novo destino.
- `PYTHONPATH=/home/Danilo/tools/python:backend python -m pytest backend/tests -q`: **69 passaram**. Inclui preservação de dados privados e conflitos na carga real. Esquema/migrações 001 não foram alterados.

Próximo passo em andamento: regenerar/revisar diagramas e UML. Depois documentar demonstração limpa e executar verificação completa. Interface Fetch e cobertura factual por jogo continuam obrigatórias. Não confundir cobertura global do snapshot com cobertura de fichas/mecânicas/regulamentos.
