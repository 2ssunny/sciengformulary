"""Tests for the special functions and combinatorial counts added in math batch M1b.

Reference values come from 50-digit mpmath (the phase-3 accuracy scripts), exact integer and
Fraction arithmetic, brute-force enumeration, or closed forms evaluated in the test itself;
none is produced by the evaluators under test.
"""

import itertools
import math
import random
import unittest
from fractions import Fraction

from sciengformulary.catalog.mathematics._incomplete_gamma import _zeta
from sciengformulary.catalog.mathematics.bell_number import bell_number
from sciengformulary.catalog.mathematics.double_factorial import double_factorial
from sciengformulary.catalog.mathematics.falling_factorial import falling_factorial
from sciengformulary.catalog.mathematics.gamma_function import gamma_function
from sciengformulary.catalog.mathematics.harmonic_number import harmonic_number
from sciengformulary.catalog.mathematics.hyperbolic_sine import hyperbolic_sine
from sciengformulary.catalog.mathematics.k_permutations import k_permutations
from sciengformulary.catalog.mathematics.lower_incomplete_gamma import lower_incomplete_gamma
from sciengformulary.catalog.mathematics.regularized_incomplete_beta import (
    regularized_incomplete_beta,
)
from sciengformulary.catalog.mathematics.rising_factorial import rising_factorial
from sciengformulary.catalog.mathematics.sinc_unnormalized import sinc_unnormalized
from sciengformulary.catalog.mathematics.stirling_number_first_kind_unsigned import (
    stirling_number_first_kind_unsigned,
)
from sciengformulary.catalog.mathematics.stirling_number_second_kind import (
    stirling_number_second_kind,
)
from sciengformulary.catalog.mathematics.upper_incomplete_gamma import upper_incomplete_gamma
from sciengformulary.core import FormulaSpec

REL = 1e-12


def _close(actual, expected, rel_tol=REL):
    """Relative comparison with no absolute floor (all reference values here are nonzero)."""
    return math.isclose(actual, expected, rel_tol=rel_tol, abs_tol=0.0)


def _set_partition_block_counts(n):
    """Yield the number of blocks of every partition of {0, ..., n - 1} (restricted growth)."""

    def extend(prefix, blocks):
        if len(prefix) == n:
            yield blocks
            return
        for label in range(blocks + 1):
            yield from extend(prefix + [label], max(blocks, label + 1))

    yield from extend([], 0)


def _cycle_count(permutation):
    seen = [False] * len(permutation)
    cycles = 0
    for start in range(len(permutation)):
        if not seen[start]:
            cycles += 1
            position = start
            while not seen[position]:
                seen[position] = True
                position = permutation[position]
    return cycles


class IntegerInputChecks:
    """Domain checks shared by formulas whose whole-number inputs are listed in ``names``."""

    formula = None
    valid = None

    def test_constructed(self):
        self.assertIsInstance(self.formula, FormulaSpec)

    def test_rejects_negative_non_integer_bool_and_non_finite(self):
        for name in self.valid:
            for bad in (-1, 2.5, True, math.nan, math.inf, "3"):
                inputs = dict(self.valid, **{name: bad})
                with self.subTest(name=name, value=bad), self.assertRaises(ValueError):
                    self.formula.evaluate(**inputs)

    def test_accepts_integral_float(self):
        as_float = {name: float(value) for name, value in self.valid.items()}
        self.assertEqual(self.formula.evaluate(**as_float), self.formula.evaluate(**self.valid))


