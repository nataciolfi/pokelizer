# PokéAnalyzer — backend inicial (Etapa 2)

Esta pasta contém uma implementação inicial do backend em Python, POO, SQLite e Flask, preparada para demonstrar cadastro e consulta no banco.

**Importante:** o schema SQLite é um recorte funcional e provisório do modelo conceitual 3.0. Não substitui o DER nem representa aprovação do modelo lógico. Depois que o DER for concluído no brModelo, tabelas, chaves, nulabilidade e restrições deverão ser comparadas e ajustadas.

## Requisitos
- Python 3.10 ou superior.
- pip.

## Instalação no Windows (PowerShell)
Entre na pasta backend e execute:

    py -3.13 -m venv .venv
    .\.venv\Scripts\Activate.ps1
    python -m pip install --upgrade pip
    pip install -r requirements.txt

Se a política do PowerShell bloquear a ativação:

    .\.venv\Scripts\python.exe -m pip install -r requirements.txt

## Configuração e execução
Configure uma chave secreta longa:

    $env:POKEANALYZER_SECRET_KEY = "substitua-por-uma-chave-aleatoria-longa"
    python run.py

A API ficará em http://127.0.0.1:5000. O SQLite será criado automaticamente em instance/pokelizer.sqlite3.

A base começa vazia. Para testar o fluxo sem importar o catálogo oficial, rode python scripts/seed_demo.py. O script insere uma ficha fictícia, claramente identificada como demonstração; ela não representa dados oficiais. Depois, consulte GET /api/pokemon e use o id_dados_forma retornado.

## Rotas implementadas

| Método | Rota | Autenticação | Função |
|---|---|---|---|
| GET | /api/status | Não | Verificar a API. |
| GET | /api/csrf | Não | Obter token CSRF. |
| POST | /api/auth/cadastro | CSRF | Criar usuário e iniciar sessão. |
| POST | /api/auth/login | CSRF | Autenticar usuário. |
| POST | /api/auth/logout | Sessão + CSRF | Encerrar sessão. |
| GET | /api/auth/me | Sessão | Consultar o usuário atual. |
| GET | /api/pokemon?busca=... | Não | Pesquisar espécies/formas. |
| GET | /api/pokemon/<id> | Não | Consultar uma ficha forma/jogo. |
| GET | /api/colecao | Sessão | Listar coleção do usuário. |
| POST | /api/colecao | Sessão + CSRF | Cadastrar exemplar. |
| GET | /api/colecao/<id> | Sessão | Consultar exemplar próprio. |
| DELETE | /api/colecao/<id> | Sessão + CSRF | Excluir exemplar próprio. |

O identificador de /api/pokemon/<id> é id_dados_forma: ficha de uma forma em um jogo específico, não apenas o número nacional.

## Fluxo de cadastro e consulta
1. Faça GET /api/csrf e guarde o token.
2. Faça POST /api/auth/cadastro com nome_usuario, email e senha, enviando X-CSRF-Token. O cadastro inicia a sessão.
3. A resposta contém um novo csrf_token; use-o nas operações seguintes.
4. Consulte GET /api/pokemon e obtenha um id_dados_forma.
5. Faça POST /api/colecao com id_dados_forma_atual e, opcionalmente, apelido, nível, origem, método, natureza, habilidade e observação.
6. Consulte GET /api/colecao.

Exemplo de corpo JSON:

    {"id_dados_forma_atual": 1, "apelido": "Meu Pokémon", "nivel": 25}

Todas as rotas de escrita exigem X-CSRF-Token. A coleção é filtrada pelo usuário autenticado.

## Dados fictícios de demonstração
Execute python scripts/seed_demo.py. O script é idempotente e cria apenas um registro fictício. Apague o banco local para removê-lo. Não use essa ficha como informação oficial.

## Testes
Com o ambiente ativado, execute pytest -q. Os testes usam banco temporário e cobrem pesquisa, cadastro, sessão, coleção, isolamento entre usuários, CSRF e validações.

## Organização
- pokeanalyzer/models.py: modelos de domínio (dataclasses).
- pokeanalyzer/dao.py: SQL parametrizado e persistência.
- pokeanalyzer/services.py: regras de negócio, validações e hash de senha.
- pokeanalyzer/api.py: rotas HTTP.
- pokeanalyzer/db.py: conexão SQLite e schema.
- schema.sql: tabelas e restrições provisórias.
- tests/test_api.py: testes automatizados.

## Limites
- Não há frontend final nem integração Fetch nesta etapa.
- O catálogo não vem populado com uma Pokédex completa.
- Análise IV/EV, perfis, regulamentos e cálculo de atributos não foram implementados.
- Histórico de transferências não foi implementado.
- O schema será revisado após o DER no brModelo.
- Antes de publicar o serviço, configure uma chave exclusiva e habilite cookie seguro em HTTPS.
