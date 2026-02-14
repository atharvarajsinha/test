from pathlib import Path
from lexer.common import tokenize_source, write_tokens


def lex_cpp(source_code: str, output_path: Path):
    return write_tokens(tokenize_source(source_code, 'cpp'), output_path)
