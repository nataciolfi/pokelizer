# Revisão e fechamento do DER

**Versão:** 3.0  
**Data:** 03/11/2026

## Problemas encontrados no modelo anterior

1. Estatísticas-base estavam globais, embora dependam do jogo.
2. Tipos e habilidades não tinham contexto de jogo.
3. Método de obtenção era um único campo, embora existam vários caminhos.
4. Coleção apontava diretamente para dados de forma/jogo e misturava origem com estado atual.
5. Colunas fixas de IV/EV não representavam sistemas de treinamento diferentes.
6. Elegibilidade era interpretada como legalidade integral do exemplar.
7. Perfil e regulamento não estavam suficientemente separados.
8. A coleção guardava uma espécie fixa, o que entrava em conflito com a evolução.
9. A tela de detalhes previa evolução, mas o modelo não tinha relação evolutiva; transformação de batalha não substitui evolução.
10. Status booleanos não distinguiam regra inexistente de dado não verificado.

## Correções da versão 3.0

- ESPECIE e FORMA compõem o catálogo global.
- JOGO representa a edição; MECANICA_JOGO representa regras de atributos/treinamento.
- DADOS_FORMA_JOGO guarda atributos, presença e registrabilidade por contexto.
- DADOS_FORMA_TIPO guarda tipo primário/secundário.
- HABILIDADE_FORMA_JOGO garante opções por contexto.
- METODO_OBTENCAO e OBTENCAO_FORMA_JOGO permitem vários métodos por forma/jogo.
- POKEMON_COLECAO identifica o indivíduo e guarda procedência, não espécie atual.
- POKEMON_ESTADO_JOGO guarda forma atual e atributos daquele exemplar no contexto.
- EVOLUCAO_FORMA_JOGO representa evolução permanente; TRANSFORMACAO_FORMA representa transformação de estado.
- ATRIBUTO_TREINAMENTO e valores relacionados permitem contextos de treinamento diferentes.
- PERFIL_ANALISE permanece separado de REGULAMENTO.
- ELEGIBILIDADE_REGULAMENTO se limita à forma.
- Status trivalorados preservam desconhecimento.

## Decisões sobre jogos

- Scarlet/Violet são edições distintas e formam o primeiro contexto numérico.
- Pokémon Champions tem recrutamento, visitantes e treinamento próprios; nenhum treinamento é convertido automaticamente para IV/EV.
- Legends: Z-A possui contexto próprio.
- Winds/Waves não recebe regras antes do lançamento e de fontes verificadas.

## Checklist

- [x] Separar espécie e forma.
- [x] Separar catálogo global e dados por jogo.
- [x] Diferenciar edição, mecânica e regulamento.
- [x] Separar presença, obtenibilidade e registrabilidade.
- [x] Separar exemplar e estado por jogo.
- [x] Permitir evolução sem criar exemplar duplicado.
- [x] Diferenciar evolução e transformação.
- [x] Modelar atributos de treinamento por contexto.
- [x] Resolver N:N de tipos, habilidades recomendadas e obtenção.
- [x] Separar perfil e regulamento.
- [x] Limitar elegibilidade ao nível realmente verificado.
- [x] Diferenciar zero, não aplicável e não verificado.
- [x] Normalizar limites individuais e agregados de treinamento sem duplicar regras.
- [ ] Desenhar DER v3 no brModelo e conferir cardinalidades.
- [ ] Converter para modelo lógico e testar FKs compostas.
- [ ] Fazer revisão visual final antes de aprovar.

## Casos de teste conceituais

1. Forma regional possui dados próprios diferentes da forma padrão.
2. Forma disponível por transformação não vira captura independente.
3. Pokémon transferido pode ter estados por jogo sem conversão de treinamento.
4. Pokémon evolui e mantém o mesmo registro individual.
5. Forma de origem permanece preservada após evolução.
6. Uma espécie aparece na Pokédex, mas está ausente de um jogo.
7. Elegibilidade não verificada não é interpretada como proibida.
8. Perfil personalizado existe sem regulamento.
9. Perfil competitivo específico referencia contexto e regulamento corretos.
10. Uma forma tem vários métodos de obtenção no mesmo jogo.

**O DER só estará fechado quando a representação visual corresponder a esta documentação e as restrições do modelo lógico forem verificadas.**
