"""Tests for the m1b probability distributions in the mathematics domain.

Reference values come from independent oracles: the phase-2b oracle (50-digit mpmath, exact
fractions, scipy cross-checks) and the accuracy scripts, which evaluate each law at 50 digits
in mpmath (for derived formulas through the source's original form: the beta-function form of
the t density, the Weibull form of the Rayleigh density, quadrature of the normal density).
Exact Fraction enumeration is done in the tests themselves. No reference value is produced by
an evaluator under test.
"""

import itertools
import math
import unittest
from fractions import Fraction

from sciengformulary.catalog.mathematics.beta_probability_density import (
    beta_probability_density,
)
from sciengformulary.catalog.mathematics.cauchy_probability_density import (
    cauchy_probability_density,
)
from sciengformulary.catalog.mathematics.chi_squared_probability_density import (
    chi_squared_probability_density,
)
from sciengformulary.catalog.mathematics.exponential_probability_density import (
    exponential_probability_density,
)
from sciengformulary.catalog.mathematics.geometric_probability_mass_trials import (
    geometric_probability_mass_trials,
)
from sciengformulary.catalog.mathematics.gumbel_max_probability_density import (
    gumbel_max_probability_density,
)
from sciengformulary.catalog.mathematics.gumbel_min_probability_density import (
    gumbel_min_probability_density,
)
from sciengformulary.catalog.mathematics.laplace_probability_density import (
    laplace_probability_density,
)
from sciengformulary.catalog.mathematics.lognormal_probability_density import (
    lognormal_probability_density,
)
from sciengformulary.catalog.mathematics.normal_cumulative_distribution import (
    normal_cumulative_distribution,
)
from sciengformulary.catalog.mathematics.pareto_probability_density import (
    pareto_probability_density,
)
from sciengformulary.catalog.mathematics.rayleigh_probability_density import (
    rayleigh_probability_density,
)
from sciengformulary.catalog.mathematics.student_t_probability_density import (
    student_t_probability_density,
)
from sciengformulary.catalog.mathematics.weibull_probability_density import (
    weibull_probability_density,
)
from sciengformulary.catalog._sources import MATH_ACCESSED
from sciengformulary.core import FormulaSpec

REL = 1e-12


class _OracleMixin:
    formula: FormulaSpec

    def assert_oracle(self, cases, rel_tol=REL):
        for inputs, expected in cases:
            with self.subTest(**inputs):
                actual = self.formula.evaluate(**inputs)
                self.assertTrue(
                    math.isclose(actual, expected, rel_tol=rel_tol),
                    f"{inputs}: got {actual!r}, expected {expected!r}",
                )


class BetaProbabilityDensityTest(_OracleMixin, unittest.TestCase):
    formula = beta_probability_density

    def test_constructed(self):
        self.assertIsInstance(beta_probability_density, FormulaSpec)
        self.assertEqual(beta_probability_density.id, "mathematics.beta_probability_density")

    def test_domain_rules(self):
        evaluate = beta_probability_density.evaluate
        with self.assertRaises(ValueError):
            evaluate(x=0.5, alpha=0.0, beta=2.0)
        with self.assertRaises(ValueError):
            evaluate(x=0.5, alpha=2.0, beta=-1.0)
        with self.assertRaises(ValueError):
            evaluate(x=math.nan, alpha=2.0, beta=2.0)
        with self.assertRaises(ValueError):
            evaluate(x=0.5, alpha=math.inf, beta=2.0)
        with self.assertRaises(ValueError):
            evaluate(x=0.0, alpha=0.5, beta=2.0)  # unbounded at x = 0
        with self.assertRaises(ValueError):
            evaluate(x=1.0, alpha=2.0, beta=0.5)  # unbounded at x = 1

    def test_oracle_values(self):
        self.assert_oracle(
            [
                ({"x": 0.2, "alpha": 0.5, "beta": 0.5}, 0.7957747154594766),
                ({"x": 0.999, "alpha": 7.0, "beta": 0.3}, 73.86720909190844),
                ({"x": 0.5, "alpha": 55.0, "beta": 55.0}, 8.34928690218888),
                ({"x": 1e-3, "alpha": 0.7, "beta": 20.0}, 48.629501536512436),
                ({"x": 0.05, "alpha": 100.0, "beta": 2.5}, 1.119615431425903e-124),
                ({"x": 0.71, "alpha": 1.5, "beta": 1.0}, 1.2639224659764539),
            ]
        )

    def test_boundaries(self):
        evaluate = beta_probability_density.evaluate
        self.assertEqual(evaluate(x=-0.1, alpha=2.0, beta=3.0), 0.0)
        self.assertEqual(evaluate(x=1.0, alpha=2.0, beta=3.0), 0.0)
        self.assertEqual(evaluate(x=1.0, alpha=0.5, beta=1.0), 0.5)
        self.assertEqual(evaluate(x=0.0, alpha=1.0, beta=0.5), 0.5)

    def test_overflow_raises(self):
        with self.assertRaises(OverflowError):
            beta_probability_density.evaluate(x=1e-320, alpha=0.01, beta=1.0)


