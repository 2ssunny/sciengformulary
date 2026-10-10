"""Independent-route checks for the vibration formulas derived from the NASA sources.

The NASA sources print the natural frequency, the damping ratio zeta = c / (2 sqrt(m k)),
omega_d = omega_n sqrt(1 - zeta^2) and the complex steady-state amplitude. These tests check
the catalog forms against the characteristic equation m s^2 + c s + k = 0 and complex
arithmetic, never against the evaluators' own algebra.
"""

import cmath
import math
import unittest

from sciengformulary import formulas

CASES = [(200.0, 2.0), (3.5, 0.25), (1.0e4, 12.0)]  # (k, m)


class CriticalDampingTest(unittest.TestCase):
    def test_critical_damping_gives_a_repeated_root(self):
        formula = formulas.get("mechanics.critical_damping_coefficient")
        for k, m in CASES:
            c = formula.evaluate(k=k, m=m)
            # Repeated root of m s^2 + c s + k = 0 when the discriminant c^2 - 4 m k vanishes,
            # i.e. damping ratio zeta = c / (2 sqrt(m k)) equals 1.
            self.assertTrue(math.isclose(c * c, 4 * m * k, rel_tol=1e-14))


class DampedFrequencyTest(unittest.TestCase):
    def test_matches_imaginary_part_of_characteristic_roots(self):
        formula = formulas.get("mechanics.damped_angular_frequency")
        for k, m in CASES:
            for zeta in (0.0, 0.1, 0.7, 0.99):
                b = zeta * 2 * math.sqrt(m * k)
                root = (-b + cmath.sqrt(b * b - 4 * m * k)) / (2 * m)
                value = formula.evaluate(k=k, m=m, b=b)
                self.assertTrue(math.isclose(value, abs(root.imag), rel_tol=1e-12, abs_tol=1e-12))
                # The printed form omega_n sqrt(1 - zeta^2).
                printed = math.sqrt(k / m) * math.sqrt(1 - zeta * zeta)
                self.assertTrue(math.isclose(value, printed, rel_tol=1e-12, abs_tol=1e-12))


class ForcedAmplitudeTest(unittest.TestCase):
    def test_matches_modulus_of_complex_amplitude(self):
        formula = formulas.get("mechanics.forced_vibration_amplitude")
        names = formula.input_names
        for k, m in CASES:
            for b in (0.0, 0.3, 5.0):
                for omega in (0.1, math.sqrt(k / m) * 0.9, math.sqrt(k / m) * 3.0):
                    if b == 0.0 and math.isclose(omega * omega, k / m):
                        continue
                    f0 = 7.0
                    complex_amplitude = f0 / complex(k - m * omega * omega, b * omega)
                    values = {"F0": f0, "m": m, "k": k, "b": b, "omega": omega}
                    value = formula.evaluate(**{n: values[n] for n in names})
                    self.assertTrue(math.isclose(value, abs(complex_amplitude), rel_tol=1e-12))


class NaturalFrequencyTest(unittest.TestCase):
    def test_undamped_roots_are_plus_minus_i_omega_n(self):
        formula = formulas.get("mechanics.natural_angular_frequency")
        for k, m in CASES:
            root = cmath.sqrt(-4 * m * k) / (2 * m)
            self.assertTrue(math.isclose(formula.evaluate(k=k, m=m), root.imag, rel_tol=1e-14))


if __name__ == "__main__":
    unittest.main()
