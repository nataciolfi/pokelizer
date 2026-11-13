# Escopo do PokéAnalyzer — revisão após auditoria

## 1. Visão geral

Website educacional com catálogo de espécies e formas Pokémon documentadas, coleção individual por usuário e analisador de atributos contextualizado por jogo. Catálogo global, dados por jogo e mecânicas versionadas ficam separados.

Cada registro da coleção representa um exemplar. Jogo atual, jogo de origem e método de obtenção são informações diferentes.

## 2. Objetivos

1. Consultar espécies e formas oficiais documentadas.
2. Identificar formas por código estável, não só pelo nome.
3. Separar dados globais e dados específicos de jogo.
4. Permitir contas e coleções privadas.
5. Separar jogo atual, origem e método real.
6. Registrar valores de treinamento sem converter sistemas.
7. Comparar exemplares com perfis personalizados ou de referência.
8. Exibir elegibilidade da espécie/forma por regulamento, sem prometer legalidade completa.
9. Explicar resultados com contexto e fontes.

## 3. Contextos de jogo

### Scarlet e Violet
Primeiro contexto completo do analisador para IV, EV e natureza. Limites devem ser cadastrados na versão de mecânica e testados.

### Pokémon Champions
Contexto separado para recrutamento, transferência por HOME e treinamento com Pontos de Vitória. O projeto não converte valores de Champions em IV/EV. A análise numérica só será liberada quando a escala do treinamento estiver documentada. Fontes oficiais: https://champions.pokemon.com/pt-br/pokemon/ e https://champions.pokemon.com/pt-br/gameplay/

### Pokémon Legends: Z-A
Contexto próprio. Só cadastrar dados e regras confirmados; não herdar fórmulas de Scarlet/Violet.

### Pokémon Ventos e Ondas
Site oficial anuncia lançamento mundial em 2027 para Nintendo Switch 2: https://windswaves.pokemon.com/pt-br/. Não cadastrar mecânicas presumidas antes de fontes suficientes.

### Outros jogos
Podem ser adicionados com contexto, dados e mecânicas documentados.

## 4. Critério do catálogo

- ESPECIE é a entrada nacional.
- FORMA é uma variação oficial documentada.
- Toda espécie possui uma forma padrão.
- Formas adicionais precisam de código, categoria, fonte e data.
- Variações de gênero, região, estação, cosméticas, fusões e batalha precisam de classificação explícita.
- Uma forma pode existir no catálogo sem aparecer em qualquer jogo.
- Formas temporárias não são automaticamente registráveis.
- Contagem é versionada por importação, nunca fixa no código.

A Pokédex oficial consultada apresenta a faixa nacional 1–1025 em 04/11/2026: https://www.pokemon.com/br/pokedex. Isso é uma referência da data, não garantia de que a página contenha todas as formas alternativas.

## 5. MVP

- Cadastro/login/logout.
- Catálogo de espécies/formas com fonte.
- Pesquisa e filtros.
- Detalhe por forma/jogo.
- CRUD de exemplares.
- Perfis personalizados.
- Analisador IV/EV/natureza de Scarlet/Violet.
- Elegibilidade da espécie/forma quando houver regulamento confirmado.
- Validações, mensagens de erro e estados vazios.
- Testes de banco, autenticação e cálculos.

## 6. Extensões condicionadas à documentação

- Treinamento próprio de Champions sem conversão.
- Dados/mecânicas específicos de Legends: Z-A.
- Outros jogos e regulamentos.
- Histórico de contexto/transferências.

O banco deve admitir extensão, mas a primeira entrega não simula regras que não foram confirmadas.

## 7. Fora do escopo inicial

- Legalidade completa de exemplar individual.
- Simulador de batalha e cálculo de dano.
- Banco completo de golpes/itens.
- Gerenciamento de equipes.
- Integração automática com HOME ou leitura de save.
- Marketplace e funcionalidades sociais.
- Histórico completo de transferências.
- Aplicativo móvel nativo.

## 8. Premissas técnicas

Python, Flask, SQLite, SQL, HTML, CSS e JavaScript. Chaves estrangeiras ativas, SQL parametrizado, regras de domínio no backend e fonte/data de verificação para dados importados.
