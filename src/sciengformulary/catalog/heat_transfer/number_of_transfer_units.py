"""Number of Transfer Units: NTU = U * A / C_min."""

from sciengformulary.catalog._domain import finite_result, non_negative, positive
from sciengformulary.catalog._sources import ENGINEERING_ACCESSED, lienhard_heat_transfer
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(
    U: float,  # noqa: N803
    A: float,  # noqa: N803
    C_min: float,  # noqa: N803
) -> float:
    non_negative("U", U)
    non_negative("A", A)
    positive("C_min", C_min)
    return finite_result(U * A / C_min)


number_of_transfer_units = FormulaSpec(
    id="heat_transfer.number_of_transfer_units",
    name="Number of Transfer Units",
    equation="NTU = U * A / C_min",
    description=(
        "Dimensionless size of a heat exchanger: its total thermal conductance U A compared "
        "with the smaller of the two stream capacity rates."
    ),
    inputs=(
        VariableSpec(
            name="U",
            symbol="U",
            description="Overall heat transfer coefficient, referred to the area A",
            dimension="M T^-3 Theta^-1",
            si_unit="W/(m^2*K)",
        ),
        VariableSpec(
            name="A",
            symbol="A",
            description="Heat transfer area on which U is based",
            dimension="L^2",
            si_unit="m^2",
        ),
        VariableSpec(
            name="C_min",
            symbol="C_{min}",
            description="Smaller of the two stream capacity rates (mass flow rate times c_p)",
            dimension="M L^2 T^-3 Theta^-1",
            si_unit="W/K",
        ),
    ),
    output=VariableSpec(
        name="NTU",
        symbol="NTU",
        description="Number of transfer units",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        lienhard_heat_transfer("sec. 3.3, eq. (3.18), p. 122", accessed=ENGINEERING_ACCESSED),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"U": 500.0, "A": 30.0, "C_min": 10000.0},
            expected=1.5,
            rel_tol=1e-12,
            note=(
                "Worked example in the cited section (Example 3.5, p. 123) prints "
                "NTU = 500 * 30 / 10000 = 1.5; exact."
            ),
        ),
        VerificationCase(
            inputs={"U": 25.0, "A": 0.4, "C_min": 1000.0},
            expected=0.01,
            rel_tol=1e-12,
            note="Small exchanger; hand calculation 25 * 0.4 / 1000 = 0.01.",
        ),
    ),
    assumptions=(
        "U is a constant, area-averaged overall coefficient referred to the same area A.",
        "C_min is the smaller capacity rate of the two streams; the caller must choose it.",
        "U and A must be finite and not negative (zero gives NTU = 0); C_min must be finite "
        "and positive; otherwise ValueError is raised.",
        "Dimensionally homogeneous: U * A and C_min in one consistent unit system (W/K here).",
    ),
    tags=("heat exchanger", "NTU", "number of transfer units", "effectiveness-NTU"),
)
