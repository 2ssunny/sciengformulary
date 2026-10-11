"""Tests for the E3 thermodynamics formulas (equilibrium constants, chemical potential, NASA
polynomials).

Reference values come from the independent oracle (exact rational or 50-digit mpmath
arithmetic). R = 8.31446261815324 J/(mol K) is the exact product of the SI-defined Avogadro and
Boltzmann constants, as used by the oracle. The derived relations (K_p, K_c) are checked by a
second route: an ideal-gas equilibrium found by minimising the Gibbs energy, with K_p and K_c
read from the resulting composition. The NASA polynomials use invented coefficients (no species
data) and are checked against each other and against numerical differentiation.
"""

import math
import unittest

from sciengformulary.catalog.thermodynamics.ideal_gas_mixture_chemical_potential import (
    ideal_gas_mixture_chemical_potential,
)
from sciengformulary.catalog.thermodynamics.kp_kc_conversion import kp_kc_conversion
from sciengformulary.catalog.thermodynamics.nasa7_enthalpy import nasa7_enthalpy
from sciengformulary.catalog.thermodynamics.nasa7_entropy import nasa7_entropy
from sciengformulary.catalog.thermodynamics.nasa7_heat_capacity import (
    nasa7_heat_capacity,
)
from sciengformulary.catalog.thermodynamics.nasa9_heat_capacity import (
    nasa9_heat_capacity,
)
from sciengformulary.catalog.thermodynamics.pressure_equilibrium_constant import (
    pressure_equilibrium_constant,
)

REL = 1e-12
NAN = math.nan
INF = math.inf
R = 8.31446261815324  # N_A * k_B, exact SI value (oracle)


def close(actual, expected, rel=REL, abs_tol=0.0):
    return math.isclose(actual, expected, rel_tol=rel, abs_tol=abs_tol)


class DomainMixin:
    """Shared check that every listed (name, value) pair is rejected with ValueError."""

    def assert_rejected(self, formula, base, bad):
        for name, value in bad:
            with self.subTest(**{name: value}):
                with self.assertRaises(ValueError):
                    formula.evaluate(**{**base, name: value})


def equilibrium_a_to_2b(dg0, temperature, pressure, p0):
    """Gibbs minimisation for A <-> 2B from 1 mol A (mu0_A = 0, mu0_B = dg0 / 2).

    Returns the mole fractions (x_A, x_B) by bisection on dG/d(xi) = 0.
    """

    def slope(xi):
        n = 1.0 + xi
        return -math.log(pressure * (1.0 - xi) / (n * p0)) + 2.0 * (
            dg0 / 2.0 / (R * temperature) + math.log(pressure * 2.0 * xi / (n * p0))
        )

    low, high = 1e-15, 1.0 - 1e-15
    for _ in range(200):
        mid = 0.5 * (low + high)
        if slope(mid) < 0.0:
            low = mid
        else:
            high = mid
    xi = 0.5 * (low + high)
    n = 1.0 + xi
    return (1.0 - xi) / n, 2.0 * xi / n


def equilibrium_a_plus_b_to_c(dg0, temperature, pressure, p0):
    """Gibbs minimisation for A + B <-> C from 1 mol each (mu0_A = mu0_B = 0, mu0_C = dg0)."""

    def slope(xi):
        n = 2.0 - xi
        return (
            math.log(pressure * xi / (n * p0))
            + dg0 / (R * temperature)
            - 2.0 * math.log(pressure * (1.0 - xi) / (n * p0))
        )

    low, high = 1e-15, 1.0 - 1e-15
    for _ in range(200):
        mid = 0.5 * (low + high)
        if slope(mid) < 0.0:
            low = mid
        else:
            high = mid
    xi = 0.5 * (low + high)
    n = 2.0 - xi
    return (1.0 - xi) / n, (1.0 - xi) / n, xi / n


