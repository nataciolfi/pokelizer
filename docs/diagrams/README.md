# Modelos brModelo — Etapas 1 e 2

Os arquivos desta pasta foram criados **com os objetos nativos, o gravador e o exportador de imagens do brModelo 3.3.2**, distribuído pelo [site oficial](https://brmodelo.com/download.html). A automação em Java organiza os objetos; não desenha os símbolos nem fabrica o formato de arquivo. A classe `ImageGenerate` do próprio brModelo renderiza os PNG. Os `.brM3` são arquivos binários nativos, reabertos pelo carregador do brModelo durante a geração; os `.xml` são a segunda opção de gravação editável oferecida pelo próprio programa.

A ferramenta foi obtida em 13/11/2026 e executada em Java 21, sem instalar pacotes no sistema. Versão, URL, SHA-256 do JAR, SHA-256 do SQL e hashes de todos os arquivos estão em [manifest.json](manifest.json). O código-fonte público consultado é [chcandido/brModelo](https://github.com/chcandido/brModelo). Nenhum JAR de terceiro está versionado neste repositório.

Os metadados públicos `autor` e `data` do invólucro nativo `GuardaPadraoBrM` são definidos como `Pokelizer project` e vazio. A distribuição preenche esses campos com o nome do autor da ferramenta e uma data histórica fixa, mesmo quando o modelo é novo. Após a gravação oficial, a automação altera somente esses dois campos públicos e regrava o mesmo objeto com a serialização Java nativa; o conteúdo do diagrama é preservado. A atribuição da ferramenta permanece nos links oficiais desta documentação. Todos os 34 arquivos foram novamente reabertos pelo carregador oficial após essa limpeza; XML e PNG conservaram seus hashes. Veja a [revisão visual e de metadados](visual-review.md).

## Abrir e revisar

Abra [conceitual.brM3](conceitual.brM3) e [logico.brM3](logico.brM3) em **Arquivo → Abrir** no brModelo. Os arquivos completos contêm **26 entidades/tabelas, 183 atributos/campos e 43 relações**. [Conceitual PNG](conceitual.png) e [lógico PNG](logico.png) são as visões gerais.

## Visões principais para apresentar

Comece pelos domínios abaixo: entidades relacionadas próximas, nomes de relações por papel e linhas sem cruzamentos nas visões conceituais. São recortes nativos editáveis para navegação; omitem atributos e algumas relações externas. O modelo integral e as pranchas R preservam todos os campos, chaves e vínculos. Cada imagem abaixo tem `.brM3` e `.xml` com o mesmo nome-base.

| Domínio | Conceitual | Lógico |
|---|---|---|
| Catálogo global/fichas | [PNG](conceitual-visao-catalogo.png) · [brM3](conceitual-visao-catalogo.brM3) | [PNG](logico-visao-catalogo.png) · [brM3](logico-visao-catalogo.brM3) |
| Propriedade/coleção | [PNG](conceitual-visao-colecao.png) · [brM3](conceitual-visao-colecao.brM3) | [PNG](logico-visao-colecao.png) · [brM3](logico-visao-colecao.brM3) |
| Mecânicas/atributos | [PNG](conceitual-visao-atributos.png) · [brM3](conceitual-visao-atributos.brM3) | [PNG](logico-visao-atributos.png) · [brM3](logico-visao-atributos.brM3) |
| Perfis/alvos | [PNG](conceitual-visao-perfis.png) · [brM3](conceitual-visao-perfis.brM3) | [PNG](logico-visao-perfis.png) · [brM3](logico-visao-perfis.brM3) |
| Regulamentos/elegibilidade | [PNG](conceitual-visao-regulamentos.png) · [brM3](conceitual-visao-regulamentos.brM3) | [PNG](logico-visao-regulamentos.png) · [brM3](logico-visao-regulamentos.brM3) |

Os completos foram reordenados por proximidade de domínio e recebem nomes como “da espécie”, “estado atual”, “tem origem” e “sob limites”. Continuam grandes e densos: não imprimir a visão integral reduzida como único material de leitura. As visões gerais são grandes. Para apresentação e impressão, use também as folhas ampliadas abaixo: cada painel mostra uma relação, seus dois participantes com todos os atributos/campos, cardinalidades, colunas vinculadas e ações referenciais. Uma entidade reaparece em várias folhas como vista do mesmo objeto de negócio; isso não representa novas tabelas. Cada folha tem também seu próprio `.brM3` editável e XML, com o mesmo nome base do PNG.

| Folha | Relações | Conceitual | Lógico |
|---|---|---|---|
| 01 | R1–R4 | [PNG](conceitual-relacoes-01.png) · [brM3](conceitual-relacoes-01.brM3) | [PNG](logico-relacoes-01.png) · [brM3](logico-relacoes-01.brM3) |
| 02 | R5–R8 | [PNG](conceitual-relacoes-02.png) · [brM3](conceitual-relacoes-02.brM3) | [PNG](logico-relacoes-02.png) · [brM3](logico-relacoes-02.brM3) |
| 03 | R9–R12 | [PNG](conceitual-relacoes-03.png) · [brM3](conceitual-relacoes-03.brM3) | [PNG](logico-relacoes-03.png) · [brM3](logico-relacoes-03.brM3) |
| 04 | R13–R16 | [PNG](conceitual-relacoes-04.png) · [brM3](conceitual-relacoes-04.brM3) | [PNG](logico-relacoes-04.png) · [brM3](logico-relacoes-04.brM3) |
| 05 | R17–R20 | [PNG](conceitual-relacoes-05.png) · [brM3](conceitual-relacoes-05.brM3) | [PNG](logico-relacoes-05.png) · [brM3](logico-relacoes-05.brM3) |
| 06 | R21–R24 | [PNG](conceitual-relacoes-06.png) · [brM3](conceitual-relacoes-06.brM3) | [PNG](logico-relacoes-06.png) · [brM3](logico-relacoes-06.brM3) |
| 07 | R25–R28 | [PNG](conceitual-relacoes-07.png) · [brM3](conceitual-relacoes-07.brM3) | [PNG](logico-relacoes-07.png) · [brM3](logico-relacoes-07.brM3) |
| 08 | R29–R32 | [PNG](conceitual-relacoes-08.png) · [brM3](conceitual-relacoes-08.brM3) | [PNG](logico-relacoes-08.png) · [brM3](logico-relacoes-08.brM3) |
| 09 | R33–R36 | [PNG](conceitual-relacoes-09.png) · [brM3](conceitual-relacoes-09.brM3) | [PNG](logico-relacoes-09.png) · [brM3](logico-relacoes-09.brM3) |
| 10 | R37–R40 | [PNG](conceitual-relacoes-10.png) · [brM3](conceitual-relacoes-10.brM3) | [PNG](logico-relacoes-10.png) · [brM3](logico-relacoes-10.brM3) |
| 11 | R41–R43 | [PNG](conceitual-relacoes-11.png) · [brM3](conceitual-relacoes-11.brM3) | [PNG](logico-relacoes-11.png) · [brM3](logico-relacoes-11.brM3) |

No conceitual, círculo preenchido identifica o atributo identificador, círculo tracejado indica opcionalidade; os relacionamentos são losangos. As entidades associativas foram explicitadas como entidades com seus próprios vínculos, preservando disponibilidade, valores, elegibilidade e proveniência. No lógico, ícones de chave indicam PK/FK; tipos são os do SQLite. `NOT NULL` está no complemento nativo de cada campo e as chaves únicas estão nas restrições editáveis da tabela. O arquivo físico executável é [backend/schema.sql](../../backend/schema.sql).

Cardinalidades desenhadas representam os vínculos estruturais: filho → pai `1..1` para FK obrigatória ou `0..1` para FK opcional; pai → filhos `0..N`. Regras condicionais não cabem em uma cardinalidade estática: espécie completa tem exatamente uma forma padrão; tipos confirmados têm posições 1 e, opcionalmente, 2; perfil personalizado tem um proprietário, perfil de referência não tem proprietário. Essas condições estão registradas nas folhas e detalhadas nas [regras de integridade](../stage1/integrity.md) e na [especificação](../stage1/README.md). FKs compostas são um único vínculo R com todas as colunas, não relações independentes. Origem e destino de transformação são papéis distintos.

## Verificação e reprodução

Sem dependências Python adicionais, na raiz do repositório:

```bash
python docs/diagrams/tooling/check_models.py
```

O verificador executa o SQL em memória e compara os XML efetivamente gravados pelo brModelo: entidades, atributos/campos, tipos, nulabilidade, identificadores/PK/FK, chaves únicas, relações compostas, cardinalidades e ações de exclusão/atualização. Também confere a cobertura das folhas, o hash do SQL e todos os binários/imagens. A evidência de reabertura de **cada** arquivo nativo está em [tooling/reopen-verification.txt](tooling/reopen-verification.txt).

Para regenerar após uma alteração do SQL, obtenha o JAR no site oficial e use um JDK (Java 21 verificado nesta entrega):

```bash
export BRMODELO_JAR=/caminho/brModelo.jar
python docs/diagrams/tooling/export_models.py
python docs/diagrams/tooling/check_models.py
```

Se `java`/`javac` não estiverem no PATH, defina `JAVA` e `JAVAC` para os executáveis. O script usa um diretório temporário para compilar o adaptador. Apenas os callbacks de interface do editor (inspector, recentes e autosave) são omitidos; objetos, conexões, formatos, salvamento, carregamento e renderização permanecem os da distribuição oficial. Revise os PNG após regenerar. O SQL e o texto dos invariantes continuam sendo a autoridade para CHECKs e regras de contexto que a notação não representa diretamente; não execute o DDL gerado automaticamente pelo brModelo como substituto do SQL revisado.