class BellNumberTest(IntegerInputChecks, unittest.TestCase):
    formula = bell_number
    valid = {"n": 6}

    def test_matches_set_partition_enumeration(self):
        # Independent route for the derived (index-shifted) recurrence and the counting meaning.
        for n in range(8):
            with self.subTest(n=n):
                count = sum(1 for _ in _set_partition_block_counts(n))
                self.assertEqual(bell_number.evaluate(n=n), count)

    def test_oracle_values(self):
        # Brute force for n <= 8 and Dobinski's series (50-digit mpmath) for n = 15.
        expected = [1, 1, 2, 5, 15, 52, 203, 877, 4140]
        self.assertEqual([bell_number.evaluate(n=n) for n in range(9)], expected)
        self.assertEqual(bell_number.evaluate(n=15), 1382958545)

    def test_source_form_of_recurrence(self):
        # Mathlib's statement B(n + 1) = sum choose(n, i) B(n - i), with B values from brute force.
        bells = [1, 1, 2, 5, 15, 52, 203, 877, 4140]
        for n in range(8):
            with self.subTest(n=n):
                total = sum(math.comb(n, i) * bells[n - i] for i in range(n + 1))
                self.assertEqual(total, bells[n + 1])


class StirlingSecondKindTest(IntegerInputChecks, unittest.TestCase):
    formula = stirling_number_second_kind
    valid = {"n": 5, "k": 2}

    def test_matches_enumeration(self):
        for n in range(8):
            counts = {}
            for blocks in _set_partition_block_counts(n):
                counts[blocks] = counts.get(blocks, 0) + 1
            for k in range(n + 2):
                with self.subTest(n=n, k=k):
                    self.assertEqual(
                        stirling_number_second_kind.evaluate(n=n, k=k), counts.get(k, 0)
                    )

    def test_matches_inclusion_exclusion(self):
        for n in range(15):
            for k in range(15):
                exact = sum((-1) ** j * math.comb(k, j) * (k - j) ** n for j in range(k + 1))
                with self.subTest(n=n, k=k):
                    self.assertEqual(
                        stirling_number_second_kind.evaluate(n=n, k=k),
                        exact // math.factorial(k),
                    )

    def test_genuine_zeros(self):
        self.assertEqual(stirling_number_second_kind.evaluate(n=4, k=7), 0)
        self.assertEqual(stirling_number_second_kind.evaluate(n=3, k=0), 0)
        self.assertEqual(stirling_number_second_kind.evaluate(n=0, k=0), 1)


class StirlingFirstKindUnsignedTest(IntegerInputChecks, unittest.TestCase):
    formula = stirling_number_first_kind_unsigned
    valid = {"n": 5, "k": 2}

    def test_matches_permutation_cycle_count(self):
        for n in range(7):
            counts = {}
            for permutation in itertools.permutations(range(n)):
                cycles = _cycle_count(permutation)
                counts[cycles] = counts.get(cycles, 0) + 1
            for k in range(n + 2):
                with self.subTest(n=n, k=k):
                    self.assertEqual(
                        stirling_number_first_kind_unsigned.evaluate(n=n, k=k),
                        counts.get(k, 0),
                    )

    def test_matches_rising_factorial_coefficients(self):
        # Coefficients of x (x + 1) ... (x + n - 1), expanded by exact polynomial products.
        coefficients = [1]
        for n in range(1, 11):
            factor_constant = n - 1
            coefficients = [
                factor_constant * (coefficients[j] if j < len(coefficients) else 0)
                + (coefficients[j - 1] if j >= 1 else 0)
                for j in range(len(coefficients) + 1)
            ]
            for k, value in enumerate(coefficients):
                with self.subTest(n=n, k=k):
                    self.assertEqual(stirling_number_first_kind_unsigned.evaluate(n=n, k=k), value)

    def test_k_equals_one_is_factorial(self):
        self.assertEqual(
            stirling_number_first_kind_unsigned.evaluate(n=12, k=1), math.factorial(11)
        )
        self.assertEqual(stirling_number_first_kind_unsigned.evaluate(n=3, k=5), 0)


class DoubleFactorialTest(IntegerInputChecks, unittest.TestCase):
    formula = double_factorial
    valid = {"n": 7}

    def test_even_closed_form(self):
        for m in range(30):
            with self.subTest(m=m):
                self.assertEqual(double_factorial.evaluate(n=2 * m), 2**m * math.factorial(m))

    def test_factorial_identity(self):
        # (n + 1)! = (n + 1)!! * n!! (Mathlib factorial_eq_mul_doubleFactorial).
        for n in range(40):
            with self.subTest(n=n):
                self.assertEqual(
                    double_factorial.evaluate(n=n + 1) * double_factorial.evaluate(n=n),
                    math.factorial(n + 1),
                )