class PressureEquilibriumConstantTest(DomainMixin, unittest.TestCase):
    formula = pressure_equilibrium_constant
    base = {"dG0": -5000.0, "T": 298.15, "R": R}

    def test_constructed(self):
        self.assertEqual(self.formula.id, "thermodynamics.pressure_equilibrium_constant")

    def test_oracle_values(self):
        cases = [
            ({"dG0": -5000.0, "T": 298.15, "R": R}, 7.515573071036743),
            ({"dG0": 0.0, "T": 1000.0, "R": R}, 1.0),
            ({"dG0": 20000.0, "T": 1000.0, "R": R}, 0.09022514685021799),
        ]
        for inputs, expected in cases:
            with self.subTest(**inputs):
                self.assertTrue(close(self.formula.evaluate(**inputs), expected))

    def test_domain_rules(self):
        self.assert_rejected(
            self.formula,
            self.base,
            [
                ("dG0", NAN),
                ("dG0", INF),
                ("dG0", -INF),
                ("T", 0.0),
                ("T", -300.0),
                ("T", NAN),
                ("T", INF),
                ("R", 0.0),
                ("R", -8.314),
                ("R", NAN),
            ],
        )

    def test_exponent_boundary(self):
        # The exponent -dG0 / (R T) is 709 at dG0 = -709 R T: finite. At 710 the result
        # exceeds the float range and raises instead of returning inf.
        t = 500.0
        self.assertTrue(math.isfinite(self.formula.evaluate(dG0=-709.0 * R * t, T=t, R=R)))
        with self.assertRaises(OverflowError):
            self.formula.evaluate(dG0=-710.0 * R * t, T=t, R=R)

    def test_underflow_raises(self):
        with self.assertRaises(OverflowError):
            self.formula.evaluate(dG0=1e7, T=300.0, R=R)

    def test_matches_gibbs_minimised_equilibrium(self):
        # Independent route: solve A <-> 2B by minimising the Gibbs energy of the mixture, read
        # K_p = (P x_B / p0)^2 / (P x_A / p0) off the composition, compare with exp(-dG0 / R T).
        for dg0, temperature, pressure, p0 in [
            (-5000.0, 298.15, 100000.0, 100000.0),
            (20000.0, 1000.0, 250000.0, 100000.0),
            (0.0, 700.0, 50000.0, 100000.0),
        ]:
            with self.subTest(dg0=dg0, T=temperature, P=pressure):
                x_a, x_b = equilibrium_a_to_2b(dg0, temperature, pressure, p0)
                kp_from_composition = (pressure * x_b / p0) ** 2 / (pressure * x_a / p0)
                actual = self.formula.evaluate(dG0=dg0, T=temperature, R=R)
                self.assertTrue(close(actual, kp_from_composition, rel=1e-9))

    def test_matches_dimerisation_equilibrium(self):
        # A + B <-> C with dn = -1, from a second composition solve.
        dg0, temperature, pressure, p0 = -30000.0, 500.0, 200000.0, 100000.0
        x_a, x_b, x_c = equilibrium_a_plus_b_to_c(dg0, temperature, pressure, p0)
        kp_from_composition = (pressure * x_c / p0) / (
            (pressure * x_a / p0) * (pressure * x_b / p0)
        )
        actual = self.formula.evaluate(dG0=dg0, T=temperature, R=R)
        self.assertTrue(close(actual, kp_from_composition, rel=1e-9))