class ChiSquaredProbabilityDensityTest(_OracleMixin, unittest.TestCase):
    formula = chi_squared_probability_density

    def test_constructed(self):
        self.assertEqual(
            chi_squared_probability_density.id, "mathematics.chi_squared_probability_density"
        )

    def test_domain_rules(self):
        evaluate = chi_squared_probability_density.evaluate
        with self.assertRaises(ValueError):
            evaluate(x=1.0, k=0.0)
        with self.assertRaises(ValueError):
            evaluate(x=1.0, k=-2.0)
        with self.assertRaises(ValueError):
            evaluate(x=math.inf, k=3.0)
        with self.assertRaises(ValueError):
            evaluate(x=0.0, k=1.0)  # unbounded at x = 0

    def test_oracle_values(self):
        self.assert_oracle(
            [
                ({"x": 0.05, "k": 0.5}, 2.13932398726506),
                ({"x": 10.0, "k": 10.0}, 0.08773368488392536),
                ({"x": 150.0, "k": 150.0}, 0.023007365502951883),
                ({"x": 400.0, "k": 200.0}, 4.699368913725254e-16),
                ({"x": 1e-3, "k": 1.9}, 0.7085243494595787),
                ({"x": 25.0, "k": 3.4}, 1.2015303462346678e-05),
            ]
        )

    def test_boundaries(self):
        evaluate = chi_squared_probability_density.evaluate
        self.assertEqual(evaluate(x=-0.5, k=0.5), 0.0)
        self.assertEqual(evaluate(x=0.0, k=7.0), 0.0)
        self.assertEqual(evaluate(x=1e6, k=3.0), 0.0)  # far tail underflows


class GeometricProbabilityMassTrialsTest(_OracleMixin, unittest.TestCase):
    formula = geometric_probability_mass_trials

    def test_constructed(self):
        self.assertEqual(
            geometric_probability_mass_trials.id, "mathematics.geometric_probability_mass_trials"
        )

    def test_domain_rules(self):
        evaluate = geometric_probability_mass_trials.evaluate
        with self.assertRaises(ValueError):
            evaluate(p=0.0, k=1)
        with self.assertRaises(ValueError):
            evaluate(p=-0.1, k=1)
        with self.assertRaises(ValueError):
            evaluate(p=1.1, k=1)
        with self.assertRaises(ValueError):
            evaluate(p=math.nan, k=1)
        with self.assertRaises(ValueError):
            evaluate(p=0.5, k=2.5)
        with self.assertRaises(ValueError):
            evaluate(p=0.5, k=True)

    def test_oracle_values(self):
        self.assert_oracle(
            [
                ({"p": 1e-6, "k": 1000000}, 3.678796251112702e-07),
                ({"p": 0.9, "k": 5}, 8.999999999999992e-05),
                ({"p": 0.01, "k": 300}, 0.0004953625663766248),
                ({"p": 0.75, "k": 21}, 6.821210263296962e-13),
            ]
        )

    def test_derived_shift_matches_enumeration(self):
        # Independent route for the index shift: the summed weight of all length-6 outcome
        # strings whose first success is at position k, and the source's failures form
        # (1 - p)^n * p at n = k - 1, both in exact Fractions of the float p.
        evaluate = geometric_probability_mass_trials.evaluate
        for p in (0.2, 0.35):
            q = Fraction(p)
            for k in range(1, 7):
                enumerated = Fraction(0)
                for bits in itertools.product((False, True), repeat=6):
                    if True in bits and bits.index(True) == k - 1:
                        weight = Fraction(1)
                        for success in bits:
                            weight *= q if success else 1 - q
                        enumerated += weight
                failures_form = (1 - q) ** (k - 1) * q
                with self.subTest(p=p, k=k):
                    self.assertEqual(enumerated, failures_form)
                    self.assertTrue(
                        math.isclose(evaluate(p=p, k=k), float(enumerated), rel_tol=REL)
                    )

    def test_boundaries(self):
        evaluate = geometric_probability_mass_trials.evaluate
        self.assertEqual(evaluate(p=0.4, k=-3), 0.0)
        self.assertEqual(evaluate(p=1.0, k=2), 0.0)
        self.assertEqual(evaluate(p=0.5, k=3.0), 0.125)
        self.assertEqual(evaluate(p=0.5, k=10**6), 0.0)  # underflow, not an error