class FallingFactorialTest(unittest.TestCase):
    def test_constructed(self):
        self.assertEqual(falling_factorial.id, "mathematics.falling_factorial")

    def test_domain_rules(self):
        evaluate = falling_factorial.evaluate
        with self.assertRaises(ValueError):
            evaluate(x=math.nan, k=2)
        with self.assertRaises(ValueError):
            evaluate(x=math.inf, k=2)
        with self.assertRaises(ValueError):
            evaluate(x=True, k=2)
        with self.assertRaises(ValueError):
            evaluate(x=2.0, k=-1)
        with self.assertRaises(ValueError):
            evaluate(x=2.0, k=1.5)

    def test_equals_k_permutations_for_whole_x(self):
        for n in range(12):
            for k in range(n + 1):
                with self.subTest(n=n, k=k):
                    self.assertEqual(
                        falling_factorial.evaluate(x=float(n), k=k),
                        float(k_permutations.evaluate(n=n, k=k)),
                    )

    def test_gamma_ratio(self):
        # Independent route: Gamma(x + 1) / Gamma(x - k + 1) for x = 7.3, k = 4.
        expected = math.gamma(8.3) / math.gamma(4.3)
        self.assertTrue(_close(falling_factorial.evaluate(x=7.3, k=4), expected, rel_tol=REL))

    def test_boundaries(self):
        self.assertEqual(falling_factorial.evaluate(x=400.0, k=500), 0.0)
        self.assertEqual(falling_factorial.evaluate(x=-1.5, k=0), 1.0)
        with self.assertRaises(OverflowError):
            falling_factorial.evaluate(x=1e200, k=2)


class RisingFactorialTest(unittest.TestCase):
    def test_constructed(self):
        self.assertEqual(rising_factorial.id, "mathematics.rising_factorial")

    def test_domain_rules(self):
        evaluate = rising_factorial.evaluate
        with self.assertRaises(ValueError):
            evaluate(x=math.nan, k=2)
        with self.assertRaises(ValueError):
            evaluate(x=-math.inf, k=2)
        with self.assertRaises(ValueError):
            evaluate(x=False, k=2)
        with self.assertRaises(ValueError):
            evaluate(x=2.0, k=-3)
        with self.assertRaises(ValueError):
            evaluate(x=2.0, k=0.5)

    def test_gamma_ratio(self):
        # Independent route for the product derived by induction: Gamma(x + k) / Gamma(x).
        for x, k in ((0.7, 5), (3.25, 7), (10.0, 3)):
            with self.subTest(x=x, k=k):
                expected = math.gamma(x + k) / math.gamma(x)
                self.assertTrue(
                    _close(rising_factorial.evaluate(x=x, k=k), expected, rel_tol=1e-13)
                )

    def test_x_one_is_factorial(self):
        for k in range(20):
            with self.subTest(k=k):
                self.assertEqual(rising_factorial.evaluate(x=1.0, k=k), float(math.factorial(k)))

    def test_link_with_falling_factorial(self):
        # descPochhammer_eval_eq_ascPochhammer: (r)_n falling = (r - n + 1)^(n) rising.
        exact = Fraction(1)
        for i in range(4):
            exact *= Fraction(5.5) - i
        self.assertEqual(rising_factorial.evaluate(x=2.5, k=4), float(exact))

    def test_boundaries(self):
        self.assertEqual(rising_factorial.evaluate(x=-400.0, k=500), 0.0)
        self.assertNotEqual(rising_factorial.evaluate(x=-2.0, k=2), 0.0)
        with self.assertRaises(OverflowError):
            rising_factorial.evaluate(x=1e200, k=2)


