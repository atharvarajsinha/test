"""Simple educational parser that converts token stream into a compact AST.

This parser is intentionally lightweight and line-based for educational use.
It supports the requested subset: declarations/assignments, function defs/calls,
if/else, for/while and print-like statements.
"""
import json
from pathlib import Path


PRINT_TOKENS = {'print', 'println', 'cout'}


def _tokens_by_line(tokens):
    lines = {}
    for t in tokens:
        lines.setdefault(t['line'], []).append(t['value'])
    return [lines[k] for k in sorted(lines)]


def _extract_print_value(line_tokens):
    """Normalize print payload into a language-agnostic expression string."""
    if 'print' in line_tokens:
        # Python style: print ( expr )
        start = line_tokens.index('print')
        if '(' in line_tokens[start:]:
            open_idx = line_tokens.index('(', start)
            close_idx = len(line_tokens) - 1 - line_tokens[::-1].index(')') if ')' in line_tokens[open_idx:] else len(line_tokens)
            expr = line_tokens[open_idx + 1:close_idx]
            return ' '.join(expr).strip()
    if 'println' in line_tokens:
        # Java style: System . out . println ( expr ) ;
        start = line_tokens.index('println')
        if '(' in line_tokens[start:]:
            open_idx = line_tokens.index('(', start)
            close_idx = len(line_tokens) - 1 - line_tokens[::-1].index(')') if ')' in line_tokens[open_idx:] else len(line_tokens)
            expr = line_tokens[open_idx + 1:close_idx]
            return ' '.join(expr).strip()
    if 'cout' in line_tokens:
        # C++ style: cout << expr << endl ;
        start = line_tokens.index('cout')
        rest = line_tokens[start + 1:]
        if '<<' in rest:
            # collect tokens between first << and next << endl / end
            first_shift = start + 1 + rest.index('<<')
            payload = line_tokens[first_shift + 1:]
            if '<<' in payload:
                payload = payload[:payload.index('<<')]
            return ' '.join([t for t in payload if t not in {';', 'endl'}]).strip()
    # fallback - preserve readability
    return ' '.join([t for t in line_tokens if t not in {';'}]).strip()


def parse_tokens_file(tokens_file: Path, ast_output_path: Path):
    token_data = json.loads(tokens_file.read_text(encoding='utf-8'))
    lines = _tokens_by_line(token_data['tokens'])
    body = []

    for line_tokens in lines:
        if not line_tokens:
            continue
        first = line_tokens[0]
        joined = ' '.join(line_tokens)

        if first in {'def', 'void', 'int', 'float', 'double'} and '(' in line_tokens and '{' in line_tokens:
            name = line_tokens[line_tokens.index('(') - 1]
            params = []
            if ')' in line_tokens:
                param_tokens = line_tokens[line_tokens.index('(') + 1:line_tokens.index(')')]
                params = [p for p in param_tokens if p not in {',', 'int', 'float', 'double', 'String', 'string'}]
            body.append({'type': 'Function', 'name': name, 'params': params, 'body': []})
        elif first == 'if':
            cond = joined[joined.find('(') + 1:joined.rfind(')')] if '(' in joined else joined[2:]
            body.append({'type': 'If', 'condition': cond.strip(), 'then': [], 'else': []})
        elif first == 'else':
            body.append({'type': 'Else'})
        elif first == 'for':
            body.append({'type': 'For', 'header': joined})
        elif first == 'while':
            cond = joined[joined.find('(') + 1:joined.rfind(')')] if '(' in joined else joined[5:]
            body.append({'type': 'While', 'condition': cond.strip(), 'body': []})
        elif any(tok in line_tokens for tok in PRINT_TOKENS):
            body.append({'type': 'Print', 'value': _extract_print_value(line_tokens)})
        elif '=' in line_tokens:
            idx = line_tokens.index('=')
            body.append({'type': 'Assignment', 'target': line_tokens[idx - 1], 'value': ' '.join(line_tokens[idx + 1:]).strip(';')})
        elif '(' in line_tokens and ')' in line_tokens:
            name = line_tokens[0]
            args = [x for x in line_tokens[1:] if x not in {'(', ')', ',', ';'}]
            body.append({'type': 'Call', 'name': name, 'args': args})

    ast = {'type': 'Program', 'body': body}
    ast_output_path.write_text(json.dumps(ast, indent=2), encoding='utf-8')
    return str(ast_output_path)
