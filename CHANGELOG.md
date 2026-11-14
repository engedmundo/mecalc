# Changelog

Todas as mudanças relevantes do projeto são registradas neste arquivo.

O formato segue o [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/) e o projeto adota o [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [Não publicado]

### Adicionado

- Estrutura inicial do projeto e documentação (visão geral e arquitetura).
- `pyproject.toml` com dependências, extras (`ui`, `postgres`) e configuração de ruff, mypy e pytest.
- Licença MIT.
- Pre-commit com ruff, mypy e verificações básicas.
- Integração contínua no GitHub Actions (lint, formatação, tipos e testes).
- Configuração centralizada com pydantic-settings (`MECALC_DATABASE_URL`, `MECALC_HISTORY_BACKEND`).
