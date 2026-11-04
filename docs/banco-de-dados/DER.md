# Diagrama Entidade-Relacionamento — versão 3.0

**Status:** DER textual proposto após auditoria.  
**Referência conceitual:** [modelo-conceitual-v3.md](modelo-conceitual-v3.md)

Este DER separa catálogo, dados por jogo, mecânicas versionadas, exemplares individuais, valores de atributos, perfis e regulamentos. Ele ainda precisa ser desenhado e conferido no brModelo.

```mermaid
erDiagram
    USUARIO ||--o{ POKEMON_COLECAO : possui
    DADOS_FORMA_JOGO ||--o{ POKEMON_COLECAO : contexto_atual
    JOGO |o--o{ POKEMON_COLECAO : jogo_origem
    METODO_OBTENCAO |o--o{ POKEMON_COLECAO : metodo_real
    NATUREZA |o--o{ POKEMON_COLECAO : natureza
    HABILIDADE_FORMA_JOGO |o--o{ POKEMON_COLECAO : habilidade_atual

    ESPECIE ||--|{ FORMA : possui
    FORMA ||--o{ DADOS_FORMA_JOGO : aparece_como
    JOGO ||--o{ DADOS_FORMA_JOGO : descreve
    DADOS_FORMA_JOGO ||--o{ TIPO_FORMA_JOGO : possui_tipo
    TIPO ||--o{ TIPO_FORMA_JOGO : classifica
    DADOS_FORMA_JOGO ||--o{ HABILIDADE_FORMA_JOGO : disponibiliza
    HABILIDADE ||--o{ HABILIDADE_FORMA_JOGO : habilidade
    DADOS_FORMA_JOGO ||--o{ METODO_FORMA_JOGO : admite
    METODO_OBTENCAO ||--o{ METODO_FORMA_JOGO : metodo_possivel

    JOGO ||--o{ MECANICA_JOGO : possui_versoes
    MECANICA_JOGO ||--o{ MECANICA_SISTEMA_ATRIBUTO : define_sistema
    SISTEMA_ATRIBUTO ||--o{ MECANICA_SISTEMA_ATRIBUTO : classifica
    POKEMON_COLECAO ||--o{ VALOR_ATRIBUTO_POKEMON : recebe
    MECANICA_SISTEMA_ATRIBUTO ||--o{ VALOR_ATRIBUTO_POKEMON : valida
    ATRIBUTO_BATALHA ||--o{ VALOR_ATRIBUTO_POKEMON : afeta

    DADOS_FORMA_JOGO ||--o{ PERFIL_ANALISE : alvo
    MECANICA_JOGO ||--o{ PERFIL_ANALISE : usa_regras
    USUARIO |o--o{ PERFIL_ANALISE : cria
    REGULAMENTO |o--o{ PERFIL_ANALISE : contextualiza
    PERFIL_ANALISE ||--o{ VALOR_PERFIL_ANALISE : define
    MECANICA_SISTEMA_ATRIBUTO ||--o{ VALOR_PERFIL_ANALISE : usa_sistema
    ATRIBUTO_BATALHA ||--o{ VALOR_PERFIL_ANALISE : define_atributo
    PERFIL_ANALISE ||--o{ PERFIL_NATUREZA : recomenda
    NATUREZA ||--o{ PERFIL_NATUREZA : pode_ser_recomendada
    PERFIL_ANALISE ||--o{ PERFIL_HABILIDADE : recomenda
    HABILIDADE_FORMA_JOGO ||--o{ PERFIL_HABILIDADE : opcao_compativel

    MECANICA_JOGO ||--o{ REGULAMENTO : recebe
    REGULAMENTO ||--o{ ELEGIBILIDADE_FORMA_REGULAMENTO : define
    DADOS_FORMA_JOGO ||--o{ ELEGIBILIDADE_FORMA_REGULAMENTO : avaliada
    DADOS_FORMA_JOGO ||--o{ TRANSFORMACAO_FORMA : origem
    DADOS_FORMA_JOGO ||--o{ TRANSFORMACAO_FORMA : destino

    USUARIO {
        int id_usuario PK
        string nome_usuario UK
        string email UK
        string senha_hash
        date data_cadastro
    }
    ESPECIE {
        int id_especie PK
        int numero_nacional UK
        string nome_pt
        string nome_en
        int geracao_origem
    }
    FORMA {
        int id_forma PK
        int id_especie FK
        string codigo_forma
        string nome_forma
        string categoria
        string estado_forma
        boolean forma_padrao
        string fonte_url
        date data_verificacao
    }
    JOGO {
        int id_jogo PK
        string nome UK
        string categoria
        int geracao
        string plataforma
        date data_lancamento
    }
    DADOS_FORMA_JOGO {
        int id_dados_forma PK
        int id_forma FK
        int id_jogo FK
        string status_presenca
        string pode_ser_registrada
        float altura_m
        float peso_kg
        int hp_base
        int ataque_base
        int defesa_base
        int ataque_especial_base
        int defesa_especial_base
        int velocidade_base
        string fonte_url
        date data_verificacao
    }
    TIPO {
        int id_tipo PK
        string nome_tipo UK
    }
    TIPO_FORMA_JOGO {
        int id_dados_forma PK, FK
        int id_tipo PK, FK
        int posicao
    }
    HABILIDADE {
        int id_habilidade PK
        string nome UK
        string descricao
    }
    HABILIDADE_FORMA_JOGO {
        int id_habilidade_forma PK
        int id_dados_forma FK
        int id_habilidade FK
        string slot
        string condicao
    }
    METODO_OBTENCAO {
        int id_metodo PK
        string nome UK
        string descricao
    }
    METODO_FORMA_JOGO {
        int id_dados_forma PK, FK
        int id_metodo PK, FK
        string condicao
    }
    MECANICA_JOGO {
        int id_mecanica PK
        int id_jogo FK
        string versao
        boolean usa_natureza
        date data_inicio
        date data_fim
        string fonte_url
        date data_verificacao
    }
    NATUREZA {
        int id_natureza PK
        string nome UK
        string atributo_aumentado
        string atributo_reduzido
    }
    POKEMON_COLECAO {
        int id_pokemon_colecao PK
        int id_usuario FK
        int id_dados_forma_atual FK
        int id_jogo_origem FK
        int id_metodo_obtencao FK
        int id_natureza FK
        int id_habilidade_forma FK
        string apelido
        int nivel
        date data_registro
        string observacao
    }
    ATRIBUTO_BATALHA {
        int id_atributo PK
        string codigo UK
        string nome
    }
    SISTEMA_ATRIBUTO {
        int id_sistema_atributo PK
        string codigo UK
        string nome
        string descricao
    }
    MECANICA_SISTEMA_ATRIBUTO {
        int id_mecanica_sistema_atributo PK
        int id_mecanica FK
        int id_sistema_atributo FK
        string aplicabilidade
        string unidade
        int valor_minimo
        int valor_maximo_atributo
        int valor_maximo_total
        string fonte_url
        date data_verificacao
    }
    VALOR_ATRIBUTO_POKEMON {
        int id_valor_atributo PK
        int id_pokemon_colecao FK
        int id_mecanica_sistema_atributo FK
        int id_atributo FK
        int valor
    }
    PERFIL_ANALISE {
        int id_perfil PK
        int id_dados_forma FK
        int id_mecanica FK
        int id_usuario FK
        int id_regulamento FK
        string nome_perfil
        string descricao
        string tipo_perfil
        string fonte_url
        date data_verificacao
    }
    VALOR_PERFIL_ANALISE {
        int id_valor_perfil PK
        int id_perfil FK
        int id_mecanica_sistema_atributo FK
        int id_atributo FK
        int valor_alvo
    }
    PERFIL_NATUREZA {
        int id_perfil PK, FK
        int id_natureza PK, FK
    }
    PERFIL_HABILIDADE {
        int id_perfil PK, FK
        int id_habilidade_forma PK, FK
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
        string fonte_url
        date data_verificacao
    }
    ELEGIBILIDADE_FORMA_REGULAMENTO {
        int id_elegibilidade PK
        int id_regulamento FK
        int id_dados_forma FK
        string status
        string condicao
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
    }
```

