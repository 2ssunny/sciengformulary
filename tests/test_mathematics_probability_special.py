"""Tests for the probability distributions and special functions in the mathematics domain.

Reference values come from the independent oracle (50-digit mpmath, exact fractions and
scipy cross-checks), or from exact Fraction arithmetic done in the test itself; none is
produced by the evaluators under test.
"""

import math
import unittest
from fractions import Fraction

from sciengformulary.catalog.mathematics.bayes_posterior_probability import (
    bayes_posterior_probability,
)
from sciengformulary.catalog.mathematics.beta_function import beta_function
from sciengformulary.catalog.mathematics.binomial_probability_mass import (
    binomial_probability_mass,
)
from sciengformulary.catalog.mathematics.cauchy_probability_density import (
    cauchy_probability_density,
)
from sciengformulary.catalog.mathematics.exponential_cumulative_distribution import (
    exponential_cumulative_distribution,
)
from sciengformulary.catalog.mathematics.exponential_probability_density import (
    exponential_probability_density,
)
from sciengformulary.catalog.mathematics.gamma_probability_density import (
    gamma_probability_density,
)
from sciengformulary.catalog.mathematics.geometric_probability_mass_failures import (
    geometric_probability_mass_failures,
)
from sciengformulary.catalog.mathematics.poisson_probability_mass import (
    poisson_probability_mass,
)
from sciengformulary.core import FormulaSpec

REL = 1e-12


class BinomialProbabilityMassTest(unittest.TestCase):
    def test_constructed(self):
        self.assertIsInstance(binomial_probability_mass, FormulaSpec)
        self.assertEqual(binomial_probability_mass.id, "mathematics.binomial_probability_mass")

    def test_domain_rules(self):
        evaluate = binomial_probability_mass.evaluate
        with self.assertRaises(ValueError):
            evaluate(n=-1, k=0, p=0.5)
        with self.assertRaises(ValueError):
            evaluate(n=4.5, k=2, p=0.5)
        with self.assertRaises(ValueError):
            evaluate(n=5, k=2.5, p=0.5)
        with self.assertRaises(ValueError):
            evaluate(n=5, k=2, p=-0.1)
        with self.assertRaises(ValueError):
            evaluate(n=5, k=2, p=1.1)
        with self.assertRaises(ValueError):
            evaluate(n=5, k=2, p=math.nan)
        with self.assertRaises(ValueError):
            evaluate(n=True, k=0, p=0.5)

    def test_oracle_values(self):
        evaluate = binomial_probability_mass.evaluate
        self.assertTrue(math.isclose(evaluate(n=4, k=4, p=0.3), 0.0081, rel_tol=REL))
        self.assertEqual(evaluate(n=0, k=0, p=0.7), 1.0)

    def test_outside_support_and_degenerate_p(self):
        evaluate = binomial_probability_mass.evaluate
        self.assertEqual(evaluate(n=5, k=-1, p=0.5), 0.0)
        self.assertEqual(evaluate(n=5, k=6, p=0.5), 0.0)
        self.assertEqual(evaluate(n=6, k=2, p=0.0), 0.0)
        self.assertEqual(evaluate(n=6, k=6, p=1.0), 1.0)
        self.assertEqual(evaluate(n=6.0, k=0.0, p=0.0), 1.0)

    def test_power_underflow_uses_log_space(self):
        # 0.2^500 underflows a float although the mass itself (~3e-99) does not.
        p = 0.2
        exact = Fraction(math.comb(1000, 500)) * Fraction(p) ** 500 * (1 - Fraction(p)) ** 500
        actual = binomial_probability_mass.evaluate(n=1000, k=500, p=p)
        self.assertTrue(math.isclose(actual, float(exact), rel_tol=1e-9))


class PoissonProbabilityMassTest(unittest.TestCase):
    def test_constructed(self):
        self.assertIsInstance(poisson_probability_mass, FormulaSpec)

    def test_domain_rules(self):
        evaluate = poisson_probability_mass.evaluate
        with self.assertRaises(ValueError):
            evaluate(lam=-0.5, k=1)
        with self.assertRaises(ValueError):
            evaluate(lam=math.inf, k=1)
        with self.assertRaises(ValueError):
            evaluate(lam=2.0, k=1.5)

    def test_oracle_values(self):
        evaluate = poisson_probability_mass.evaluate
        self.assertTrue(math.isclose(evaluate(lam=2.0, k=2), 0.2706705664732254, rel_tol=REL))
        self.assertEqual(evaluate(lam=0.0, k=2), 0.0)

    def test_outside_support(self):
        self.assertEqual(poisson_probability_mass.evaluate(lam=3.5, k=-1), 0.0)


