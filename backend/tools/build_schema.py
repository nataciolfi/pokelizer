"""Build physical SQL from the reviewed source and reusable integrity guards.

No catalog facts or seed data are generated. Run from the repository root.
"""
from pathlib import Path
import argparse

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--check", action="store_true", help="Check generated artifacts without writing files")
args = parser.parse_args()

ROOT = Path(__file__).resolve().parents[1]
base = ROOT / 'tools' / 'schema_base.sql'
sql = base.read_text()


def trigger(name, event, table, body, when=None):
    global sql
    sql += f'\nCREATE TRIGGER {name} {event} ON {table}\n'
    if when:
        sql += f'WHEN {when}\n'
    sql += f'BEGIN\n{body}\nEND;\n'


def guard(condition, message):
    return f"    SELECT CASE WHEN {condition} THEN RAISE(ABORT, '{message}') END;"


def both(name, table, body):
    for event in ('INSERT', 'UPDATE'):
        trigger(name + '_' + event.lower(), 'BEFORE ' + event, table, body)

# Exactly one standard form for complete catalog species, including reverse edits.
both('especie_completa', 'ESPECIE', guard("NEW.status_catalogo = 'completo' AND (SELECT count(*) FROM FORMA WHERE id_especie=NEW.id_especie AND forma_padrao=1) != 1", 'Especie completa exige exatamente uma forma padrao'))
trigger('forma_padrao_preservada_update', 'BEFORE UPDATE', 'FORMA', guard("EXISTS (SELECT 1 FROM ESPECIE WHERE id_especie=OLD.id_especie AND status_catalogo='completo') AND OLD.forma_padrao=1 AND (NEW.forma_padrao!=1 OR NEW.id_especie!=OLD.id_especie)", 'Forma padrao de especie completa deve ser preservada'))
trigger('forma_padrao_preservada_delete', 'BEFORE DELETE', 'FORMA', guard("OLD.forma_padrao=1 AND EXISTS (SELECT 1 FROM ESPECIE WHERE id_especie=OLD.id_especie AND status_catalogo='completo')", 'Forma padrao de especie completa deve ser preservada'))

# REPLACE must not silently remove the sole standard through an implicit deletion.
trigger('forma_padrao_preservada_replace', 'BEFORE INSERT', 'FORMA', guard("EXISTS (SELECT 1 FROM FORMA f JOIN ESPECIE e ON e.id_especie=f.id_especie WHERE f.forma_padrao=1 AND e.status_catalogo='completo' AND (f.id_forma=NEW.id_forma OR (f.id_especie=NEW.id_especie AND (f.codigo_forma=NEW.codigo_forma OR NEW.forma_padrao=1))))", 'Substituicao implicita da forma padrao nao permitida'))

# Staging a type set permits transactional loading; confirmed sets require primary coverage.
both('tipos_confirmados', 'DADOS_FORMA_JOGO', guard("NEW.status_tipos='aplicavel' AND NOT EXISTS (SELECT 1 FROM TIPO_FORMA_JOGO WHERE id_dados_forma=NEW.id_dados_forma AND posicao=1)", 'Tipos aplicaveis exigem tipo primario') + '\n' + guard("NEW.status_tipos='nao_aplicavel' AND EXISTS (SELECT 1 FROM TIPO_FORMA_JOGO WHERE id_dados_forma=NEW.id_dados_forma)", 'Contexto sem tipos nao admite tipos'))
for event in ('INSERT', 'UPDATE'):
    trigger('tipo_aplicavel_' + event.lower(), 'BEFORE ' + event, 'TIPO_FORMA_JOGO', guard("EXISTS (SELECT 1 FROM DADOS_FORMA_JOGO WHERE id_dados_forma=NEW.id_dados_forma AND status_tipos='nao_aplicavel')", 'Tipos nao aplicaveis ao contexto'))
