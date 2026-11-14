"""Check the reviewed UML class inventory/members against Python AST and export hashes.

Run --record only after regenerating AND visually reviewing both exports.
It records reviewed bytes, not a claim of automatic layout quality validation.
"""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent


def check_source():
    source = (HERE / "classes.puml").read_text()
    python_classes = {}
    for filename in ("models.py", "dao.py", "services.py"):
        tree = ast.parse((ROOT / "backend" / "pokeanalyzer" / filename).read_text())
        python_classes.update({node.name: node for node in tree.body if isinstance(node, ast.ClassDef)})
    blocks = dict(re.findall(r"class (\w+)[^\n{]*\{\n(.*?)\n\}", source, re.S))
    planned = {name for name in blocks if re.search(r"class " + re.escape(name) + r" <<planned>>", source)}
    assert set(blocks) - planned == set(python_classes), "UML/Python class inventory differs"
    for name, node in python_classes.items():
        displayed_methods = set(re.findall(r"^[ \t]*[+-](\w+)\(", blocks[name], re.M))
        implemented_methods = {member.name for member in node.body if isinstance(member, ast.FunctionDef) and member.name != "__init__"}
        assert displayed_methods == implemented_methods, f"UML methods differ: {name}"
        fields = {member.target.id for member in node.body if isinstance(member, ast.AnnAssign) and isinstance(member.target, ast.Name)}
        displayed_fields = set(re.findall(r"^[ \t]*[+-](\w+):", blocks[name], re.M))
        if fields:
            assert displayed_fields <= fields, f"UML field absent from Python: {name}"
        else:
            instance_fields = {member.targets[0].attr for member in ast.walk(node)
                               if isinstance(member, ast.Assign) and isinstance(member.targets[0], ast.Attribute)
                               and isinstance(member.targets[0].value, ast.Name) and member.targets[0].value.id == "self"}
            assert displayed_fields <= instance_fields, f"UML injected dependency absent: {name}"
    for filename in ("api.py",):
        tree = ast.parse((ROOT / "backend" / "pokeanalyzer" / filename).read_text())
        for node in ast.walk(tree):
            assert not (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                        and node.func.attr in {"execute", "executemany", "executescript"}), "SQL leaked into HTTP route module"
    return len(python_classes)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--record", action="store_true")
    args = parser.parse_args()
    count = check_source()
    hashes = {name: hashlib.sha256((HERE / name).read_bytes()).hexdigest()
              for name in ("classes.puml", "classes.svg", "classes.png")}
    manifest = HERE / "reviewed_exports.json"
    if args.record:
        manifest.write_text(json.dumps(hashes, indent=2) + "\n")
    else:
        assert json.loads(manifest.read_text()) == hashes, "UML/export bytes changed after recorded review; regenerate and review"
    print(f"UML: {count} implemented classes and their methods agree with Python; exports match reviewed hashes.")


if __name__ == "__main__":
    main()