class KpKcConversionTest(DomainMixin, unittest.TestCase):
    formula = kp_kc_conversion
    base = {"K_p": 2.5, "T": 1000.0, "dn": 1.0, "p0": 100000.0, "R": R}

    def test_constructed(self):
        self.assertEqual(self.formula.id, "thermodynamics.kp_kc_conversion")

    def test_oracle_values(self):
        cases = [
            ({"K_p": 2.5, "T": 1000.0, "dn": 1.0, "p0": 100000.0, "R": R}, 30.068088760681512),
            ({"K_p": 7.25, "T": 500.0, "dn": 0.0, "p0": 100000.0, "R": R}, 7.25),
            (
                {"K_p": 0.4, "T": 298.15, "dn": -2.0, "p0": 101325.0, "R": R},
                0.0002394223912236188,
            ),
        ]
        for inputs, expected in cases:
            with self.subTest(**inputs):
                self.assertTrue(close(self.formula.evaluate(**inputs), expected))

    def test_domain_rules(self):
        self.assert_rejected(
            self.formula,
            self.base,
            [
                ("K_p", 0.0),
                ("K_p", -1.0),
                ("K_p", NAN),
                ("K_p", INF),
                ("T", 0.0),
                ("T", -1000.0),
                ("T", NAN),
                ("T", INF),
                ("dn", 0.5),
                ("dn", -1.5),
                ("dn", NAN),
                ("dn", INF),
                ("p0", 0.0),
                ("p0", -1.0),
                ("p0", NAN),
                ("R", 0.0),
                ("R", -1.0),
            ],
        )

    def test_integer_valued_float_and_int_dn_agree(self):
        with_float = self.formula.evaluate(**{**self.base, "dn": 2.0})
        with_int = self.formula.evaluate(**{**self.base, "dn": 2})
        self.assertEqual(with_float, with_int)

    def test_overflow_and_underflow_raise(self):
        # p0 / (R T) is about 12 here, so +-1000 leaves the float range either way.
        with self.assertRaises(OverflowError):
            self.formula.evaluate(**{**self.base, "dn": 1000.0})
        with self.assertRaises(OverflowError):
            self.formula.evaluate(**{**self.base, "dn": -1000.0})

    def test_matches_concentrations_of_gibbs_equilibrium(self):
        # Independent route: K_c read from concentrations c_j = P x_j / (R T) of a Gibbs
        # minimised equilibrium must equal K_p (p0 / R T)^dn.
        dg0, temperature, pressure, p0 = 20000.0, 1000.0, 250000.0, 100000.0
        x_a, x_b = equilibrium_a_to_2b(dg0, temperature, pressure, p0)
        c_a = pressure * x_a / (R * temperature)
        c_b = pressure * x_b / (R * temperature)
        kp = (pressure * x_b / p0) ** 2 / (pressure * x_a / p0)
        actual = self.formula.evaluate(K_p=kp, T=temperature, dn=1.0, p0=p0, R=R)
        self.assertTrue(close(actual, c_b**2 / c_a, rel=1e-9))

        dg0, temperature, pressure, p0 = -30000.0, 500.0, 200000.0, 100000.0
        x_a, x_b, x_c = equilibrium_a_plus_b_to_c(dg0, temperature, pressure, p0)
        c_a, c_b, c_c = (pressure * x / (R * temperature) for x in (x_a, x_b, x_c))
        kp = (pressure * x_c / p0) / ((pressure * x_a / p0) * (pressure * x_b / p0))
        actual = self.formula.evaluate(K_p=kp, T=temperature, dn=-1.0, p0=p0, R=R)
        self.assertTrue(close(actual, c_c / (c_a * c_b), rel=1e-9))

    def test_composition_with_pressure_constant_matches_gibbs_route(self):
        # exp(-dG0 / R T) fed into the conversion equals K_c from concentrations.
        dg0, temperature, pressure, p0 = 20000.0, 1000.0, 250000.0, 100000.0
        x_a, x_b = equilibrium_a_to_2b(dg0, temperature, pressure, p0)
        c_a = pressure * x_a / (R * temperature)
        c_b = pressure * x_b / (R * temperature)
        kp = pressure_equilibrium_constant.evaluate(dG0=dg0, T=temperature, R=R)
        actual = self.formula.evaluate(K_p=kp, T=temperature, dn=1.0, p0=p0, R=R)
        self.assertTrue(close(actual, c_b**2 / c_a, rel=1e-9))


