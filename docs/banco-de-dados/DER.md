# Diagrama Entidade-Relacionamento

Este diagrama é a representação visual inicial do modelo conceitual. Ele usa a sintaxe ER do Mermaid para ficar versionado em texto e poder ser visualizado diretamente no GitHub.

```mermaid
erDiagram
    USUARIO ||--o{ POKEMON_CAPTURADO : possui
    ESPECIE ||--|{ FORMA : possui
    FORMA }|--|{ TIPO : possui
    FORMA }o--|{ HABILIDADE : disponibiliza
    FORMA ||--o{ POKEMON_CAPTURADO : representa
    NATUREZA ||--o{ POKEMON_CAPTURADO : caracteriza
    HABILIDADE ||--o{ POKEMON_CAPTURADO : selecionada
    FORMA ||--o{ PERFIL_ANALISE : orienta
    USUARIO o|--o{ PERFIL_ANALISE : cria
    REGULAMENTO o|--o{ PERFIL_ANALISE : contextualiza
    PERFIL_ANALISE }|--|{ NATUREZA : recomenda
    REGULAMENTO }o--o{ FORMA : permite

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
        int geracao
    }

    FORMA {
        int id_forma PK
        string nome_forma
        string categoria
        float altura
        float peso
        int hp_base
        int ataque_base
        int defesa_base
        int ataque_especial_base
        int defesa_especial_base
        int velocidade_base
        string imagem_url
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

    NATUREZA {
        int id_natureza PK
        string nome
        string atributo_aumentado
        string atributo_reduzido
    }

    POKEMON_CAPTURADO {
        int id_capturado PK
        string apelido
        int nivel
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
        string nome
        string jogo
        string formato
        string temporada
        date data_inicio
        date data_fim
        string fonte_oficial
        boolean ativo
    }
```

## Observações

- `||--o{` representa um lado obrigatório e único ligado a zero ou muitos registros do outro lado.
- `}|--|{` representa uma relação de muitos para muitos em que cada lado participa de pelo menos um relacionamento no catálogo.
- Os relacionamentos opcionais de PERFIL_ANALISE com USUARIO e REGULAMENTO representam os perfis que podem ser mantidos pelo sistema e os perfis personalizados.
- Limites como "uma forma pode ter no máximo dois tipos" não são expressos completamente pela notação do diagrama; são regras de negócio.
- Este é um DER conceitual inicial. O modelo lógico ainda deverá converter as relações N:N em estruturas apropriadas e definir as chaves estrangeiras.
