# Regras de integridade e validação

**Versão:** 3.0  
**Objetivo:** transformar as regras conceituais em restrições a implementar no modelo lógico, SQLite e serviços Python.

## 1. Identidade e catálogo

1. ESPECIE.numero_nacional é único e não nulo.
2. Cada FORMA pertence a uma ESPECIE.
3. FORMA.codigo_forma é único dentro da espécie.
4. Cada espécie possui uma forma padrão; validar a unicidade da forma padrão por espécie.
5. DADOS_FORMA_JOGO é único para forma + mecânica.
6. Nome traduzido não é chave primária.
7. Imagem pode ser nula; falta de imagem não impede cadastrar uma forma.

## 2. Jogo e mecânicas

1. JOGO representa título/edição. Scarlet e Violet são registros distintos.
2. MECANICA_JOGO pertence a exatamente um jogo.
3. Status de IV, EV e natureza aceitam USA, NAO_USA ou NAO_VERIFICADO.
4. Limites numéricos ficam ausentes quando não aplicáveis/desconhecidos, com motivo preservado na aplicação.
5. Mecânica sem fonte suficiente não habilita cálculo numérico.
6. Regulamento/temporada não é versão de mecânica.

## 3. Dados de forma por jogo

1. Presença aceita PRESENTE, AUSENTE ou NAO_VERIFICADO.
2. Registrabilidade aceita INDEPENDENTE, APENAS_TRANSFORMACAO, NAO_REGISTRAVEL ou NAO_VERIFICADO.
3. Métodos de obtenção são registros múltiplos em OBTENCAO_FORMA_JOGO.
4. Forma ausente não é removida do catálogo global.
5. Atributos-base respeitam faixas válidas; altura/peso são não negativos e têm unidades.
6. Cada dado contextual tem fonte e data/versão de verificação.

## 4. Tipos

1. DADOS_FORMA_TIPO é associação entre contexto e tipo.
2. Um contexto tem no máximo dois tipos.
3. O mesmo tipo não pode ocupar os dois slots.
4. Slot aceita PRIMARIO ou SECUNDARIO.
5. Contexto com um tipo não recebe segundo tipo presumido.

O limite de dois tipos pode exigir validação transacional no serviço ou gatilho SQLite; validar apenas no formulário é insuficiente.

## 5. Habilidades e naturezas

1. A habilidade selecionada deve pertencer ao mesmo DADOS_FORMA_JOGO do estado.
2. Usar chave estrangeira composta para impedir habilidade de outra forma/jogo.
3. Slot/condição da habilidade devem ser documentados.
4. Natureza é opcional quando desconhecida ou não aplicável.
5. Natureza só pode ser selecionada se a mecânica a utilizar.
6. Naturezas neutras usam NENHUM em atributo aumentado/reduzido.

## 6. Obtenção

1. Um método pode existir em muitos contextos; um contexto pode aceitar vários métodos.
2. A combinação contexto + método não deve ser duplicada sem motivo.
3. O exemplar guarda método real de origem, que pode ser desconhecido.
4. Jogo de origem não é inferido pelo jogo em que o exemplar está sendo analisado.
5. Método original e método de transferência posterior não são o mesmo dado; a primeira versão registra a origem inicial, e histórico de transferências fica fora do escopo.

## 7. Exemplar e estados por jogo

1. Cada exemplar pertence a exatamente um usuário.
2. POKEMON_COLECAO não guarda a espécie atual fixa.
3. Forma de origem é opcional e representa a forma quando obtido; não muda ao evoluir.
4. Um exemplar pode ter zero ou vários estados em contextos distintos.
5. Cada estado aponta para uma mecânica e uma forma pertencente a essa mecânica.
6. Deve existir no máximo um estado atual por exemplar + mecânica.
7. Quando o exemplar evolui, atualizar a forma em POKEMON_ESTADO_JOGO; não criar outro POKEMON_COLECAO.
8. A espécie atual é derivada de DADOS_FORMA_JOGO → FORMA → ESPECIE.
9. Nível, natureza, habilidade e treinamento são valores do estado em jogo, não propriedades globais do exemplar.
10. A mesma coleção pode ter estados separados em Scarlet/Violet e Champions sem conversão de treinamento.
11. Só criar estado independente quando a registrabilidade da forma permitir; forma disponível apenas por transformação não cria exemplar separado.

