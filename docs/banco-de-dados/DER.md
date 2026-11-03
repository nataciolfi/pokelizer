# Diagrama Entidade-Relacionamento — PokéAnalyzer

**Versão:** 3.0  
**Status:** DER textual corrigido; ainda precisa ser reproduzido e conferido no brModelo.

O diagrama separa catálogo, contexto de jogo, exemplar individual, estado por jogo, evolução, transformação, treinamento, perfil e regulamento.

```mermaid
erDiagram
    USUARIO ||--o{ POKEMON_COLECAO : possui
    FORMA o|--o{ POKEMON_COLECAO : forma_origem
    JOGO o|--o{ POKEMON_COLECAO : jogo_origem
    METODO_OBTENCAO o|--o{ POKEMON_COLECAO : metodo_origem
    USUARIO o|--o{ PERFIL_ANALISE : cria
    ESPECIE ||--|{ FORMA : possui
    FORMA ||--o{ DADOS_FORMA_JOGO : representa
    JOGO ||--|{ MECANICA_JOGO : possui
    MECANICA_JOGO ||--o{ DADOS_FORMA_JOGO : contextualiza

    DADOS_FORMA_JOGO ||--o{ DADOS_FORMA_TIPO : tem
    TIPO ||--o{ DADOS_FORMA_TIPO : classifica
    DADOS_FORMA_JOGO ||--o{ HABILIDADE_FORMA_JOGO : disponibiliza
    HABILIDADE ||--o{ HABILIDADE_FORMA_JOGO : aparece
    DADOS_FORMA_JOGO ||--o{ OBTENCAO_FORMA_JOGO : permite
    METODO_OBTENCAO ||--o{ OBTENCAO_FORMA_JOGO : descreve

    POKEMON_COLECAO ||--o{ POKEMON_ESTADO_JOGO : possui_estado
    MECANICA_JOGO ||--o{ POKEMON_ESTADO_JOGO : contextualiza
    DADOS_FORMA_JOGO ||--o{ POKEMON_ESTADO_JOGO : define_forma
    NATUREZA o|--o{ POKEMON_ESTADO_JOGO : natureza
    HABILIDADE_FORMA_JOGO o|--o{ POKEMON_ESTADO_JOGO : habilidade

    MECANICA_JOGO ||--o{ GRUPO_LIMITE_TREINAMENTO : define_limites
    MECANICA_JOGO ||--o{ ATRIBUTO_TREINAMENTO : define
    GRUPO_LIMITE_TREINAMENTO o|--o{ ATRIBUTO_TREINAMENTO : agrupa
    POKEMON_ESTADO_JOGO ||--o{ VALOR_TREINAMENTO_POKEMON : registra
    ATRIBUTO_TREINAMENTO ||--o{ VALOR_TREINAMENTO_POKEMON : mede

    DADOS_FORMA_JOGO ||--o{ PERFIL_ANALISE : recebe_perfil
    REGULAMENTO o|--o{ PERFIL_ANALISE : contextualiza
    PERFIL_ANALISE ||--o{ VALOR_TREINAMENTO_PERFIL : define
    ATRIBUTO_TREINAMENTO ||--o{ VALOR_TREINAMENTO_PERFIL : referencia
    PERFIL_ANALISE ||--o{ PERFIL_NATUREZA : recomenda
    NATUREZA ||--o{ PERFIL_NATUREZA : aparece
    PERFIL_ANALISE ||--o{ PERFIL_HABILIDADE : recomenda
    HABILIDADE_FORMA_JOGO ||--o{ PERFIL_HABILIDADE : aparece

    MECANICA_JOGO ||--o{ REGULAMENTO : recebe
    REGULAMENTO ||--o{ ELEGIBILIDADE_REGULAMENTO : define
    DADOS_FORMA_JOGO ||--o{ ELEGIBILIDADE_REGULAMENTO : avaliada

    DADOS_FORMA_JOGO ||--o{ EVOLUCAO_FORMA_JOGO : evolui_de
    DADOS_FORMA_JOGO ||--o{ EVOLUCAO_FORMA_JOGO : evolui_para
    DADOS_FORMA_JOGO ||--o{ TRANSFORMACAO_FORMA : transforma_de
    DADOS_FORMA_JOGO ||--o{ TRANSFORMACAO_FORMA : transforma_para

    USUARIO {
        int id_usuario PK
        string nome_usuario UK
        string email UK
        string senha_hash
        datetime data_cadastro
    }
    ESPECIE {
        int id_especie PK
        int numero_nacional UK
        string nome_pt
        string nome_en
        int geracao_origem
        string codigo_catalogo
        string fonte_url
        string fonte_versao
    }
    FORMA {
        int id_forma PK
        int id_especie FK
        string codigo_forma
        string nome_forma
        string categoria
        boolean forma_padrao
        string descricao
        string fonte_url
    }
    JOGO {
        int id_jogo PK
        string nome
        string edicao
        string categoria
        int geracao
        string plataforma
        date data_lancamento
    }
    MECANICA_JOGO {
        int id_mecanica PK
        int id_jogo FK
        string nome_contexto
        string versao_referencia
        string status_iv
        string status_ev
        string status_natureza
        string sistema_treinamento
        string formula_atributos
        string fonte_regras
        date data_verificacao
        date vigencia_inicio
        date vigencia_fim
    }
    DADOS_FORMA_JOGO {
        int id_dados_forma PK
        int id_forma FK
        int id_mecanica FK
        string status_presenca
        string status_registrabilidade
        float altura
        float peso
        int hp_base
        int ataque_base
        int defesa_base
        int ataque_especial_base
        int defesa_especial_base
        int velocidade_base
        string fonte_dados
        string versao_dados
        date data_verificacao
    }
    TIPO {
        int id_tipo PK
        string nome_tipo UK
    }
    DADOS_FORMA_TIPO {
        int id_dados_forma PK,FK
        int id_tipo PK,FK
        string slot
    }
    HABILIDADE {
        int id_habilidade PK
        string nome
        string codigo_catalogo
    }
    HABILIDADE_FORMA_JOGO {
        int id_habilidade_forma PK
        int id_dados_forma FK
        int id_habilidade FK
        string slot
        string condicao
        string fonte_url
        date data_verificacao
    }
    NATUREZA {
        int id_natureza PK
        string nome UK
        string atributo_aumentado
        string atributo_reduzido
    }
    METODO_OBTENCAO {
        int id_metodo PK
        string codigo UK
        string nome
    }
    OBTENCAO_FORMA_JOGO {
        int id_obtencao PK
        int id_dados_forma FK
        int id_metodo FK
        string condicao
        string fonte_url
        date data_verificacao
    }
    POKEMON_COLECAO {
        int id_pokemon_colecao PK
        int id_usuario FK
        int id_forma_origem FK
        int id_jogo_origem FK
        int id_metodo_origem FK
        string apelido
        date data_obtencao
        datetime data_registro
        string observacao
    }
    POKEMON_ESTADO_JOGO {
        int id_estado_jogo PK
        int id_pokemon_colecao FK
        int id_mecanica FK
        int id_dados_forma FK
        int id_natureza FK
        int id_habilidade_forma FK
        int nivel
        string observacao
        datetime data_atualizacao
    }
    GRUPO_LIMITE_TREINAMENTO {
        int id_grupo_limite PK
        int id_mecanica FK
        string codigo
        string nome
        float limite_total
        string unidade
        string fonte_url
        date data_verificacao
    }
    ATRIBUTO_TREINAMENTO {
        int id_atributo_treinamento PK
        int id_mecanica FK
        int id_grupo_limite FK
        string codigo
        string categoria
        string atributo
        string nome_exibicao
        string tipo_valor
        string unidade
        float valor_minimo
        float valor_maximo
        float incremento
        string fonte_url
        date data_verificacao
    }
    VALOR_TREINAMENTO_POKEMON {
        int id_estado_jogo PK,FK
        int id_atributo_treinamento PK,FK
        float valor
        string observacao
    }
    PERFIL_ANALISE {
        int id_perfil PK
        int id_dados_forma FK
        int id_usuario FK
        int id_regulamento FK
        string nome_perfil
        string descricao
        string tipo_perfil
        string fonte_perfil
        string versao_perfil
        datetime data_criacao
    }
    VALOR_TREINAMENTO_PERFIL {
        int id_perfil PK,FK
        int id_atributo_treinamento PK,FK
        float valor_minimo_desejado
        float valor_maximo_desejado
        float peso_prioridade
    }
    PERFIL_NATUREZA {
        int id_perfil PK,FK
        int id_natureza PK,FK
        string preferencia
        float prioridade
    }
    PERFIL_HABILIDADE {
        int id_perfil PK,FK
        int id_habilidade_forma PK,FK
        string preferencia
        float prioridade
    }
    REGULAMENTO {
        int id_regulamento PK
        int id_mecanica FK
        string codigo
        string nome
        string formato
        string temporada
        date data_inicio
        date data_fim
        string fonte_oficial
        date data_verificacao
    }
    ELEGIBILIDADE_REGULAMENTO {
        int id_elegibilidade PK
        int id_regulamento FK
        int id_dados_forma FK
        string status
        string condicao
        string fonte_verificacao
        date data_verificacao
    }
    EVOLUCAO_FORMA_JOGO {
        int id_evolucao PK
        int id_dados_forma_origem FK
        int id_dados_forma_destino FK
        string metodo_evolucao
        string condicao
        string item_requerido
        string fonte_url
        date data_verificacao
    }
    TRANSFORMACAO_FORMA {
        int id_transformacao PK
        int id_dados_forma_origem FK
        int id_dados_forma_destino FK
        string tipo_transformacao
        string condicao
        string item_requerido
        string observacao
        string fonte_url
        date data_verificacao
    }
```