## Restrições que não ficam totalmente visíveis no desenho

1. Uma forma pertence a uma espécie; codigo_forma é único dentro da espécie.
2. Deve existir exatamente uma forma padrão por espécie.
3. A combinação forma + jogo é única em DADOS_FORMA_JOGO.
4. TIPO_FORMA_JOGO aceita somente posição 1 ou 2, sem repetir tipo ou posição; no máximo duas linhas por ficha.
5. A combinação ficha + habilidade + slot é única.
6. A combinação ficha + método é única.
7. A combinação jogo + versão de mecânica é única.
8. A combinação mecânica + sistema de valores de atributo é única.
9. A combinação exemplar + sistema de valores de atributo + atributo é única.
10. A combinação perfil + sistema de valores de atributo + atributo é única.
11. Perfil personalizado exige usuário; perfil de referência é mantido pelo sistema.
12. Forma e mecânica de perfil devem pertencer ao mesmo jogo.
13. Elegibilidade é única por regulamento + ficha da forma.
14. Uma transformação deve ligar duas fichas do mesmo jogo.
15. Valores e limites não confirmados não devem ser presumidos.

**Atenção:** Mermaid é uma representação documental. A cardinalidade, obrigatoriedade e as restrições acima precisam ser reproduzidas e conferidas no brModelo e depois no modelo lógico.


## Semântica da camada de valores de atributos

Os nomes SISTEMA_ATRIBUTO, MECANICA_SISTEMA_ATRIBUTO e VALOR_ATRIBUTO_POKEMON são intencionais: IV não é treinamento. O modelo agrupa sistemas que fornecem valores de atributos sem declarar que todos funcionam da mesma forma.