class GeometricProbabilityMassFailuresTest(unittest.TestCase):
    def test_constructed(self):
        self.assertEqual(
            geometric_probability_mass_failures.id,
            "mathematics.geometric_probability_mass_failures",
        )

    def test_domain_rules(self):
        evaluate = geometric_probability_mass_failures.evaluate
        with self.assertRaises(ValueError):
            evaluate(p=0.0, k=1)
        with self.assertRaises(ValueError):
            evaluate(p=-0.2, k=1)
        with self.assertRaises(ValueError):
            evaluate(p=1.5, k=1)
        with self.assertRaises(ValueError):
            evaluate(p=0.5, k=0.5)

    def test_oracle_values(self):
        evaluate = geometric_probability_mass_failures.evaluate
        self.assertTrue(math.isclose(evaluate(p=0.5, k=2), 0.125, rel_tol=REL))
        self.assertEqual(evaluate(p=1.0, k=0), 1.0)

    def test_outside_support_and_underflow(self):
        evaluate = geometric_probability_mass_failures.evaluate
        self.assertEqual(evaluate(p=0.3, k=-1), 0.0)
        self.assertEqual(evaluate(p=0.5, k=10**6), 0.0)


class ExponentialDistributionTest(unittest.TestCase):
    def test_constructed(self):
        self.assertIsInstance(exponential_probability_density, FormulaSpec)
        self.assertIsInstance(exponential_cumulative_distribution, FormulaSpec)

    def test_domain_rules(self):
        for formula in (exponential_probability_density, exponential_cumulative_distribution):
            with self.subTest(formula=formula.id):
                with self.assertRaises(ValueError):
                    formula.evaluate(x=1.0, lam=0.0)
                with self.assertRaises(ValueError):
                    formula.evaluate(x=1.0, lam=-2.0)
                with self.assertRaises(ValueError):
                    formula.evaluate(x=math.nan, lam=1.0)
                with self.assertRaises(ValueError):
                    formula.evaluate(x=math.inf, lam=1.0)

    def test_oracle_values(self):
        pdf = exponential_probability_density.evaluate
        self.assertTrue(math.isclose(pdf(x=1.0, lam=1.0), 0.36787944117144233, rel_tol=REL))
        self.assertTrue(math.isclose(pdf(x=10.0, lam=0.25), 0.0205212496559747, rel_tol=REL))

    def test_outside_support(self):
        self.assertEqual(exponential_probability_density.evaluate(x=-0.1, lam=2.0), 0.0)
        self.assertEqual(exponential_cumulative_distribution.evaluate(x=-3.0, lam=2.0), 0.0)


class GammaProbabilityDensityTest(unittest.TestCase):
    def test_constructed(self):
        self.assertIsInstance(gamma_probability_density, FormulaSpec)

    def test_domain_rules(self):
        evaluate = gamma_probability_density.evaluate
        with self.assertRaises(ValueError):
            evaluate(x=1.0, alpha=0.0, lam=1.0)
        with self.assertRaises(ValueError):
            evaluate(x=1.0, alpha=2.0, lam=0.0)
        with self.assertRaises(ValueError):
            evaluate(x=math.nan, alpha=2.0, lam=1.0)
        with self.assertRaises(ValueError):
            evaluate(x=0.0, alpha=0.5, lam=1.0)

    def test_oracle_values(self):
        # alpha = 1 reduces to the exponential density 2 e^-1.
        actual = gamma_probability_density.evaluate(x=0.5, alpha=1.0, lam=2.0)
        self.assertTrue(math.isclose(actual, 0.7357588823428847, rel_tol=REL))

    def test_outside_support(self):
        self.assertEqual(gamma_probability_density.evaluate(x=-0.5, alpha=2.0, lam=3.0), 0.0)