## Como interpretar

- ESPECIE e FORMA compõem o catálogo global.
- POKEMON_COLECAO identifica o indivíduo; não fixa sua espécie atual.
- POKEMON_ESTADO_JOGO indica a forma atual, o nível, a natureza, a habilidade e o treinamento naquele contexto.
- EVOLUCAO_FORMA_JOGO descreve mudanças permanentes por jogo; TRANSFORMACAO_FORMA descreve mudanças de estado, normalmente temporárias.
- MECANICA_JOGO identifica regras de atributos/treinamento, não uma temporada competitiva.
- GRUPO_LIMITE_TREINAMENTO armazena limites agregados uma vez; ATRIBUTO_TREINAMENTO armazena limites individuais, tipo numérico e incremento.
- DADOS_FORMA_JOGO contextualiza atributos, tipos, habilidades, presença e registrabilidade.
- OBTENCAO_FORMA_JOGO aceita vários métodos por forma/contexto.
- ATRIBUTO_TREINAMENTO e VALOR_TREINAMENTO_POKEMON não fixam IV/EV como campos universais.
- PERFIL_ANALISE é referência de comparação; REGULAMENTO é regra de competição.
- ELEGIBILIDADE_REGULAMENTO trata da forma, não da legalidade integral do exemplar.

## Restrições que precisam aparecer no modelo lógico

1. Forma + mecânica única em DADOS_FORMA_JOGO.
2. No máximo dois tipos e slots distintos por contexto.
3. Limites agregados ficam em GRUPO_LIMITE_TREINAMENTO, não duplicados em MECANICA_JOGO e atributos.
3. Habilidade do estado no mesmo contexto de forma.
4. Atributo de treinamento da mesma mecânica do estado.
5. No máximo um estado atual por exemplar + mecânica.
6. Perfil, regulamento, evolução e transformação com contextos compatíveis.
7. Evolução atualiza a forma do estado sem criar exemplar novo.
8. Limites agregados de treinamento.
9. Ausência de elegibilidade significa não verificado.

As regras detalhadas estão em [regras-integridade.md](regras-integridade.md). O DER visual ainda deve ser conferido no brModelo.