class IdealGasMixtureChemicalPotentialTest(DomainMixin, unittest.TestCase):
    formula = ideal_gas_mixture_chemical_potential
    base = {"mu_ref": -20000.0, "T": 298.15, "P": 200000.0, "X": 0.21, "P_ref": 100000.0, "R": R}

    def test_constructed(self):
        self.assertEqual(self.formula.id, "thermodynamics.ideal_gas_mixture_chemical_potential")

    def test_oracle_values(self):
        cases = [
            (self.base, -22150.496630495687),
            (
                {"mu_ref": -5000.0, "T": 500.0, "P": 100000.0, "X": 1.0, "P_ref": 100000.0, "R": R},
                -5000.0,
            ),
            (
                {
                    "mu_ref": 1000.0,
                    "T": 1000.0,
                    "P": 50000.0,
                    "X": 1e-06,
                    "P_ref": 100000.0,
                    "R": R,
                },
                -119631.69240653935,
            ),
        ]
        for inputs, expected in cases:
            with self.subTest(**inputs):
                self.assertTrue(close(self.formula.evaluate(**inputs), expected))

    def test_domain_rules(self):
        self.assert_rejected(
            self.formula,
            self.base,
            [
                ("mu_ref", NAN),
                ("mu_ref", INF),
                ("T", 0.0),
                ("T", -1.0),
                ("T", NAN),
                ("P", 0.0),
                ("P", -1.0),
                ("P", INF),
                ("X", 0.0),
                ("X", -0.1),
                ("X", 1.0000001),
                ("X", NAN),
                ("P_ref", 0.0),
                ("P_ref", -1.0),
                ("P_ref", NAN),
                ("R", 0.0),
                ("R", -1.0),
            ],
        )

    def test_boundary_mole_fraction_one_is_accepted(self):
        value = self.formula.evaluate(**{**self.base, "X": 1.0})
        self.assertTrue(close(value, -20000.0 + R * 298.15 * math.log(2.0)))

    def test_pressure_derivative_is_molar_volume(self):
        # Independent route: for a pure ideal gas (X = 1), (d mu / dP) at constant T is the molar
        # volume R T / P. Central difference with a small relative step.
        temperature, pressure = 400.0, 150000.0
        step = pressure * 1e-5
        high = self.formula.evaluate(
            mu_ref=0.0, T=temperature, P=pressure + step, X=1.0, P_ref=100000.0, R=R
        )
        low = self.formula.evaluate(
            mu_ref=0.0, T=temperature, P=pressure - step, X=1.0, P_ref=100000.0, R=R
        )
        slope = (high - low) / (2.0 * step)
        self.assertTrue(close(slope, R * temperature / pressure, rel=1e-8))

    def test_mixing_term_is_rt_ln_x(self):
        pure = self.formula.evaluate(**{**self.base, "X": 1.0})
        mixed = self.formula.evaluate(**{**self.base, "X": 0.3})
        self.assertTrue(close(mixed - pure, R * 298.15 * math.log(0.3), rel=1e-9))

    def test_equilibrium_condition_balances_gibbs_minimised_composition(self):
        # At the Gibbs-minimised A <-> 2B composition the chemical potentials satisfy
        # 2 mu_B - mu_A = 0 (mu0_A = 0, mu0_B = dG0 / 2).
        dg0, temperature, pressure, p0 = 20000.0, 1000.0, 250000.0, 100000.0
        x_a, x_b = equilibrium_a_to_2b(dg0, temperature, pressure, p0)
        mu_a = self.formula.evaluate(mu_ref=0.0, T=temperature, P=pressure, X=x_a, P_ref=p0, R=R)
        mu_b = self.formula.evaluate(
            mu_ref=dg0 / 2.0, T=temperature, P=pressure, X=x_b, P_ref=p0, R=R
        )
        self.assertTrue(close(2.0 * mu_b - mu_a, 0.0, abs_tol=1e-6))


