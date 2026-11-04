# Requisitos do PokéAnalyzer — revisão 2.0

## Requisitos funcionais

| ID | Requisito |
|---|---|
| RF01 | Criar conta de usuário. |
| RF02 | Autenticar e encerrar sessão. |
| RF03 | Armazenar somente hash seguro de senha. |
| RF04 | Consultar espécies por número nacional e nome. |
| RF05 | Pesquisar por número, nome e código de forma. |
| RF06 | Filtrar por tipo, geração e disponibilidade em jogo. |
| RF07 | Exibir formas oficiais com categoria e fonte. |
| RF08 | Distinguir presença, transferência, métodos de obtenção e registro independente. |
| RF09 | Exibir dados de uma forma em jogo específico. |
| RF10 | Registrar um exemplar individual na coleção. |
| RF11 | Separar jogo atual, jogo de origem e método real de obtenção. |
| RF12 | Registrar nível, natureza e habilidade quando aplicáveis. |
| RF13 | Registrar valores por sistema, atributo e versão de mecânica. |
| RF14 | Consultar, editar e excluir somente exemplares próprios. |
| RF15 | Permitir vários exemplares da mesma espécie/forma. |
| RF16 | Criar, editar e excluir perfis personalizados. |
| RF17 | Consultar perfis de referência com fonte e data. |
| RF18 | Comparar exemplar e perfil somente em contexto compatível. |
| RF19 | Apresentar divergências e recomendações explicáveis. |
| RF20 | Consultar elegibilidade de espécie/forma por regulamento. |
| RF21 | Exibir fonte, data de verificação e estado não verificado. |
| RF22 | Representar transformações sem criar captura automática. |
| RF23 | Ocultar ou desabilitar treinamento quando não aplicável/não confirmado. |
| RF24 | Exibir a Pokédex mesmo sem disponibilidade ou elegibilidade confirmada. |

## Requisitos não funcionais

| ID | Requisito |
|---|---|
| RNF01 | Interface simples para iniciantes. |
| RNF02 | Código modular, legível e explicável academicamente. |
| RNF03 | Integridade referencial no banco. |
| RNF04 | Isolamento de dados por usuário autenticado. |
| RNF05 | SQL parametrizado. |
| RNF06 | Entradas validadas no servidor. |
| RNF07 | Recomendações identificam jogo, mecânica, perfil e dados usados. |
| RNF08 | Dados variáveis registram fonte e data de verificação. |
| RNF09 | Execução local na fase de desenvolvimento. |
| RNF10 | Atualizar mecânicas não deve duplicar o catálogo. |
| RNF11 | Não converter treinamento sem equivalência documentada. |
| RNF12 | Formulários têm rótulos e mensagens de erro associadas. |
| RNF13 | Interface adaptável a telas menores. |
| RNF14 | Segredos não são versionados no Git. |
| RNF15 | Formulários de alteração possuem proteção CSRF. |

## Regras de negócio

1. Uma espécie possui uma ou mais formas; cada forma pertence a uma espécie.
2. Existe uma forma padrão por espécie.
3. Uma forma pode existir no catálogo sem estar presente em um jogo.
4. Presença, transferência, obtenção e elegibilidade são conceitos diferentes.
5. Métodos possíveis são associados à forma/jogo; o exemplar guarda o método real.
6. Jogo de origem pode ser diferente do jogo atual.
7. Cada registro de coleção representa um exemplar, não uma espécie agrupada.
8. Um usuário pode ter vários exemplares da mesma forma.
9. A habilidade selecionada deve existir para a forma no jogo atual.
10. Natureza só é exigida quando aplicável e confirmada.
11. Valores de treinamento pertencem a sistema, atributo e versão de mecânica.
12. Nulo significa não informado/não aplicável; zero é valor real.
13. Limites desconhecidos permanecem desconhecidos.
14. Perfil personalizado exige proprietário.
15. Perfil de referência informa fonte e data.
16. Perfil e exemplar precisam de jogo/mecânica compatíveis.
17. Regulamento não determina sozinho uma distribuição ideal.
18. Elegibilidade da espécie/forma não é legalidade completa do exemplar.
19. Ausência de elegibilidade registrada não significa proibição.
20. Transformação temporária não cria exemplar independente.
21. Nunca misturar valores de treinamento de jogos diferentes.
22. Toda operação da coleção verifica o proprietário no servidor.

## Critérios de aceitação

- Usuário não acessa registros de outra conta.
- Vários exemplares da mesma forma coexistem.
- Jogo de origem difere do atual sem perda da informação.
- Formas indisponíveis continuam visíveis na Pokédex.
- Um terceiro tipo é rejeitado.
- Habilidade incompatível é rejeitada.
- Jogo sem IV/EV não exibe nem exige esses valores.
- Pokémon de Champions pode ser registrado sem inventar IV/EV.
- Perfil de outro jogo não pode ser usado na análise.
- Elegibilidade não verificada nunca é apresentada como proibida.
- Fonte e data acompanham recomendações.


## Regra adicional do analisador

A primeira versão compara cada atributo com o alvo explícito do perfil e classifica igual, abaixo, acima ou sem dado. Não calcula uma nota global nem assume que valor maior é melhor. A elegibilidade da espécie/forma fica em painel independente. Consulte [algoritmo de análise](algoritmo-analise.md).
