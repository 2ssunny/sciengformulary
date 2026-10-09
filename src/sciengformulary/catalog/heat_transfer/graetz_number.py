"""Graetz Number: Gz = Re_D * Pr * D / x."""

from sciengformulary.catalog._domain import finite_result, positive
from sciengformulary.catalog._sources import ENGINEERING_ACCESSED, lienhard_heat_transfer
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(
    Re_D: float,  # noqa: N803
    Pr: float,  # noqa: N803
    D: float,  # noqa: N803
    x: float,
) -> float:
    positive("Re_D", Re_D)
    positive("Pr", Pr)
    positive("D", D)
    positive("x", x)
    return finite_result(Re_D * Pr * D / x)


graetz_number = FormulaSpec(
    id="heat_transfer.graetz_number",
    name="Graetz Number",
    equation="Gz = Re_D * Pr * D / x",
    description=(
        "Dimensionless inverse axial distance that governs the thermal entry region of laminar "
        "flow in a pipe."
    ),
    inputs=(
        VariableSpec(
            name="Re_D",
            symbol="Re_D",
            description="Reynolds number based on pipe diameter and mean velocity",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="Pr",
            symbol="Pr",
            description="Prandtl number",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="D",
            symbol="D",
            description="Pipe diameter",
            dimension="L",
            si_unit="m",
        ),
        VariableSpec(
            name="x",
            symbol="x",
            description="Distance from the start of heating",
            dimension="L",
            si_unit="m",
        ),
    ),
    output=VariableSpec(
        name="Gz",
        symbol="Gz",
        description="Graetz number",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # The source writes the same quantity as Re_D Pr D / x; the equivalent form
        # u_av D^2 / (x alpha) follows from Re_D Pr = u_av D / alpha.
        lienhard_heat_transfer("sec. 7.2, eq. (7.26), p. 362", accessed=ENGINEERING_ACCESSED),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"Re_D": 1000.0, "Pr": 7.0, "D": 0.01, "x": 0.5},
            expected=140.0,
            rel_tol=1e-12,
            note="Hand calculation: 1000 * 7 * 0.01 / 0.5 = 140; 50-digit mpmath agrees.",
        ),
        VerificationCase(
            inputs={"Re_D": 2000.0, "Pr": 0.7, "D": 0.02, "x": 0.02},
            expected=1400.0,
            rel_tol=1e-12,
            note="Station one diameter from the start of heating: 2000 * 0.7 * 1 = 1400.",
        ),
    ),
    assumptions=(
        "Convention without the factor pi/4 that some texts include, and not its inverse; this "
        "follows the cited equation.",
        "All four inputs must be finite and positive; otherwise ValueError is raised.",
        "Meant for thermally developing laminar pipe flow; the evaluator only checks the "
        "inputs, not the flow regime.",
        "Dimensionally homogeneous: D and x in the same length unit.",
    ),
    tags=("Graetz number", "dimensionless group", "internal flow", "thermal entry length"),
)
