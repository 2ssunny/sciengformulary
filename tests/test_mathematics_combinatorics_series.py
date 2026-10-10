"""Tests for the combinatorics and series formulas in the mathematics domain.

Extra numeric values come from the independent oracle (brute-force enumeration, exact integer
and Fraction arithmetic, mpmath), never from the evaluators under test.
"""

import math
import unittest

from sciengformulary.catalog.mathematics.arithmetic_series_sum_first_integers import (
    arithmetic_series_sum_first_integers,
)
from sciengformulary.catalog.mathematics.binomial_coefficient import binomial_coefficient
from sciengformulary.catalog.mathematics.catalan_number import catalan_number
from sciengformulary.catalog.mathematics.combinations_with_repetition import (
    combinations_with_repetition,
)
from sciengformulary.catalog.mathematics.derangement_count import derangement_count
from sciengformulary.catalog.mathematics.fibonacci_binet import fibonacci_binet
from sciengformulary.catalog.mathematics.finite_geometric_series_sum import (
    finite_geometric_series_sum,
)
from sciengformulary.catalog.mathematics.infinite_geometric_series_sum import (
    infinite_geometric_series_sum,
)
from sciengformulary.catalog.mathematics.k_permutations import k_permutations


class IntegerInputMixin:
    """Shared checks for a single whole-number input named ``n``."""

    formula = None
    minimum = 0

    def test_rejects_below_minimum(self):
        with self.assertRaises(ValueError):
            self.formula.evaluate(n=self.minimum - 1)

    def test_rejects_non_integer(self):
        with self.assertRaises(ValueError):
            self.formula.evaluate(n=self.minimum + 2.5)

    def test_rejects_bool_and_non_finite(self):
        for value in (True, math.nan, math.inf, "3"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                self.formula.evaluate(n=value)


class PairCountMixin:
    """Shared domain checks for counts with inputs ``n`` and ``k``."""

    formula = None

    def test_rejects_negative_k(self):
        with self.assertRaises(ValueError):
            self.formula.evaluate(n=5, k=-1)

    def test_rejects_non_integer_inputs(self):
        with self.assertRaises(ValueError):
            self.formula.evaluate(n=5.5, k=2)
        with self.assertRaises(ValueError):
            self.formula.evaluate(n=5, k=1.5)

    def test_rejects_bool_and_non_finite(self):
        for value in (True, math.nan, math.inf):
            with self.subTest(value=value), self.assertRaises(ValueError):
                self.formula.evaluate(n=value, k=1)
            with self.subTest(value=value), self.assertRaises(ValueError):
                self.formula.evaluate(n=5, k=value)


class BinomialCoefficientTest(PairCountMixin, unittest.TestCase):
    formula = binomial_coefficient

    def test_constructed(self):
        self.assertEqual(binomial_coefficient.id, "mathematics.binomial_coefficient")

    def test_rejects_negative_n(self):
        with self.assertRaises(ValueError):
            binomial_coefficient.evaluate(n=-1, k=0)

    def test_rejects_k_above_n(self):
        with self.assertRaises(ValueError):
            binomial_coefficient.evaluate(n=3, k=4)

    def test_oracle_values(self):
        # Brute-force subset counts from the oracle.
        self.assertEqual(binomial_coefficient.evaluate(n=15, k=8), 6435)
        self.assertEqual(binomial_coefficient.evaluate(n=10, k=7), 120)

    def test_integral_float_accepted_and_result_exact_int(self):
        result = binomial_coefficient.evaluate(n=10.0, k=3.0)
        self.assertIsInstance(result, int)
        self.assertEqual(result, 120)


class KPermutationsTest(PairCountMixin, unittest.TestCase):
    formula = k_permutations

    def test_constructed(self):
        self.assertEqual(k_permutations.id, "mathematics.k_permutations")

    def test_rejects_negative_n(self):
        with self.assertRaises(ValueError):
            k_permutations.evaluate(n=-1, k=0)

    def test_rejects_k_above_n(self):
        with self.assertRaises(ValueError):
            k_permutations.evaluate(n=3, k=4)

    def test_oracle_values(self):
        self.assertEqual(k_permutations.evaluate(n=4, k=1), 4)

    def test_result_is_exact_int(self):
        self.assertIsInstance(k_permutations.evaluate(n=10, k=3), int)


class CombinationsWithRepetitionTest(PairCountMixin, unittest.TestCase):
    formula = combinations_with_repetition

    def test_constructed(self):
        self.assertEqual(
            combinations_with_repetition.id, "mathematics.combinations_with_repetition"
        )

    def test_rejects_zero_types(self):
        with self.assertRaises(ValueError):
            combinations_with_repetition.evaluate(n=0, k=0)
        with self.assertRaises(ValueError):
            combinations_with_repetition.evaluate(n=0, k=3)

    def test_oracle_values(self):
        self.assertEqual(combinations_with_repetition.evaluate(n=2, k=2), 3)
        self.assertEqual(combinations_with_repetition.evaluate(n=1, k=0), 1)

    def test_k_may_exceed_n(self):
        # Oracle: brute force M(1, 7) = 1; any k >= 0 is allowed.
        self.assertEqual(combinations_with_repetition.evaluate(n=1, k=7), 1)


class CatalanNumberTest(IntegerInputMixin, unittest.TestCase):
    formula = catalan_number

    def test_constructed(self):
        self.assertEqual(catalan_number.id, "mathematics.catalan_number")

    def test_oracle_values(self):
        # Tree enumeration, Dyck words and Segner recurrence agree on 42.
        self.assertEqual(catalan_number.evaluate(n=5), 42)

    def test_result_is_exact_int(self):
        self.assertIsInstance(catalan_number.evaluate(n=15), int)


class DerangementCountTest(IntegerInputMixin, unittest.TestCase):
    formula = derangement_count

    def test_constructed(self):
        self.assertEqual(derangement_count.id, "mathematics.derangement_count")

    def test_oracle_values(self):
        # Brute-force counts of fixed-point-free permutations.
        self.assertEqual(derangement_count.evaluate(n=2), 1)
        self.assertEqual(derangement_count.evaluate(n=5), 44)
        self.assertEqual(derangement_count.evaluate(n=8), 14833)

    def test_exact_integer_for_large_n(self):
        result = derangement_count.evaluate(n=20)
        self.assertIsInstance(result, int)
        self.assertEqual(result, 895014631192902121)


class FibonacciBinetTest(IntegerInputMixin, unittest.TestCase):
    formula = fibonacci_binet

    def test_constructed(self):
        self.assertEqual(fibonacci_binet.id, "mathematics.fibonacci_binet")

    def test_rejects_index_above_float_range(self):
        with self.assertRaises(ValueError):
            fibonacci_binet.evaluate(n=1475)

    def test_largest_index_is_finite(self):
        self.assertTrue(math.isfinite(fibonacci_binet.evaluate(n=1474)))

    def test_oracle_values(self):
        # Exact integer recurrence: F_2 = 1.
        self.assertTrue(math.isclose(fibonacci_binet.evaluate(n=2), 1, rel_tol=1e-12))

    def test_returns_unrounded_float(self):
        result = fibonacci_binet.evaluate(n=30)
        self.assertIsInstance(result, float)
        # Exact F_30 = 832040 from the oracle; the float result is close but need not be exact.
        self.assertTrue(math.isclose(result, 832040, rel_tol=1e-12))


class ArithmeticSeriesSumTest(IntegerInputMixin, unittest.TestCase):
    formula = arithmetic_series_sum_first_integers

    def test_constructed(self):
        self.assertEqual(
            arithmetic_series_sum_first_integers.id,
            "mathematics.arithmetic_series_sum_first_integers",
        )

    def test_empty_sum(self):
        self.assertEqual(arithmetic_series_sum_first_integers.evaluate(n=0), 0)

    def test_oracle_values(self):
        self.assertEqual(arithmetic_series_sum_first_integers.evaluate(n=4), 10)


class FiniteGeometricSeriesSumTest(unittest.TestCase):
    def test_constructed(self):
        self.assertEqual(finite_geometric_series_sum.id, "mathematics.finite_geometric_series_sum")

    def test_rejects_ratio_one(self):
        with self.assertRaises(ValueError):
            finite_geometric_series_sum.evaluate(x=1.0, n=5)
        with self.assertRaises(ValueError):
            finite_geometric_series_sum.evaluate(x=1, n=5)

    def test_rejects_non_finite_ratio(self):
        for value in (math.nan, math.inf, True):
            with self.subTest(value=value), self.assertRaises(ValueError):
                finite_geometric_series_sum.evaluate(x=value, n=3)

    def test_rejects_negative_n(self):
        with self.assertRaises(ValueError):
            finite_geometric_series_sum.evaluate(x=2.0, n=-1)

    def test_rejects_non_integer_n(self):
        with self.assertRaises(ValueError):
            finite_geometric_series_sum.evaluate(x=2.0, n=2.5)

    def test_rejects_overflow(self):
        # x^n itself overflows.
        with self.assertRaises(ValueError):
            finite_geometric_series_sum.evaluate(x=10.0, n=400)
        # x^n fits, but dividing by x - 1 = 0.5 overflows.
        with self.assertRaises(ValueError):
            finite_geometric_series_sum.evaluate(x=1.5, n=1750)

    def test_oracle_values(self):
        # Exact Fraction direct sum: a single term equals 1.
        self.assertTrue(
            math.isclose(finite_geometric_series_sum.evaluate(x=1.5, n=1), 1.0, rel_tol=1e-12)
        )

    def test_empty_sum(self):
        self.assertEqual(finite_geometric_series_sum.evaluate(x=3.0, n=0), 0.0)


class InfiniteGeometricSeriesSumTest(unittest.TestCase):
    def test_constructed(self):
        self.assertEqual(
            infinite_geometric_series_sum.id, "mathematics.infinite_geometric_series_sum"
        )

    def test_rejects_divergent_ratios(self):
        for value in (1.0, -1.0, 1.5, -2.0):
            with self.subTest(value=value), self.assertRaises(ValueError):
                infinite_geometric_series_sum.evaluate(r=value)

    def test_rejects_non_finite(self):
        for value in (math.nan, math.inf, -math.inf, True):
            with self.subTest(value=value), self.assertRaises(ValueError):
                infinite_geometric_series_sum.evaluate(r=value)

    def test_oracle_values(self):
        # Exact Fraction 4/3, matched by 60-digit mpmath summation.
        self.assertTrue(
            math.isclose(
                infinite_geometric_series_sum.evaluate(r=0.25), 1.3333333333333333, rel_tol=1e-12
            )
        )


if __name__ == "__main__":
    unittest.main()
