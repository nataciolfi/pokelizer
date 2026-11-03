# Regras de integridade e validação

**Versão:** 3.0  
**Objetivo:** transformar as regras conceituais do PokéAnalyzer em restrições que deverão ser implementadas no modelo lógico, SQLite e serviços Python.

## 1. Identidade e catálogo

1. ESPECIE.numero_nacional é único, não nulo e não deve identificar formas.
2. Cada FORMA pertence exatamente a uma ESPECIE.
3. FORMA.codigo_forma é único dentro da espécie.
4. Cada espécie deve ter uma forma padrão identificada; a unicidade da forma padrão deve ser validada por espécie.
5. DADOS_FORMA_JOGO deve ser único para a combinação de forma e mecânica.
6. Nome traduzido é atributo de apresentação, não chave primária.
7. A referência visual pode ser nula; ausência de imagem não impede o cadastro da forma.

## 2. Jogo e mecânicas

1. JOGO representa título/edição. Scarlet e Violet devem ser registros diferentes.
2. MECANICA_JOGO pertence a exatamente um jogo.
3. Status de IV, EV e natureza aceitam USA, NAO_USA ou NAO_VERIFICADO.
4. Limites numéricos ficam nulos quando não aplicáveis ou desconhecidos; a lógica deve distinguir os motivos.
5. Uma mecânica sem fonte suficiente não pode habilitar cálculo numérico.
6. Regulamento e temporada não são armazenados como versão de mecânica.

## 3. Dados de forma por jogo

1. Presença no jogo aceita PRESENTE, AUSENTE ou NAO_VERIFICADO.
2. Registrabilidade aceita INDEPENDENTE, APENAS_TRANSFORMACAO, NAO_REGISTRAVEL ou NAO_VERIFICADO.
3. Métodos de obtenção são registros múltiplos em OBTENCAO_FORMA_JOGO.
4. Uma forma ausente não deve ser removida do catálogo global.
5. Atributos-base devem ter faixa inteira válida; altura/peso devem ser não negativos e usar unidade documentada.
6. Cada registro deve ter fonte e data/versão de verificação.

## 4. Tipos

1. DADOS_FORMA_TIPO é uma tabela associativa.
2. Um contexto pode ter no máximo dois tipos.
3. O mesmo tipo não pode ocupar dois slots no mesmo contexto.
4. Slot aceita somente PRIMARIO ou SECUNDARIO.
5. Um contexto com somente um tipo não pode ter um segundo tipo inventado.

A restrição de no máximo dois tipos pode ser aplicada por validação transacional no serviço e/ou gatilho SQLite. Não basta validar o formulário.

## 5. Habilidades e naturezas

1. Uma habilidade selecionada deve estar associada ao mesmo DADOS_FORMA_JOGO do estado do exemplar.
2. A chave estrangeira composta deve impedir habilidade de outra forma/jogo.
3. A habilidade deve ter slot/condição documentados.
4. Natureza pode ser nula quando não informada ou não aplicável.
5. Natureza só pode ser selecionada quando a mecânica a utiliza ou quando houver confirmação explícita.
6. Naturezas neutras devem representar aumento e redução iguais a NENHUM, sem inventar atributo.

## 6. Obtenção

1. Um método pode estar disponível em muitos contextos.
2. Um contexto pode ter muitos métodos de obtenção.
3. A mesma combinação contexto + método não deve ser duplicada sem motivo documentado.
4. O exemplar guarda seu método real de origem, que pode ser desconhecido.
5. A origem do exemplar não pode ser inferida do jogo em que está sendo analisado.

## 7. Coleção e estados por jogo

1. Cada exemplar pertence a exatamente um usuário.
2. Cada exemplar pertence a exatamente uma espécie.
3. Um exemplar pode ter zero ou muitos estados por jogo.
4. Cada estado aponta para um único contexto de forma/mecânica.
5. O estado só pode ser criado quando a registrabilidade permite um exemplar naquele contexto ou quando existir regra explícita para um caso especial.
6. Nível é validado pelo contexto; não presumir que todos os jogos usem o mesmo intervalo.
7. Natureza e habilidade são opcionais se desconhecidas ou não aplicáveis.
8. Valores de treinamento pertencem ao estado, nunca diretamente ao exemplar global.
9. Um estado só pode referenciar atributos de treinamento da mesma mecânica.
10. A mesma coleção pode ter um estado em Scarlet/Violet e outro em Champions sem conversão de valores.