for event in ('DELETE', 'UPDATE'):
    after = " AND NOT EXISTS (SELECT 1 FROM TIPO_FORMA_JOGO WHERE id_dados_forma=OLD.id_dados_forma AND posicao=1)"
    trigger('cobertura_tipo_' + event.lower(), 'AFTER ' + event, 'TIPO_FORMA_JOGO', guard("EXISTS (SELECT 1 FROM DADOS_FORMA_JOGO WHERE id_dados_forma=OLD.id_dados_forma AND status_tipos='aplicavel')" + after, 'Remocao invalidaria cobertura de tipos'))

trigger('cobertura_tipo_insert', 'AFTER INSERT', 'TIPO_FORMA_JOGO', guard("EXISTS (SELECT 1 FROM DADOS_FORMA_JOGO WHERE id_dados_forma=NEW.id_dados_forma AND status_tipos='aplicavel') AND NOT EXISTS (SELECT 1 FROM TIPO_FORMA_JOGO WHERE id_dados_forma=NEW.id_dados_forma AND posicao=1)", 'Substituicao invalidaria cobertura de tipos'))

# No implicit version changes after a dependent row exists. Changes require new version/context.
for table, pk in [('DADOS_FORMA_JOGO','id_dados_forma'), ('MECANICA_JOGO','id_mecanica'), ('MECANICA_SISTEMA_ATRIBUTO','id_mecanica_sistema_atributo'), ('REGULAMENTO','id_regulamento')]:
    dependents = {
        'DADOS_FORMA_JOGO': [('POKEMON_COLECAO','id_dados_forma_atual'), ('POKEMON_COLECAO','id_dados_forma_origem'), ('PERFIL_ANALISE','id_dados_forma'), ('ELEGIBILIDADE_FORMA_REGULAMENTO','id_dados_forma'), ('TRANSFORMACAO_FORMA','id_dados_forma_origem'), ('TRANSFORMACAO_FORMA','id_dados_forma_destino')],
        'MECANICA_JOGO': [('POKEMON_COLECAO','id_mecanica'), ('PERFIL_ANALISE','id_mecanica'), ('REGULAMENTO','id_mecanica'), ('MECANICA_SISTEMA_ATRIBUTO','id_mecanica')],
        'MECANICA_SISTEMA_ATRIBUTO': [('VALOR_ATRIBUTO_POKEMON','id_mecanica_sistema_atributo'), ('VALOR_PERFIL_ANALISE','id_mecanica_sistema_atributo')],
        'REGULAMENTO': [('PERFIL_ANALISE','id_regulamento'), ('ELEGIBILIDADE_FORMA_REGULAMENTO','id_regulamento')],
    }[table]
    immutable = {
        'DADOS_FORMA_JOGO': ['id_forma','id_jogo','status_presenca','pode_ser_registrada'],
        'MECANICA_JOGO': ['id_jogo','versao','usa_natureza','usa_habilidade','usa_nivel','nivel_minimo','nivel_maximo'],
        'MECANICA_SISTEMA_ATRIBUTO': ['id_mecanica','id_sistema_atributo','aplicabilidade','unidade','valor_minimo','valor_maximo_atributo','valor_maximo_total','limite_total_status'],
        'REGULAMENTO': ['id_mecanica','codigo','versao','formato','temporada'],
    }[table]
    changed = ' OR '.join(f'NEW.{c} IS NOT OLD.{c}' for c in immutable)
    used = ' OR '.join(f'EXISTS (SELECT 1 FROM {t} WHERE {c}=OLD.{pk})' for t,c in dependents)
    trigger('preservar_' + table.lower(), 'BEFORE UPDATE', table, guard(f'({changed}) AND ({used})', 'Registro utilizado: crie nova versao ou remova dependencias em transacao'))