class GumbelProbabilityDensityTest(unittest.TestCase):
    def test_constructed(self):
        self.assertEqual(
            gumbel_max_probability_density.id, "mathematics.gumbel_max_probability_density"
        )
        self.assertEqual(
            gumbel_min_probability_density.id, "mathematics.gumbel_min_probability_density"
        )

    def test_domain_rules(self):
        for formula in (gumbel_max_probability_density, gumbel_min_probability_density):
            evaluate = formula.evaluate
            with self.subTest(formula=formula.id):
                with self.assertRaises(ValueError):
                    evaluate(x=0.0, mu=0.0, beta=0.0)
                with self.assertRaises(ValueError):
                    evaluate(x=0.0, mu=0.0, beta=-1.0)
                with self.assertRaises(ValueError):
                    evaluate(x=math.inf, mu=0.0, beta=1.0)
                with self.assertRaises(ValueError):
                    evaluate(x=0.0, mu=math.nan, beta=1.0)

    def test_oracle_values_max(self):
        cases = [
            ({"x": -3.0, "mu": 0.0, "beta": 1.0}, 3.8005425040443575e-08),
            ({"x": 13.0, "mu": 3.0, "beta": 2.0}, 0.0033463498387677573),
            ({"x": 100.0, "mu": 0.0, "beta": 10.0}, 4.539786865564982e-06),
            ({"x": 0.5, "mu": 0.3, "beta": 0.1}, 1.1820495159314315),
            ({"x": 30.0, "mu": 0.0, "beta": 1.0}, 9.357622968839299e-14),
        ]
        for inputs, expected in cases:
            with self.subTest(**inputs):
                actual = gumbel_max_probability_density.evaluate(**inputs)
                self.assertTrue(math.isclose(actual, expected, rel_tol=REL))

    def test_oracle_values_min(self):
        cases = [
            ({"x": 3.0, "mu": 0.0, "beta": 1.0}, 3.8005425040443575e-08),
            ({"x": -7.0, "mu": 3.0, "beta": 2.0}, 0.0033463498387677573),
            ({"x": -100.0, "mu": 0.0, "beta": 10.0}, 4.539786865564982e-06),
            ({"x": 0.1, "mu": 0.3, "beta": 0.1}, 1.1820495159314317),
            ({"x": -30.0, "mu": 0.0, "beta": 1.0}, 9.357622968839299e-14),
        ]
        for inputs, expected in cases:
            with self.subTest(**inputs):
                actual = gumbel_min_probability_density.evaluate(**inputs)
                self.assertTrue(math.isclose(actual, expected, rel_tol=REL))

    def test_min_is_mirror_of_max(self):
        for x, mu, beta in [(1.3, 0.2, 0.7), (-4.0, 1.0, 2.0), (25.0, -3.0, 5.0)]:
            with self.subTest(x=x, mu=mu, beta=beta):
                self.assertEqual(
                    gumbel_min_probability_density.evaluate(x=x, mu=mu, beta=beta),
                    gumbel_max_probability_density.evaluate(x=-x, mu=-mu, beta=beta),
                )

    def test_short_tail_underflows_without_error(self):
        self.assertEqual(gumbel_max_probability_density.evaluate(x=-1e6, mu=0.0, beta=1.0), 0.0)
        self.assertEqual(gumbel_min_probability_density.evaluate(x=1e6, mu=0.0, beta=1.0), 0.0)
        self.assertEqual(gumbel_max_probability_density.evaluate(x=1e6, mu=0.0, beta=1.0), 0.0)


