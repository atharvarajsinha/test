# Educational Source-to-Source Compiler Backend

This repository provides a Django + PostgreSQL backend that demonstrates a compiler pipeline:

`Lexer -> Parser -> AST -> IR -> Code Generator`

## Features
- REST API for compile, run, and history endpoints.
- Language-aware lexers/parsers for Python, Java, and C++.
- Shared IR schema and IR-based code generation.
- Secure(ish) execution in temporary directories with timeout.
- PostgreSQL persistence of all pipeline outputs.

## Setup
1. Create virtualenv and install dependencies:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Configure local PostgreSQL (defaults already in settings):
   - DB_NAME=compiler_db
   - DB_USER=postgres
   - DB_PASSWORD=postgres
   - DB_HOST=localhost
   - DB_PORT=5432
3. Run migrations:
   ```bash
   python manage.py migrate
   ```
4. Start API server:
   ```bash
   python manage.py runserver
   ```

## API
- `POST /api/compile/`
- `POST /api/run/`
- `GET /api/history/`

Example compile payload:
```json
{
  "source_language": "python",
  "target_language": "java",
  "code": "x = 1\nprint(x)"
}
```

## Project Structure
- `lexer/`: language-specific lexical analyzers.
- `parser/`: language-specific parsers.
- `ast/`: AST normalization.
- `ir/`: shared IR generator + schema.
- `codegen/`: IR to Python/Java/C++ generators.
- `runner/`: execution wrappers for Python/Java/C++.
- `compiler_api/`: DRF endpoints, DB models, orchestration pipeline.
