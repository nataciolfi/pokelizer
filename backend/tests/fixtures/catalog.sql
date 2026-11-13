-- TEST FIXTURE ONLY: synthetic context, names, limits and evidence. NOT Pokémon facts.
INSERT INTO ESPECIE(id_especie,numero_nacional,nome_pt,nome_en,geracao_origem)
VALUES (1,99901,'FIXTURE species A','FIXTURE species A',1) ON CONFLICT DO NOTHING;
INSERT INTO FORMA(id_forma,id_especie,codigo_forma,nome_forma,forma_padrao)
VALUES(1,1,'fixture-standard','FIXTURE standard',1) ON CONFLICT DO NOTHING;
INSERT INTO JOGO(id_jogo,nome,categoria,geracao) VALUES(1,'FIXTURE game A','teste',1) ON CONFLICT DO NOTHING;
INSERT INTO DADOS_FORMA_JOGO(id_dados_forma,id_forma,id_jogo,status_presenca,pode_ser_registrada,fonte_url,data_verificacao)
VALUES(1,1,1,'nativa','sim','https://example.invalid/fixture','2026-11-13') ON CONFLICT DO NOTHING;
INSERT INTO TIPO(id_tipo,nome_tipo) VALUES(1,'FIXTURE type A') ON CONFLICT DO NOTHING;
INSERT INTO TIPO_FORMA_JOGO(id_dados_forma,id_tipo,posicao) VALUES(1,1,1) ON CONFLICT DO NOTHING;
UPDATE DADOS_FORMA_JOGO SET status_tipos='aplicavel' WHERE id_dados_forma=1;
INSERT INTO METODO_OBTENCAO(id_metodo,nome) VALUES(1,'FIXTURE capture') ON CONFLICT DO NOTHING;
INSERT INTO METODO_FORMA_JOGO(id_dados_forma,id_metodo,fonte_url,data_verificacao)
VALUES(1,1,'https://example.invalid/fixture','2026-11-13') ON CONFLICT DO NOTHING;
INSERT INTO HABILIDADE(id_habilidade,nome) VALUES(1,'FIXTURE ability') ON CONFLICT DO NOTHING;
INSERT INTO HABILIDADE_FORMA_JOGO(id_habilidade_forma,id_dados_forma,id_habilidade,slot,fonte_url,data_verificacao)
VALUES(1,1,1,'fixture-slot','https://example.invalid/fixture','2026-11-13') ON CONFLICT DO NOTHING;
INSERT INTO MECANICA_JOGO(id_mecanica,id_jogo,versao,usa_natureza,usa_habilidade,usa_nivel,nivel_minimo,nivel_maximo,fonte_url,data_verificacao)
VALUES(1,1,'FIXTURE v1','sim','sim','sim',1,100,'https://example.invalid/fixture','2026-11-13') ON CONFLICT DO NOTHING;
