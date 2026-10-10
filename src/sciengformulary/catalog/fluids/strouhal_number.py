"""Strouhal Number: Sr = f * L / V."""

from sciengformulary.catalog._domain import finite_result, non_negative, positive
from sciengformulary.catalog._sources import ENGINEERING_ACCESSED, lienhard_heat_transfer
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(
    f: float,
    L: float,  # noqa: N803
    V: float,  # noqa: N803
) -> float:
    non_negative("f", f)
    positive("L", L)
    positive("V", V)
    return finite_result(f * L / V)


strouhal_number = FormulaSpec(
    id="fluids.strouhal_number",
    name="Strouhal Number",
    equation="Sr = f * L / V",
    description=(
        "Dimensionless frequency of a periodic flow phenomenon such as vortex shedding, "
        "formed with a characteristic length and the flow speed."
    ),
    inputs=(
        VariableSpec(
            name="f",
            symbol="f",
            description="Frequency of the periodic phenomenon",
            dimension="T^-1",
            si_unit="Hz",
        ),
        VariableSpec(
            name="L",
            symbol="L",
            description="Characteristic length (the cylinder diameter in the source)",
            dimension="L",
            si_unit="m",
        ),
        VariableSpec(
            name="V",
            symbol="u",
            description="Free-stream flow speed",
            dimension="L T^-1",
            si_unit="m/s",
        ),
    ),
    output=VariableSpec(
        name="Sr",
        symbol="Str",
        description="Strouhal number",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # The source writes Str = f_v D / u_inf for vortex shedding from a cylinder in
        # crossflow; here f_v -> f, D -> L and u_inf -> V.
        lienhard_heat_transfer("eq. (7.64), p. 387", accessed=ENGINEERING_ACCESSED),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"f": 8.0, "L": 2.0, "V": 4.0},
            expected=4.0,
            rel_tol=1e-12,
            note="Hand calculation: 8 * 2 / 4 = 4.",
        ),
        VerificationCase(
            inputs={"f": 40.0, "L": 0.01, "V": 2.0},
            expected=0.2,
            rel_tol=1e-12,
            note="Hand calculation with cylinder-like numbers: 40 * 0.01 / 2 = 0.2.",
        ),
        VerificationCase(
            inputs={"f": 0.0, "L": 0.01, "V": 2.0},
            expected=0.0,
            rel_tol=1e-12,
            abs_tol=1e-15,
            note="Edge case of zero frequency, where the number is zero by hand.",
        ),
    ),
    assumptions=(
        "Definition of a dimensionless group. The source applies it to vortex shedding behind "
        "a circular cylinder with L equal to the diameter, where it depends on the "
        "diameter-based Reynolds number.",
        "L must be the length scale of whatever correlation gives Sr. f must not be negative "
        "and L and V must be positive, otherwise ValueError is raised.",
        "Dimensionless: any consistent unit system gives the same value.",
    ),
    tags=("Strouhal number", "vortex shedding", "dimensionless group", "similarity"),
)
