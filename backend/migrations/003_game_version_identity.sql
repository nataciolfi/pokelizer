-- Preserve existing game IDs and links. NULL means the source version is unknown.
ALTER TABLE JOGO ADD COLUMN codigo_versao_pokeapi TEXT CHECK(codigo_versao_pokeapi IS NULL OR length(trim(codigo_versao_pokeapi))>0);
CREATE UNIQUE INDEX jogo_codigo_pokeapi_unico ON JOGO(codigo_versao_pokeapi COLLATE NOCASE) WHERE codigo_versao_pokeapi IS NOT NULL;
CREATE TRIGGER jogo_versao_preservada BEFORE UPDATE OF codigo_versao_pokeapi ON JOGO
WHEN OLD.codigo_versao_pokeapi IS NOT NULL AND NEW.codigo_versao_pokeapi IS NOT OLD.codigo_versao_pokeapi
 AND (EXISTS (SELECT 1 FROM DADOS_FORMA_JOGO WHERE id_jogo=OLD.id_jogo)
      OR EXISTS (SELECT 1 FROM MECANICA_JOGO WHERE id_jogo=OLD.id_jogo)
      OR EXISTS (SELECT 1 FROM POKEMON_COLECAO WHERE id_jogo_origem=OLD.id_jogo))
BEGIN
    SELECT RAISE(ABORT, 'Versao utilizada nao pode mudar de identidade');
END;
