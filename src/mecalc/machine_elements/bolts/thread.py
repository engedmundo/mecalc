"""Geometria de roscas métricas ISO (perfil de 60°).

Todas as grandezas estão em unidades do SI: comprimentos em metros e áreas
em metros quadrados.

Referências:
    BUDYNAS, R. G. Elementos de máquinas de Shigley. 10. ed. 2026.
        Capítulo 8, Tabela 8-1 e nota da tabela (equações de dp, dr e At).
"""

import math
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, computed_field, model_validator

# Coeficientes multiplicados pelo passo (Budynas, nota da Tabela 8-1):
#   dp = d - 0,649519·p
#   dr = d - 1,226869·p
PITCH_DIAMETER_FACTOR = 0.649519
MINOR_DIAMETER_FACTOR = 1.226869


def _circle_area(diameter: float) -> float:
    """Área de um círculo a partir do diâmetro: A = π · d² / 4."""
    return math.pi / 4 * diameter**2


class MetricThread(BaseModel):
    """Rosca métrica ISO, definida pelo diâmetro externo, pelo passo e pelo
    número de entradas.

    As grandezas derivadas (avanço, diâmetros e áreas) são propriedades
    calculadas a partir das entradas e também aparecem na serialização do
    modelo (``model_dump``), o que permite guardar o cálculo no histórico.
    """

    model_config = ConfigDict(
        frozen=True,
        validate_by_name=True,
        validate_by_alias=True,
    )

    # --- Entradas -------------------------------------------------------------

    external_diameter: float = Field(
        gt=0,
        alias="d",
        title="Diâmetro externo",
        description="Diâmetro nominal (externo) da rosca.",
        json_schema_extra={"unit": "m", "display_unit": "mm"},
    )
    pitch: float = Field(
        gt=0,
        alias="p",
        title="Passo",
        description="Distância axial entre dois filetes adjacentes.",
        json_schema_extra={"unit": "m", "display_unit": "mm"},
    )
    number_of_starts: int = Field(
        default=1,
        ge=1,
        alias="ne",
        title="Número de entradas",
        description="Número de filetes independentes da rosca (1 para rosca simples).",
        json_schema_extra={"unit": "", "display_unit": ""},
    )

    # --- Validação ------------------------------------------------------------

    @model_validator(mode="after")
    def _validate_minor_diameter_is_positive(self) -> Self:
        """Recusa combinações de diâmetro e passo que deixariam o diâmetro menor
        nulo ou negativo (em geral, um erro de unidade na entrada)."""
        if self.minor_diameter <= 0:
            message = (
                f"Passo de {self.pitch} m é grande demais para o diâmetro externo "
                f"de {self.external_diameter} m: o diâmetro menor seria nulo ou negativo."
            )
            raise ValueError(message)

        return self

    # --- Grandezas derivadas --------------------------------------------------

    @computed_field
    @property
    def lead(self) -> float:
        """Avanço L = nₑ · p [m]: distância axial percorrida em uma volta."""
        return self.number_of_starts * self.pitch

    @computed_field
    @property
    def pitch_diameter(self) -> float:
        """Diâmetro primitivo dp = d - 0,649519 · p [m]."""
        reduction = PITCH_DIAMETER_FACTOR * self.pitch
        return self.external_diameter - reduction

    @computed_field
    @property
    def minor_diameter(self) -> float:
        """Diâmetro menor (raiz) dr = d - 1,226869 · p [m]."""
        reduction = MINOR_DIAMETER_FACTOR * self.pitch
        return self.external_diameter - reduction

    @computed_field
    @property
    def tensile_stress_area(self) -> float:
        """Área sob tração At = π/4 · ((dp + dr) / 2)² [m²].

        Ensaios mostram que a resistência à tração de uma barra rosqueada
        corresponde à média entre os diâmetros primitivo e menor.
        """
        mean_diameter = (self.pitch_diameter + self.minor_diameter) / 2
        return _circle_area(mean_diameter)

    @computed_field
    @property
    def minor_diameter_area(self) -> float:
        """Área do diâmetro menor Ar = π · dr² / 4 [m²]"""
        return _circle_area(self.minor_diameter)

    @computed_field
    @property
    def external_diameter_area(self) -> float:
        """Área do diâmetro externo Ad = π · d² / 4 [m²]"""
        return _circle_area(self.external_diameter)
