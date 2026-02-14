from pathlib import Path
from codegen.common import read_ir


def generate_java(ir_path: Path, output_path: Path, class_name: str = 'Main'):
    ir = read_ir(ir_path)
    lines = ["// Generated from shared IR", f"public class {class_name} {{", "  public static void main(String[] args) {"]
    for n in ir['body']:
        op = n['op']
        if op == 'assign':
            lines.append(f"    int {n['target']} = {n['value'].replace(';', '')};")
        elif op == 'print':
            lines.append(f"    System.out.println({n['value']});")
        elif op == 'if':
            lines += [f"    if ({n['condition']}) {{", "    }"]
        elif op == 'for':
            lines += ["    for (int i = 0; i < 3; i++) {", "    }"]
        elif op == 'while':
            lines += [f"    while ({n['condition']}) {{", "      break;", "    }"]
        elif op == 'call':
            lines.append(f"    {n['name']}({', '.join(n.get('args', []))});")
    lines += ["  }", "}"]
    output_path.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    return output_path.read_text(encoding='utf-8')