class HarmonicNumberTest(IntegerInputChecks, unittest.TestCase):
    formula = harmonic_number
    valid = {"n": 10}

    def test_exact_fraction_sums(self):
        for n in (2, 3, 7, 30, 1000):
            exact = sum(Fraction(1, i) for i in range(1, n + 1))
            with self.subTest(n=n):
                self.assertTrue(_close(harmonic_number.evaluate(n=n), float(exact), rel_tol=REL))

    def test_empty_sum(self):
        self.assertEqual(harmonic_number.evaluate(n=0), 0.0)


class GammaFunctionTest(unittest.TestCase):
    def test_constructed(self):
        self.assertEqual(gamma_function.id, "mathematics.gamma_function")

    def test_domain_rules(self):
        for bad in (0.0, -0.5, -3.0, math.nan, math.inf, True):
            with self.subTest(x=bad), self.assertRaises(ValueError):
                gamma_function.evaluate(x=bad)

    def test_mpmath_values(self):
        # 50-digit mpmath values (phase3/m1b_accuracy/gamma_function.py).
        cases = {
            1e-08: 99999999.422784343,
            0.3: 2.9915689876875907,
            1.7: 0.90863873285329044,
            7.25: 1155.3810139199897,
            33.3: 7.4875775965226323e35,
            171.0: 7.257415615307999e306,
        }
        for x, expected in cases.items():
            with self.subTest(x=x):
                self.assertTrue(_close(gamma_function.evaluate(x=x), expected, rel_tol=REL))

    def test_factorials(self):
        for n in range(1, 30):
            with self.subTest(n=n):
                self.assertTrue(
                    _close(gamma_function.evaluate(x=float(n)), math.factorial(n - 1), rel_tol=REL)
                )

    def test_overflow(self):
        with self.assertRaises(OverflowError):
            gamma_function.evaluate(x=172.0)
        with self.assertRaises(OverflowError):
            gamma_function.evaluate(x=1e-310)


class IncompleteGammaChecks:
    formula = None

    def test_domain_rules(self):
        evaluate = self.formula.evaluate
        with self.assertRaises(ValueError):
            evaluate(s=0.0, x=1.0)
        with self.assertRaises(ValueError):
            evaluate(s=-1.0, x=1.0)
        with self.assertRaises(ValueError):
            evaluate(s=1.0, x=-0.5)
        with self.assertRaises(ValueError):
            evaluate(s=math.nan, x=1.0)
        with self.assertRaises(ValueError):
            evaluate(s=1.0, x=math.inf)
        with self.assertRaises(ValueError):
            evaluate(s=True, x=1.0)


class LowerIncompleteGammaTest(IncompleteGammaChecks, unittest.TestCase):
    formula = lower_incomplete_gamma

    def test_mpmath_values(self):
        # 50-digit mpmath gammainc (phase3/m1b_accuracy/incomplete_gamma.py).
        cases = [
            (0.01, 0.5, 98.873102204949252),
            (0.05, 3.0, 19.456146571435206),
            (7.5, 4.0, 142.62194459719881),
            (25.0, 30.0, 5.2288783724788487e23),
            (100.0, 90.0, 1.476616612456674e155),
            (150.0, 400.0, 3.8089226376305697e260),
            (0.5, 1e-06, 0.0019999993333335333),
            (60.0, 61.0, 7.8777215838810137e79),
        ]
        for s, x, expected in cases:
            with self.subTest(s=s, x=x):
                self.assertTrue(
                    _close(lower_incomplete_gamma.evaluate(s=s, x=x), expected, rel_tol=1e-12)
                )

    def test_closed_form_integer_shape(self):
        # gamma(2, x) = 1 - (1 + x) e^(-x) in both numerical regions.
        for x in (0.3, 2.9, 3.1, 25.0):
            with self.subTest(x=x):
                expected = 1.0 - (1.0 + x) * math.exp(-x)
                self.assertTrue(
                    _close(lower_incomplete_gamma.evaluate(s=2.0, x=x), expected, rel_tol=1e-13)
                )

    def test_boundaries(self):
        self.assertEqual(lower_incomplete_gamma.evaluate(s=3.0, x=0.0), 0.0)
        self.assertTrue(_close(lower_incomplete_gamma.evaluate(s=3.0, x=200.0), 2.0, rel_tol=REL))
        with self.assertRaises(OverflowError):
            lower_incomplete_gamma.evaluate(s=200.0, x=1000.0)


