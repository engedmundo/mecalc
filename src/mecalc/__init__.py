"""mecalc: calculadora técnica de engenharia mecânica."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("mecalc")
except PackageNotFoundError:  # executando sem o pacote instalado
    __version__ = "0.0.0"

__all__ = ["__version__"]
