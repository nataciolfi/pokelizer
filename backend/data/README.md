# Dados reais e cobertura

Fonte: [CSV do projeto PokéAPI](https://github.com/PokeAPI/pokeapi/tree/8a92bfa7dab2f12b84b5d151562f9857c133ff30/data/v2/csv), commit fixo `8a92bfa7dab2f12b84b5d151562f9857c133ff30`, consultado em 13/11/2026. A semântica dos recursos está na [documentação da PokéAPI](https://pokeapi.co/docs/v2). PokéAPI é uma fonte comunitária; estes dados não são uma certificação oficial da The Pokémon Company. Licença e atribuição preservadas em [LICENSE.md](pokeapi/LICENSE.md).

O [manifest](pokeapi/manifest.json) fixa URL e SHA-256 de cada arquivo. As cópias permitem executar a carga offline. Nomes ingleses vêm de `local_language_id=9`; `nome_pt` herdado é usado como nome de exibição, sem alegar tradução confirmada. `codigo_forma` é o identificador da fonte. Forma padrão exige Pokémon padrão da espécie e forma padrão daquele Pokémon. Uma forma de batalha recebe estado temporário; os demais estados permanecem não verificados. Espécies permanecem rascunho para curadoria. Nenhum fato de presença, tipagem histórica, habilidade, mecânica ou elegibilidade é inferido de identidade global.

```bash
# Banco já inicializado, com DATABASE apontando para arquivo escolhido:
python -m flask --app pokeanalyzer:create_app catalog-import
python -m flask --app pokeanalyzer:create_app catalog-coverage
# Reobter os mesmos bytes em um NOVO diretório (exige rede):
python backend/scripts/download_catalog.py /caminho/novo/snapshot
```

Executar as duas primeiras operações a partir de `backend/`, ou definir `PYTHONPATH=backend` na raiz. A carga verifica todos os hashes antes de escrever. Usa números nacionais e códigos, sem assumir os IDs internos da base de destino. Repetição não duplica. Conflitos com curadoria prévia abortam a transação inteira e exigem revisão; não usar REPLACE nem apagar coleção/perfis para resolvê-los.

[Relatório de cobertura real executado](../../docs/stage2/coverage.json): 1.025 espécies, 1.579 formas, 51 jogos; zero fichas por jogo, mecânicas, regulamentos e elegibilidades. Cobertura completa do snapshot global não significa catálogo contextual completo ou atualizado para sempre. Para concluir o produto, importar fichas e regras a partir de fontes específicas por jogo/versão, conservar fonte/data e reexecutar testes e relatório. Dados não verificados devem permanecer identificados dessa forma.

Fixtures em `backend/tests/fixtures/` têm nomes `FIXTURE`, números sintéticos e fontes `example.invalid`; não são fatos oficiais e não são carregadas por `catalog-import` ou startup. A [demonstração](../../tools/demonstrate_stage2.py) cria e remove seu próprio banco temporário.
