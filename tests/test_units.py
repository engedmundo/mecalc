from mecalc.units import (
    DimensionalityError,
    UndefinedUnitError,
    convert,
    format_quantity,
    is_compatible,
)
from tests.helpers import EngineeringTestCase


class TestConvert(EngineeringTestCase):
    """Conversão de valores entre unidades."""

    def test_converts_simple_and_offset_units(self) -> None:
        """Converte unidades simples (mm para m) e unidades com deslocamento (°C para K).
        O caso da temperatura protege a decisão de criar a quantidade diretamente na
        unidade de origem, que é o que faz °C e °F funcionarem."""
        # Given
        cases = [
            (2500, "mm", "m", 2.5),
            (25, "degC", "K", 298.15),
        ]
        for value, from_unit, to_unit, expected in cases:
            with self.subTest(f"{value} {from_unit} -> {to_unit}"):
                # When
                result = convert(value, from_unit, to_unit)

                # Then
                self.assertClose(result, expected)

    def test_returns_plain_float(self) -> None:
        """O resultado é um float puro, e não uma Quantity do pint, para ser usado
        diretamente nos cálculos."""
        # Given
        value = 1
        from_unit = "m"
        to_unit = "mm"

        # When
        result = convert(value, from_unit, to_unit)

        # Then
        self.assertIs(type(result), float)

    def test_raises_when_units_are_incompatible(self) -> None:
        """Converter entre grandezas diferentes (comprimento para pressão) gera o
        DimensionalityError exportado por mecalc.units, que a interface usa para
        avisar o usuário."""
        # Given
        length_unit = "mm"
        pressure_unit = "Pa"

        # When / Then
        with self.assertRaises(DimensionalityError):
            convert(1, length_unit, pressure_unit)

    def test_raises_when_unit_does_not_exist(self) -> None:
        """Uma unidade inexistente ou digitada errado gera o UndefinedUnitError
        exportado por mecalc.units."""
        # Given
        unknown_unit = "furlongz"

        # When / Then
        with self.assertRaises(UndefinedUnitError):
            convert(1, "mm", unknown_unit)


class TestIsCompatible(EngineeringTestCase):
    """Verificação de compatibilidade entre unidades."""

    def test_identifies_compatible_and_incompatible_units(self) -> None:
        """Reconhece unidades da mesma grandeza (mm e in) e rejeita unidades de
        grandezas diferentes (mm e Pa), devolvendo sempre um bool."""
        # Given
        cases = [
            ("mm", "in", True),
            ("mm", "Pa", False),
        ]
        for unit_a, unit_b, expected in cases:
            with self.subTest(f"{unit_a} x {unit_b}"):
                # When
                result = is_compatible(unit_a, unit_b)

                # Then
                self.assertIs(result, expected)


class TestFormatQuantity(EngineeringTestCase):
    """Formatação de valores com unidade para exibição.

    Estes testes também avisam se uma atualização do pint mudar o formato que o
    usuário vê na interface e no memorial de cálculo.
    """

    def test_formats_as_text_with_conversion(self) -> None:
        """Uma força em N é exibida em kN, com 4 algarismos significativos."""
        # Given
        force_n = 78956.7

        # When
        text = format_quantity(force_n, "N", to_unit="kN")

        # Then
        self.assertEqual(text, "78.96 kN")

    def test_formats_without_conversion(self) -> None:
        """Sem unidade de exibição, o valor é mostrado na própria unidade de entrada."""
        # Given
        length_m = 2.5

        # When
        text = format_quantity(length_m, "m")

        # Then
        self.assertEqual(text, "2.5 m")

    def test_respects_significant_digits(self) -> None:
        """O número de algarismos significativos pode ser escolhido."""
        # Given
        value = 3.14159265

        # When
        text = format_quantity(value, "m", digits=3)

        # Then
        self.assertEqual(text, "3.14 m")

    def test_formats_as_latex(self) -> None:
        """Uma tensão em Pa é exibida em MPa no formato LaTeX, usado no memorial
        de cálculo."""
        # Given
        stress_pa = 2.5e8

        # When
        text = format_quantity(stress_pa, "Pa", to_unit="MPa", latex=True)

        # Then
        self.assertEqual(text, r"250\ \mathrm{MPa}")
