"""Net Radiative Exchange with Surroundings: Q = eps * sigma * A * (T_b^4 - T_e^4)."""

from sciengformulary.catalog._constants import (
    STEFAN_BOLTZMANN_CONSTANT,
    STEFAN_BOLTZMANN_CONSTANT_REFERENCE,
)
from sciengformulary.catalog._sources import (
    lienhard_heat_transfer,
    openstax_university_physics,
)
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(
    eps: float,
    A: float,  # noqa: N803
    T_b: float,  # noqa: N803
    T_e: float,  # noqa: N803
) -> float:
    return eps * STEFAN_BOLTZMANN_CONSTANT * A * (T_b**4 - T_e**4)


net_radiative_exchange = FormulaSpec(
    id="heat_transfer.net_radiative_exchange",
    name="Net Radiative Exchange with Surroundings",
    equation="Q = eps * sigma * A * (T_b^4 - T_e^4)",
    description=(
        "Net rate of radiant heat loss from a grey body to large surroundings at a different "
        "temperature."
    ),
    inputs=(
        VariableSpec(
            name="eps",
            symbol=r"\varepsilon",
            description="Emissivity of the body",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="A",
            symbol="A",
            description="Radiating surface area of the body",
            dimension="L^2",
            si_unit="m^2",
        ),
        VariableSpec(
            name="T_b",
            symbol="T_b",
            description="Absolute temperature of the body",
            dimension="Theta",
            si_unit="K",
        ),
        VariableSpec(
            name="T_e",
            symbol="T_e",
            description="Absolute temperature of the surroundings",
            dimension="Theta",
            si_unit="K",
        ),
    ),
    output=VariableSpec(
        name="Q",
        symbol="Q",
        description="Net radiant heat loss rate (negative for a net gain)",
        dimension="M L^2 T^-3",
        si_unit="W",
    ),
    evaluator=_evaluate,
    references=(
        # The source writes P_net = sigma e A (T2^4 - T1^4) with T2 the body and T1 the
        # surroundings.
        openstax_university_physics(2, "1-6-mechanisms-of-heat-transfer", "sec. 1.6, eq. (1.10)"),
        STEFAN_BOLTZMANN_CONSTANT_REFERENCE,
        # For a small body enclosed by a much larger isothermal environment the view factor equals
        # the body emissivity.
        lienhard_heat_transfer("sec. 1.3, eqs. (1.34)-(1.35), p. 33"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"eps": 0.9, "A": 2.0, "T_b": 310.0, "T_e": 290.0},
            expected=220.70911759279937,
            rel_tol=1e-12,
            note="60-digit evaluation of 0.9 * sigma * 2 * (310^4 - 290^4), sigma exact (derived).",
        ),
    ),
    assumptions=(
        "Grey body much smaller than, and fully enclosed by, surroundings at uniform temperature.",
        "Absolute temperatures; non-absorbing medium.",
    ),
    tags=("thermal radiation", "net radiation", "grey body", "Stefan-Boltzmann"),
)
