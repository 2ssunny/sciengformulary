"""Darcy-Weisbach Pressure Drop: delta_p = f_D * (L / D) * rho * V^2 / 2."""

from sciengformulary.catalog._domain import finite_result, non_negative, positive
from sciengformulary.catalog._sources import ENGINEERING_ACCESSED, lienhard_heat_transfer
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(
    f_D: float,  # noqa: N803
    L: float,  # noqa: N803
    D: float,  # noqa: N803
    rho: float,
    V: float,  # noqa: N803
) -> float:
    positive("f_D", f_D)
    positive("L", L)
    positive("D", D)
    positive("rho", rho)
    non_negative("V", V)
    return finite_result(f_D * (L / D) * rho * V**2 / 2.0)


darcy_weisbach_pressure_drop = FormulaSpec(
    id="fluids.darcy_weisbach_pressure_drop",
    name="Darcy-Weisbach Pressure Drop",
    equation="delta_p = f_D * (L / D) * rho * V^2 / 2",
    description=(
        "Frictional pressure drop of fully developed pipe flow, written with the Darcy "
        "friction factor, the length-to-diameter ratio of the pipe and the dynamic pressure."
    ),
    inputs=(
        VariableSpec(
            name="f_D",
            symbol="f",
            description="Darcy-Weisbach friction factor (not the Fanning factor; f_D = 4 f_F)",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="L",
            symbol="L",
            description="Pipe length over which the pressure drop occurs",
            dimension="L",
            si_unit="m",
        ),
        VariableSpec(
            name="D",
            symbol="D",
            description="Inner diameter of the pipe",
            dimension="L",
            si_unit="m",
        ),
        VariableSpec(
            name="rho",
            symbol=r"\rho",
            description="Fluid density",
            dimension="M L^-3",
            si_unit="kg/m^3",
        ),
        VariableSpec(
            name="V",
            symbol="u_{av}",
            description="Cross-section-average flow speed",
            dimension="L T^-1",
            si_unit="m/s",
        ),
    ),
    output=VariableSpec(
        name="delta_p",
        symbol=r"\Delta p",
        description="Frictional pressure drop",
        dimension="M L^-1 T^-2",
        si_unit="Pa",
    ),
    evaluator=_evaluate,
    references=(
        # The source defines f as the pressure drop divided by (L / D) times the dynamic
        # pressure rho u_av^2 / 2 (eq. 7.33). Derived result: solving that definition for the
        # pressure drop gives delta_p = f (L / D) rho u_av^2 / 2.
        lienhard_heat_transfer("sec. 7.3, eq. (7.33), p. 367", accessed=ENGINEERING_ACCESSED),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"f_D": 0.018, "L": 100.0, "D": 0.3, "V": 3.0, "rho": 1000.0},
            expected=27000.0,
            rel_tol=1e-12,
            note="Hand calculation: f L / D = 6, so 6 * 1000 * 9 / 2 = 27000 Pa.",
        ),
        VerificationCase(
            inputs={"f_D": 0.0136, "L": 50.0, "D": 0.12, "V": 1.924, "rho": 988.0},
            expected=10362.504949333334,
            rel_tol=1e-12,
            note=(
                "Friction factor, diameter, speed and density are those of the worked pipe "
                "example on p. 372; the length is chosen here. 50-digit mpmath value."
            ),
        ),
        VerificationCase(
            inputs={"f_D": 0.018, "L": 100.0, "D": 0.3, "V": 0.0, "rho": 1000.0},
            expected=0.0,
            rel_tol=1e-12,
            abs_tol=1e-15,
            note="Edge case of zero flow speed, where the pressure drop is zero by hand.",
        ),
    ),
    assumptions=(
        "Derived result: the source defines the friction factor through this relation; the "
        "pressure drop form is that definition solved for delta_p.",
        "Steady, fully developed, single-phase flow of a constant-density fluid in a straight "
        "pipe of constant cross-section; only the friction pressure drop is returned, with no "
        "elevation, acceleration or fitting terms.",
        "f_D is the Darcy-Weisbach factor, four times the Fanning factor. It must come from a "
        "correlation valid for the actual Reynolds number and wall roughness; the relation "
        "itself places no Reynolds-number limit.",
        "Dimensionally homogeneous: any consistent unit system works (SI shown). f_D, L, D "
        "and rho must be positive and V not negative, otherwise ValueError is raised.",
    ),
    tags=("Darcy-Weisbach", "pipe flow", "pressure drop", "friction factor", "dynamic pressure"),
)