specimen_body = guard("NOT EXISTS (SELECT 1 FROM DADOS_FORMA_JOGO WHERE id_dados_forma=NEW.id_dados_forma_atual AND status_presenca IN ('nativa','transferivel') AND pode_ser_registrada='sim')", 'Contexto atual exige presenca e registro independente confirmados')
specimen_body += '\n' + guard("NEW.id_mecanica IS NOT NULL AND NOT EXISTS (SELECT 1 FROM MECANICA_JOGO m JOIN DADOS_FORMA_JOGO d ON d.id_jogo=m.id_jogo WHERE m.id_mecanica=NEW.id_mecanica AND d.id_dados_forma=NEW.id_dados_forma_atual)", 'Mecanica e contexto atual pertencem a jogos distintos')
for field, flag in [('id_natureza','usa_natureza'), ('id_habilidade_forma','usa_habilidade'), ('nivel','usa_nivel')]:
    specimen_body += '\n' + guard(f"NEW.{field} IS NOT NULL AND NOT EXISTS (SELECT 1 FROM MECANICA_JOGO WHERE id_mecanica=NEW.id_mecanica AND {flag}='sim')", 'Valor exige aplicabilidade confirmada: ' + field)
specimen_body += '\n' + guard("NEW.nivel IS NOT NULL AND NOT EXISTS (SELECT 1 FROM MECANICA_JOGO WHERE id_mecanica=NEW.id_mecanica AND nivel_minimo IS NOT NULL AND nivel_maximo IS NOT NULL AND NEW.nivel BETWEEN nivel_minimo AND nivel_maximo)", 'Nivel fora dos limites confirmados')
specimen_body += '\n' + guard("NEW.id_habilidade_forma IS NOT NULL AND NOT EXISTS (SELECT 1 FROM HABILIDADE_FORMA_JOGO WHERE id_habilidade_forma=NEW.id_habilidade_forma AND id_dados_forma=NEW.id_dados_forma_atual)", 'Habilidade incompativel com contexto atual')
specimen_body += '\n' + guard("NEW.id_dados_forma_origem IS NOT NULL AND (NEW.id_jogo_origem IS NULL OR NOT EXISTS (SELECT 1 FROM DADOS_FORMA_JOGO WHERE id_dados_forma=NEW.id_dados_forma_origem AND id_jogo=NEW.id_jogo_origem))", 'Forma de origem exige jogo de origem compativel')
both('colecao_contexto', 'POKEMON_COLECAO', specimen_body)
trigger('colecao_preservar_contexto', 'BEFORE UPDATE', 'POKEMON_COLECAO', guard("(NEW.id_dados_forma_atual IS NOT OLD.id_dados_forma_atual OR NEW.id_mecanica IS NOT OLD.id_mecanica) AND EXISTS (SELECT 1 FROM VALOR_ATRIBUTO_POKEMON WHERE id_pokemon_colecao=OLD.id_pokemon_colecao)", 'Remova valores do contexto anterior em transacao antes de mudar contexto'))

