"""Pressure Equilibrium Constant of an Ideal-Gas Reaction: K_p = exp(-dG0 / (R * T))."""

import math
import sys

from sciengformulary.catalog._domain import finite, positive
from sciengformulary.catalog._sources import nasa_rp_1311
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase

# exp overflows a float above about 709.78 and underflows to zero below about -745.
_EXP_LIMIT = 709.0


def _evaluate(
    dG0: float,  # noqa: N803
    T: float,  # noqa: N803
    R: float,  # noqa: N803
) -> float:
    finite("dG0", dG0)
    positive("T", T)
    positive("R", R)
    exponent = -dG0 / (R * T)
    if exponent > _EXP_LIMIT:
        raise OverflowError(f"K_p exceeds the floating-point range (exponent {exponent!r}).")
    result = math.exp(exponent)
    if result < sys.float_info.min:
        # Below the smallest normal float (about 2.2e-308) the result has fewer than 53 bits of
        # precision, and it is exactly zero below about 5e-324; neither is returned silently.
        raise OverflowError(
            "K_p is below the smallest normal floating-point number and would lose precision "
            f"or underflow to zero (exponent {exponent!r})."
        )
    return result


pressure_equilibrium_constant = FormulaSpec(
    id="thermodynamics.pressure_equilibrium_constant",
    name="Pressure Equilibrium Constant from Standard Gibbs Energy",
    equation="K_p = exp(-dG0 / (R * T))",
    description=(
        "Dimensionless equilibrium constant of an ideal-gas reaction, built from partial "
        "pressures divided by the standard-state pressure, obtained from the standard molar "
        "Gibbs energy change of the reaction."
    ),
    inputs=(
        VariableSpec(
            name="dG0",
            symbol=r"\Delta G^\circ",
            description=(
                "Standard molar Gibbs energy change of the reaction, the sum of nu_j * mu_j0 "
                "over products (positive nu) and reactants (negative nu)"
            ),
            dimension="M L^2 T^-2 N^-1",
            si_unit="J/mol",
        ),
        VariableSpec(
            name="T",
            symbol="T",
            description="Absolute temperature",
            dimension="Theta",
            si_unit="K",
        ),
        VariableSpec(
            name="R",
            symbol="R",
            description=(
                "Molar gas constant; 8.31446261815324 J/(mol K) is the exact product of the "
                "SI-defined Avogadro and Boltzmann constants"
            ),
            dimension="M L^2 T^-2 N^-1 Theta^-1",
            si_unit="J/(mol*K)",
        ),
    ),
    output=VariableSpec(
        name="K_p",
        symbol="K_p",
        description="Equilibrium constant, partial pressures relative to the standard pressure",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # Derived result: the report prints the ideal-gas chemical potential and the equilibrium
        # condition with element multipliers, not the equilibrium constant. For a reaction that
        # conserves every element, summing nu_j times the condition removes the multipliers and
        # leaves sum(nu_j mu_j) = 0; inserting mu_j = mu_j0 + R T ln(p_j / p0) gives
        # dG0 = -R T ln K_p with K_p = prod (p_j / p0)^nu_j. The report (p. 5) fixes no p0 for
        # its own use: it notes the IUPAC 1982 recommendation of 1 bar as the standard-state
        # pressure and that most recent compilations use it, and requires the pressure unit of
        # eq. (2.11) to be consistent with the thermodynamic data in use. Here p0 is therefore
        # the caller's convention, the one dG0 was tabulated for.
        nasa_rp_1311("eq. (2.10) and eq. (2.11), p. 5 (PDF p. 11); eq. (2.1a), p. 3 (PDF p. 9)"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"dG0": -5000.0, "T": 298.15, "R": 8.31446261815324},
            expected=7.515573071036743,
            rel_tol=1e-12,
            note=(
                "50-digit mpmath of exp(5000 / (R T)) with R = N_A k_B exact; the same value "
                "follows from a numerically minimised A <-> 2B ideal-gas equilibrium."
            ),
        ),
        VerificationCase(
            inputs={"dG0": 0.0, "T": 1000.0, "R": 8.31446261815324},
            expected=1.0,
            rel_tol=1e-12,
            note="A zero standard Gibbs energy change gives K_p = exp(0) = 1.",
        ),
        VerificationCase(
            inputs={"dG0": 20000.0, "T": 1000.0, "R": 8.31446261815324},
            expected=0.09022514685021799,
            rel_tol=1e-12,
            note="50-digit mpmath of exp(-20000 / (R * 1000)) with R = N_A k_B exact.",
        ),
    ),
    assumptions=(
        "Derived result: K_p = exp(-dG0 / (R T)) follows from the ideal-gas chemical potential "
        "and the equilibrium condition printed in NASA RP-1311 by eliminating the element "
        "multipliers for an atom-conserving reaction; the report itself does not print K_p.",
        "All species are ideal gases (no condensed phases). K_p is the product of "
        "(p_j / p0)^nu_j over the species, and dG0 must refer to the same standard-state "
        "pressure p0 as the pressures. The choice of p0 is the caller's convention: RP-1311 "
        "notes the IUPAC 1982 recommendation of 1 bar, which most recent compilations use, and "
        "requires the pressure unit to match the thermodynamic data in use. A different p0 "
        "changes dG0 and K_p together.",
        "The reaction must conserve atoms (a stoichiometric reaction).",
        "R is an input and must be in energy units matching dG0 per mole and per kelvin, for "
        "example 8.31446261815324 J/(mol K) with dG0 in J/mol and T in K; RP-1311 itself uses "
        "an older value of R.",
        "T and R must be positive and dG0 finite, otherwise ValueError is raised; a K_p outside "
        "the floating-point range (exponent above 709) or below the smallest normal float "
        "(2.2e-308, where precision is lost or the value underflows to zero) raises "
        "OverflowError.",
    ),
    tags=("equilibrium constant", "Gibbs energy", "ideal gas", "chemical equilibrium", "NASA"),
)
