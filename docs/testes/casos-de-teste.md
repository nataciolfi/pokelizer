# Matriz de testes do PokéAnalyzer

**Versão:** 3.0  
**Status:** casos especificados; ainda não existem testes automatizados nem aplicação executável.

Esta matriz transforma requisitos e regras de integridade em cenários verificáveis. Quando a implementação começar, cada caso deve virar teste unitário, de integração ou de interface conforme indicado.

## 1. Catálogo e formas

| ID | Cenário | Resultado esperado | Tipo |
|---|---|---|---|
| CAT01 | Inserir duas espécies com o mesmo número nacional | Rejeitar duplicidade | Banco |
| CAT02 | Inserir forma sem espécie proprietária | Rejeitar | Banco |
| CAT03 | Inserir duas formas com mesmo código na mesma espécie | Rejeitar | Banco |
| CAT04 | Inserir duas formas padrão para a mesma espécie | Rejeitar | Banco/serviço |
| CAT05 | Consultar forma não disponível no jogo selecionado | Manter no catálogo e mostrar status do jogo | Integração |
| CAT06 | Inserir dado sem fonte verificável | Marcar como não verificado ou rejeitar conforme política, nunca inventar fonte | Serviço |
| CAT07 | Importar forma brilhante como espécie independente sem justificativa catalográfica | Rejeitar a classificação ou exigir revisão | Importação |

## 2. Contexto de jogo

| ID | Cenário | Resultado esperado | Tipo |
|---|---|---|---|
| JOG01 | Criar registros distintos para Scarlet e Violet | Permitir os dois contextos | Banco |
| JOG02 | Associar mecânica a um jogo inexistente | Rejeitar | Banco |
| JOG03 | Configurar IV como NAO_VERIFICADO | Não permitir cálculo de IV | Serviço |
| JOG04 | Configurar IV como NAO_USA | Não mostrar campo de IV | Interface |
| JOG05 | Selecionar regra de outro jogo para análise | Bloquear análise e explicar incompatibilidade | Serviço |
| JOG06 | Cadastrar Champions sem atributo numérico verificado | Permitir contexto, mas não apresentar cálculo inventado | Serviço/UI |
| JOG07 | Tentar converter treinamento de Champions em EV de Scarlet/Violet | Não converter; exigir regra oficial explícita | Serviço |

## 3. Tipos, habilidades e métodos de obtenção

| ID | Cenário | Resultado esperado | Tipo |
|---|---|---|---|
| REL01 | Associar terceiro tipo a uma forma/contexto | Rejeitar | Banco/serviço |
| REL02 | Associar o mesmo tipo duas vezes ao mesmo contexto | Rejeitar | Banco |
| REL03 | Associar habilidade de outra forma/jogo ao estado | Rejeitar | Banco/serviço |
| REL04 | Registrar duas habilidades válidas em slots distintos | Permitir quando a fonte confirmar | Serviço |
| REL05 | Associar método de obtenção não disponível naquele contexto | Rejeitar ou marcar não verificado, conforme fonte | Serviço |
| REL06 | Registrar dois métodos de obtenção para a mesma forma/contexto | Permitir como opções distintas | Banco |
| REL07 | Cadastrar forma com métodos diferentes e condições distintas | Preservar ambos sem sobrescrita | Banco |

## 4. Exemplar e estado por jogo

| ID | Cenário | Resultado esperado | Tipo |
|---|---|---|---|
| COL01 | Usuário registra dois exemplares da mesma espécie | Permitir dois IDs individuais | Banco |
| COL02 | Criar exemplar e primeiro estado de jogo | Salvar ambos em uma transação | Integração |
| COL03 | Criar estado para outro jogo do mesmo exemplar | Manter estado separado | Integração |
| COL04 | Criar dois estados atuais do mesmo exemplar e mesma mecânica | Rejeitar duplicidade | Banco |
| COL05 | Criar estado com forma pertencente a outra mecânica | Rejeitar por FK composta/validação | Banco |
| COL06 | Consultar exemplar sem estado no jogo selecionado | Informar que não há estado cadastrado; não inventar dados | Interface |
| COL07 | Alterar estado de um exemplar | Não alterar outros exemplares da mesma espécie | Integração |
| COL08 | Registrar jogo de origem diferente do jogo do estado atual | Preservar ambos os valores | Integração |

## 5. Evolução e transformação

| ID | Cenário | Resultado esperado | Tipo |
|---|---|---|---|
| EVO01 | Evoluir Bulbasaur para Ivysaur em um estado | Atualizar forma no mesmo estado e manter id_pokemon_colecao | Integração |
| EVO02 | Evoluir novamente o mesmo indivíduo para Venusaur | Manter o mesmo exemplar | Integração |
| EVO03 | Verificar forma de origem após evolução | Manter a forma de origem sem alteração | Integração |
| EVO04 | Tentar evolução sem método/condição compatível | Bloquear ou exigir confirmação, conforme regra | Serviço |
| EVO05 | Associar evolução entre contextos de mecânicas diferentes | Rejeitar | Banco/serviço |
| EVO06 | Usar transformação temporária de batalha | Não criar novo exemplar nem evolução permanente | Serviço |
| EVO07 | Registrar forma disponível apenas como transformação na coleção | Bloquear registro independente | Serviço |

