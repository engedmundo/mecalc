"""Utilitários compartilhados pelos testes."""

import math
import unittest


class EngineeringTestCase(unittest.TestCase):
    """TestCase com asserções adequadas a valores de engenharia."""

    def assertClose(self, actual: float, expected: float, rel: float = 1e-6) -> None:  # noqa: N802
        """Compara dois valores por tolerância relativa."""
        is_close = math.isclose(actual, expected, rel_tol=rel)
        failure_message = f"{actual!r} != {expected!r} (tolerância relativa {rel})"

        self.assertTrue(is_close, failure_message)
