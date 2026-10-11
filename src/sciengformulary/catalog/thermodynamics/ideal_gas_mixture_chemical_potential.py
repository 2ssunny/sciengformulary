"""Chemical Potential of an Ideal-Gas Mixture Component: mu = mu_ref + R * T * ln(P * X / P_ref)."""

import math

from sciengformulary.catalog._domain import finite, finite_result, positive
from sciengformulary.catalog._sources import nasa_rp_1311
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(
    mu_ref: float,
    T: float,  # noqa: N803
    P: float,  # noqa: N803
    X: float,  # noqa: N803
    P_ref: float,  # noqa: N803
    R: float,  # noqa: N803
) -> float:
    finite("mu_ref", mu_ref)
    positive("T", T)
    positive("P", P)
    positive("X", X)
    if X > 1:
        raise ValueError(f"X must be a mole fraction in (0, 1], got {X!r}.")
    positive("P_ref", P_ref)
    positive("R", R)
    # The logarithm is split so that P * X cannot underflow for a trace species.
    log_ratio = math.log(P) + math.log(X) - math.log(P_ref)
    return finite_result(mu_ref + R * T * log_ratio)


ideal_gas_mixture_chemical_potential = FormulaSpec(
    id="thermodynamics.ideal_gas_mixture_chemical_potential",
    name="Chemical Potential of an Ideal-Gas Mixture Component",
    equation="mu = mu_ref + R * T * ln(P * X / P_ref)",
    description=(
        "Molar chemical potential of one species in an ideal-gas mixture from its "
        "standard-state value, the total pressure and its mole fraction."
    ),
    inputs=(
        VariableSpec(
            name="mu_ref",
            symbol=r"\mu^\circ",
            description=(
                "Standard-state molar chemical potential of the pure gas at pressure P_ref and "
                "at the temperature T"
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
            name="P",
            symbol="P",
            description="Total pressure of the mixture, in the same unit as P_ref",
            dimension="M L^-1 T^-2",
            si_unit="Pa",
        ),
        VariableSpec(
            name="X",
            symbol="X",
            description="Mole fraction of the species in the mixture, 0 < X <= 1",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="P_ref",
            symbol=r"P^\circ",
            description="Standard-state pressure at which mu_ref is defined",
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
        name="mu",
        symbol=r"\mu",
        description="Molar chemical potential of the species in the mixture",
        dimension="M L^2 T^-2 N^-1",
        si_unit="J/mol",
    ),
    evaluator=_evaluate,
    references=(
        # Stated up to symbol renaming and one generalisation: the report writes
        # mu_j = mu_j0 + RT ln(n_j/n) + RT ln P with the pressure in the unit of the
        # thermodynamic data (p. 5: the unit of pressure in eq. (2.11) must be consistent with
        # the data in use; no reference pressure is written). Here the standard pressure P_ref
        # is explicit, so P X / P_ref is the partial pressure relative to the standard state and
        # mu_ref refers to P_ref.
        nasa_rp_1311("eq. (2.11), p. 5 (PDF p. 11)"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={
                "mu_ref": -20000.0,
                "T": 298.15,
                "P": 200000.0,
                "X": 0.21,
                "P_ref": 100000.0,
                "R": 8.31446261815324,
            },
            expected=-22150.496630495687,
            rel_tol=1e-12,
            note="50-digit mpmath of -20000 + R T ln(2 * 0.21) with R = N_A k_B exact.",
        ),
        VerificationCase(
            inputs={
                "mu_ref": -5000.0,
                "T": 500.0,
                "P": 100000.0,
                "X": 1.0,
                "P_ref": 100000.0,
                "R": 8.31446261815324,
            },
            expected=-5000.0,
            rel_tol=1e-12,
            note="Pure gas at the standard pressure: the logarithm is zero, so mu = mu_ref.",
        ),
        VerificationCase(
            inputs={
                "mu_ref": 1000.0,
                "T": 1000.0,
                "P": 50000.0,
                "X": 1e-06,
                "P_ref": 100000.0,
                "R": 8.31446261815324,
            },
            expected=-119631.69240653935,
            rel_tol=1e-12,
            note="50-digit mpmath of 1000 + R * 1000 * ln(0.5e-6) with R = N_A k_B exact.",
        ),
    ),
    assumptions=(
        "Ideal-gas mixture: ideal gases without interactions. Condensed phases are not "
        "covered (RP-1311 treats them as pure, with mu equal to its standard value).",
        "mu_ref is the chemical potential of the pure gas at P_ref and at the same temperature "
        "T; it changes with T and with the choice of P_ref. The choice of P_ref is the "
        "caller's convention: RP-1311 notes the IUPAC 1982 recommendation of 1 bar, which most "
        "recent compilations use, and requires the pressure unit of eq. (2.11) to be "
        "consistent with the thermodynamic data in use. Any consistent P_ref is accepted here.",
        "P and P_ref share one pressure unit (only their ratio enters); X is the mole fraction "
        "n_j / n of the species in the gas phase.",
        "R is an input in energy per mole per kelvin matching mu_ref per mole, for example "
        "8.31446261815324 J/(mol K).",
        "T, P, P_ref and R must be positive and X in (0, 1], otherwise ValueError is raised.",
    ),
    tags=("chemical potential", "ideal gas", "mixture", "partial pressure", "NASA"),
)
