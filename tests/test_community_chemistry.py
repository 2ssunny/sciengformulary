"""Independent chemistry identities, public discovery and shared-source regressions."""

import math
import unittest

from sciengformulary import formulas
from sciengformulary.catalog._constants import (
    AVOGADRO_CONSTANT,
    BOLTZMANN_CONSTANT,
    ELEMENTARY_CHARGE,
    FARADAY_CONSTANT,
    MOLAR_GAS_CONSTANT,
)
from sciengformulary.catalog._sources import doe_fundamentals_handbook


class CommunityChemistryTest(unittest.TestCase):
    def assert_close(self, actual: float, expected: float) -> None:
        self.assertTrue(math.isclose(actual, expected, rel_tol=1e-12), (actual, expected))

    def test_public_discovery_and_invalid_inputs(self) -> None:
        domains = {
            "chemistry",
            "chemical_equilibrium",
            "chemical_kinetics",
            "electrochemistry",
            "spectroscopy",
            "chromatography",
        }
        thermodynamics = {
            "boltzmann_entropy",
            "bond_enthalpy_reaction_estimate",
            "clausius_clapeyron_pressure",
            "constant_external_pressure_work",
            "enthalpy_change",
            "first_law_internal_energy",
            "gibbs_energy_change",
            "ideal_binary_gas_mixing_entropy",
            "ideal_gas_mixture_chemical_potential",
            "kp_kc_conversion",
            "nasa7_enthalpy",
            "nasa7_entropy",
            "nasa7_heat_capacity",
            "nasa9_heat_capacity",
            "pressure_equilibrium_constant",
            "reaction_enthalpy_from_formation",
            "reaction_gibbs_energy",
            "standard_reaction_gibbs_energy",
            "total_entropy_change",
        }
        additions = [
            f
            for f in formulas.list()
            if f.id.split(".")[0] in domains
            or f.id in {f"thermodynamics.{name}" for name in thermodynamics}
        ]
        self.assertEqual(len(additions), 95)
        for formula in additions:
            self.assertIs(formulas.get(formula.id), formula)
            self.assertIn(formula, formulas.search(formula.id.replace("_", " ")))
            base = formula.verification_cases[0].inputs
            for name in formula.input_names:
                for invalid in (math.nan, math.inf, -math.inf, True, "1"):
                    with self.subTest(id=formula.id, input=name, invalid=repr(invalid)):
                        with self.assertRaises(ValueError):
                            formula.evaluate(**{**base, name: invalid})

    def test_exact_si_products(self) -> None:
        self.assertEqual(MOLAR_GAS_CONSTANT, AVOGADRO_CONSTANT * BOLTZMANN_CONSTANT)
        self.assertEqual(FARADAY_CONSTANT, AVOGADRO_CONSTANT * ELEMENTARY_CHARGE)
        thermal_voltage = formulas.get("electrochemistry.thermal_voltage")
        self.assert_close(
            thermal_voltage.evaluate(T=310), BOLTZMANN_CONSTANT * 310 / ELEMENTARY_CHARGE
        )

    def test_beer_lambert_si_conversion(self) -> None:
        # 100 L/(mol cm), 1 cm, 0.002 mol/L -> 10 m^2/mol, 0.01 m, 2 mol/m^3.
        formula = formulas.get("spectroscopy.beer_lambert_absorbance")
        self.assert_close(formula.evaluate(epsilon=10, l=0.01, c=2), 0.2)

    def test_weak_electrolyte_mass_balance_and_extreme_ratios(self) -> None:
        formula = formulas.get("chemical_equilibrium.weak_electrolyte_ion_concentration")
        concentration = formula.evaluate(Kc=0.01, C0=100)
        self.assert_close(concentration**2 / (100 - concentration), 0.01)
        self.assert_close(formula.evaluate(Kc=1e-300, C0=1e300), 1)
        self.assert_close(formula.evaluate(Kc=1e300, C0=1e-300), 1e-300)

    def test_second_order_half_life_composes_with_consumption(self) -> None:
        half_life = formulas.get("chemical_kinetics.second_order_half_life")
        concentration = formulas.get("chemical_kinetics.second_order_concentration")
        time = half_life.evaluate(c0=20, k=0.01)
        self.assert_close(concentration.evaluate(c0=20, k=0.01, t=time), 10)

    def test_gibbs_and_nernst_consistency(self) -> None:
        gibbs = formulas.get("electrochemistry.reaction_gibbs_from_potential")
        reaction = formulas.get("thermodynamics.reaction_gibbs_energy")
        nernst = formulas.get("electrochemistry.nernst_cell_potential")
        standard = gibbs.evaluate(z=2, E=0.8)
        energy = reaction.evaluate(delta_G_standard=standard, T=310, Q=7)
        potential = nernst.evaluate(E_standard=0.8, T=310, z=2, Q=7)
        self.assert_close(energy, gibbs.evaluate(z=2, E=potential))

    def test_solubility_reproduces_mass_action(self) -> None:
        formula = formulas.get("chemical_equilibrium.salt_molar_solubility")
        for p, q, constant in ((1, 1, 1e-8), (1, 2, 4e-12), (2, 3, 1e-15)):
            with self.subTest(p=p, q=q):
                solubility = formula.evaluate(Ksp=constant, p=p, q=q, c_standard=1000)
                self.assert_close(
                    (p * solubility / 1000) ** p * (q * solubility / 1000) ** q, constant
                )

    def test_fresh_solvent_improves_extraction(self) -> None:
        formula = formulas.get("chemistry.repeated_extraction_remaining_fraction")
        single = formula.evaluate(V_aq=1, V_org=1, D=5, n=1)
        double = formula.evaluate(V_aq=1, V_org=0.5, D=5, n=2)
        self.assertLess(double, single)
        self.assert_close(formula.evaluate(V_aq=1, V_org=1, D=0, n=3), 1)

    def test_van_deemter_stationary_point_is_minimum(self) -> None:
        optimum = formulas.get("chromatography.van_deemter_optimum_velocity")
        height = formulas.get("chromatography.van_deemter_plate_height")
        velocity = optimum.evaluate(B=4, C=1)
        minimum = height.evaluate(A=0.2, B=4, C=1, u=velocity)
        for other in (velocity / 2, velocity * 2):
            self.assertGreater(height.evaluate(A=0.2, B=4, C=1, u=other), minimum)

    def test_doe_electrical_volume_records(self) -> None:
        for volume in (1, 3):
            with self.subTest(volume=volume):
                number = f"DOE-HDBK-1011/{volume}-92"
                reference = doe_fundamentals_handbook(number, "title page")
                self.assertEqual(reference.report_number, number)
                self.assertEqual(reference.year, 1992)
                self.assertIn(f"Volume {volume} of 4", reference.title)
                self.assertTrue(reference.url.endswith(f"DOE-HDBK-1011-92_VOL{volume}.pdf"))
                reference.validate()
                self.assertTrue(reference.format_ieee())

    def test_doe_existing_dates_and_explicit_override(self) -> None:
        reference = doe_fundamentals_handbook("DOE-HDBK-1010-92", "title page")
        self.assertEqual(reference.accessed, "2026-10-09")
        override = doe_fundamentals_handbook("DOE-HDBK-1011/1-92", "title page", "2026-10-10")
        self.assertEqual(override.accessed, "2026-10-10")
