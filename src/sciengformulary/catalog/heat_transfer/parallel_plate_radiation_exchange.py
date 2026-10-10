"""Radiation Exchange Between Parallel Grey Plates.

Q = sigma * A * (T1^4 - T2^4) / (1/eps1 + 1/eps2 - 1).
"""

from sciengformulary.catalog._constants import (
    STEFAN_BOLTZMANN_CONSTANT,
    STEFAN_BOLTZMANN_CONSTANT_REFERENCE,
)
from sciengformulary.catalog._domain import finite, finite_result, positive
from sciengformulary.catalog._sources import ENGINEERING_ACCESSED, lienhard_heat_transfer
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _emissivity(name: str, value: float) -> float:
    if not 0 < finite(name, value) <= 1:
        raise ValueError(f"{name} must be in the interval (0, 1], got {value!r}.")
    return value


def _evaluate(
    A: float,  # noqa: N803 - symbols as written in the source
    T1: float,  # noqa: N803
    T2: float,  # noqa: N803
    eps1: float,
    eps2: float,
) -> float:
    positive("A", A)
    positive("T1", T1)
    positive("T2", T2)
    _emissivity("eps1", eps1)
    _emissivity("eps2", eps2)
    # T1^4 - T2^4 = (T1 - T2) (T1 + T2) (T1^2 + T2^2) avoids cancellation for close temperatures.
    fourth_power_difference = (T1 - T2) * (T1 + T2) * (T1 * T1 + T2 * T2)
    flux = STEFAN_BOLTZMANN_CONSTANT * fourth_power_difference / (1.0 / eps1 + 1.0 / eps2 - 1.0)
    return finite_result(A * flux)


parallel_plate_radiation_exchange = FormulaSpec(
    id="heat_transfer.parallel_plate_radiation_exchange",
    name="Radiation Exchange Between Parallel Grey Plates",
    equation="Q = sigma * A * (T1^4 - T2^4) / (1/eps1 + 1/eps2 - 1)",
    description=(
        "Net radiant heat rate between two large parallel grey plates that see only each other. "
        "Unlike the exchange of a small body with large surroundings, both emissivities enter "
        "and the plates reflect radiation back and forth; the result is a heat rate, not a "
        "coefficient."
    ),
    inputs=(
        VariableSpec(
            name="A",
            symbol="A",
            description="Area of each plate (the plates are equal), positive",
            dimension="L^2",
            si_unit="m^2",
        ),
        VariableSpec(
            name="T1",
            symbol="T_1",
            description="Absolute temperature of plate 1, positive",
            dimension="Theta",
            si_unit="K",
        ),
        VariableSpec(
            name="T2",
            symbol="T_2",
            description="Absolute temperature of plate 2, positive",
            dimension="Theta",
            si_unit="K",
        ),
        VariableSpec(
            name="eps1",
            symbol=r"\varepsilon_1",
            description="Emissivity of plate 1, in (0, 1]",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="eps2",
            symbol=r"\varepsilon_2",
            description="Emissivity of plate 2, in (0, 1]",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="Q",
        symbol="Q",
        description="Net radiant heat rate from plate 1 to plate 2 (negative if T2 > T1)",
        dimension="M L^2 T^-3",
        si_unit="W",
    ),
    evaluator=_evaluate,
    references=(
        # Derived result: the source prints the net flux between two infinite parallel
        # plates, q = sigma (T1^4 - T2^4) / (1/eps1 + 1/eps2 - 1), as eq. (10.24), from its
        # two-surface circuit (10.23) with view factor 1 and equal areas. The evaluator
        # multiplies that flux by the plate area A to give a rate.
        lienhard_heat_transfer(
            "sec. 10.4, eqs. (10.23)-(10.25), pp. 568-569", accessed=ENGINEERING_ACCESSED
        ),
        STEFAN_BOLTZMANN_CONSTANT_REFERENCE,
    ),
    verification_cases=(
        VerificationCase(
            inputs={"A": 1.0, "T1": 500.0, "T2": 300.0, "eps1": 0.8, "eps2": 0.6},
            expected=1609.4001829231304,
            rel_tol=1e-12,
            note="sigma * 5.44e10 / (1/0.8 + 1/0.6 - 1) evaluated with 50-digit arithmetic.",
        ),
        VerificationCase(
            inputs={"A": 2.0, "T1": 400.0, "T2": 300.0, "eps1": 1.0, "eps2": 1.0},
            expected=1984.63104665,
            rel_tol=1e-12,
            note="Black plates: sigma * 2 * (400^4 - 300^4) = sigma * 2 * 1.75e10, by hand.",
        ),
        VerificationCase(
            inputs={"A": 1.0, "T1": 350.0, "T2": 350.0, "eps1": 0.5, "eps2": 0.5},
            expected=0.0,
            rel_tol=1e-12,
            abs_tol=1e-15,
            note="Equal temperatures give no net exchange.",
        ),
    ),
    assumptions=(
        "Derived result: the heat rate is the textbook's net flux between infinite parallel "
        "grey plates multiplied by the plate area A.",
        "Infinite, parallel, opaque plates (edge effects negligible, so the view factor between "
        "them is 1) with grey, diffuse surfaces at uniform temperature, separated by a "
        "non-participating medium.",
        "Absolute temperatures. Uses the Stefan-Boltzmann constant in SI units, so the result "
        "is in watts for areas in m^2.",
        "Emissivities lie in (0, 1].",
    ),
    tags=("thermal radiation", "grey body", "parallel plates", "Stefan-Boltzmann", "view factor"),
)
