"""Regenerate the class inventory from AST; dependency edges are reviewed explicitly below."""
import ast
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
lines=['@startuml','set namespaceSeparator none','!pragma layout smetana','skinparam backgroundColor white','skinparam shadowing false',
       'skinparam dpi 120','skinparam packageStyle rectangle','skinparam classAttributeIconSize 0',
       'skinparam defaultFontName SansSerif','skinparam defaultFontSize 13','skinparam nodesep 45',
       'skinparam ranksep 60','title Pokelizer — classes Python implementadas — Etapa 2']
for module in ['models','dao','services']:
    lines.append(f'package "{module}.py" {{')
    tree=ast.parse((ROOT/f'backend/pokeanalyzer/{module}.py').read_text())
    for cls in (n for n in tree.body if isinstance(n,ast.ClassDef)):
        lines.append(f'class {cls.name} {{')
        for member in cls.body:
            if isinstance(member,ast.AnnAssign) and isinstance(member.target,ast.Name):
                if member.target.id.startswith('id_') or member.target.id in ['valores','naturezas','habilidades','fichas','codigo_forma']:
                    lines.append(f'  +{member.target.id}: {ast.unparse(member.annotation)}')
            elif isinstance(member,ast.FunctionDef) and member.name!='__init__':
                lines.append(f'  {"-" if member.name.startswith("_") else "+"}{member.name}()')
        lines.append('}')
    lines.append('}')
for a,b in [('AuthService','UsuarioDAO'),('ColecaoService','ColecaoDAO'),('ColecaoService','ValorDAO'),
            ('PerfilService','PerfilDAO'),('PerfilService','ValorDAO'),('ComparacaoService','ColecaoDAO'),
            ('ComparacaoService','PerfilDAO'),('ComparacaoService','ContextoDAO'),('ComparacaoService','RegulamentoDAO'),
            ('UsuarioDAO','Usuario'),('ColecaoDAO','PokemonColecao'),('PerfilDAO','PerfilAnalise'),('PokemonDAO','PokemonCatalogo')]:
    lines.append(f'{a} ..> {b}')
lines += ['note "api.py: Blueprint, autenticação e CSRF\\ndb.py: conexão, migrações e transações\\ncatalog_data.py: snapshot, carga e cobertura\\nFunções de módulo, sem classes artificiais por tabela." as Infra','@enduml']
(HERE/'classes.puml').write_text('\n'.join(lines)+'\n')