class LaplaceProbabilityDensityTest(_OracleMixin, unittest.TestCase):
    formula = laplace_probability_density

    def test_constructed(self):
        self.assertEqual(laplace_probability_density.id, "mathematics.laplace_probability_density")

    def test_domain_rules(self):
        evaluate = laplace_probability_density.evaluate
        with self.assertRaises(ValueError):
            evaluate(x=0.0, mu=0.0, b=0.0)
        with self.assertRaises(ValueError):
            evaluate(x=0.0, mu=0.0, b=-2.0)
        with self.assertRaises(ValueError):
            evaluate(x=math.inf, mu=0.0, b=1.0)
        with self.assertRaises(ValueError):
            evaluate(x=0.0, mu=math.nan, b=1.0)

    def test_oracle_values(self):
        self.assert_oracle(
            [
                ({"x": 0.3, "mu": 0.0, "b": 0.1}, 0.24893534183931976),
                ({"x": -30.0, "mu": 1.3, "b": 10.0}, 0.002185889862637547),
                ({"x": 200.0, "mu": 0.0, "b": 1.0}, 6.919482633683688e-88),
                ({"x": 5.0, "mu": -4.0, "b": 2.5}, 0.0054647444894585125),
                ({"x": 1.3, "mu": 1.3, "b": 100.0}, 0.005),
            ]
        )

    def test_symmetry_and_tail(self):
        evaluate = laplace_probability_density.evaluate
        self.assertEqual(evaluate(x=3.0, mu=1.0, b=0.5), evaluate(x=-1.0, mu=1.0, b=0.5))
        self.assertEqual(evaluate(x=1e6, mu=0.0, b=1.0), 0.0)


class LognormalProbabilityDensityTest(_OracleMixin, unittest.TestCase):
    formula = lognormal_probability_density

    def test_constructed(self):
        self.assertEqual(
            lognormal_probability_density.id, "mathematics.lognormal_probability_density"
        )

    def test_domain_rules(self):
        evaluate = lognormal_probability_density.evaluate
        with self.assertRaises(ValueError):
            evaluate(x=1.0, mu=0.0, sigma=0.0)
        with self.assertRaises(ValueError):
            evaluate(x=1.0, mu=0.0, sigma=-1.0)
        with self.assertRaises(ValueError):
            evaluate(x=math.nan, mu=0.0, sigma=1.0)
        with self.assertRaises(ValueError):
            evaluate(x=1.0, mu=math.inf, sigma=1.0)

    def test_oracle_values(self):
        self.assert_oracle(
            [
                ({"x": 0.5, "mu": 0.0, "sigma": 0.3}, 0.18433473559043442),
                ({"x": 20000.0, "mu": 10.0, "sigma": 0.05}, 6.192266344717451e-05),
                ({"x": 1e-3, "mu": -1.0, "sigma": 2.0}, 2.542055512567239),
                ({"x": 100.0, "mu": 0.5, "sigma": 1.0}, 8.738825546459802e-07),
                ({"x": 3.0, "mu": -10.0, "sigma": 10.0}, 0.007183045018528841),
            ]
        )

    def test_boundaries(self):
        evaluate = lognormal_probability_density.evaluate
        self.assertEqual(evaluate(x=-2.0, mu=0.0, sigma=1.0), 0.0)
        self.assertEqual(evaluate(x=0.0, mu=0.0, sigma=0.5), 0.0)
        self.assertEqual(evaluate(x=1e-300, mu=0.0, sigma=1.0), 0.0)  # tiny x, no overflow


