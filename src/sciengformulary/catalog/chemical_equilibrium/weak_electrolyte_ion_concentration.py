"""Quadratic weak-acid or weak-base dissociation model."""

import math

from sciengformulary.catalog._domain import finite_result, non_negative, positive
from sciengformulary.catalog._sources import (
    harvey_analytical_chemistry,
    openstax_section,
)
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(Kc: float, C0: float) -> float:
    positive("Kc", Kc)
    non_negative("C0", C0)
    if C0 == 0:
        return 0.0
    if C0 <= Kc:
        return finite_result(C0 * (2 / (1 + math.sqrt(1 + 4 * (C0 / Kc)))))
    sqrt_k = math.sqrt(Kc)
    sqrt_c = math.sqrt(C0)
    r = sqrt_k / (2 * sqrt_c)
    return finite_result((sqrt_k * sqrt_c) / (math.hypot(1, r) + r))


weak_electrolyte_ion_concentration = FormulaSpec(
    id="chemical_equilibrium.weak_electrolyte_ion_concentration",
    name="Weak Electrolyte Ion Concentration",
    equation="x = (sqrt(Kc^2 + 4*Kc*C0) - Kc) / 2",
    description="Quadratic weak-acid or weak-base dissociation model.",
    inputs=(
        VariableSpec(
            name="Kc",
            symbol="Kc",
            description="Conditional concentration-form dissociation constant with concentration units",
            dimension="N L^-3",
            si_unit="mol/m^3",
        ),
        VariableSpec(
            name="C0",
            symbol="C0",
            description="Initial formal concentration of a monoprotic weak acid or monobasic weak base",
            dimension="N L^-3",
            si_unit="mol/m^3",
        ),
    ),
    output=VariableSpec(
        name="x",
        symbol="x",
        description="Generated H+ for acid, or OH- for base",
        dimension="N L^-3",
        si_unit="mol/m^3",
    ),
    evaluator=_evaluate,
    references=(
        openstax_section(
            "chemistry-2e",
            "14-3-relative-strengths-of-acids-and-bases",
            "14.3 Relative Strengths of Acids and Bases",
            accessed="2026-10-10",
        ),
        harvey_analytical_chemistry(
            "06%3A_Equilibrium_Chemistry/6.09%3A_Activity_Effects",
            "6.9: Activity Effects",
            accessed="2026-10-10",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"Kc": 1, "C0": 2},
            expected=1,
            note="Mass action x^2/(2-x)=1 has the physical root x=1.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
        VerificationCase(
            inputs={"Kc": 1, "C0": 0},
            expected=0,
            note="Zero formal concentration produces zero ions in the water-neglecting model.",
            rel_tol=1e-12,
            abs_tol=1e-300,
        ),
    ),
    assumptions=(
        "Derived result: Solve x^2/(C0-x)=Kc and rationalize the positive quadratic root.",
        "Single weak electrolyte; no initial conjugate ion, no other acids or bases.",
        "Ignore water autoionization and nonideal activities; not valid for extremely dilute solutions.",
        "Kc has concentration units: in ideal solution Kc = Ka*c_standard (or Kb*c_standard); do not enter dimensionless Ka directly with SI concentrations.",
        "The rationalized implementation avoids subtraction cancellation.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "chemical equilibrium", "weak electrolyte ion concentration"),
)
