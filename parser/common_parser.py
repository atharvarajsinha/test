"""Simple educational parser that converts token stream into a compact AST."""
import json
from pathlib import Path

PRINT_TOKENS = {'print', 'println', 'cout'}
TYPE_TOKENS = {'int', 'float', 'double', 'bool', 'char', 'string', 'String', 'void'}
MODIFIERS = {'public', 'private', 'protected', 'static'}
CONTROL = {'if', 'for', 'while', 'switch'}


def _tokens_by_line(tokens):
    lines = {}
    for t in tokens:
        lines.setdefault(t['line'], []).append(t['value'])
    return [lines[k] for k in sorted(lines)]


def _extract_print_value(tokens):
    if 'print' in tokens:
        i = tokens.index('print')
        if '(' in tokens[i:]:
            a = tokens.index('(', i)
            b = len(tokens) - 1 - tokens[::-1].index(')') if ')' in tokens[a:] else len(tokens)
            return ' '.join(tokens[a + 1:b]).strip()
    if 'println' in tokens:
        i = tokens.index('println')
        if '(' in tokens[i:]:
            a = tokens.index('(', i)
            b = len(tokens) - 1 - tokens[::-1].index(')') if ')' in tokens[a:] else len(tokens)
            return ' '.join(tokens[a + 1:b]).strip()
    if 'cout' in tokens:
        i = tokens.index('cout')
        rest = tokens[i + 1:]
        if '<<' in rest:
            first_shift = i + 1 + rest.index('<<')
            payload = tokens[first_shift + 1:]
            if '<<' in payload:
                payload = payload[:payload.index('<<')]
            return ' '.join([t for t in payload if t not in {';', 'endl'}]).strip()
    return ' '.join([t for t in tokens if t != ';']).strip()


def _clean_params(param_tokens):
    return [p for p in param_tokens if p not in {',', '[', ']'} | TYPE_TOKENS | MODIFIERS]


def _parse_stmt(stmt):
    if not stmt:
        return None
    first = stmt[0]
    joined = ' '.join(stmt)
    if first == 'return':
        return {'type': 'Return', 'value': ' '.join([x for x in stmt[1:] if x != ';']).strip()}
    if any(t in stmt for t in PRINT_TOKENS):
        return {'type': 'Print', 'value': _extract_print_value(stmt)}
    if '=' in stmt and first not in {'if', 'for', 'while'}:
        i = stmt.index('=')
        return {'type': 'Assignment', 'target': stmt[i - 1], 'value': ' '.join([x for x in stmt[i + 1:] if x != ';']).strip()}
    if first == 'if':
        cond = joined[joined.find('(') + 1:joined.rfind(')')] if '(' in joined else joined[2:]
        return {'type': 'If', 'condition': cond.strip(), 'then': [], 'else': []}
    if first == 'for':
        return {'type': 'For', 'header': joined}
    if first == 'while':
        cond = joined[joined.find('(') + 1:joined.rfind(')')] if '(' in joined else joined[5:]
        return {'type': 'While', 'condition': cond.strip(), 'body': []}
    if '(' in stmt and ')' in stmt and first not in {'class'} | TYPE_TOKENS | MODIFIERS | CONTROL:
        args = [x for x in stmt[1:] if x not in {'(', ')', ',', ';'}]
        return {'type': 'Call', 'name': first, 'args': args}
    return None


def _parse_python(tokens):
    body = []
    current_fn = None
    for line in _tokens_by_line(tokens):
        if not line:
            continue
        first = line[0]

        if first == 'def' and '(' in line and ')' in line:
            name = line[line.index('(') - 1]
            params = _clean_params(line[line.index('(') + 1:line.index(')')])
            current_fn = {'type': 'Function', 'name': name, 'params': params, 'body': []}
            body.append(current_fn)
            continue

        node = _parse_stmt(line)
        if node and current_fn and node['type'] == 'Return':
            current_fn['body'].append(node)
            continue

        # any non-return line is treated as top-level for this educational grammar
        current_fn = None
        if node:
            body.append(node)

    return {'type': 'Program', 'body': body}


def _split_brace_statements(tokens):
    statements = []
    cur = []
    for t in tokens:
        v = t['value']
        cur.append(v)
        if v in {';', '{', '}'}:
            statements.append(cur)
            cur = []
    if cur:
        statements.append(cur)
    return statements


def _is_fn_header(stmt):
    if '(' not in stmt or ')' not in stmt or '{' not in stmt:
        return False
    if stmt[0] in CONTROL or stmt[0] in {'class'}:
        return False
    name = stmt[stmt.index('(') - 1]
    if name == 'if' or name == 'for' or name == 'while':
        return False
    return stmt[0] in TYPE_TOKENS | MODIFIERS


def _parse_brace_language(tokens):
    body = []
    fn_stack = []
    brace_depth = 0
    for stmt in _split_brace_statements(tokens):
        if not stmt:
            continue
        if stmt == ['{']:
            brace_depth += 1
            continue
        if stmt == ['}']:
            brace_depth = max(0, brace_depth - 1)
            while fn_stack and fn_stack[-1]['depth'] > brace_depth:
                fn_stack.pop()
            continue

        if _is_fn_header(stmt):
            name = stmt[stmt.index('(') - 1]
            params = _clean_params(stmt[stmt.index('(') + 1:stmt.index(')')])
            fn = {'type': 'Function', 'name': name, 'params': params, 'body': []}
            if name != 'main':
                body.append(fn)
            brace_depth += 1
            fn_stack.append({'name': name, 'node': fn, 'depth': brace_depth})
            continue

        node = _parse_stmt(stmt)
        if node:
            if fn_stack and fn_stack[-1]['name'] != 'main':
                fn_stack[-1]['node']['body'].append(node)
            else:
                body.append(node)

    return {'type': 'Program', 'body': body}


def parse_tokens_file(tokens_file: Path, ast_output_path: Path):
    token_data = json.loads(tokens_file.read_text(encoding='utf-8'))
    tokens = token_data['tokens']
    values = {t['value'] for t in tokens}

    if 'public' in values or 'cout' in values or '#include' in values:
        ast = _parse_brace_language(tokens)
    else:
        ast = _parse_python(tokens)

    ast_output_path.write_text(json.dumps(ast, indent=2), encoding='utf-8')
    return str(ast_output_path)
