import math

from pydantic import ValidationError

from mecalc.machine_elements.bolts import MetricThread
from tests.helpers import EngineeringTestCase

MM = 1e-3  # metro por milímetro
MM2 = 1e-6  # metro quadrado por milímetro quadrado


class TestMetricThreadGeometry(EngineeringTestCase):
    """Geometria de roscas métricas ISO."""

    def test_tensile_stress_area_matches_standard_table(self) -> None:
        """A área sob tração bate com os valores tabelados para roscas de passo
        grosso e fino (Budynas, Tabela 8-1). A tolerância de 0,5% cobre o
        arredondamento da tabela, que publica 3 algarismos significativos."""
        # Given
        cases = [
            # (d [mm], p [mm], At tabelada [mm²])
            (8, 1.25, 36.6),
            (10, 1.5, 58.0),
            (12, 1.75, 84.3),
            (16, 2.0, 157.0),
            (20, 2.5, 245.0),
            (10, 1.25, 61.2),
            (12, 1.25, 92.1),
        ]
        for diameter_mm, pitch_mm, expected_area_mm2 in cases:
            with self.subTest(f"M{diameter_mm}x{pitch_mm}"):
                thread = MetricThread(
                    d=diameter_mm * MM,
                    p=pitch_mm * MM,
                )

                # When
                area = thread.tensile_stress_area

                # Then
                self.assertClose(area, expected_area_mm2 * MM2, rel=5e-3)

    def test_diameters_of_m10_coarse_thread(self) -> None:
        """Para uma M10x1,5, os diâmetros primitivo e menor seguem as fórmulas
        da nota da Tabela 8-1 do Budynas: dp = d - 0,649519·p e dr = d - 1,226869·p."""
        # Given
        thread = MetricThread(d=10 * MM, p=1.5 * MM)

        # When
        pitch_diameter = thread.pitch_diameter
        minor_diameter = thread.minor_diameter

        # Then
        self.assertClose(pitch_diameter, 9.026 * MM, rel=1e-4)
        self.assertClose(minor_diameter, 8.160 * MM, rel=1e-4)

    def test_external_diameter_area(self) -> None:
        """A área do diâmetro externo de uma M10 é π·(10 mm)²/4 = 78,54 mm²."""
        # Given
        thread = MetricThread(d=10 * MM, p=1.5 * MM)

        # When
        area = thread.external_diameter_area

        # Then
        self.assertClose(area, 78.54 * MM2, rel=1e-4)

    def test_minor_diameter_area(self) -> None:
        """A área do diâmetro menor de uma M10x1,5 é π·(8,160 mm)²/4 = 52,29 mm²."""
        # Given
        thread = MetricThread(d=10 * MM, p=1.5 * MM)

        # When
        area = thread.minor_diameter_area

        # Then
        self.assertClose(area, 52.29 * MM2, rel=1e-3)


class TestMetricThreadLead(EngineeringTestCase):
    """Avanço de roscas com uma ou mais entradas."""

    def test_lead_equals_pitch_for_single_start(self) -> None:
        """Em uma rosca de entrada simples, o avanço é igual ao passo."""
        # Given
        thread = MetricThread(d=10 * MM, p=1.5 * MM)

        # When
        lead = thread.lead

        # Then
        self.assertClose(lead, 1.5 * MM)

    def test_lead_multiplies_pitch_by_number_of_starts(self) -> None:
        """Em uma rosca de duas entradas, o avanço é o dobro do passo."""
        # Given
        thread = MetricThread(d=10 * MM, p=1.5 * MM, ne=2)

        # When
        lead = thread.lead

        # Then
        self.assertClose(lead, 3.0 * MM)


class TestMetricThreadValidation(EngineeringTestCase):
    """Validação das entradas da rosca."""

    def test_rejects_pitch_too_large_for_diameter(self) -> None:
        """Um passo que deixaria o diâmetro menor nulo ou negativo é recusado."""
        # Given
        diameter = 2 * MM
        pitch = 2 * MM

        # When / Then
        with self.assertRaises(ValidationError):
            MetricThread(d=diameter, p=pitch)


class TestMetricThreadSerialization(EngineeringTestCase):
    """Serialização do modelo, usada para guardar o cálculo no histórico."""

    def test_dump_includes_inputs_and_results(self) -> None:
        """O model_dump traz as entradas e as grandezas calculadas, para que o
        histórico guarde o cálculo completo."""
        # Given
        thread = MetricThread(d=10 * MM, p=1.5 * MM)

        # When
        data = thread.model_dump()

        # Then
        expected_keys = {
            "external_diameter",
            "pitch",
            "number_of_starts",
            "lead",
            "pitch_diameter",
            "minor_diameter",
            "tensile_stress_area",
            "minor_diameter_area",
            "external_diameter_area",
        }
        self.assertEqual(set(data), expected_keys)
        self.assertTrue(math.isclose(data["tensile_stress_area"], thread.tensile_stress_area))
