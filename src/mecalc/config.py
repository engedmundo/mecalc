"""Configuração centralizada do mecalc.

Todas as variáveis de ambiente usam o prefixo ``MECALC_`` e também podem
ser definidas em um arquivo ``.env`` na raiz do projeto.

Exemplo::

    MECALC_DATABASE_URL=postgresql+psycopg://user:senha@localhost/mecalc
    MECALC_HISTORY_BACKEND=sql
"""

from typing import Literal

from platformdirs import user_data_path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

HistoryBackend = Literal["memory", "sql"]


def _default_database_url() -> str:
    """SQLite na pasta de dados do usuário (ex.: ~/.local/share/mecalc no Linux).

    A pasta não é criada aqui; isso fica a cargo de quem abrir a conexão.
    """
    db_path = user_data_path("mecalc", appauthor=False) / "mecalc.db"
    return f"sqlite:///{db_path}"


class Settings(BaseSettings):
    """Configurações do mecalc, lidas de variáveis de ambiente e do ``.env``."""

    model_config = SettingsConfigDict(
        env_prefix="MECALC_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: str = Field(
        default_factory=_default_database_url,
        description="URL de conexão do SQLAlchemy (SQLite por padrão).",
    )
    history_backend: HistoryBackend = Field(
        default="memory",
        description="Onde guardar o histórico: 'memory' (sessão) ou 'sql' (banco).",
    )
