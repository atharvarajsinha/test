"""Shared lexical helper used by per-language lexers."""
import json
import re
from pathlib import Path

KEYWORDS = {
    'python': {'def', 'if', 'else', 'for', 'while', 'return', 'print', 'in', 'range'},
    'java': {'public', 'class', 'static', 'void', 'int', 'double', 'float', 'if', 'else', 'for', 'while', 'return', 'System', 'out', 'println'},
    'cpp': {'#include', 'int', 'float', 'double', 'if', 'else', 'for', 'while', 'return', 'cout', 'std', 'void'},
}

DATATYPES = {'int', 'float', 'double', 'bool', 'char', 'string', 'String', 'void'}
OPERATORS = {'+', '-', '*', '/', '%', '=', '==', '!=', '<', '>', '<=', '>=', '<<', '>>', '&&', '||'}

TOKEN_REGEX = re.compile(
    r'(".*?"|\'.*?\'|==|!=|<=|>=|<<|>>|&&|\|\||[A-Za-z_][A-Za-z0-9_]*|\d+\.\d+|\d+|[{}()\[\],;:+\-*/%<>=])'
)


def classify(token: str, language: str) -> str:
    if token in KEYWORDS[language]:
        return 'KEYWORD'
    if token in DATATYPES:
        return 'DATATYPE'
    if token in OPERATORS:
        return 'OPERATOR'
    if re.fullmatch(r'\d+\.\d+|\d+', token):
        return 'LITERAL'
    if re.fullmatch(r'".*"|\'.*\'', token):
        return 'LITERAL'
    if token in {'(', ')', '{', '}', '[', ']', ',', ';', ':'}:
        return 'PUNCTUATION'
    if token == 'def' or token == 'void':
        return 'FUNCTION_DEF'
    return 'IDENTIFIER'


def tokenize_source(source_code: str, language: str):
    tokens = []
    for line_no, raw_line in enumerate(source_code.splitlines(), start=1):
        for tok in TOKEN_REGEX.findall(raw_line):
            tokens.append({
                'type': classify(tok, language),
                'value': tok,
                'line': line_no,
            })
    return {'tokens': tokens}


def write_tokens(tokens: dict, output_path: Path) -> str:
    output_path.write_text(json.dumps(tokens, indent=2), encoding='utf-8')
    return str(output_path)
