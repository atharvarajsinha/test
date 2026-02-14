from pathlib import Path
from codegen.common import read_ir


def _emit_fn_stmt(stmt):
    t = stmt.get('type')
    if t == 'Return':
        return [f"    return {stmt['value']}"]
    if t == 'Assignment':
        return [f"    {stmt['target']} = {stmt['value']}"]
    if t == 'Print':
        return [f"    print({stmt['value']})"]
    if t == 'Call':
        return [f"    {stmt['name']}({', '.join(stmt.get('args', []))})"]
    return ["    pass"]


def generate_python(ir_path: Path, output_path: Path):
    ir = read_ir(ir_path)
    lines = ["# Generated from shared IR"]
    for n in ir['body']:
        op = n['op']
        if op == 'function':
            params = ', '.join(n.get('params', []))
            lines.append(f"def {n['name']}({params}):")
            body_nodes = n.get('body', [])
            if body_nodes:
                for stmt in body_nodes:
                    lines.extend(_emit_fn_stmt(stmt))
            else:
                lines.append("    pass")
            lines.append("")
        elif op == 'assign':
            lines.append(f"{n['target']} = {n['value']}")
        elif op == 'print':
            lines.append(f"print({n['value']})")
        elif op == 'if':
            lines += [f"if {n['condition']}:", "    pass"]
        elif op == 'for':
            lines += ["for i in range(0, 3):", "    pass"]
        elif op == 'while':
            lines += [f"while {n['condition']}:", "    break"]
        elif op == 'call':
            lines.append(f"{n['name']}({', '.join(n.get('args', []))})")
    output_path.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    return output_path.read_text(encoding='utf-8')