class CauchyProbabilityDensityTest(unittest.TestCase):
    def test_constructed(self):
        self.assertIsInstance(cauchy_probability_density, FormulaSpec)

    def test_domain_rules(self):
        evaluate = cauchy_probability_density.evaluate
        with self.assertRaises(ValueError):
            evaluate(x=0.0, x0=0.0, s=0.0)
        with self.assertRaises(ValueError):
            evaluate(x=0.0, x0=0.0, s=-1.0)
        with self.assertRaises(ValueError):
            evaluate(x=math.inf, x0=0.0, s=1.0)
        with self.assertRaises(ValueError):
            evaluate(x=0.0, x0=math.nan, s=1.0)

    def test_oracle_values(self):
        evaluate = cauchy_probability_density.evaluate
        self.assertTrue(
            math.isclose(evaluate(x=1.0, x0=0.0, s=1.0), 0.15915494309189535, rel_tol=REL)
        )
        self.assertTrue(
            math.isclose(evaluate(x=2.0, x0=2.0, s=0.5), 0.6366197723675814, rel_tol=REL)
        )

    def test_far_tail_underflows_to_zero(self):
        self.assertEqual(cauchy_probability_density.evaluate(x=1e300, x0=-1e300, s=1e-10), 0.0)


class BayesPosteriorProbabilityTest(unittest.TestCase):
    def test_constructed(self):
        self.assertIsInstance(bayes_posterior_probability, FormulaSpec)

    def test_domain_rules(self):
        evaluate = bayes_posterior_probability.evaluate
        with self.assertRaises(ValueError):
            evaluate(P_B_given_A=0.5, P_A=0.5, P_B=0.0)
        with self.assertRaises(ValueError):
            evaluate(P_B_given_A=0.5, P_A=1.2, P_B=0.5)
        with self.assertRaises(ValueError):
            evaluate(P_B_given_A=-0.1, P_A=0.5, P_B=0.5)
        with self.assertRaises(ValueError):
            evaluate(P_B_given_A=0.5, P_A=0.5, P_B=math.nan)
        # P(A and B) = 0.45 cannot exceed P(B) = 0.3.
        with self.assertRaises(ValueError):
            evaluate(P_B_given_A=0.9, P_A=0.5, P_B=0.3)

    def test_oracle_values(self):
        evaluate = bayes_posterior_probability.evaluate
        self.assertTrue(math.isclose(evaluate(P_B_given_A=0.3, P_A=0.3, P_B=0.3), 0.3, rel_tol=REL))
        self.assertTrue(
            math.isclose(evaluate(P_B_given_A=0.8, P_A=0.25, P_B=0.5), 0.4, rel_tol=REL)
        )

    def test_rounding_slack_caps_at_one(self):
        evaluate = bayes_posterior_probability.evaluate
        # Joint exceeds P_B by a relative 1e-14: inside the slack, so capped at 1.0.
        self.assertEqual(evaluate(P_B_given_A=1.0, P_A=0.3, P_B=0.3 * (1 - 1e-14)), 1.0)
        # A relative excess of 1e-9 is outside the slack and must raise.
        with self.assertRaises(ValueError):
            evaluate(P_B_given_A=1.0, P_A=0.3, P_B=0.3 * (1 - 1e-9))


class BetaFunctionTest(unittest.TestCase):
    def test_constructed(self):
        self.assertIsInstance(beta_function, FormulaSpec)

    def test_domain_rules(self):
        evaluate = beta_function.evaluate
        with self.assertRaises(ValueError):
            evaluate(a=0.0, b=1.0)
        with self.assertRaises(ValueError):
            evaluate(a=1.0, b=-2.0)
        with self.assertRaises(ValueError):
            evaluate(a=math.inf, b=1.0)

    def test_oracle_values(self):
        evaluate = beta_function.evaluate
        self.assertTrue(math.isclose(evaluate(a=4.0, b=1.0), 0.25, rel_tol=REL))
        self.assertTrue(math.isclose(evaluate(a=0.3, b=7.25), 1.6754863582161394, rel_tol=REL))

    def test_symmetry(self):
        self.assertTrue(
            math.isclose(
                beta_function.evaluate(a=2.5, b=0.7),
                beta_function.evaluate(a=0.7, b=2.5),
                rel_tol=REL,
            )
        )

    def test_gamma_overflow_falls_back_to_log_space(self):
        # For tiny a and b, B(a, b) = (a + b) / (a b) to within a relative O(a), here 2e200,
        # while Gamma(a) * Gamma(b) alone overflows a float.
        actual = beta_function.evaluate(a=1e-200, b=1e-200)
        self.assertTrue(math.isclose(actual, 2e200, rel_tol=1e-12))


if __name__ == "__main__":
    unittest.main()