class UpperIncompleteGammaTest(IncompleteGammaChecks, unittest.TestCase):
    formula = upper_incomplete_gamma

    def test_mpmath_values(self):
        # 50-digit mpmath gammainc of the tail (phase3/m1b_accuracy/incomplete_gamma.py).
        cases = [
            (0.01, 0.5, 0.55948291420134991),
            (0.05, 3.0, 0.013938739820305516),
            (7.5, 4.0, 1728.6323612005895),
            (25.0, 30.0, 9.7560564485354572e22),
            (100.0, 90.0, 7.8560049319377413e155),
            (150.0, 400.0, 1.5506686877768911e214),
            (0.5, 1e-06, 1.7704538515721825),
            (60.0, 61.0, 5.9905902706879698e79),
        ]
        for s, x, expected in cases:
            with self.subTest(s=s, x=x):
                self.assertTrue(
                    _close(upper_incomplete_gamma.evaluate(s=s, x=x), expected, rel_tol=1e-12)
                )

    def test_derived_form_against_tail_closed_form(self):
        # Independent route for G = Gamma(s) - gamma(s, x): the tail integral of t^2 e^(-t)
        # is (x^2 + 2x + 2) e^(-x), on both sides of the x = s + 1 switch.
        for x in (0.5, 3.9, 4.1, 30.0):
            with self.subTest(x=x):
                expected = (x * x + 2.0 * x + 2.0) * math.exp(-x)
                self.assertTrue(
                    _close(upper_incomplete_gamma.evaluate(s=3.0, x=x), expected, rel_tol=1e-13)
                )

    def test_complements_lower_function(self):
        # Gamma(s) minus a closed-form lower integral, where no cancellation occurs: s = 1.
        for x in (0.1, 1.5, 7.0):
            with self.subTest(x=x):
                expected = math.gamma(1.0) - (1.0 - math.exp(-x))
                self.assertTrue(
                    _close(upper_incomplete_gamma.evaluate(s=1.0, x=x), expected, rel_tol=1e-13)
                )

    def test_boundaries(self):
        self.assertTrue(_close(upper_incomplete_gamma.evaluate(s=4.0, x=0.0), 6.0, rel_tol=REL))
        self.assertEqual(upper_incomplete_gamma.evaluate(s=0.5, x=1e5), 0.0)
        with self.assertRaises(OverflowError):
            upper_incomplete_gamma.evaluate(s=200.0, x=10.0)


