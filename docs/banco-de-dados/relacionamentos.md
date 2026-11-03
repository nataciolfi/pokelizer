# Relacionamentos e cardinalidades — PokéAnalyzer

**Versão:** 3.0

| Entidade A | Relacionamento | Entidade B | Cardinalidade |
|---|---|---|---|
| USUARIO | possui | POKEMON_COLECAO | 1:N |
| ESPECIE | possui | FORMA | 1:N |
| FORMA | possui dados em | DADOS_FORMA_JOGO | 1:N |
| JOGO | possui contextos | MECANICA_JOGO | 1:N |
| MECANICA_JOGO | contextualiza | DADOS_FORMA_JOGO | 1:N |
| DADOS_FORMA_JOGO | possui tipos | TIPO | N:N, por DADOS_FORMA_TIPO |
| DADOS_FORMA_JOGO | disponibiliza | HABILIDADE_FORMA_JOGO | 1:N |
| HABILIDADE | aparece em | HABILIDADE_FORMA_JOGO | 1:N |
| DADOS_FORMA_JOGO | permite métodos | METODO_OBTENCAO | N:N, por OBTENCAO_FORMA_JOGO |
| JOGO | é origem de | POKEMON_COLECAO | 1:N opcional no exemplar |
| METODO_OBTENCAO | descreve a origem | POKEMON_COLECAO | 1:N opcional no exemplar |
| POKEMON_COLECAO | possui estados | POKEMON_ESTADO_JOGO | 1:N |
| DADOS_FORMA_JOGO | define contexto de | POKEMON_ESTADO_JOGO | 1:N |
| NATUREZA | caracteriza | POKEMON_ESTADO_JOGO | 1:N opcional no estado |
| HABILIDADE_FORMA_JOGO | é selecionada em | POKEMON_ESTADO_JOGO | 1:N opcional no estado |
| MECANICA_JOGO | define | ATRIBUTO_TREINAMENTO | 1:N |
| POKEMON_ESTADO_JOGO | registra | VALOR_TREINAMENTO_POKEMON | 1:N |
| ATRIBUTO_TREINAMENTO | é medido em | VALOR_TREINAMENTO_POKEMON | 1:N |
| DADOS_FORMA_JOGO | recebe perfis | PERFIL_ANALISE | 1:N |
| USUARIO | cria | PERFIL_ANALISE | 1:N opcional no perfil do sistema |
| REGULAMENTO | contextualiza | PERFIL_ANALISE | 1:N opcional no perfil |
| PERFIL_ANALISE | define valores | VALOR_TREINAMENTO_PERFIL | 1:N |
| ATRIBUTO_TREINAMENTO | é referência de | VALOR_TREINAMENTO_PERFIL | 1:N |
| PERFIL_ANALISE | recomenda | NATUREZA | N:N, por PERFIL_NATUREZA |
| PERFIL_ANALISE | recomenda | HABILIDADE_FORMA_JOGO | N:N, por PERFIL_HABILIDADE |
| MECANICA_JOGO | recebe | REGULAMENTO | 1:N |
| REGULAMENTO | define | ELEGIBILIDADE_REGULAMENTO | 1:N |
| DADOS_FORMA_JOGO | é avaliada em | ELEGIBILIDADE_REGULAMENTO | 1:N |
| DADOS_FORMA_JOGO (origem) | inicia | TRANSFORMACAO_FORMA | 1:N |
| DADOS_FORMA_JOGO (destino) | recebe | TRANSFORMACAO_FORMA | 1:N |

## Explicação das relações principais

### Catálogo e contexto

**ESPECIE — FORMA (1:N)**  
Uma espécie possui uma ou mais formas. Cada forma pertence a exatamente uma espécie. O número nacional identifica a espécie, não cada forma.

**FORMA — DADOS_FORMA_JOGO (1:N)**  
Uma forma pode ter dados em vários contextos de jogo. Uma forma catalogada não precisa estar presente em todos os títulos.

**JOGO — MECANICA_JOGO (1:N)**  
Cada jogo pode ter um ou mais contextos documentados de mecânicas. JOGO identifica a edição; MECANICA_JOGO guarda regras de treinamento/atributos. Regulamento competitivo não é uma mecânica.

**MECANICA_JOGO — DADOS_FORMA_JOGO (1:N)**  
Um contexto de mecânicas descreve muitas formas. Cada linha de dados pertence a um único contexto.

### Tipos, habilidades e obtenção