profile = guard("NOT EXISTS (SELECT 1 FROM DADOS_FORMA_JOGO d JOIN MECANICA_JOGO m ON m.id_jogo=d.id_jogo WHERE d.id_dados_forma=NEW.id_dados_forma AND m.id_mecanica=NEW.id_mecanica)", 'Perfil: forma e mecanica de jogos distintos')
profile += '\n' + guard("NEW.id_regulamento IS NOT NULL AND NOT EXISTS (SELECT 1 FROM REGULAMENTO WHERE id_regulamento=NEW.id_regulamento AND id_mecanica=NEW.id_mecanica)", 'Perfil e regulamento de mecanicas distintas')
both('perfil_contexto', 'PERFIL_ANALISE', profile)
trigger('perfil_preservar_contexto', 'BEFORE UPDATE', 'PERFIL_ANALISE', guard("(NEW.id_dados_forma IS NOT OLD.id_dados_forma OR NEW.id_mecanica IS NOT OLD.id_mecanica) AND (EXISTS (SELECT 1 FROM VALOR_PERFIL_ANALISE WHERE id_perfil=OLD.id_perfil) OR EXISTS (SELECT 1 FROM PERFIL_NATUREZA WHERE id_perfil=OLD.id_perfil) OR EXISTS (SELECT 1 FROM PERFIL_HABILIDADE WHERE id_perfil=OLD.id_perfil))", 'Perfil utilizado exige revisao das opcoes antes de mudar contexto'))
both('perfil_natureza_compativel', 'PERFIL_NATUREZA', guard("NOT EXISTS (SELECT 1 FROM PERFIL_ANALISE p JOIN MECANICA_JOGO m ON m.id_mecanica=p.id_mecanica WHERE p.id_perfil=NEW.id_perfil AND m.usa_natureza='sim')", 'Natureza nao confirmada para perfil'))
both('perfil_habilidade_compativel', 'PERFIL_HABILIDADE', guard("NOT EXISTS (SELECT 1 FROM PERFIL_ANALISE p JOIN HABILIDADE_FORMA_JOGO h ON h.id_dados_forma=p.id_dados_forma JOIN MECANICA_JOGO m ON m.id_mecanica=p.id_mecanica WHERE p.id_perfil=NEW.id_perfil AND h.id_habilidade_forma=NEW.id_habilidade_forma AND m.usa_habilidade='sim')", 'Habilidade incompativel com perfil'))
trigger('habilidade_contexto_imutavel', 'BEFORE UPDATE', 'HABILIDADE_FORMA_JOGO', guard("(NEW.id_dados_forma IS NOT OLD.id_dados_forma OR NEW.id_habilidade IS NOT OLD.id_habilidade OR NEW.slot IS NOT OLD.slot) AND (EXISTS (SELECT 1 FROM POKEMON_COLECAO WHERE id_habilidade_forma=OLD.id_habilidade_forma) OR EXISTS (SELECT 1 FROM PERFIL_HABILIDADE WHERE id_habilidade_forma=OLD.id_habilidade_forma))", 'Habilidade utilizada nao pode mudar de identidade'))

both('elegibilidade_contexto', 'ELEGIBILIDADE_FORMA_REGULAMENTO', guard("NOT EXISTS (SELECT 1 FROM REGULAMENTO r JOIN MECANICA_JOGO m ON m.id_mecanica=r.id_mecanica JOIN DADOS_FORMA_JOGO d ON d.id_jogo=m.id_jogo WHERE r.id_regulamento=NEW.id_regulamento AND d.id_dados_forma=NEW.id_dados_forma)", 'Elegibilidade de jogo incompativel'))
both('transformacao_contexto', 'TRANSFORMACAO_FORMA', guard("NOT EXISTS (SELECT 1 FROM DADOS_FORMA_JOGO a JOIN DADOS_FORMA_JOGO b ON b.id_jogo=a.id_jogo WHERE a.id_dados_forma=NEW.id_dados_forma_origem AND b.id_dados_forma=NEW.id_dados_forma_destino)", 'Transformacao exige endpoints do mesmo jogo'))