class RegularizedIncompleteBetaTest(unittest.TestCase):
    def test_constructed(self):
        self.assertEqual(regularized_incomplete_beta.id, "mathematics.regularized_incomplete_beta")

    def test_domain_rules(self):
        evaluate = regularized_incomplete_beta.evaluate
        with self.assertRaises(ValueError):
            evaluate(z=-0.1, a=2.0, b=3.0)
        with self.assertRaises(ValueError):
            evaluate(z=1.1, a=2.0, b=3.0)
        with self.assertRaises(ValueError):
            evaluate(z=0.5, a=0.0, b=3.0)
        with self.assertRaises(ValueError):
            evaluate(z=0.5, a=2.0, b=-1.0)
        with self.assertRaises(ValueError):
            evaluate(z=math.nan, a=2.0, b=3.0)
        with self.assertRaises(ValueError):
            evaluate(z=0.5, a=math.inf, b=3.0)

    def test_mpmath_values(self):
        # 50-digit mpmath betainc (phase3/m1b_accuracy/regularized_incomplete_beta.py).
        cases = [
            (1e-08, 0.1, 0.5, 0.13997006263844584),
            (0.3, 0.5, 2.5, 0.79688933627994504),
            (0.6, 10.0, 10.0, 0.81390797858458823),
            (0.45, 100.0, 120.0, 0.44780123014770762),
            (0.99, 2.5, 0.1, 0.28771585067198769),
            (0.05, 1.0, 100.0, 0.99407947077966598),
            (0.9, 30.0, 2.0, 0.16956463310086491),
        ]
        for z, a, b, expected in cases:
            with self.subTest(z=z, a=a, b=b):
                self.assertTrue(
                    _close(
                        regularized_incomplete_beta.evaluate(z=z, a=a, b=b), expected, rel_tol=1e-12
                    )
                )

    def test_exact_binomial_identity(self):
        # For whole a, b: I_z(a, b) = sum_{j=a}^{a+b-1} C(a+b-1, j) z^j (1-z)^(a+b-1-j), exact.
        for z, a, b in ((0.3, 3, 4), (0.75, 5, 2), (0.05, 2, 9)):
            n = a + b - 1
            zf = Fraction(z)
            exact = sum(math.comb(n, j) * zf**j * (1 - zf) ** (n - j) for j in range(a, n + 1))
            with self.subTest(z=z, a=a, b=b):
                self.assertTrue(
                    _close(
                        regularized_incomplete_beta.evaluate(z=z, a=float(a), b=float(b)),
                        float(exact),
                        rel_tol=1e-13,
                    )
                )

    def test_boundaries(self):
        self.assertEqual(regularized_incomplete_beta.evaluate(z=0.0, a=0.5, b=0.5), 0.0)
        self.assertEqual(regularized_incomplete_beta.evaluate(z=1.0, a=0.5, b=0.5), 1.0)


class HyperbolicSineTest(unittest.TestCase):
    def test_constructed(self):
        self.assertEqual(hyperbolic_sine.id, "mathematics.hyperbolic_sine")

    def test_domain_rules(self):
        for bad in (math.nan, math.inf, -math.inf, True):
            with self.subTest(x=bad), self.assertRaises(ValueError):
                hyperbolic_sine.evaluate(x=bad)

    def test_mpmath_values(self):
        cases = {
            0.25: 0.25261231680816831,
            -3.0: -10.017874927409902,
            50.0: 2.5923527642935362e21,
            700.0: 5.0711602736750225e303,
        }
        for x, expected in cases.items():
            with self.subTest(x=x):
                self.assertTrue(_close(hyperbolic_sine.evaluate(x=x), expected, rel_tol=REL))

    def test_odd_and_overflow(self):
        self.assertEqual(hyperbolic_sine.evaluate(x=-1.5), -hyperbolic_sine.evaluate(x=1.5))
        with self.assertRaises(OverflowError):
            hyperbolic_sine.evaluate(x=711.0)


class SincUnnormalizedTest(unittest.TestCase):
    def test_constructed(self):
        self.assertEqual(sinc_unnormalized.id, "mathematics.sinc_unnormalized")
        self.assertEqual(sinc_unnormalized.inputs[0].si_unit, "rad")

    def test_domain_rules(self):
        for bad in (math.nan, math.inf, -math.inf, True):
            with self.subTest(x=bad), self.assertRaises(ValueError):
                sinc_unnormalized.evaluate(x=bad)

    def test_mpmath_values(self):
        cases = {
            0.5: 0.958851077208406,
            2.0: 0.45464871341284085,
            -7.5: 0.12506666356996518,
            1000.0: 0.00082687954053200256,
        }
        for x, expected in cases.items():
            with self.subTest(x=x):
                self.assertTrue(_close(sinc_unnormalized.evaluate(x=x), expected, rel_tol=REL))

    def test_origin(self):
        self.assertEqual(sinc_unnormalized.evaluate(x=0.0), 1.0)
        self.assertEqual(sinc_unnormalized.evaluate(x=-0.0), 1.0)
        self.assertEqual(sinc_unnormalized.evaluate(x=1e-300), 1.0)


