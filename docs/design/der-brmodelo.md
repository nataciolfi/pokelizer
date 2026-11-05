# DER 3.0 — construção no brModelo

**Ferramenta escolhida:** brModelo.  
**Modelo de referência:** [modelo conceitual 3.0](../banco-de-dados/modelo-conceitual-v3.md).  
**DER textual:** [DER.md](../banco-de-dados/DER.md).

## Estado

**Status: pendente de construção e validação visual.**

O brModelo será a ferramenta utilizada inicialmente para elaborar o DER visual do PokéAnalyzer. Este documento orienta a montagem, mas não significa que o arquivo visual já tenha sido produzido ou aprovado.

## Orientação para montagem

1. Usar o modelo conceitual 3.0 como fonte das entidades, atributos e regras.
2. Representar as 25 entidades descritas no modelo.
3. Incluir todos os relacionamentos e suas cardinalidades.
4. Identificar chaves primárias e estrangeiras conforme o DER textual.
5. Resolver as entidades associativas dos relacionamentos N:N.
6. Registrar nulabilidade, unicidade e demais restrições que não forem expressas graficamente.
7. Organizar o diagrama para reduzir cruzamentos e manter os nomes legíveis.
8. Conferir o resultado com a seção de relacionamentos e com as restrições do DER.md.

## Domínios para organizar a leitura

A organização visual pode separar os grupos abaixo, mantendo as relações entre eles no modelo completo:

- **Catálogo e jogos:** ESPECIE, FORMA, JOGO, DADOS_FORMA_JOGO, MECANICA_JOGO, TIPO, TIPO_FORMA_JOGO, HABILIDADE, HABILIDADE_FORMA_JOGO, METODO_OBTENCAO, METODO_FORMA_JOGO e TRANSFORMACAO_FORMA.
- **Coleção e atributos:** USUARIO, POKEMON_COLECAO, NATUREZA, ATRIBUTO_BATALHA, SISTEMA_ATRIBUTO, MECANICA_SISTEMA_ATRIBUTO e VALOR_ATRIBUTO_POKEMON.
- **Análise e regulamentos:** PERFIL_ANALISE, VALOR_PERFIL_ANALISE, PERFIL_NATUREZA, PERFIL_HABILIDADE, REGULAMENTO e ELEGIBILIDADE_FORMA_REGULAMENTO.

## Revisão antes do modelo lógico

- [ ] Todas as entidades do modelo conceitual estão presentes.
- [ ] Toda FK possui relacionamento correspondente.
- [ ] Cardinalidades 1:1, 1:N e N:N estão corretas.
- [ ] Relacionamentos opcionais e obrigatórios estão diferenciados.
- [ ] Entidades associativas possuem suas chaves e atributos.
- [ ] Restrições que não aparecem no desenho estão documentadas.
- [ ] O diagrama foi conferido com o arquivo DER.md.

**Regra:** não iniciar o modelo lógico nem o banco físico antes de concluir e revisar o DER no brModelo.