class NormalCumulativeDistributionTest(_OracleMixin, unittest.TestCase):
    formula = normal_cumulative_distribution

    def test_constructed(self):
        self.assertEqual(
            normal_cumulative_distribution.id, "mathematics.normal_cumulative_distribution"
        )

    def test_domain_rules(self):
        evaluate = normal_cumulative_distribution.evaluate
        with self.assertRaises(ValueError):
            evaluate(x=0.0, mu=0.0, sigma=0.0)
        with self.assertRaises(ValueError):
            evaluate(x=0.0, mu=0.0, sigma=-1.0)
        with self.assertRaises(ValueError):
            evaluate(x=math.nan, mu=0.0, sigma=1.0)
        with self.assertRaises(ValueError):
            evaluate(x=0.0, mu=math.inf, sigma=1.0)

    def test_oracle_values(self):
        self.assert_oracle(
            [
                ({"x": -2.0, "mu": 0.0, "sigma": 1.0}, 0.02275013194817921),
                ({"x": -5.0, "mu": 0.0, "sigma": 1.0}, 2.866515718791939e-07),
                ({"x": -20.0, "mu": 0.0, "sigma": 1.0}, 2.7536241186062337e-89),
                ({"x": 2.5, "mu": 0.0, "sigma": 1.0}, 0.9937903346742238),
                ({"x": 7.0, "mu": 10.0, "sigma": 2.0}, 0.06680720126885807),
                ({"x": -30.0, "mu": -3.0, "sigma": 1.0}, 7.389481006885018e-161),
            ]
        )

    def test_derived_form_matches_quadrature_of_density(self):
        # Independent route: 50-digit mpmath quadrature of the normal density from -inf to x
        # (the source's integral statement), from the accuracy script.
        self.assert_oracle(
            [
                ({"x": -2.0, "mu": 0.0, "sigma": 1.0}, 0.02275013194817921),
                ({"x": -5.0, "mu": 0.0, "sigma": 1.0}, 2.866515718791939e-07),
                ({"x": 2.5, "mu": 0.0, "sigma": 1.0}, 0.9937903346742238),
                ({"x": 7.0, "mu": 10.0, "sigma": 2.0}, 0.06680720126885807),
            ]
        )

    def test_tails_and_symmetry(self):
        evaluate = normal_cumulative_distribution.evaluate
        self.assertEqual(evaluate(x=100.0, mu=0.0, sigma=1.0), 1.0)
        self.assertEqual(evaluate(x=-100.0, mu=0.0, sigma=1.0), 0.0)
        lower = evaluate(x=-1.3, mu=0.0, sigma=1.0)
        upper = evaluate(x=1.3, mu=0.0, sigma=1.0)
        self.assertTrue(math.isclose(lower + upper, 1.0, rel_tol=1e-15))


class ParetoProbabilityDensityTest(_OracleMixin, unittest.TestCase):
    formula = pareto_probability_density

    def test_constructed(self):
        self.assertEqual(pareto_probability_density.id, "mathematics.pareto_probability_density")

    def test_domain_rules(self):
        evaluate = pareto_probability_density.evaluate
        with self.assertRaises(ValueError):
            evaluate(x=2.0, x_m=0.0, alpha=1.0)
        with self.assertRaises(ValueError):
            evaluate(x=2.0, x_m=-1.0, alpha=1.0)
        with self.assertRaises(ValueError):
            evaluate(x=2.0, x_m=1.0, alpha=0.0)
        with self.assertRaises(ValueError):
            evaluate(x=math.nan, x_m=1.0, alpha=1.0)

    def test_oracle_values(self):
        self.assert_oracle(
            [
                ({"x": 1.001, "x_m": 1.0, "alpha": 50.0}, 47.51514434022251),
                ({"x": 3000.0, "x_m": 1e3, "alpha": 0.5}, 9.622504486493763e-05),
                ({"x": 1e3, "x_m": 1e-3, "alpha": 0.1}, 2.51188643150958e-05),
                ({"x": 2.002, "x_m": 1.0, "alpha": 10.0}, 0.004829422436513702),
                ({"x": 6.6, "x_m": 2.0, "alpha": 3.0}, 0.012648397321575387),
            ]
        )

    def test_boundaries(self):
        evaluate = pareto_probability_density.evaluate
        self.assertEqual(evaluate(x=-5.0, x_m=1.0, alpha=2.0), 0.0)
        self.assertEqual(evaluate(x=0.999, x_m=1.0, alpha=2.0), 0.0)
        self.assertTrue(math.isclose(evaluate(x=4.0, x_m=4.0, alpha=0.5), 0.125, rel_tol=REL))