class UpperIncompleteGammaSmallShapeTest(unittest.TestCase):
    """Fixes from the independent M1b review (reference values: 60-digit mpmath gammainc)."""

    # (s, x, Gamma(s, x)); oracle script oracles.py. Before the fix the first rows were wrong
    # in the 11th digit or worse (and negative at s = x = 1e-20).
    SMALL_SHAPE = (
        (1e-05, 0.1, 1.8229041057013653),
        (1e-08, 1e-08, 17.8434634023341),
        (1e-20, 1e-20, 45.474486194979384),
        (1e-300, 1e-300, 690.1983122333122),
        (5e-324, 0.2, 1.222650544183893),
        (0.001, 0.2, 1.2218433737692058),
        (0.25, 0.0625, 1.6501820664124829),
        (0.9, 1e-300, 1.0686287021193193),
        (0.5, 0.2499, 0.8500476216049832),
        (0.999999, 0.249, 0.7795800098311565),
    )
    # The continued-fraction side of the x = 0.25 switch for tiny shapes.
    SMALL_SHAPE_CONTINUED_FRACTION = (
        (1e-300, 0.5, 0.5597735947761608),
        (0.001, 0.3, 0.9053161194756633),
        (1e-08, 2.0, 0.04890051118966199),
    )

    def test_small_shape_matches_mpmath_to_rounding(self):
        for s, x, expected in self.SMALL_SHAPE:
            with self.subTest(s=s, x=x):
                actual = upper_incomplete_gamma.evaluate(s=s, x=x)
                self.assertGreater(actual, 0.0)
                self.assertTrue(_close(actual, expected, rel_tol=1e-14), (actual, expected))

    def test_small_shape_continued_fraction_side(self):
        for s, x, expected in self.SMALL_SHAPE_CONTINUED_FRACTION:
            with self.subTest(s=s, x=x):
                actual = upper_incomplete_gamma.evaluate(s=s, x=x)
                self.assertTrue(_close(actual, expected, rel_tol=1e-12), (actual, expected))

    def test_zeta_values_used_by_the_log_gamma_series_match_mpmath(self):
        # zeta(k) from mpmath (oracle script oracles.py).
        zeta_values = (
            (2, 1.6449340668482264),
            (3, 1.2020569031595942),
            (5, 1.03692775514337),
            (10, 1.000994575127818),
            (20, 1.0000009539620338),
            (40, 1.0000000000009095),
        )
        for order, expected in zeta_values:
            with self.subTest(order=order):
                self.assertTrue(_close(_zeta(order), expected, rel_tol=4e-16))

    def test_result_is_never_negative_for_tiny_shapes(self):
        for s in (1e-12, 1e-16, 1e-20, 1e-30, 1e-100, 1e-200):
            for x in (1e-300, 1e-20, 1e-5, 0.1, 0.24):
                with self.subTest(s=s, x=x):
                    self.assertGreater(upper_incomplete_gamma.evaluate(s=s, x=x), 0.0)

    def test_upper_plus_lower_is_gamma_for_small_shape(self):
        # Gamma(s, x) + gamma(s, x) = Gamma(s) at s = 0.3 (no cancellation in the lower series).
        for x in (0.01, 0.1, 0.2):
            with self.subTest(x=x):
                upper = upper_incomplete_gamma.evaluate(s=0.3, x=x)
                lower = lower_incomplete_gamma.evaluate(s=0.3, x=x)
                self.assertTrue(_close(upper + lower, math.gamma(0.3), rel_tol=1e-13))

    def test_huge_shape_with_x_equal_to_shape_raises_arithmetic_error_not_zero_division(self):
        for formula in (upper_incomplete_gamma, lower_incomplete_gamma):
            with self.subTest(formula=formula.id), self.assertRaises(ArithmeticError):
                formula.evaluate(s=1e300, x=1e300)