# Value guards apply on BOTH insert and update, excluding the old row in aggregate updates.
for table, owner_table, owner_pk, owner_fk, value, pk in [
    ('VALOR_ATRIBUTO_POKEMON','POKEMON_COLECAO','id_pokemon_colecao','id_pokemon_colecao','valor','id_valor_atributo'),
    ('VALOR_PERFIL_ANALISE','PERFIL_ANALISE','id_perfil','id_perfil','valor_alvo','id_valor_perfil')]:
    for event in ('INSERT','UPDATE'):
        body = guard(f"NOT EXISTS (SELECT 1 FROM {owner_table} o JOIN MECANICA_SISTEMA_ATRIBUTO s ON s.id_mecanica=o.id_mecanica WHERE o.{owner_pk}=NEW.{owner_fk} AND s.id_mecanica_sistema_atributo=NEW.id_mecanica_sistema_atributo)", 'Valor e proprietario de mecanicas distintas')
        body += '\n' + guard("NEW.estado='conhecido' AND NOT EXISTS (SELECT 1 FROM MECANICA_SISTEMA_ATRIBUTO s JOIN MECANICA_ATRIBUTO a USING(id_mecanica_sistema_atributo) WHERE s.id_mecanica_sistema_atributo=NEW.id_mecanica_sistema_atributo AND a.id_atributo=NEW.id_atributo AND s.aplicabilidade='aplicavel' AND a.aplicabilidade='aplicavel' AND s.valor_minimo IS NOT NULL AND s.valor_maximo_atributo IS NOT NULL AND s.limite_total_status!='nao_verificado' AND NEW." + value + " BETWEEN s.valor_minimo AND s.valor_maximo_atributo)", 'Valor exige aplicabilidade e limites confirmados')
        body += '\n' + guard("NEW.estado='nao_aplicavel' AND NOT EXISTS (SELECT 1 FROM MECANICA_SISTEMA_ATRIBUTO s LEFT JOIN MECANICA_ATRIBUTO a ON a.id_mecanica_sistema_atributo=s.id_mecanica_sistema_atributo AND a.id_atributo=NEW.id_atributo WHERE s.id_mecanica_sistema_atributo=NEW.id_mecanica_sistema_atributo AND (s.aplicabilidade='nao_aplicavel' OR a.aplicabilidade='nao_aplicavel'))", 'Inaplicabilidade deve ser confirmada')
        exclusion = f' AND v.{pk}!=OLD.{pk}' if event=='UPDATE' else ''
        body += '\n' + guard(f"NEW.estado='conhecido' AND NEW.{value} + COALESCE((SELECT sum(v.{value}) FROM {table} v WHERE v.{owner_fk}=NEW.{owner_fk} AND v.id_mecanica_sistema_atributo=NEW.id_mecanica_sistema_atributo AND v.estado='conhecido'{exclusion}),0) > (SELECT valor_maximo_total FROM MECANICA_SISTEMA_ATRIBUTO WHERE id_mecanica_sistema_atributo=NEW.id_mecanica_sistema_atributo AND limite_total_status='confirmado')", 'Soma ultrapassa limite combinado confirmado')
        trigger(table.lower() + '_' + event.lower(), 'BEFORE ' + event, table, body)

for event in ('UPDATE','DELETE'):
    trigger('mecanica_atributo_preservada_' + event.lower(), 'BEFORE ' + event, 'MECANICA_ATRIBUTO', guard("EXISTS (SELECT 1 FROM VALOR_ATRIBUTO_POKEMON WHERE id_mecanica_sistema_atributo=OLD.id_mecanica_sistema_atributo AND id_atributo=OLD.id_atributo) OR EXISTS (SELECT 1 FROM VALOR_PERFIL_ANALISE WHERE id_mecanica_sistema_atributo=OLD.id_mecanica_sistema_atributo AND id_atributo=OLD.id_atributo)", 'Aplicabilidade utilizada: crie nova versao'))

trigger('mecanica_atributo_preservada_replace', 'BEFORE INSERT', 'MECANICA_ATRIBUTO', guard("EXISTS (SELECT 1 FROM MECANICA_ATRIBUTO WHERE id_mecanica_sistema_atributo=NEW.id_mecanica_sistema_atributo AND id_atributo=NEW.id_atributo) AND (EXISTS (SELECT 1 FROM VALOR_ATRIBUTO_POKEMON WHERE id_mecanica_sistema_atributo=NEW.id_mecanica_sistema_atributo AND id_atributo=NEW.id_atributo) OR EXISTS (SELECT 1 FROM VALOR_PERFIL_ANALISE WHERE id_mecanica_sistema_atributo=NEW.id_mecanica_sistema_atributo AND id_atributo=NEW.id_atributo))", 'Aplicabilidade utilizada nao admite substituicao implicita'))

