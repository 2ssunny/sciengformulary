"""Burning Rate from Propellant Mass Flow: r = mdot / (rho_p * A_b)."""

from sciengformulary.catalog._domain import finite_result, non_negative, positive
from sciengformulary.catalog._sources import nasa_technical_report
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(mdot: float, rho_p: float, A_b: float) -> float:  # noqa: N803 - source symbols
    non_negative("mdot", mdot)
    positive("rho_p", rho_p)
    positive("A_b", A_b)
    return finite_result(mdot / (rho_p * A_b))


regression_rate_from_mass_flow = FormulaSpec(
    id="propulsion.regression_rate_from_mass_flow",
    name="Burning Rate from Propellant Mass Flow",
    equation="r_dot = mdot / (rho_p * A_b)",
    description=(
        "Linear burning rate (burning-front progression rate) of a solid propellant from the "
        "propellant mass flow rate, the propellant density and the burning-surface area. It "
        "is a mass balance on the burning surface, not an empirical burning-rate law, and it "
        "is the reverse of the relation that gives mdot from r_dot."
    ),
    inputs=(
        VariableSpec(
            name="mdot",
            symbol=r"\dot{m}_p",
            description="Propellant mass flow rate generated at the burning surface",
            dimension="M T^-1",
            si_unit="kg/s",
        ),
        VariableSpec(
            name="rho_p",
            symbol=r"\rho_p",
            description="Propellant (solid grain) density",
            dimension="M L^-3",
            si_unit="kg/m^3",
        ),
        VariableSpec(
            name="A_b",
            symbol="A_b",
            description="Burning-surface area",
            dimension="L^2",
            si_unit="m^2",
        ),
    ),
    output=VariableSpec(
        name="r_dot",
        symbol="r_b",
        description="Burning-front progression rate (linear burning rate)",
        dimension="L T^-1",
        si_unit="m/s",
    ),
    evaluator=_evaluate,
    references=(
        # Derived: the report prints mdot_p = A_b * r_b * rho_p; solving that relation for r_b
        # gives the equation above.
        nasa_technical_report(
            "Solid Rocket Motor Performance Analysis and Prediction",
            (),
            "NASA SP-8039",
            1971,
            "https://ntrs.nasa.gov/citations/19720011135",
            "sec. 2.1, eq. (4), p. 5",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"mdot": 2.0, "rho_p": 1800.0, "A_b": 0.1},
            expected=0.01111111111111111,
            rel_tol=1e-12,
            note="Hand calculation: 2 / (1800 * 0.1) = 1/90 = 0.0111... m/s.",
        ),
        VerificationCase(
            inputs={"mdot": 0.35, "rho_p": 1750.0, "A_b": 0.02},
            expected=0.009999999999999998,
            rel_tol=1e-12,
            note="Hand calculation: 0.35 / (1750 * 0.02) = 0.01 m/s (small grain).",
        ),
        VerificationCase(
            inputs={"mdot": 0.0, "rho_p": 1800.0, "A_b": 0.1},
            expected=0.0,
            rel_tol=1e-12,
            abs_tol=1e-15,
            note="Edge case: zero mass flow gives a zero burning rate.",
        ),
    ),
    assumptions=(
        "Derived result: the cited report prints the mass balance mdot_p = A_b * r_b * rho_p; "
        "this entry solves it for r_b.",
        "Quasi-steady burning with a uniform regression rate over the burning surface.",
        "mdot must not be negative; rho_p and A_b must be positive.",
    ),
    tags=("burning rate", "regression rate", "solid rocket motor", "internal ballistics"),
)
