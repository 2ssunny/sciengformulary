"""Sherwood Number: Sh = k_m * L / D_AB."""

from sciengformulary.catalog._domain import finite_result, non_negative, positive
from sciengformulary.catalog._sources import ENGINEERING_ACCESSED, lienhard_heat_transfer
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(
    k_m: float,
    L: float,  # noqa: N803
    D_AB: float,  # noqa: N803
) -> float:
    non_negative("k_m", k_m)
    positive("L", L)
    positive("D_AB", D_AB)
    return finite_result(k_m * L / D_AB)


sherwood_number = FormulaSpec(
    id="heat_transfer.sherwood_number",
    name="Sherwood Number",
    equation="Sh = k_m * L / D_AB",
    description=(
        "Dimensionless mass transfer coefficient, the mass-transfer analogue of the Nusselt number."
    ),
    inputs=(
        VariableSpec(
            name="k_m",
            symbol="k_m",
            description="Mass transfer coefficient in velocity form, g_m / rho",
            dimension="L T^-1",
            si_unit="m/s",
        ),
        VariableSpec(
            name="L",
            symbol="L",
            description="Characteristic length",
            dimension="L",
            si_unit="m",
        ),
        VariableSpec(
            name="D_AB",
            symbol="D_{AB}",
            description="Binary mass diffusivity",
            dimension="L^2 T^-1",
            si_unit="m^2/s",
        ),
    ),
    output=VariableSpec(
        name="Sh",
        symbol="Sh",
        description="Sherwood number",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # The source defines the group with the mass-flux coefficient g_m (kg/(m^2*s)) as
        # g_m x / (rho D_im). Writing k_m = g_m / rho gives Sh = k_m L / D_AB: a one-line
        # substitution, checked in the independent-route test.
        lienhard_heat_transfer(
            "sec. 11.6, eq. (11.69) and Table 11.2, p. 658; named Sherwood number on p. 659",
            accessed=ENGINEERING_ACCESSED,
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"k_m": 0.01, "L": 0.05, "D_AB": 2e-05},
            expected=25.0,
            rel_tol=1e-12,
            note="Hand calculation: 0.01 * 0.05 / 2e-5 = 25; 50-digit mpmath agrees.",
        ),
        VerificationCase(
            inputs={"k_m": 0.0, "L": 0.05, "D_AB": 2e-05},
            expected=0.0,
            rel_tol=1e-12,
            abs_tol=1e-15,
            note="No mass transfer coefficient gives zero.",
        ),
    ),
    assumptions=(
        "Derived result: the source writes the group with the mass-flux coefficient g_m "
        "(kg/(m^2*s)) as g_m L / (rho D). Substituting k_m = g_m / rho, a coefficient with "
        "units of velocity, gives Sh = k_m L / D_AB. Pass k_m, not g_m.",
        "Used with heat-transfer correlations through the analogy only at low mass-transfer "
        "rates; the source's table of the analogy states |B_m| <= 0.2.",
        "k_m must be finite and not negative; L and D_AB must be finite and positive; "
        "otherwise ValueError is raised.",
        "Dimensionally homogeneous: any consistent units.",
    ),
    tags=("Sherwood number", "dimensionless group", "mass transfer", "convection"),
)
