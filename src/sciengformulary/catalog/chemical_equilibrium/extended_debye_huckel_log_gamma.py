"""Extended Debye-Huckel activity correction with explicit normalization."""

import math

from sciengformulary.catalog._domain import (
    finite_result,
    integer,
    non_negative,
    positive,
)
from sciengformulary.catalog._sources import (
    harvey_analytical_chemistry,
)
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(A: float, B: float, a: float, z: float, I: float, c_standard: float) -> float:  # noqa: E741 - symbols as written in the source
    non_negative("A", A)
    non_negative("B", B)
    non_negative("a", a)
    z = integer("z", z)
    non_negative("I", I)
    positive("c_standard", c_standard)
    return finite_result(
        -A * z**2 * math.sqrt(I / c_standard) / (1 + B * a * math.sqrt(I / c_standard))
    )


extended_debye_huckel_log_gamma = FormulaSpec(
    id="chemical_equilibrium.extended_debye_huckel_log_gamma",
    name="Extended Debye Huckel Log Gamma",
    equation="log10(gamma) = -A*z^2*sqrt(I/c_standard)/(1+B*a*sqrt(I/c_standard))",
    description="Extended Debye-Huckel activity correction with explicit normalization.",
    inputs=(
        VariableSpec(
            name="A",
            symbol="A",
            description="Solvent/temperature Debye-Huckel coefficient for the normalized concentration convention",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="B",
            symbol="B",
            description="Inverse-length coefficient for the same convention",
            dimension="L^-1",
            si_unit="1/m",
        ),
        VariableSpec(
            name="a",
            symbol="a",
            description="Effective ion-size parameter",
            dimension="L",
            si_unit="m",
        ),
        VariableSpec(
            name="z", symbol="z", description="Ion charge number", dimension="1", si_unit="-"
        ),
        VariableSpec(
            name="I",
            symbol="I",
            description="Concentration-based ionic strength",
            dimension="N L^-3",
            si_unit="mol/m^3",
        ),
        VariableSpec(
            name="c_standard",
            symbol="c_standard",
            description="Concentration reference used to define A and B",
            dimension="N L^-3",
            si_unit="mol/m^3",
        ),
    ),
    output=VariableSpec(
        name="log_gamma",
        symbol="log_gamma",
        description="Base-ten logarithm of the single-ion activity coefficient",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        harvey_analytical_chemistry(
            "06%3A_Equilibrium_Chemistry/6.09%3A_Activity_Effects",
            "6.9: Activity Effects",
            accessed="2026-10-10",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"A": 0.51, "B": 3300000000.0, "a": 3e-10, "z": 1, "I": 0, "c_standard": 1000},
            expected=0,
            note="At zero ionic strength, log gamma = 0.",
            rel_tol=1e-12,
            abs_tol=1e-300,
        ),
        VerificationCase(
            inputs={"A": 0.51, "B": 3300000000.0, "a": 3e-10, "z": 1, "I": 100, "c_standard": 1000},
            expected=-0.12282415621967799,
            note="Independent Decimal calculation for 0.1 mol/L and 0.3 nm.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
    ),
    assumptions=(
        "Derived result: Convert the source mol/L and nm convention to normalized SI inputs.",
        "Extended Debye-Huckel approximation in its low-ionic-strength regime, with coefficients appropriate to solvent and temperature.",
        "For the source aqueous 25 C convention: c_standard=1000 mol/m^3, A=0.51, B=3.3e9 m^-1 and a in m.",
        "Do not use these aqueous coefficients for arbitrary solvents, temperatures or concentrated solutions.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "chemical equilibrium", "extended debye huckel log gamma"),
)