## 6. Treinamento e análise

| ID | Cenário | Resultado esperado | Tipo |
|---|---|---|---|
| ANA01 | Inserir valor abaixo do mínimo ou acima do máximo | Rejeitar | Banco/serviço |
| ANA02 | Inserir dois valores para o mesmo atributo e estado | Rejeitar duplicidade | Banco |
| ANA03 | Associar atributo de treinamento de outra mecânica | Rejeitar | Banco/serviço |
| ANA04 | Somar valores acima do limite total do contexto | Rejeitar a transação | Serviço |
| ANA05 | Analisar valor zero | Tratar como valor real | Serviço |
| ANA06 | Analisar valor não informado | Marcar análise incompleta; não tratar como zero | Serviço |
| ANA07 | Analisar atributo não aplicável | Excluir da comparação e explicar | Serviço/UI |
| ANA08 | Perfil pede IV baixo em um atributo | Reconhecer preferência do perfil; não presumir máximo | Serviço |
| ANA09 | Perfil e estado têm mecânicas incompatíveis | Bloquear análise | Serviço |
| ANA10 | Perfil de referência sem fonte/versão | Não publicar como referência verificada | Serviço |
| ANA11 | Gerar nota total sem fórmula documentada | Não mostrar nota global | Serviço/UI |
| ANA12 | Gerar recomendação | Exibir valor atual, alvo, regra e justificativa | Integração/UI |

## 7. Perfis e regulamentos

| ID | Cenário | Resultado esperado | Tipo |
|---|---|---|---|
| REG01 | Usuário cria perfil personalizado | Perfil recebe o proprietário autenticado | Integração |
| REG02 | Usuário tenta acessar perfil privado de outro usuário | Negar acesso | Segurança |
| REG03 | Perfil personalizado não tem regulamento | Permitir | Banco/serviço |
| REG04 | Perfil competitivo se associa a regulamento de outro jogo | Rejeitar | Banco/serviço |
| REG05 | Consultar elegibilidade sem registro | Mostrar NAO_VERIFICADO | Serviço/UI |
| REG06 | Status restrito sem condição | Rejeitar registro incompleto | Serviço |
| REG07 | Forma permitida no regulamento, mas exemplar tem dados individuais não verificados | Mostrar apenas elegibilidade da forma; não certificar legalidade completa | UI |
| REG08 | Regulamento fora de vigência | Identificar como expirado/fora de vigência | Serviço/UI |

## 8. Segurança e privacidade

| ID | Cenário | Resultado esperado | Tipo |
|---|---|---|---|
| SEG01 | Usuário A consulta ID de exemplar do usuário B | Não retornar dados privados | Segurança |
| SEG02 | Usuário A atualiza ou exclui ID de usuário B | Negar e não modificar dados | Segurança |
| SEG03 | Cliente envia id_usuario de outra conta | Ignorar esse valor e usar usuário da sessão | Segurança |
| SEG04 | Senha é salva | Persistir apenas hash apropriado | Segurança |
| SEG05 | Entrada contém caracteres SQL especiais | Tratar como dado por consulta parametrizada | Segurança |
| SEG06 | Requisição autenticada de alteração sem token CSRF | Rejeitar | Segurança |
| SEG07 | Conexão SQLite é aberta | Verificar PRAGMA foreign_keys = ON | Integração |

## 9. Importação e rastreabilidade

| ID | Cenário | Resultado esperado | Tipo |
|---|---|---|---|
| IMP01 | Importar catálogo com fonte/versão | Registrar origem e data | Integração |
| IMP02 | Importação encontra identificador duplicado | Atualizar ou rejeitar segundo regra documentada, sem duplicar | Integração |
| IMP03 | Importação rejeita registros | Gerar contagem e motivo | Integração |
| IMP04 | Importar dado sem confirmação | Marcar não verificado; não preencher por inferência | Integração |
| IMP05 | Atualizar lote | Preservar histórico de versão da fonte usada anteriormente | Integração |

## 10. Critério de aprovação

- Todos os testes de banco e domínio devem passar antes da interface ser considerada concluída.
- Testes de autorização devem ser executados com pelo menos dois usuários distintos.
- Casos de evolução devem comprovar que a identidade individual não muda.
- Casos de jogo devem comprovar que dados de treinamento nunca são convertidos sem regra documentada.
- Análises devem falhar de forma explícita diante de dados incompatíveis ou incompletos.
- A cobertura do catálogo deve ter relatório independente; não basta um teste de contagem.
- Até os testes serem implementados e executados, estes casos são **especificações de teste**, não evidência de que o sistema passou.
