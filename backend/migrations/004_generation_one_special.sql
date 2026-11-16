-- Generation I has one Special base stat; do not duplicate it into later stats.
-- Existing records remain NULL until sourced historical facts are imported.
ALTER TABLE DADOS_FORMA_JOGO ADD COLUMN especial_base INTEGER CHECK(especial_base IS NULL OR especial_base>=0);