class Nasa7Test(DomainMixin, unittest.TestCase):
    """The three 7-coefficient relations share one coefficient set."""

    coeffs_a = {"a1": 3.5, "a2": -0.0012, "a3": 2.5e-06, "a4": -1.8e-09, "a5": 4e-13}
    coeffs_b = {"a1": 2.9, "a2": 0.0015, "a3": -6e-07, "a4": 1.1e-10, "a5": -7.5e-15}

    def test_constructed(self):
        self.assertEqual(nasa7_heat_capacity.id, "thermodynamics.nasa7_heat_capacity")
        self.assertEqual(nasa7_enthalpy.id, "thermodynamics.nasa7_enthalpy")
        self.assertEqual(nasa7_entropy.id, "thermodynamics.nasa7_entropy")

    def test_heat_capacity_oracle_values(self):
        cases = [
            (self.coeffs_a, 300.0, 3.31964),
            (self.coeffs_b, 1000.0, 3.9025),
            (self.coeffs_a, 200.0, 3.34624),
        ]
        for coeffs, t, expected in cases:
            with self.subTest(T=t):
                self.assertTrue(close(nasa7_heat_capacity.evaluate(**coeffs, T=t), expected))

    def test_enthalpy_oracle_values(self):
        cases = [
            (self.coeffs_a, -1050.0, 300.0, -0.116502),
            (self.coeffs_b, -9000.0, 1000.0, -5.524),
            (self.coeffs_a, -1050.0, 200.0, -1.8401386666666666),
        ]
        for coeffs, a6, t, expected in cases:
            with self.subTest(T=t):
                self.assertTrue(close(nasa7_enthalpy.evaluate(**coeffs, a6=a6, T=t), expected))

    def test_entropy_oracle_values(self):
        cases = [
            (self.coeffs_a, 3.2, 300.0, 22.900348661296704),
            (self.coeffs_b, 6.5, 1000.0, 27.767281975714866),
            (self.coeffs_a, 3.2, 200.0, 21.549470782918128),
        ]
        for coeffs, a7, t, expected in cases:
            with self.subTest(T=t):
                self.assertTrue(close(nasa7_entropy.evaluate(**coeffs, a7=a7, T=t), expected))

    def test_domain_rules(self):
        bad_t = [("T", 0.0), ("T", -300.0), ("T", NAN), ("T", INF)]
        bad_coeffs = [(n, v) for n in ("a1", "a2", "a3", "a4", "a5") for v in (NAN, INF)]
        self.assert_rejected(nasa7_heat_capacity, {**self.coeffs_a, "T": 300.0}, bad_t + bad_coeffs)
        self.assert_rejected(
            nasa7_enthalpy,
            {**self.coeffs_a, "a6": -1050.0, "T": 300.0},
            bad_t + bad_coeffs + [("a6", NAN), ("a6", -INF)],
        )
        self.assert_rejected(
            nasa7_entropy,
            {**self.coeffs_a, "a7": 3.2, "T": 300.0},
            bad_t + bad_coeffs + [("a7", NAN), ("a7", INF)],
        )

    def test_overflow_raises(self):
        with self.assertRaises(OverflowError):
            nasa7_heat_capacity.evaluate(a1=0.0, a2=0.0, a3=0.0, a4=0.0, a5=1e300, T=1e10)

    def test_enthalpy_derivative_gives_heat_capacity(self):
        # Independent route: H = R T * h_over_RT, so d(T * h_over_RT)/dT must equal cp/R.
        # Five-point central difference, step 1e-2 K (exact for the quartic part).
        a6, step = -1050.0, 1e-2
        for t in (200.0, 300.0, 650.0, 1000.0):
            with self.subTest(T=t):

                def th(x):
                    return x * nasa7_enthalpy.evaluate(**self.coeffs_a, a6=a6, T=x)

                slope = (
                    -th(t + 2 * step) + 8 * th(t + step) - 8 * th(t - step) + th(t - 2 * step)
                ) / (12 * step)
                expected = nasa7_heat_capacity.evaluate(**self.coeffs_a, T=t)
                self.assertTrue(close(slope, expected, rel=1e-7))

    def test_entropy_derivative_gives_heat_capacity_over_t(self):
        # Independent route: dS/dT = cp / T at constant pressure.
        a7, step = 3.2, 1e-2
        for t in (200.0, 300.0, 650.0, 1000.0):
            with self.subTest(T=t):

                def s(x):
                    return nasa7_entropy.evaluate(**self.coeffs_a, a7=a7, T=x)

                slope = (-s(t + 2 * step) + 8 * s(t + step) - 8 * s(t - step) + s(t - 2 * step)) / (
                    12 * step
                )
                expected = nasa7_heat_capacity.evaluate(**self.coeffs_a, T=t) / t
                self.assertTrue(close(slope, expected, rel=1e-8))

    def test_entropy_constant_shifts_result(self):
        base = nasa7_entropy.evaluate(**self.coeffs_a, a7=0.0, T=300.0)
        shifted = nasa7_entropy.evaluate(**self.coeffs_a, a7=2.5, T=300.0)
        self.assertTrue(close(shifted - base, 2.5, rel=1e-12))


