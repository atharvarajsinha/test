"""AST builder placeholder.
The language specific parsers already emit canonical AST; this module validates shape.
"""
import json
from pathlib import Path


def normalize_ast(ast_path: Path) -> dict:
    ast = json.loads(ast_path.read_text(encoding='utf-8'))
    if ast.get('type') != 'Program':
        raise ValueError('Invalid AST root')
    return ast