class RegularizedIncompleteBetaRangeTest(unittest.TestCase):
    """The result must lie in [0, 1] (reference values: 60-digit mpmath betainc)."""

    # (z, a, b, true value). Rounding in the log-space prefactor pushes the raw result out of
    # [0, 1] by about 5e-10 (first row, above 1) and 6e-10 (second row, below 0): clamped.
    CLAMPED = (
        (1.6509029600430078e-07, 6.208423733283957e-10, 3404365.3121983777, 0.9999999996951927),
        (0.9999999999989749, 1216963.07056449, 1.2926709224028263e-12, 1.6826927795293157e-11),
    )
    # Raw excursions of 1.2e-8 and 2.6e-9 are beyond rounding level: an error, not a probability.
    REJECTED = (
        (2.686948563811759e-15, 1.4166031035718546e-12, 9721021.600315224, 0.999999999976083),
        (0.9999999999987795, 3053894.073044711, 1.6718202347645775e-11, 1.993252205420316e-10),
    )

    def test_rounding_level_excursions_are_clamped_into_the_unit_interval(self):
        for z, a, b, true_value in self.CLAMPED:
            with self.subTest(z=z, a=a, b=b):
                actual = regularized_incomplete_beta.evaluate(z=z, a=a, b=b)
                self.assertTrue(0.0 <= actual <= 1.0, actual)
                self.assertLess(abs(actual - true_value), 1e-9)

    def test_larger_excursions_raise_arithmetic_error(self):
        for z, a, b, true_value in self.REJECTED:
            with self.subTest(z=z, a=a, b=b, true_value=true_value):
                with self.assertRaises(ArithmeticError):
                    regularized_incomplete_beta.evaluate(z=z, a=a, b=b)

    def test_random_extreme_shapes_never_leave_the_unit_interval(self):
        rng = random.Random(11)
        for _ in range(3000):
            a = math.exp(rng.uniform(math.log(1e-12), math.log(1e7)))
            b = math.exp(rng.uniform(math.log(1e-12), math.log(1e7)))
            z = rng.choice((rng.random(), 1.0 - math.exp(rng.uniform(-35.0, 0.0))))
            if not 0.0 < z < 1.0:
                continue
            try:
                actual = regularized_incomplete_beta.evaluate(z=z, a=a, b=b)
            except (ArithmeticError, OverflowError):
                continue
            self.assertTrue(0.0 <= actual <= 1.0, (z, a, b, actual))


class FactorialPartialProductOverflowTest(unittest.TestCase):
    """A partial product beyond the float range must not raise when the result is in range."""

    def test_falling_factorial_recovers_after_a_partial_overflow(self):
        # 60-digit mpmath: (171 + 1e-12) falling 172 = 1.2345149246432812e297, although the
        # product of the first 171 factors is about 1.2e309.
        actual = falling_factorial.evaluate(x=171 + 1e-12, k=172)
        self.assertTrue(_close(actual, 1.2345149246432812e297, rel_tol=1e-13), actual)

    def test_rising_factorial_recovers_after_a_partial_overflow(self):
        actual = rising_factorial.evaluate(x=-171 + 1e-11, k=172)
        self.assertTrue(_close(actual, -1.2415692955631042e298, rel_tol=1e-13), actual)

    def test_values_near_the_top_of_the_range_still_match_mpmath(self):
        falling = ((100.5, 100, 1.0570168486832423e159), (170.5, 171, 5.350417198157183e307))
        for x, k, expected in falling:
            with self.subTest(kind="falling", x=x, k=k):
                self.assertTrue(_close(falling_factorial.evaluate(x=x, k=k), expected, 1e-13))
        rising = ((-100.5, 100, 1.0570168486832423e159), (-170.5, 171, -5.350417198157183e307))
        for x, k, expected in rising:
            with self.subTest(kind="rising", x=x, k=k):
                self.assertTrue(_close(rising_factorial.evaluate(x=x, k=k), expected, 1e-13))

    def test_a_final_value_beyond_the_range_still_raises(self):
        with self.assertRaises(OverflowError):
            falling_factorial.evaluate(x=200.5, k=190)
        with self.assertRaises(OverflowError):
            rising_factorial.evaluate(x=-200.5, k=190)
        with self.assertRaises(OverflowError):
            rising_factorial.evaluate(x=-180.25, k=175)


if __name__ == "__main__":
    unittest.main()