**DADOS_FORMA_JOGO — TIPO (N:N)**  
A relação é resolvida por DADOS_FORMA_TIPO, que guarda slot primário/secundário. A regra adicional limita a dois tipos.

**DADOS_FORMA_JOGO — HABILIDADE_FORMA_JOGO (1:N)**  
Uma forma/contexto pode oferecer várias opções de habilidade. Cada opção pertence a exatamente um contexto.

**DADOS_FORMA_JOGO — METODO_OBTENCAO (N:N)**  
A relação é resolvida por OBTENCAO_FORMA_JOGO. Isso permite vários métodos e condições para uma forma no mesmo jogo.

### Exemplar e estados

**USUARIO — POKEMON_COLECAO (1:N)**  
Um usuário pode ter muitos exemplares, inclusive vários da mesma espécie. Cada exemplar pertence a um único usuário.

**POKEMON_COLECAO — POKEMON_ESTADO_JOGO (1:N)**  
Um exemplar pode ter zero ou vários estados, um por contexto de jogo em que esteja registrado. Isso separa a origem do exemplar do jogo no qual ele será analisado.

**DADOS_FORMA_JOGO — POKEMON_ESTADO_JOGO (1:N)**  
Muitos exemplares podem compartilhar o mesmo contexto de forma/jogo. Cada estado aponta para uma forma e mecânica específicas.

**NATUREZA e HABILIDADE_FORMA_JOGO — POKEMON_ESTADO_JOGO (1:N opcional)**  
Um estado pode ter zero ou uma natureza/habilidade selecionada, conforme aplicabilidade e dados conhecidos. A habilidade deve pertencer ao mesmo contexto de forma/jogo do estado.

### Treinamento e perfil

**MECANICA_JOGO — ATRIBUTO_TREINAMENTO (1:N)**  
Cada mecânica define os atributos de treinamento que realmente existem naquele jogo. Isso impede assumir IV/EV em todos os títulos.

**POKEMON_ESTADO_JOGO — VALOR_TREINAMENTO_POKEMON (1:N)**  
Cada estado armazena seus valores por atributo. A combinação estado + atributo deve ser única.

**PERFIL_ANALISE — VALOR_TREINAMENTO_PERFIL (1:N)**  
Cada perfil define faixas ou valores desejados. Os atributos usados precisam pertencer à mesma mecânica do perfil.

**PERFIL_ANALISE — NATUREZA e HABILIDADE_FORMA_JOGO (N:N)**  
Associações permitem registrar várias preferências e prioridades. Preferência não é sinônimo de obrigação; o tipo deve ser explícito.

### Regulamentos e transformações

**MECANICA_JOGO — REGULAMENTO (1:N)**  
Um contexto de jogo pode receber vários regulamentos, formatos ou temporadas. Cada regulamento pertence a um único contexto.

**REGULAMENTO — ELEGIBILIDADE_REGULAMENTO (1:N)**  
Um regulamento tem registros para as formas avaliadas. Sem registro verificado, o resultado é não verificado, não proibido.

**DADOS_FORMA_JOGO — ELEGIBILIDADE_REGULAMENTO (1:N)**  
Uma forma/contexto pode ser verificada em vários regulamentos. A relação só informa elegibilidade da forma, não legalidade completa do exemplar.

**DADOS_FORMA_JOGO — TRANSFORMACAO_FORMA**  
Cada transformação tem um contexto de origem e outro de destino. Origem e destino devem pertencer ao mesmo contexto de mecânicas, exceto exceção oficial documentada. Transformação não cria uma captura independente automaticamente.

## Restrições para o modelo lógico

- E-mail e nome de usuário únicos.
- Número nacional único por espécie.
- Código de forma único dentro da espécie.
- Combinação FORMA + MECANICA_JOGO única.
- No máximo dois tipos por contexto, com slots distintos.
- Habilidade selecionada compatível com o estado de jogo.
- Método de origem do exemplar separado do jogo atual.
- Valores de treinamento ligados à mesma mecânica do estado.
- Limites individuais e agregados de treinamento respeitados.
- Perfil compatível com forma/mecânica do estado analisado.
- Perfil personalizado com proprietário.
- Perfil de sistema sem proprietário.
- Regulamento e forma pertencentes ao mesmo jogo/contexto.
- Elegibilidade única por regulamento e forma/contexto.
- Ausência de registro de elegibilidade = não verificado.
- Transformação com origem e destino contextualmente compatíveis.
- Toda coleção consultada ou alterada deve ser filtrada pelo usuário autenticado.

As restrições detalhadas e os testes mínimos estão em [regras-integridade.md](regras-integridade.md).