class RayleighProbabilityDensityTest(_OracleMixin, unittest.TestCase):
    formula = rayleigh_probability_density

    def test_constructed(self):
        self.assertEqual(
            rayleigh_probability_density.id, "mathematics.rayleigh_probability_density"
        )

    def test_domain_rules(self):
        evaluate = rayleigh_probability_density.evaluate
        with self.assertRaises(ValueError):
            evaluate(x=1.0, sigma=0.0)
        with self.assertRaises(ValueError):
            evaluate(x=1.0, sigma=-1.0)
        with self.assertRaises(ValueError):
            evaluate(x=math.inf, sigma=1.0)

    def test_derived_form_matches_weibull_route(self):
        # Independent route: 50-digit mpmath of the source's Weibull density with shape 2 and
        # scale alpha = sigma * sqrt(2), from the accuracy script.
        self.assert_oracle(
            [
                ({"x": 2.0, "sigma": 1.0}, 0.2706705664732254),
                ({"x": 0.05, "sigma": 0.1}, 4.412484512922977),
                ({"x": 500.0, "sigma": 100.0}, 1.8633265860393355e-07),
                ({"x": 12.0, "sigma": 2.0}, 4.5689939234137884e-08),
                ({"x": 1e-3, "sigma": 1.0}, 0.000999999500000125),
            ]
        )

    def test_consistent_with_weibull_shape_two(self):
        for x, sigma in [(0.4, 0.3), (2.0, 1.0), (7.5, 2.5)]:
            with self.subTest(x=x, sigma=sigma):
                weibull = weibull_probability_density.evaluate(
                    x=x, k=2.0, lam=sigma * math.sqrt(2.0)
                )
                self.assertTrue(
                    math.isclose(
                        rayleigh_probability_density.evaluate(x=x, sigma=sigma),
                        weibull,
                        rel_tol=1e-13,
                    )
                )

    def test_boundaries(self):
        evaluate = rayleigh_probability_density.evaluate
        self.assertEqual(evaluate(x=-1.0, sigma=1.0), 0.0)
        self.assertEqual(evaluate(x=0.0, sigma=3.0), 0.0)
        self.assertEqual(evaluate(x=1e3, sigma=1.0), 0.0)


class StudentTProbabilityDensityTest(_OracleMixin, unittest.TestCase):
    formula = student_t_probability_density

    def test_constructed(self):
        self.assertEqual(
            student_t_probability_density.id, "mathematics.student_t_probability_density"
        )

    def test_domain_rules(self):
        evaluate = student_t_probability_density.evaluate
        with self.assertRaises(ValueError):
            evaluate(x=0.0, nu=0)
        with self.assertRaises(ValueError):
            evaluate(x=0.0, nu=-3)
        with self.assertRaises(ValueError):
            evaluate(x=0.0, nu=2.5)
        with self.assertRaises(ValueError):
            evaluate(x=0.0, nu=True)
        with self.assertRaises(ValueError):
            evaluate(x=0.0, nu=math.nan)
        with self.assertRaises(ValueError):
            evaluate(x=math.inf, nu=3)

    def test_derived_form_matches_beta_form(self):
        # Independent route: 50-digit mpmath of the source's beta-function form
        # (1 + x^2/nu)^(-(nu + 1)/2) / (B(1/2, nu/2) sqrt(nu)), from the accuracy script.
        # nu = 49 and 50 straddle the switch from direct gamma values to the series.
        self.assert_oracle(
            [
                ({"x": 0.7, "nu": 3}, 0.2715883590882466),
                ({"x": -10.0, "nu": 10}, 7.28468572291254e-07),
                ({"x": 2.5, "nu": 49}, 0.019737374118229057),
                ({"x": 2.5, "nu": 50}, 0.019694702081706598),
                ({"x": 1.0, "nu": 1000}, 0.24184978955233824),
                ({"x": 3.0, "nu": 10**6}, 0.004431917105672042),
                ({"x": 100.0, "nu": 2}, 9.99700074982504e-07),
            ]
        )

    def test_nu_one_is_cauchy(self):
        for x in (0.0, 0.5, -3.0):
            with self.subTest(x=x):
                self.assertTrue(
                    math.isclose(
                        student_t_probability_density.evaluate(x=x, nu=1),
                        cauchy_probability_density.evaluate(x=x, x0=0.0, s=1.0),
                        rel_tol=1e-14,
                    )
                )

    def test_far_tail_and_integral_float(self):
        evaluate = student_t_probability_density.evaluate
        self.assertEqual(evaluate(x=1e200, nu=3), 0.0)
        self.assertEqual(evaluate(x=1.3, nu=5.0), evaluate(x=1.3, nu=5))


