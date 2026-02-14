from pathlib import Path

from codegen.common import read_ir


def _emit_stmt(stmt, indent='  '):
    t = stmt.get('type')
    if t == 'Return':
        return [f"{indent}return {stmt['value']};"]
    if t == 'Assignment':
        return [f"{indent}int {stmt['target']} = {stmt['value']};"]
    if t == 'Print':
        return [f"{indent}cout << {stmt['value']} << endl;"]
    if t == 'Call':
        return [f"{indent}{stmt['name']}({', '.join(stmt.get('args', []))});"]
    if t == 'If':
        lines = [f"{indent}if ({stmt['condition']}) {{"]
        for n in stmt.get('then', []):
            lines.extend(_emit_stmt(n, indent + '  '))
        lines.append(f"{indent}}}")
        if stmt.get('else'):
            lines.append(f"{indent}else {{")
            for n in stmt.get('else', []):
                lines.extend(_emit_stmt(n, indent + '  '))
            lines.append(f"{indent}}}")
        return lines
    return []


def generate_cpp(ir_path: Path, output_path: Path):
    ir = read_ir(ir_path)
    lines = ["// Generated from shared IR", "#include <iostream>", "using namespace std;"]

    for n in ir['body']:
        if n['op'] == 'function':
            params = ', '.join([f"int {p}" for p in n.get('params', [])])
            lines.append(f"int {n['name']}({params}) {{")
            for stmt in n.get('body', []):
                lines.extend(_emit_stmt(stmt, '  '))
            if not n.get('body'):
                lines.append("  return 0;")
            lines.append("}")

    lines.append("int main() {")
    for n in ir['body']:
        op = n['op']
        if op == 'assign':
            lines.append(f"  int {n['target']} = {n['value'].replace(';', '')};")
        elif op == 'print':
            lines.append(f"  cout << {n['value']} << endl;")
        elif op == 'if':
            lines.extend(_emit_stmt({'type': 'If', 'condition': n['condition'], 'then': n.get('then', []), 'else': n.get('else', [])}, '  '))
        elif op == 'for':
            lines += ["  for (int i = 0; i < 3; i++) {", "  }"]
        elif op == 'while':
            lines += [f"  while ({n['condition']}) {{", "    break;", "  }"]
        elif op == 'call':
            lines.append(f"  {n['name']}({', '.join(n.get('args', []))});")
    lines += ["  return 0;", "}"]
    output_path.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    return output_path.read_text(encoding='utf-8')
