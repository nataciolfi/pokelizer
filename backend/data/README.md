# Dados reais e cobertura

Fonte: [CSV do projeto PokéAPI](https://github.com/PokeAPI/pokeapi/tree/8a92bfa7dab2f12b84b5d151562f9857c133ff30/data/v2/csv), commit fixo `8a92bfa7dab2f12b84b5d151562f9857c133ff30`, consultado em 13/11/2026. A semântica dos recursos está na [documentação da PokéAPI](https://pokeapi.co/docs/v2). PokéAPI é uma fonte comunitária; estes dados não são uma certificação oficial da The Pokémon Company. Licença e atribuição preservadas em [LICENSE.md](pokeapi/LICENSE.md).

O [manifest](pokeapi/manifest.json) fixa URL e SHA-256 de cada arquivo. As cópias permitem executar a carga offline. Nomes ingleses vêm de `local_language_id=9`; `nome_pt` herdado é usado como nome de exibição, sem alegar tradução confirmada. `codigo_forma` é o identificador da fonte. Forma padrão exige Pokémon padrão da espécie e forma padrão daquele Pokémon. Categoria padrão é atribuída somente à forma padrão; categorias alternativas permanecem não verificadas, sem usar o default SQL como fato. Uma forma de batalha recebe estado temporário; os demais estados permanecem não verificados. Espécies permanecem rascunho para curadoria. Nenhum fato de presença, tipagem histórica, habilidade, mecânica ou elegibilidade é inferido de identidade global.

```bash
# Banco já inicializado, com DATABASE apontando para arquivo escolhido:
python -m flask --app pokeanalyzer:create_app catalog-import
python -m flask --app pokeanalyzer:create_app catalog-coverage
# Reobter os mesmos bytes em um NOVO diretório (exige rede):
python backend/scripts/download_catalog.py /caminho/novo/snapshot
```

Executar as duas primeiras operações a partir de `backend/`, ou definir `PYTHONPATH=backend` na raiz. A carga verifica todos os hashes antes de escrever. Usa números nacionais e códigos, sem assumir os IDs internos da base de destino. Repetição não duplica. Conflitos com curadoria prévia abortam a transação inteira e exigem revisão; não usar REPLACE nem apagar coleção/perfis para resolvê-los.

[Relatório inicial da Etapa 2](../../docs/stage2/coverage.json) registrava zero fichas por jogo. A [cobertura atual](../../docs/project/coverage-final.json), executada em banco vazio, registra 1.025 espécies, 1.579 formas, 51 jogos e 5.072 fichas de encontros selvagens; mecânicas, regulamentos e elegibilidades permanecem sem dados reais importados. Cobertura completa do snapshot global não significa catálogo contextual completo ou atualizado para sempre. Para concluir o produto, importar fichas e regras a partir de fontes específicas por jogo/versão, conservar fonte/data e reexecutar testes e relatório. Dados não verificados devem permanecer identificados dessa forma.

Fixtures em `backend/tests/fixtures/` têm nomes `FIXTURE`, números sintéticos e fontes `example.invalid`; não são fatos oficiais e não são carregadas por `catalog-import` ou startup. A [demonstração](../../tools/demonstrate_stage2.py) cria e remove seu próprio banco temporário.

## Encontros selvagens no contexto de jogo

`encounters.csv.gz` é uma cópia compactada do arquivo de encontros do mesmo commit fixo. O manifest registra o SHA-256 tanto dos bytes originais quanto do gzip reproduzível. O importador considera somente um encontro registrado para uma forma que é a única forma daquele `pokemon_id`, é a padrão desse Pokémon e não é exclusiva de batalha. Apenas métodos identificados como grama, água, pesca, pedras, árvores ou terrenos selvagens selecionados são aceitos; presentes, trocas com NPC, eventos e outros métodos são excluídos. Cada ficha inserida tem estado `nativa`, registro independente `sim`, fonte e data; o método é “Encontro selvagem”. Uma linha de encontro comprova esse caso documentado, não todos os métodos ou a legalidade de um exemplar. A ausência de linha não comprova indisponibilidade.

O esquema atual identifica jogos pelo nome; como as versões Red/Red japonesa e Blue/Blue japonesa da fonte compartilham nomes ingleses, **ambas as versões de cada par foram excluídas da importação contextual** até existir identidade de versão sem ambiguidade. Índices internos de jogo não foram usados como evidência de presença. Contextos preexistentes são preservados sem sobreposição; o relatório mostra quantas fichas pertencem a outras fontes. As regras de mecânica e os tipos/estatísticas históricos ainda exigem importação versionada própria.

## Imagens de espécies e formas

A interface referencia imagens do repositório [PokéAPI Sprites](https://github.com/PokeAPI/sprites/tree/c0542f7c51215d9672439012838c99f520596cbd), fixado no commit `c0542f7c51215d9672439012838c99f520596cbd`. O mapeamento usa o `pokemon_id` somente quando ele corresponde a uma única forma na tabela versionada, evitando atribuir a mesma imagem indevidamente a variantes distintas. Sem mapeamento, conexão ou imagem disponível, aparece um símbolo neutro.

A [licença declarada pelo repositório](https://github.com/PokeAPI/sprites/blob/c0542f7c51215d9672439012838c99f520596cbd/LICENCE.txt) identifica direitos das imagens à The Pokémon Company e declara CC0 para o repositório; essa declaração não comprova concessão de todos os direitos das imagens por seus titulares. Os arquivos de imagem não são distribuídos neste repositório e são buscados diretamente da fonte. Para publicação ou redistribuição além da apresentação escolar, verifique as permissões aplicáveis com os titulares.
