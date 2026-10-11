"""Kp to Kc Conversion for an Ideal-Gas Reaction: K_c = K_p * (p0 / (R * T))^dn."""

import sys

from sciengformulary.catalog._domain import finite_result, integer, positive
from sciengformulary.catalog._sources import nasa_rp_1311
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(
    K_p: float,  # noqa: N803
    T: float,  # noqa: N803
    dn: float,
    p0: float,
    R: float,  # noqa: N803
) -> float:
    positive("K_p", K_p)
    positive("T", T)
    exponent = integer("dn", dn)
    positive("p0", p0)
    positive("R", R)
    try:
        result = K_p * (p0 / (R * T)) ** exponent
    except (OverflowError, ZeroDivisionError):
        raise OverflowError("K_c is outside the floating-point range.") from None
    if result < sys.float_info.min:
        # Below the smallest normal float (about 2.2e-308) the result has fewer than 53 bits of
        # precision, and it is exactly zero below about 5e-324; neither is returned silently.
        raise OverflowError(
            "K_c is below the smallest normal floating-point number and would lose precision "
            "or underflow to zero."
        )
    return finite_result(result)


kp_kc_conversion = FormulaSpec(
    id="thermodynamics.kp_kc_conversion",
    name="Kp to Kc Conversion",
    equation="K_c = K_p * (p0 / (R * T))^dn",
    description=(
        "Concentration-based equilibrium constant of an ideal-gas reaction from the "
        "dimensionless pressure-based constant K_p, the temperature and the net change dn of "
        "stoichiometric coefficients."
    ),
    inputs=(
        VariableSpec(
            name="K_p",
            symbol="K_p",
            description="Pressure equilibrium constant (partial pressures relative to p0)",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="T",
            symbol="T",
            description="Absolute temperature",
            dimension="Theta",
            si_unit="K",
        ),
        VariableSpec(
            name="dn",
            symbol=r"\Delta n",
            description=(
                "Net change in stoichiometric coefficients, the sum of nu_j with products "
                "positive and reactants negative; a whole number"
            ),
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="p0",
            symbol=r"p^\circ",
            description=(
                "Standard-state pressure used to define K_p, in the pressure unit inside R * T "
                "(for example 1 bar = 1e5 Pa)"
            ),
            dimension="M L^-1 T^-2",
            si_unit="Pa",
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
        name="K_c",
        symbol="K_c",
        description=(
            "Equilibrium constant in concentration form, the product of c_j^nu_j with "
            "concentrations in mol/m^3"
        ),
        dimension="(N L^-3)^dn",
        si_unit="(mol/m^3)^dn",
    ),
    evaluator=_evaluate,
    references=(
        # Derived result: the report prints the ideal-gas law PV = nRT, so p_j = c_j R T. Then
        # K_p = prod (c_j R T / p0)^nu_j = K_c (R T / p0)^dn, which is solved here for K_c.
        # Notation: in RP-1311 eqs. (2.1) V is the specific volume (m^3/kg) and n the moles per
        # unit mass of mixture (kmol/kg), defined just after the equations on p. 4. The ratio
        # n / V is the amount per volume, so p_j = c_j R T is unchanged by the per-mass basis.
        nasa_rp_1311("eq. (2.1a)-(2.1b), p. 3 (PDF p. 9)"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"K_p": 2.5, "T": 1000.0, "dn": 1.0, "p0": 100000.0, "R": 8.31446261815324},
            expected=30.068088760681512,
            rel_tol=1e-12,
            note="Exact rational arithmetic with R = N_A k_B: 2.5 * 1e5 / (R * 1000).",
        ),
        VerificationCase(
            inputs={"K_p": 7.25, "T": 500.0, "dn": 0.0, "p0": 100000.0, "R": 8.31446261815324},
            expected=7.25,
            rel_tol=1e-12,
            note="With dn = 0 the conversion factor is 1, so K_c = K_p.",
        ),
        VerificationCase(
            inputs={"K_p": 0.4, "T": 298.15, "dn": -2.0, "p0": 101325.0, "R": 8.31446261815324},
            expected=0.0002394223912236188,
            rel_tol=1e-12,
            note="Exact rational arithmetic with R = N_A k_B: 0.4 * (R * 298.15 / 101325)^2.",
        ),
    ),
    assumptions=(
        "Derived result: K_c = K_p (p0 / (R T))^dn follows from the ideal-gas law printed in "
        "NASA RP-1311 (partial pressure = concentration * R * T); the report does not print the "
        "conversion itself.",
        "All species are ideal gases. K_c is built from concentrations in mol/m^3 with no "
        "reference concentration, so it carries the unit (mol/m^3)^dn; K_p is dimensionless.",
        "p0 is the standard-state pressure convention K_p was built with (the caller's choice: "
        "the IUPAC 1982 recommendation is 1 bar, historically it was 1 atm) and must match the "
        "one used for the thermodynamic data behind K_p.",
        "p0 and the pressure unit inside R * T must agree, e.g. p0 in Pa with R in J/(mol K) "
        "and T in K.",
        "dn must be a whole number; K_p, T, p0 and R must be positive and finite, otherwise "
        "ValueError is raised. A K_c outside the floating-point range, or below the smallest normal float (2.2e-308, where precision is lost or the value underflows to zero), raises OverflowError.",
    ),
    tags=("equilibrium constant", "Kp", "Kc", "ideal gas", "NASA"),
)