## 8. Evolução e transformação

1. EVOLUCAO_FORMA_JOGO e TRANSFORMACAO_FORMA são entidades distintas.
2. Evolução é transição permanente com método/condição do jogo.
3. Uma origem pode ter vários destinos; condição diferencia caminhos como evoluções ramificadas.
4. Origem e destino da evolução devem pertencer ao mesmo contexto de mecânicas.
5. Transformação representa estado temporário/de batalha e não cria um novo exemplar.
6. Origem e destino da transformação devem pertencer ao mesmo contexto, salvo exceção oficial documentada.
7. Item/condição só podem ser exibidos quando a fonte confirmar.
8. Evolução de um exemplar altera o estado atual do mesmo indivíduo.

## 9. Atributos e valores de treinamento

1. GRUPO_LIMITE_TREINAMENTO pertence a uma MECANICA_JOGO.
2. Código do grupo é único dentro da mecânica.
3. ATRIBUTO_TREINAMENTO pertence a uma MECANICA_JOGO e pode apontar para um grupo daquela mesma mecânica.
4. Código do atributo é único dentro da mecânica.
5. Cada atributo define tipo numérico, unidade, mínimo, máximo e incremento quando conhecidos.
6. Cada valor pertence a um estado e a um atributo compatível.
7. Estado + atributo é único.
8. Valor respeita mínimo, máximo e incremento do atributo.
9. Limites agregados são armazenados uma única vez no grupo, não repetidos em MECANICA_JOGO ou em cada atributo.
10. Soma do grupo é verificada em transação no serviço e coberta por testes.
11. Atributo não cadastrado não é presumido como zero.
12. IV, EV e treinamento próprio são categorias distintas.

## 10. Perfis de análise

1. Perfil personalizado possui exatamente um proprietário.
2. Perfil de sistema não possui proprietário de usuário.
3. Perfil aponta para forma/contexto específico.
4. Valores de perfil usam atributos da mesma mecânica.
5. Perfil e estado do exemplar precisam ter forma/mecânica compatíveis.
6. Natureza recomendada é aplicável ao contexto.
7. Habilidade recomendada pertence ao contexto exato.
8. Perfil de referência identifica fonte e versão.
9. Perfil pode existir sem regulamento.
10. Perfil não define elegibilidade competitiva por si só.

## 11. Regulamento e elegibilidade

1. Regulamento pertence a uma mecânica/jogo.
2. Código + formato + temporada devem identificar o regulamento.
3. Data final pode ser nula enquanto vigente e não pode anteceder a inicial.
4. Elegibilidade é única por regulamento + dados da forma.
5. Forma avaliada pertence ao mesmo contexto de mecânicas do regulamento.
6. Status aceita PERMITIDO, RESTRITO, PROIBIDO, CONDICIONAL ou NAO_VERIFICADO.
7. Restrito/condicional exige condição explicada.
8. Decisão verificada exige fonte e data.
9. Ausência de linha significa NAO_VERIFICADO, nunca PROIBIDO.
10. O resultado não certifica legalidade integral do exemplar.

## 12. Segurança da aplicação

- Toda consulta privada filtra por id_usuario da sessão.
- Nunca confiar em id_usuario enviado pelo formulário.
- Senhas usam hash próprio para senhas, com salt e parâmetros adequados.
- SQL parametrizado.
- CSRF protection em formulários autenticados por sessão.
- Validação no backend.
- Transações em operações que alterem várias tabelas.
- Hash de senha nunca é enviado a templates/respostas.
- SQLite ativa PRAGMA foreign_keys = ON em toda conexão.

## 13. Testes mínimos

- Número nacional duplicado falha.
- Forma duplicada na mesma espécie falha.
- Terceiro tipo no contexto falha.
- Habilidade de outra forma/jogo falha.
- Atributo de treinamento de outra mecânica falha.
- Exemplar não tem dois estados atuais para a mesma mecânica.
- Evoluir altera o estado e mantém o mesmo exemplar.
- Evolução não cria automaticamente novo exemplar.
- Transformação não cria captura.
- Soma de valores acima do limite falha.
- Perfil de outro usuário não pode ser lido/editado/excluído.
- Regulamento e forma de jogos incompatíveis falham.
- Elegibilidade ausente retorna não verificado.