# Semantic identities cannot be repurposed underneath existing observations.
trigger('forma_identidade_preservada', 'BEFORE UPDATE', 'FORMA', guard("(NEW.id_especie IS NOT OLD.id_especie OR NEW.codigo_forma IS NOT OLD.codigo_forma) AND EXISTS (SELECT 1 FROM DADOS_FORMA_JOGO WHERE id_forma=OLD.id_forma)", 'Forma utilizada nao pode mudar de identidade'))
trigger('natureza_efeito_preservado', 'BEFORE UPDATE', 'NATUREZA', guard("(NEW.estado_efeito IS NOT OLD.estado_efeito OR NEW.atributo_aumentado IS NOT OLD.atributo_aumentado OR NEW.atributo_reduzido IS NOT OLD.atributo_reduzido) AND (EXISTS (SELECT 1 FROM POKEMON_COLECAO WHERE id_natureza=OLD.id_natureza) OR EXISTS (SELECT 1 FROM PERFIL_NATUREZA WHERE id_natureza=OLD.id_natureza))", 'Natureza utilizada exige revisao explicita antes de mudar efeito'))
trigger('sistema_codigo_preservado', 'BEFORE UPDATE OF codigo', 'SISTEMA_ATRIBUTO', guard("NEW.codigo IS NOT OLD.codigo AND EXISTS (SELECT 1 FROM MECANICA_SISTEMA_ATRIBUTO WHERE id_sistema_atributo=OLD.id_sistema_atributo)", 'Sistema utilizado nao pode mudar de codigo'))
trigger('atributo_codigo_preservado', 'BEFORE UPDATE OF codigo', 'ATRIBUTO_BATALHA', guard("NEW.codigo IS NOT OLD.codigo AND (EXISTS (SELECT 1 FROM MECANICA_ATRIBUTO WHERE id_atributo=OLD.id_atributo) OR EXISTS (SELECT 1 FROM VALOR_ATRIBUTO_POKEMON WHERE id_atributo=OLD.id_atributo) OR EXISTS (SELECT 1 FROM VALOR_PERFIL_ANALISE WHERE id_atributo=OLD.id_atributo))", 'Atributo utilizado nao pode mudar de codigo'))

# Stable surrogate keys avoid indirect re-identification of children and SQLite REPLACE surprises.
keys = {'USUARIO':'id_usuario','ESPECIE':'id_especie','FORMA':'id_forma','JOGO':'id_jogo','DADOS_FORMA_JOGO':'id_dados_forma','TIPO':'id_tipo','HABILIDADE':'id_habilidade','HABILIDADE_FORMA_JOGO':'id_habilidade_forma','METODO_OBTENCAO':'id_metodo','NATUREZA':'id_natureza','MECANICA_JOGO':'id_mecanica','ATRIBUTO_BATALHA':'id_atributo','SISTEMA_ATRIBUTO':'id_sistema_atributo','MECANICA_SISTEMA_ATRIBUTO':'id_mecanica_sistema_atributo','POKEMON_COLECAO':'id_pokemon_colecao','PERFIL_ANALISE':'id_perfil','REGULAMENTO':'id_regulamento','ELEGIBILIDADE_FORMA_REGULAMENTO':'id_elegibilidade','TRANSFORMACAO_FORMA':'id_transformacao'}
for table, pk in keys.items():
    trigger('identidade_' + table.lower(), 'BEFORE UPDATE OF ' + pk, table, guard(f'NEW.{pk}!=OLD.{pk}', 'Chave de identidade imutavel'))

header = '-- Pokelizer Stage 1 physical model. SQLite >= 3.37 (STRICT).\n-- Generated by backend/tools/build_schema.py; edit source + regenerate.\n-- Empty database only. Existing databases use explicit migrations via Python CLI.\nPRAGMA foreign_keys = ON;\nPRAGMA recursive_triggers = ON;\n'
generated = (header + sql).encode('utf-8')
outputs = [ROOT / 'schema.sql', ROOT / 'migrations' / '001_stage1.sql']
if args.check:
    stale = [str(path) for path in outputs if not path.is_file() or path.read_bytes() != generated]
    if stale:
        raise SystemExit('Generated SQL differs from source: ' + ', '.join(stale))
else:
    for path in outputs:
        path.write_bytes(generated)
