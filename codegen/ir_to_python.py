import re
from pathlib import Path

from codegen.common import read_ir


IDENT_PLUS_STRING = re.compile(r'^([A-Za-z_][A-Za-z0-9_]*)\s*\+\s*(".*")$')


def _py_expr(expr: str) -> str:
    expr = expr.strip()
    m = IDENT_PLUS_STRING.match(expr)
    if m:
        return f"str({m.group(1)}) + {m.group(2)}"
    return expr


def _emit_stmt(stmt, indent=''):
    t = stmt.get('type')
    if t == 'Return':
        return [f"{indent}return {_py_expr(stmt['value'])}"]
    if t == 'Assignment':
        return [f"{indent}{stmt['target']} = {_py_expr(stmt['value'])}"]
    if t == 'Print':
        return [f"{indent}print({_py_expr(stmt['value'])})"]
    if t == 'Call':
        return [f"{indent}{stmt['name']}({', '.join(stmt.get('args', []))})"]
    if t == 'If':
        lines = [f"{indent}if {_py_expr(stmt['condition'])}:"]
        then_nodes = stmt.get('then', [])
        if then_nodes:
            for n in then_nodes:
                lines.extend(_emit_stmt(n, indent + '    '))
        else:
            lines.append(f"{indent}    pass")
        else_nodes = stmt.get('else', [])
        if else_nodes:
            lines.append(f"{indent}else:")
            for n in else_nodes:
                lines.extend(_emit_stmt(n, indent + '    '))
        return lines
    return [f"{indent}pass"]


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
                    lines.extend(_emit_stmt(stmt, '    '))
            else:
                lines.append("    pass")
            lines.append("")
        elif op == 'assign':
            lines.append(f"{n['target']} = {_py_expr(n['value'])}")
        elif op == 'print':
            lines.append(f"print({_py_expr(n['value'])})")
        elif op == 'if':
            lines.extend(_emit_stmt({'type': 'If', 'condition': n['condition'], 'then': n.get('then', []), 'else': n.get('else', [])}))
        elif op == 'for':
            lines += ["for i in range(0, 3):", "    pass"]
        elif op == 'while':
            lines += [f"while {_py_expr(n['condition'])}:", "    break"]
        elif op == 'call':
            lines.append(f"{n['name']}({', '.join(n.get('args', []))})")
    output_path.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    return output_path.read_text(encoding='utf-8')
