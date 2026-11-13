# Fontes e política de verificação de dados

**Última revisão das referências:** 03/11/2026

## 1. Fontes oficiais prioritárias

### Catálogo
- [Pokédex oficial Pokémon](https://www.pokemon.com/br/pokedex)
- [Portal oficial de imprensa Pokémon](https://press.pokemon.com/)

A Pokédex oficial é uma fonte de consulta e conferência. Antes de declarar a cobertura completa de espécies e formas, o projeto precisa confrontar a lista importada com uma referência versionada e documentar o tratamento de formas regionais, alternativas, sazonais, cosméticas, de gênero e de batalha.

Não presumir que uma página visual da Pokédex ofereça um arquivo completo ou uma API pública para importação. A origem técnica de cada conjunto importado deverá ser registrada separadamente.

### Pokémon Champions
- [Pokémon e recrutamento em Pokémon Champions](https://champions.pokemon.com/pt-br/pokemon/)
- [Mecânicas de Pokémon Champions](https://champions.pokemon.com/pt-br/gameplay/)
- [Notícias de Pokémon Champions](https://champions.pokemon.com/pt-br/news/)
- [Transição das competições Play! Pokémon para Champions, anúncio de 24/03/2026](https://www.pokemon.com/uk/news/play-pokemon-competitions-transition-to-pokemon-champions-on-april-and-may-2026)

Pontos confirmados nas páginas oficiais consultadas:
- Pokémon podem entrar como visitantes via Pokémon HOME, desde que apareçam em Champions.
- Também existem Pokémon recrutados no próprio jogo.
- O treinamento do Champions usa Pontos de Vitória e é próprio do jogo.
- O treinamento feito em Champions não é mantido no Pokémon HOME ao retornar o visitante; ao voltar a Champions, o visitante pode recuperar o treinamento anterior salvo naquele contexto. Uma mudança de forma ao sair e retornar pode apagar o treinamento de Champions.
- O anúncio de 24/03/2026 informou a transição das competições de videogame Play! Pokémon para Champions a partir de 08/04/2026.

Consequência para o modelo: o mesmo exemplar precisa poder ter estados distintos em jogos diferentes. Valores do treinamento de Champions não podem ser gravados como IV/EV de Scarlet/Violet.

### Regulamentos competitivos
- [Regras e formatos do Play! Pokémon](https://play.pokemon.com/pt-br/resources/rules/?category=vgc)
- [Documentos e recursos oficiais Play! Pokémon](https://play.pokemon.com/pt-br/resources/documents/)

Cada regulamento deverá ser identificado pelo jogo/mecânica, código ou nome, formato, temporada/série, data de início, data de término quando houver, fonte oficial e data da última verificação. Uma temporada ou série não deve ser armazenada como se fosse uma versão de mecânicas do jogo.

### Pokémon Winds e Pokémon Waves
- [Site oficial de Pokémon Ventos e Pokémon Ondas](https://windswaves.pokemon.com/pt-br/)

A página oficial consultada informa lançamento global simultâneo em 2027, exclusivamente para Nintendo Switch 2. Portanto, em 03/11/2026, o projeto não deve inventar disponibilidade, atributos ou mecânicas desses jogos.

## 2. Fontes técnicas secundárias

Quando uma fonte oficial não publicar um dado em formato utilizável, poderá ser considerada uma fonte secundária estruturada, desde que:
- seja identificada como não oficial;
- tenha cobertura e consistência verificadas;
- tenha licença/termos de uso avaliados;
- registre versão, data de coleta e URL;
- seja comparada com fontes oficiais para uma amostra;
- possa ser substituída sem mudar a identidade interna das espécies/formas.

Não usar scraping frágil de páginas visuais como única fonte de dados. Não assumir que uma API de comunidade seja oficial ou tenha permissão irrestrita de uso.

## 3. Política de importação

Cada lote de importação deve registrar:
1. fonte e URL;
2. versão/data da fonte;
3. data de importação;
4. quantidade de registros processados;
5. quantidade inserida, atualizada, ignorada e rejeitada;
6. erros e registros sem confirmação;
7. critério usado para identificar espécies e formas.

Usar identificadores internos estáveis. Nomes traduzidos não devem ser usados como chaves primárias.

## 4. Estados de conhecimento

- **Verificado:** há fonte suficiente e uma data de verificação.
- **Não verificado:** falta confirmação; não significa indisponível ou proibido.
- **Não aplicável:** a mecânica não usa aquele atributo.
- **Desconhecido:** o dado deveria existir, mas a fonte/registro ainda não foi encontrado.

Não usar um único NULL de modo ambíguo para todos esses significados na lógica da aplicação. O banco pode usar nulo onde apropriado, mas a interface deve preservar o motivo da ausência.

## 5. Conceitos que não devem ser confundidos

- **Espécie:** identidade da Pokédex Nacional.
- **Forma:** variante oficialmente documentada da espécie.
- **Jogo:** título/edição, como Scarlet ou Violet.
- **Mecânica:** conjunto de regras de atributos e treinamento usado naquele contexto.
- **Presença:** se a forma aparece nos dados do jogo.
- **Obtenibilidade:** como o exemplar pode ser obtido/transferido naquele contexto.
- **Registrabilidade:** se a forma é um exemplar independente ou apenas um estado de transformação.
- **Regulamento:** regras de uma competição com formato e vigência.
- **Elegibilidade da forma:** status catalogado da forma no regulamento.
- **Perfil de análise:** objetivo de comparação; não é um regulamento.
- **Estado do exemplar no jogo:** forma, habilidade, nível e treinamento naquele contexto.