class Nasa9HeatCapacityTest(DomainMixin, unittest.TestCase):
    formula = nasa9_heat_capacity
    coeffs_a = {
        "a1": 100000.0,
        "a2": -1500.0,
        "a3": 4.2,
        "a4": -0.002,
        "a5": 1.4e-06,
        "a6": -3e-10,
        "a7": 2e-14,
    }
    coeffs_b = {
        "a1": -50000.0,
        "a2": 800.0,
        "a3": 3.0,
        "a4": 0.001,
        "a5": -4e-07,
        "a6": 9e-11,
        "a7": -6e-15,
    }

    def test_constructed(self):
        self.assertEqual(self.formula.id, "thermodynamics.nasa9_heat_capacity")

    def test_oracle_values(self):
        cases = [
            (self.coeffs_a, 500.0, 0.91375),
            (self.coeffs_b, 1000.0, 4.434),
            (self.coeffs_a, 200.0, -1.146368),
        ]
        for coeffs, t, expected in cases:
            with self.subTest(T=t):
                self.assertTrue(close(self.formula.evaluate(**coeffs, T=t), expected))

    def test_domain_rules(self):
        base = {**self.coeffs_a, "T": 500.0}
        bad = [("T", 0.0), ("T", -500.0), ("T", NAN), ("T", INF)]
        bad += [(f"a{k}", v) for k in range(1, 8) for v in (NAN, INF)]
        self.assert_rejected(self.formula, base, bad)

    def test_small_temperature_boundary(self):
        # T just above zero is valid input; the 1/T^2 term then dominates.
        value = self.formula.evaluate(**{**self.coeffs_a, "a1": 1.0}, T=1.0)
        self.assertTrue(math.isfinite(value))

    def test_overflow_raises(self):
        with self.assertRaises(OverflowError):
            self.formula.evaluate(**{**self.coeffs_a, "a1": 1e300}, T=1e-10)

    def test_reduces_to_seven_coefficient_form(self):
        # Independent route: with a1 = a2 = 0, the nine-coefficient heat-capacity terms
        # a3..a7 are the polynomial a1..a5 of the seven-coefficient form.
        old = Nasa7Test.coeffs_a
        shifted = dict(zip(("a3", "a4", "a5", "a6", "a7"), old.values()))
        for t in (200.0, 450.0, 1000.0, 3000.0):
            with self.subTest(T=t):
                new = self.formula.evaluate(a1=0.0, a2=0.0, **shifted, T=t)
                self.assertTrue(close(new, nasa7_heat_capacity.evaluate(**old, T=t), rel=1e-12))

    def test_inverse_power_terms_by_direct_sum(self):
        # Independent route: term-by-term sum with explicit powers for the first coefficient set.
        t = 750.0
        c = self.coeffs_a
        direct = (
            c["a1"] * t**-2
            + c["a2"] * t**-1
            + c["a3"]
            + c["a4"] * t
            + c["a5"] * t**2
            + c["a6"] * t**3
            + c["a7"] * t**4
        )
        self.assertTrue(close(self.formula.evaluate(**c, T=t), direct, rel=1e-12))


if __name__ == "__main__":
    unittest.main()