class WeibullProbabilityDensityTest(_OracleMixin, unittest.TestCase):
    formula = weibull_probability_density

    def test_constructed(self):
        self.assertEqual(weibull_probability_density.id, "mathematics.weibull_probability_density")

    def test_domain_rules(self):
        evaluate = weibull_probability_density.evaluate
        with self.assertRaises(ValueError):
            evaluate(x=1.0, k=0.0, lam=1.0)
        with self.assertRaises(ValueError):
            evaluate(x=1.0, k=2.0, lam=-1.0)
        with self.assertRaises(ValueError):
            evaluate(x=math.nan, k=2.0, lam=1.0)
        with self.assertRaises(ValueError):
            evaluate(x=0.0, k=0.5, lam=1.0)  # unbounded at x = 0

    def test_oracle_values(self):
        self.assert_oracle(
            [
                ({"x": 0.5, "k": 0.5, "lam": 1.0}, 0.34865221527635115),
                ({"x": 3000.0, "k": 3.6, "lam": 5000.0}, 0.00016273512106631694),
                ({"x": 1.1, "k": 20.0, "lam": 1.0}, 0.14647884561418908),
                ({"x": 20.0, "k": 1.5, "lam": 2.2}, 2.5639373029328813e-12),
                ({"x": 1e-4, "k": 0.1, "lam": 1e-3}, 358.944770831502),
                ({"x": 4.0, "k": 2.0, "lam": 1.0}, 9.002813977540729e-07),
            ]
        )

    def test_shape_one_is_exponential_with_rate_one_over_scale(self):
        for x, lam in [(0.3, 2.0), (5.0, 1.5)]:
            with self.subTest(x=x, lam=lam):
                self.assertTrue(
                    math.isclose(
                        weibull_probability_density.evaluate(x=x, k=1.0, lam=lam),
                        exponential_probability_density.evaluate(x=x, lam=1.0 / lam),
                        rel_tol=1e-14,
                    )
                )

    def test_boundaries(self):
        evaluate = weibull_probability_density.evaluate
        self.assertEqual(evaluate(x=-0.1, k=2.0, lam=1.0), 0.0)
        self.assertEqual(evaluate(x=0.0, k=3.0, lam=1.0), 0.0)
        self.assertEqual(evaluate(x=1e6, k=3.0, lam=1.0), 0.0)  # (x/lam)^k overflow guarded


class RayleighRegressionTest(unittest.TestCase):
    """Fixes from the independent M1b review."""

    def test_derived_step_matches_two_dimensional_quadrature(self):
        # The step "Rayleigh = radial distance of two independent N(0, sigma^2) coordinates" is
        # checked without using the Weibull algebra: P(R <= r) for sigma = 1.5 is the integral
        # of the product of two normal densities over the disc of radius r, computed by nested
        # 20-digit mpmath quadrature (values pasted as constants; they also equal
        # 1 - exp(-r^2 / (2 sigma^2)) to all printed digits). Here the evaluator's density is
        # integrated from 0 to r by composite Simpson and must reproduce those masses.
        sigma = 1.5
        disc_masses = (
            (1.0, 0.19926259708319195922),
            (2.0, 0.58888770949281256407),
            (4.0, 0.97143449921544962736),
        )
        steps = 4000
        for radius, mass in disc_masses:
            h = radius / steps
            total = 0.0
            for i in range(steps + 1):
                weight = 1 if i in (0, steps) else (4 if i % 2 else 2)
                total += weight * rayleigh_probability_density.evaluate(x=i * h, sigma=sigma)
            integral = total * h / 3.0
            with self.subTest(radius=radius):
                self.assertTrue(math.isclose(integral, mass, rel_tol=1e-10), (integral, mass))

    def test_x_over_sigma_overflow_gives_zero_not_overflow_error(self):
        # x / sigma = 1e310 is beyond the float range; the true density is 0 (mpmath).
        evaluate = rayleigh_probability_density.evaluate
        self.assertEqual(evaluate(x=1e300, sigma=1e-10), 0.0)
        self.assertEqual(evaluate(x=1e200, sigma=1e-10), 0.0)  # u * u overflows only
        self.assertEqual(evaluate(x=1.7e308, sigma=1e-300), 0.0)

    def test_tiny_sigma_keeps_values_that_exp_alone_would_underflow(self):
        # Values from 50-digit mpmath (oracle script oracles.py); exp(-x^2 / (2 sigma^2)) alone
        # is subnormal here but dividing by the tiny sigma brings the product back in range.
        cases = (
            ({"x": 3.85e-299, "sigma": 1e-300}, 5.235556238142763e-21),
            ({"x": 4e-299, "sigma": 1e-300}, 1.4671498336711527e-46),
            ({"x": 3.9e-199, "sigma": 1e-200}, 2.0422604153601678e-129),
        )
        for inputs, expected in cases:
            with self.subTest(**inputs):
                actual = rayleigh_probability_density.evaluate(**inputs)
                self.assertTrue(math.isclose(actual, expected, rel_tol=1e-12), (actual, expected))

    def test_result_beyond_the_float_range_still_raises(self):
        with self.assertRaises(OverflowError):
            rayleigh_probability_density.evaluate(x=5e-324, sigma=5e-324)  # 0.6 / 5e-324