## 8. Atributos e valores de treinamento

1. ATRIBUTO_TREINAMENTO pertence a uma única MECANICA_JOGO.
2. Código do atributo deve ser único dentro da mecânica.
3. Cada valor pertence a um estado e a um atributo compatível.
4. A combinação estado + atributo é única.
5. O valor precisa respeitar mínimo e máximo daquele atributo.
6. Limites individuais são verificados no banco ou no serviço.
7. Limites totais (por exemplo, soma de valores em um grupo) exigem validação transacional no serviço e teste automatizado.
8. Um atributo não cadastrado não deve ser presumido como zero.
9. Categorias como IV, EV e treinamento próprio de um jogo são distintas e não intercambiáveis.

## 9. Perfis de análise

1. Perfil personalizado possui exatamente um proprietário.
2. Perfil mantido pelo sistema não possui proprietário de usuário.
3. Perfil aponta para um contexto específico de forma/mecânica.
4. Valores do perfil devem usar atributos da mesma mecânica.
5. Perfil e exemplar precisam ter forma/mecânica compatíveis antes da análise.
6. Uma natureza recomendada deve existir e ser aplicável ao contexto.
7. Habilidade recomendada deve ser uma opção do mesmo contexto de forma.
8. Perfil competitivo ou estratégico precisa identificar fonte e versão.
9. Perfil sem regulamento não é automaticamente inválido; perfil personalizado pode ser livre.
10. Perfil não define por si só elegibilidade de competição.

## 10. Regulamentos e elegibilidade

1. Regulamento pertence a uma mecânica/jogo específicos.
2. Código + formato + temporada devem identificar o regulamento sem ambiguidade.
3. Data final pode ser nula enquanto estiver vigente.
4. Data final não pode anteceder a data inicial.
5. Elegibilidade é única por regulamento + contexto de forma.
6. O contexto avaliado deve pertencer ao mesmo jogo/mecânica do regulamento.
7. Status deve ser um de PERMITIDO, RESTRITO, PROIBIDO, CONDICIONAL, NAO_VERIFICADO.
8. Status restrito/condicional exige condição explicada.
9. Toda decisão verificada exige fonte e data.
10. Ausência de linha significa NAO_VERIFICADO, nunca PROIBIDO.
11. O resultado não certifica legalidade integral do exemplar individual.

## 11. Transformações

1. Cada transformação possui uma origem e um destino.
2. Origem e destino devem pertencer ao mesmo contexto de mecânica, salvo exceção oficial documentada.
3. Condição, item ou requisito devem ser registrados quando aplicáveis.
4. Transformação de batalha não cria exemplar em POKEMON_COLECAO.
5. O destino deve ser uma forma catalogada com fonte verificável.
6. Formas de origem e destino não devem ser confundidas com linha evolutiva.

## 12. Segurança da aplicação

- Todas as consultas de dados privados devem filtrar por id_usuario da sessão autenticada.
- Nunca confiar em id_usuario enviado pelo formulário como prova de autorização.
- Senhas devem usar hash próprio para senhas, com salt e parâmetros adequados.
- Não concatenar entradas em SQL.
- Usar CSRF protection em operações autenticadas por sessão.
- Validar valores no backend.
- Usar transações em cadastro/alteração que envolvam várias tabelas.
- Não retornar hash de senha em respostas ou templates.
- No SQLite, ativar PRAGMA foreign_keys = ON em todas as conexões.

## 13. Testes mínimos derivados

- Duplicar número nacional deve falhar.
- Duplicar forma dentro da mesma espécie deve falhar.
- Associar habilidade de outra forma/jogo deve falhar.
- Inserir terceiro tipo deve falhar.
- Somar valores de treinamento acima do limite deve falhar.
- Associar atributo de treinamento de outra mecânica deve falhar.
- Criar perfil de outro usuário ou acessar perfil privado por ID deve falhar.
- Associar regulamento e forma de jogos incompatíveis deve falhar.
- Cadastrar forma ausente não deve removê-la da Pokédex.
- Consultar elegibilidade sem registro deve retornar não verificado.
- Transformação não deve criar automaticamente novo exemplar.
