"""Unidades físicas do mecalc.

Este módulo contém o **único** registro de unidades do projeto. Todo código que
precisar do pint deve importar daqui, pois quantidades de registros diferentes
não podem ser combinadas.

Convenção do projeto: os cálculos trabalham com ``float`` em unidades do SI.
O pint é usado nas bordas, para converter a entrada do usuário para o SI e o
resultado do SI para a unidade de exibição.

Exemplo::

    >>> convert(2500, "mm", "m")
    2.5
    >>> format_quantity(78956.7, "N", to_unit="kN")
    '78.96 kN'
"""

import pint

ureg = pint.UnitRegistry()
pint.set_application_registry(ureg)

Q_ = ureg.Quantity

DimensionalityError = pint.DimensionalityError
UndefinedUnitError = pint.UndefinedUnitError

__all__ = [
    "Q_",
    "DimensionalityError",
    "UndefinedUnitError",
    "convert",
    "format_quantity",
    "is_compatible",
    "ureg",
]


def convert(value: float, from_unit: str, to_unit: str) -> float:
    """Converte ``value`` de ``from_unit`` para ``to_unit``.

    Funciona também com unidades com deslocamento (°C, °F), pois a quantidade
    é criada diretamente na unidade de origem.

    Raises:
        DimensionalityError: se as unidades não forem da mesma grandeza.
        UndefinedUnitError: se alguma unidade não existir no registro.
    """
    return float(Q_(value, from_unit).to(to_unit).magnitude)


def is_compatible(unit_a: str, unit_b: str) -> bool:
    """Indica se duas unidades medem a mesma grandeza (ex.: ``mm`` e ``in``)."""
    return bool(ureg.Unit(unit_a).is_compatible_with(ureg.Unit(unit_b)))


def format_quantity(
    value: float,
    unit: str,
    *,
    to_unit: str | None = None,
    digits: int = 4,
    latex: bool = False,
) -> str:
    """Formata um valor com unidade para exibição.

    Args:
        value: valor numérico, expresso em ``unit``.
        unit: unidade de ``value``.
        to_unit: unidade de exibição; se omitida, usa ``unit``.
        digits: algarismos significativos.
        latex: se verdadeiro, gera LaTeX (para o memorial e ``st.latex``).
    """
    quantity = Q_(value, unit)
    if to_unit is not None:
        quantity = quantity.to(to_unit)
    spec = f".{digits}g~L" if latex else f".{digits}g~P"
    return format(quantity, spec)
