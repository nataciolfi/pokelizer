-- Additional provenance for independent type and base-stat datasets.
-- Existing facts retain NULL provenance; do not invent sources during migration.
ALTER TABLE DADOS_FORMA_JOGO ADD COLUMN fonte_tipos TEXT CHECK(fonte_tipos IS NULL OR length(trim(fonte_tipos))>0);
ALTER TABLE DADOS_FORMA_JOGO ADD COLUMN data_verificacao_tipos TEXT CHECK(data_verificacao_tipos IS NULL OR (date(data_verificacao_tipos,'+0 days') IS NOT NULL AND date(data_verificacao_tipos,'+0 days')=data_verificacao_tipos));
ALTER TABLE DADOS_FORMA_JOGO ADD COLUMN fonte_estatisticas TEXT CHECK(fonte_estatisticas IS NULL OR length(trim(fonte_estatisticas))>0);
ALTER TABLE DADOS_FORMA_JOGO ADD COLUMN data_verificacao_estatisticas TEXT CHECK(data_verificacao_estatisticas IS NULL OR (date(data_verificacao_estatisticas,'+0 days') IS NOT NULL AND date(data_verificacao_estatisticas,'+0 days')=data_verificacao_estatisticas));
CREATE TRIGGER evidencia_catalogo_insert BEFORE INSERT ON DADOS_FORMA_JOGO BEGIN
    SELECT CASE WHEN (NEW.fonte_tipos IS NULL)!=(NEW.data_verificacao_tipos IS NULL) OR (NEW.fonte_estatisticas IS NULL)!=(NEW.data_verificacao_estatisticas IS NULL) THEN RAISE(ABORT, 'Fonte e data devem ser informadas em conjunto') END;
END;
CREATE TRIGGER evidencia_catalogo_update BEFORE UPDATE ON DADOS_FORMA_JOGO BEGIN
    SELECT CASE WHEN (NEW.fonte_tipos IS NULL)!=(NEW.data_verificacao_tipos IS NULL) OR (NEW.fonte_estatisticas IS NULL)!=(NEW.data_verificacao_estatisticas IS NULL) THEN RAISE(ABORT, 'Fonte e data devem ser informadas em conjunto') END;
END;
