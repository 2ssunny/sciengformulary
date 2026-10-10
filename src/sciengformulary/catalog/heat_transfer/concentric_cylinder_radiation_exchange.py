"""Radiation Exchange Between Long Concentric Cylinders.

Q = sigma * 2 pi r1 L (T1^4 - T2^4) / (1/eps1 + (r1/r2) (1/eps2 - 1)).
"""

import math

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
    r1: float,
    r2: float,
    L: float,  # noqa: N803 - symbols as written in the source
    T1: float,  # noqa: N803
    T2: float,  # noqa: N803
    eps1: float,
    eps2: float,
) -> float:
    positive("r1", r1)
    positive("r2", r2)
    positive("L", L)
    positive("T1", T1)
    positive("T2", T2)
    _emissivity("eps1", eps1)
    _emissivity("eps2", eps2)
    if r2 <= r1:
        raise ValueError(f"r2 must exceed r1, got r1={r1!r} and r2={r2!r}.")
    area_1 = 2.0 * math.pi * r1 * L
    denominator = 1.0 / eps1 + (r1 / r2) * (1.0 / eps2 - 1.0)
    # T1^4 - T2^4 = (T1 - T2) (T1 + T2) (T1^2 + T2^2) avoids cancellation for close temperatures.
    fourth_power_difference = (T1 - T2) * (T1 + T2) * (T1 * T1 + T2 * T2)
    return finite_result(STEFAN_BOLTZMANN_CONSTANT * area_1 * fourth_power_difference / denominator)


concentric_cylinder_radiation_exchange = FormulaSpec(
    id="heat_transfer.concentric_cylinder_radiation_exchange",
    name="Radiation Exchange Between Long Concentric Cylinders",
    equation="Q = sigma * 2 * pi * r1 * L * (T1^4 - T2^4) / (1/eps1 + (r1/r2) * (1/eps2 - 1))",
    description=(
        "Net radiant heat rate from a long inner cylinder to the long concentric cylinder that "
        "encloses it, both grey. Unlike exchange with large surroundings, the emissivity and "
        "size of the enclosing surface enter; the result is a heat rate, not a coefficient."
    ),
    inputs=(
        VariableSpec(
            name="r1",
            symbol="r_1",
            description="Radius of the inner cylinder, positive",
            dimension="L",
            si_unit="m",
        ),
        VariableSpec(
            name="r2",
            symbol="r_2",
            description="Radius of the outer (enclosing) cylinder, larger than r1",
            dimension="L",
            si_unit="m",
        ),
        VariableSpec(
            name="L",
            symbol="L",
            description="Length of the cylinders, positive",
            dimension="L",
            si_unit="m",
        ),
        VariableSpec(
            name="T1",
            symbol="T_1",
            description="Absolute temperature of the inner surface, positive",
            dimension="Theta",
            si_unit="K",
        ),
        VariableSpec(
            name="T2",
            symbol="T_2",
            description="Absolute temperature of the outer surface, positive",
            dimension="Theta",
            si_unit="K",
        ),
        VariableSpec(
            name="eps1",
            symbol=r"\varepsilon_1",
            description="Emissivity of the inner surface, in (0, 1]",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="eps2",
            symbol=r"\varepsilon_2",
            description="Emissivity of the outer surface, in (0, 1]",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="Q",
        symbol="Q",
        description="Net radiant heat rate from the inner to the outer cylinder",
        dimension="M L^2 T^-3",
        si_unit="W",
    ),
    evaluator=_evaluate,
    references=(
        # Derived result: the source prints the exchange between a body 1 that does not view
        # itself and an enclosing body 2 as A1 sigma (T1^4 - T2^4) / (1/eps1 + (A1/A2)
        # (1/eps2 - 1)) (eq. 10.27, in Example 10.5). For long cylinders A1 = 2 pi r1 L and
        # A2 = 2 pi r2 L, so A1/A2 = r1/r2; the evaluator uses that substitution.
        lienhard_heat_transfer(
            "sec. 10.4, Example 10.5, eq. (10.27), p. 570", accessed=ENGINEERING_ACCESSED
        ),
        STEFAN_BOLTZMANN_CONSTANT_REFERENCE,
    ),
    verification_cases=(
        VerificationCase(
            inputs={
                "r1": 0.05,
                "r2": 0.1,
                "L": 1.0,
                "T1": 600.0,
                "T2": 300.0,
                "eps1": 0.5,
                "eps2": 0.5,
            },
            expected=865.7607216548861,
            rel_tol=1e-12,
            note="Enclosure formula with A1/A2 = 1/2 evaluated with 50-digit arithmetic.",
        ),
        VerificationCase(
            inputs={
                "r1": 0.05,
                "r2": 0.1,
                "L": 2.0,
                "T1": 800.0,
                "T2": 300.0,
                "eps1": 0.3,
                "eps2": 1.0,
            },
            expected=4291.394194375763,
            rel_tol=1e-12,
            note=(
                "Black outer cylinder: the result reduces to eps1 * A1 * sigma * (T1^4 - T2^4), "
                "evaluated with 50-digit arithmetic."
            ),
        ),
    ),
    assumptions=(
        "Derived result: the area ratio A1/A2 of the enclosure relation is replaced by r1/r2, "
        "which holds for long concentric cylinders of equal length.",
        "The inner cylinder is convex (it does not view itself) and fully enclosed. The "
        "cylinders are long enough that end losses are neglected.",
        "Grey, diffuse, opaque surfaces at uniform temperature, separated by a non-participating "
        "medium; absolute temperatures; emissivities in (0, 1]; r2 > r1 > 0.",
        "Uses the Stefan-Boltzmann constant in SI units, so the result is in watts for lengths "
        "in metres.",
    ),
    tags=(
        "thermal radiation",
        "grey body",
        "concentric cylinders",
        "enclosure",
        "Stefan-Boltzmann",
    ),
)
