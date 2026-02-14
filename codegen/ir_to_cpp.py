from pathlib import Path
from codegen.common import read_ir


def generate_cpp(ir_path: Path, output_path: Path):
    ir = read_ir(ir_path)
    lines = ["// Generated from shared IR", "#include <iostream>", "using namespace std;", "int main() {"]
    for n in ir['body']:
        op = n['op']
        if op == 'assign':
            lines.append(f"  int {n['target']} = {n['value'].replace(';', '')};")
        elif op == 'print':
            lines.append(f"  cout << {n['value']} << endl;")
        elif op == 'if':
            lines += [f"  if ({n['condition']}) {{", "  }"]
        elif op == 'for':
            lines += ["  for (int i = 0; i < 3; i++) {", "  }"]
        elif op == 'while':
            lines += [f"  while ({n['condition']}) {{", "    break;", "  }"]
        elif op == 'call':
            lines.append(f"  {n['name']}({', '.join(n.get('args', []))});")
    lines += ["  return 0;", "}"]
    output_path.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    return output_path.read_text(encoding='utf-8')
