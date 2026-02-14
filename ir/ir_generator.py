import json
from pathlib import Path


def ast_to_ir(ast_path: Path, ir_output_path: Path):
    ast = json.loads(ast_path.read_text(encoding='utf-8'))
    ir_body = []
    for node in ast.get('body', []):
        ntype = node.get('type')
        if ntype == 'Function':
            ir_body.append({'op': 'function', 'name': node['name'], 'params': node.get('params', []), 'body': node.get('body', [])})
        elif ntype == 'Assignment':
            ir_body.append({'op': 'assign', 'target': node['target'], 'value': node['value']})
        elif ntype == 'Print':
            ir_body.append({'op': 'print', 'value': node['value']})
        elif ntype == 'If':
            ir_body.append({'op': 'if', 'condition': node['condition'], 'then': node.get('then', []), 'else': node.get('else', [])})
        elif ntype == 'For':
            ir_body.append({'op': 'for', 'header': node.get('header', '')})
        elif ntype == 'While':
            ir_body.append({'op': 'while', 'condition': node['condition'], 'body': node.get('body', [])})
        elif ntype == 'Call':
            ir_body.append({'op': 'call', 'name': node['name'], 'args': node.get('args', [])})
        elif ntype == 'Return':
            ir_body.append({'op': 'return', 'value': node['value']})

    ir = {'type': 'program', 'body': ir_body}
    ir_output_path.write_text(json.dumps(ir, indent=2), encoding='utf-8')
    return str(ir_output_path)
