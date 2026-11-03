# Diagrama Entidade-Relacionamento

**Versão:** 2.0  
**Status:** modelo conceitual revisado

O diagrama separa o catálogo global, os dados por jogo, a coleção dos usuários e a elegibilidade competitiva.

```mermaid
erDiagram
    USUARIO ||--o{ POKEMON_COLECAO : possui
    JOGO |o--o{ POKEMON_COLECAO : jogo_origem
    ESPECIE ||--|{ FORMA : possui
    FORMA ||--o{ DADOS_FORMA_JOGO : recebe_dados
    JOGO ||--|{ MECANICA_JOGO : possui
    MECANICA_JOGO ||--o{ DADOS_FORMA_JOGO : define
    DADOS_FORMA_JOGO }|--|{ TIPO : possui
    DADOS_FORMA_JOGO ||--o{ HABILIDADE_FORMA_JOGO : disponibiliza
    HABILIDADE ||--o{ HABILIDADE_FORMA_JOGO : aparece
    DADOS_FORMA_JOGO ||--o{ POKEMON_COLECAO : identifica
    NATUREZA |o--o{ POKEMON_COLECAO : caracteriza
    HABILIDADE_FORMA_JOGO |o--o{ POKEMON_COLECAO : selecionada
    DADOS_FORMA_JOGO ||--o{ PERFIL_ANALISE : recebe_perfil
    USUARIO |o--o{ PERFIL_ANALISE : cria
    MECANICA_JOGO ||--o{ REGULAMENTO : recebe
    REGULAMENTO ||--o{ ELEGIBILIDADE_REGULAMENTO : define
    DADOS_FORMA_JOGO ||--o{ ELEGIBILIDADE_REGULAMENTO : avaliada
    PERFIL_ANALISE }o--o{ NATUREZA : recomenda
    PERFIL_ANALISE }o--o{ HABILIDADE_FORMA_JOGO : recomenda
    REGULAMENTO |o--o{ PERFIL_ANALISE : contextualiza
    DADOS_FORMA_JOGO ||--o{ TRANSFORMACAO_FORMA : origem
    DADOS_FORMA_JOGO ||--o{ TRANSFORMACAO_FORMA : destino

    USUARIO {
        int id_usuario PK
        string nome_usuario
        string email
        string senha_hash
        date data_cadastro
    }

    ESPECIE {
        int numero_nacional PK
        string nome_pt
        string nome_en
        int geracao_origem
    }

    FORMA {
        int id_forma PK
        string nome_forma
        string categoria
        string descricao
        boolean forma_padrao
        string referencia_visual
    }

    JOGO {
        int id_jogo PK
        string nome
        string categoria
        int geracao
        string plataforma
        date data_lancamento
    }

    MECANICA_JOGO {
        int id_mecanica PK
        string versao
        boolean usa_iv
        boolean usa_ev
        boolean usa_natureza
        int iv_minimo
        int iv_maximo
        int ev_maximo_atributo
        int ev_maximo_total
        string sistema_treinamento
        string fonte_regras
        date data_inicio
        date data_fim
    }

    DADOS_FORMA_JOGO {
        int id_dados_forma PK
        string status_disponibilidade
        string metodo_obtencao
        boolean pode_ser_registrada
        float altura
        float peso
        int hp_base
        int ataque_base
        int defesa_base
        int ataque_especial_base
        int defesa_especial_base
        int velocidade_base
        string fonte_dados
    }

    TIPO {
        int id_tipo PK
        string nome_tipo
    }

    HABILIDADE {
        int id_habilidade PK
        string nome
        string descricao
    }

    HABILIDADE_FORMA_JOGO {
        int id_habilidade_forma PK
        string slot
        string condicao
    }

    NATUREZA {
        int id_natureza PK
        string nome
        string atributo_aumentado
        string atributo_reduzido
    }

    POKEMON_COLECAO {
        int id_pokemon_colecao PK
        string apelido
        int nivel
        string metodo_obtencao
        date data_registro
        int iv_hp
        int iv_ataque
        int iv_defesa
        int iv_atq_especial
        int iv_def_especial
        int iv_velocidade
        int ev_hp
        int ev_ataque
        int ev_defesa
        int ev_atq_especial
        int ev_def_especial
        int ev_velocidade
    }

    PERFIL_ANALISE {
        int id_perfil PK
        string nome_perfil
        string descricao
        string tipo_perfil
        int iv_hp_ideal
        int iv_ataque_ideal
        int iv_defesa_ideal
        int iv_atq_especial_ideal
        int iv_def_especial_ideal
        int iv_velocidade_ideal
        int ev_hp
        int ev_ataque
        int ev_defesa
        int ev_atq_especial
        int ev_def_especial
        int ev_velocidade
    }

    REGULAMENTO {
        int id_regulamento PK
        string codigo
        string nome
        string formato
        string temporada
        date data_inicio
        date data_fim
        string fonte_oficial
        date data_consulta
    }

    ELEGIBILIDADE_REGULAMENTO {
        int id_elegibilidade PK
        string status
        string condicao
        string fonte_verificacao
        date data_verificacao
    }

    TRANSFORMACAO_FORMA {
        int id_transformacao PK
        string tipo_transformacao
        string condicao
        string item_requerido
        string observacao
    }
```

## Como interpretar

- ESPECIE e FORMA descrevem o catálogo global.
- DADOS_FORMA_JOGO guarda estatísticas, tipos, habilidades e disponibilidade no contexto de um jogo/mecânica.
- MECANICA_JOGO registra quais sistemas e limites se aplicam.
- POKEMON_COLECAO guarda um exemplar sem presumir que todos os jogos utilizem captura, IV ou EV.
- PERFIL_ANALISE aponta para uma forma em um contexto específico.
- REGULAMENTO e ELEGIBILIDADE_REGULAMENTO separam a presença na Pokédex da permissão competitiva.
- TRANSFORMACAO_FORMA liga a forma original à forma transformada.

## Regras importantes

1. Campos de IV/EV podem ser nulos quando não se aplicarem; nulo não equivale a zero.
2. Uma forma catalogada não precisa estar disponível em todos os jogos.
3. Uma forma transformada não é automaticamente uma captura independente.
4. Uma habilidade selecionada precisa estar disponível para a forma no jogo.
5. A legalidade é verificada por regulamento.
6. Uma forma não verificada não deve ser declarada proibida.
7. Relações N:N serão convertidas em tabelas associativas no modelo lógico.

Este DER substitui a versão conceitual anterior. Ele ainda deverá ser desenhado e conferido visualmente no brModelo antes da aprovação final.
