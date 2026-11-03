# Escopo do projeto

**Versão:** 3.0  
**Status:** especificação revisada; implementação ainda não iniciada.

## 1. Visão geral

O PokéAnalyzer será um website com catálogo de espécies e formas, coleção individual por usuário e analisador comparativo. O catálogo global não será confundido com os dados de um jogo, e um exemplar individual não será confundido com o estado dele em um jogo específico.

O sistema deverá explicar recomendações com base em dados identificados: forma, jogo, contexto de mecânicas, perfil, regulamento quando aplicável e fonte.

## 2. Objetivos

1. Manter catálogo nacional de espécies e formas oficiais documentadas.
2. Consultar formas sem presumir que estejam disponíveis em todos os jogos.
3. Guardar tipos, habilidades, atributos-base e métodos de obtenção por contexto de jogo.
4. Permitir contas e coleções isoladas por usuário.
5. Registrar exemplares individuais, inclusive múltiplos da mesma espécie.
6. Separar jogo de origem do exemplar e os estados desse exemplar em outros jogos.
7. Comparar atributos com perfis personalizados ou de referência.
8. Consultar elegibilidade de espécies/formas em regulamentos versionados.
9. Identificar fonte, versão e data de verificação dos dados.
10. Exibir limitações e dados faltantes sem inventar valores.

## 3. Política de catálogo

A unidade central é a **espécie**. Cada espécie pode ter uma ou mais **formas** catalogadas. Uma forma deve possuir identificador estável interno, nome canônico, categoria e fonte verificável.

Serão incluídas formas oficialmente documentadas como variantes de jogo, incluindo, quando aplicável, formas regionais, alternativas, sazonais, de gênero, cosméticas e de batalha. A classificação precisa ser registrada para que o sistema não trate toda variação visual como uma nova espécie.

Regras de escopo:
- Diferenças de coloração brilhante (*Shiny*) serão características de aparência do exemplar, não uma espécie ou forma nova por padrão.
- Formas que são apenas estados temporários de batalha podem existir no catálogo, mas não serão tratadas automaticamente como exemplares independentes.
- Variações cosméticas com catálogo oficial próprio podem ser representadas como formas quando houver fonte e identificador inequívocos.
- Uma forma pode pertencer ao catálogo e não possuir dados em determinado jogo.
- A contagem total do catálogo nunca será fixada no código; deve ser associada à versão da fonte importada.

A expressão “Pokédex completa” só poderá ser usada como critério de aceitação quando existir uma lista de referência versionada e um relatório de cobertura que demonstre quais espécies e formas foram importadas, quais foram excluídas pela política e quais continuam sem confirmação.

## 4. Contextos de jogo

### Scarlet e Violet

Serão registros de jogo distintos, pois disponibilidade e dados podem variar entre as edições. A primeira calculadora de IV, EV e natureza será validada para o contexto da Geração IX. Os limites não devem ser espalhados em constantes pelo código: devem vir do contexto de mecânicas e ser testados.

### Pokémon Champions

É um contexto separado. O jogo permite Pokémon visitantes via Pokémon HOME e Pokémon recrutados dentro do próprio Champions. O treinamento realizado no Champions tem comportamento próprio e não deve ser convertido em IV/EV de outro jogo. A estrutura v3 prevê estados por jogo e atributos de treinamento definidos pelo contexto.

A implementação só poderá analisar numericamente o treinamento de Champions depois de documentar seus atributos, limites, regras de persistência e fonte oficial. Antes disso, poderá registrar o contexto sem apresentar cálculo incompleto como se fosse uma análise concluída.

### Pokémon Legends: Z-A

Será um contexto separado. A disponibilidade, formas, habilidades e mecânicas precisam ser cadastradas com dados próprios. Não herdar automaticamente regras de Scarlet/Violet ou Champions.

### Pokémon Winds e Pokémon Waves

Os jogos foram anunciados para 2027. Antes do lançamento e de fontes oficiais suficientes, não serão criados dados de disponibilidade ou regras presumidas.

## 5. Funcionalidades da primeira versão

- Cadastro, login e encerramento de sessão.
- Pesquisa e filtros no catálogo.
- Consulta de espécie, formas e dados por jogo.
- Coleção privada de cada usuário.
- Registro de origem e método de obtenção.
- Registro de um exemplar em um ou mais contextos de jogo.
- Campos de treinamento definidos pelo contexto selecionado.
- Perfis personalizados e perfis estratégicos de referência.
- Comparação explicável, com tratamento de dados ausentes.
- Consulta da elegibilidade da forma em um regulamento.
- Indicação de fonte, versão e data de verificação.

## 6. O que o analisador realmente promete

O analisador compara um estado específico do exemplar com um perfil compatível de mesma forma e contexto de mecânicas.

A análise deverá:
1. verificar se o jogo e o contexto coincidem;
2. verificar se forma, natureza, habilidade e atributos são aplicáveis;
3. verificar a completude dos dados;
4. comparar cada atributo com a faixa ou preferência definida pelo perfil;
5. diferenciar divergência, dado desconhecido e dado não aplicável;
6. explicar o motivo de cada recomendação;
7. indicar, quando houver documentação, se a característica pode ser alterada naquele jogo.

O programa não deverá reduzir tudo a uma nota única sem explicar o cálculo. Um IV 31 não é automaticamente desejável: alguns perfis podem preferir IV baixo em atributos específicos. O analisador inicial não é simulador de batalha, calculadora de dano ou montador completo de equipes.

## 7. Elegibilidade e limites da verificação competitiva

A primeira versão verifica a **elegibilidade catalogada da espécie/forma no regulamento selecionado**. Isso não equivale a certificar a legalidade completa de um exemplar.

Uma validação individual completa pode depender de movimentos, itens, origem, marca, evento, habilidade, nível, restrições de transferência e outros dados que estão fora do escopo inicial. A interface deve dizer “elegibilidade da forma” ou “compatibilidade com o regulamento”, nunca “Pokémon 100% legal” sem validar todos os requisitos.

## 8. Fora do escopo inicial

- Simulador de batalhas.
- Calculadora completa de dano.
- Montagem automática de equipes.
- Catálogo completo de golpes, itens e combinações legais.
- Verificação integral de legitimidade/origem de cada exemplar.
- Integração automática com arquivos de save ou Pokémon HOME.
- Marketplace, trocas e funcionalidades sociais.
- Aplicativo móvel nativo.
- Histórico detalhado de relatórios.
- Importação de dados sem fonte e licença verificáveis.

## 9. Premissas técnicas

- SQLite será usado inicialmente.
- Python e Flask serão o backend.
- HTML, CSS e JavaScript serão usados no frontend.
- A lógica de negócio ficará fora das rotas Flask.
- Consultas SQL serão parametrizadas.
- Toda operação de coleção e perfil verificará o usuário proprietário no backend.
- O banco terá chaves estrangeiras, restrições e índices.
- Regras que envolvem soma entre vários registros serão validadas no serviço e cobertas por testes; não dependerão apenas da interface.
- Dados importados terão origem, versão e data de verificação.