class AccuracyClaimTest(unittest.TestCase):
    """Worst points found by 50-digit mpmath sweeps (oracle scripts sweep_dists.py, oracles2.py).

    Each point lies inside the range named in the formula's assumptions; the tolerance is the
    bound the assumptions state, so the stated claims are exercised at their worst case.
    """

    def check(self, formula, cases, rel_tol):
        for inputs, expected in cases:
            with self.subTest(formula=formula.id, **inputs):
                actual = formula.evaluate(**inputs)
                self.assertTrue(
                    math.isclose(actual, expected, rel_tol=rel_tol, abs_tol=0.0),
                    f"got {actual!r}, expected {expected!r}",
                )

    def test_chi_squared(self):
        self.check(
            chi_squared_probability_density,
            [({"x": 1.9532655220996315e-06, "k": 26.87666636037079}, 5.980636894397945e-85)],
            7e-14,
        )
        self.check(
            chi_squared_probability_density,
            [({"x": 192.0707254947955, "k": 192.9764060874588}, 0.02036329101104132)],
            2e-13,
        )

    def test_pareto(self):
        self.check(
            pareto_probability_density,
            [
                (
                    {"x": 1327060.8990336296, "x_m": 2.4315935202595536, "alpha": 9.07922767099425},
                    5.59280957873747e-58,
                )
            ],
            6e-14,
        )
        self.check(
            pareto_probability_density,
            [
                (
                    {"x": 74669559.18758593, "x_m": 94.1094396399075, "alpha": 41.563371732612},
                    3.483560751757641e-252,
                )
            ],
            2.5e-13,
        )

    def test_rayleigh(self):
        self.check(
            rayleigh_probability_density,
            [({"x": 1.1687117682572836, "sigma": 0.12129082208017986}, 5.482716364203658e-19)],
            2e-14,
        )
        self.check(
            rayleigh_probability_density,
            [({"x": 0.5163017771035767, "sigma": 0.015068382110258498}, 2.6451481264877174e-252)],
            2.5e-13,
        )

    def test_laplace(self):
        self.check(
            laplace_probability_density,
            [
                (
                    {"x": -2814.8765249926046, "mu": -749.7796255123956, "b": 53.97654843068959},
                    2.2440207725792126e-19,
                )
            ],
            1.2e-14,
        )
        self.check(
            laplace_probability_density,
            [
                (
                    {"x": 2181.4900076818485, "mu": -657.8040268760185, "b": 4.7046898837556475},
                    8.481164046879445e-264,
                )
            ],
            2e-13,
        )

    def test_geometric_trials(self):
        self.check(
            geometric_probability_mass_trials,
            [
                ({"p": 0.01906041482204612, "k": 28850.0}, 1.4713202136808587e-243),
                ({"p": 0.0003921204908741653, "k": 11000.0}, 5.247700980630456e-06),
            ],
            1.5e-13,
        )

    def test_student_t(self):
        self.check(
            student_t_probability_density,
            [
                ({"x": -9.435281866363185, "nu": 9764.0}, 2.2651155204670263e-20),
                ({"x": -9.667781493135603, "nu": 4500.0}, 3.2243286503769425e-21),
            ],
            3e-14,
        )
        self.check(
            student_t_probability_density,
            [({"x": 192969.1723681376, "nu": 64.0}, 5.537925128123223e-286)],
            2.5e-13,
        )


class NormalCumulativeAccessDateTest(unittest.TestCase):
    def test_nist_handbook_references_share_the_recorded_access_date(self):
        handbook = [
            reference
            for reference in normal_cumulative_distribution.references
            if reference.url and "nist.gov" in reference.url
        ]
        self.assertEqual(len(handbook), 2)
        for reference in handbook:
            with self.subTest(url=reference.url):
                self.assertEqual(reference.accessed, MATH_ACCESSED)


if __name__ == "__main__":
    unittest.main()
