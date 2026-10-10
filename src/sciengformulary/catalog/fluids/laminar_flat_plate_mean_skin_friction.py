"""Mean Skin-Friction Coefficient of a Laminar Flat-Plate Boundary Layer:
C_f_mean = 1.328 / sqrt(Re_L).
"""

import math

from sciengformulary.catalog._domain import finite_result, positive
from sciengformulary.catalog._sources import ENGINEERING_ACCESSED, lienhard_heat_transfer
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(Re_L: float) -> float:  # noqa: N803 - symbols as written in the source
    # Only a non-positive Reynolds number is rejected. The source gives no sharp bounds: the
    # boundary-layer approximations fail near the leading edge and transition begins over a
    # disturbance-dependent range, so the regime is documented in the assumptions instead.
    positive("Re_L", Re_L)
    return finite_result(1.328 / math.sqrt(Re_L))


laminar_flat_plate_mean_skin_friction = FormulaSpec(
    id="fluids.laminar_flat_plate_mean_skin_friction",
    name="Mean Skin-Friction Coefficient of a Laminar Flat-Plate Boundary Layer",
    equation="C_f_mean = 1.328 / sqrt(Re_L)",
    description=(
        "Skin-friction coefficient averaged over a plate of length L that carries a laminar "
        "boundary layer, from the Blasius solution. It is the plate-average counterpart of "
        "heat_transfer.laminar_flat_plate_skin_friction, which gives the local coefficient "
        "0.664 / sqrt(Re_x) at a distance x from the leading edge; the mean is twice the "
        "local value at x = L."
    ),
    inputs=(
        VariableSpec(
            name="Re_L",
            symbol="Re_L",
            description="Reynolds number based on plate length and free-stream speed",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="C_f_mean",
        symbol=r"\overline{C_f}",
        description="Mean skin-friction coefficient tau_w / (rho u_inf^2 / 2), one wetted side",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # Stated: the book integrates the local coefficient 0.664 / sqrt(Re_x) over the plate
        # length to get 1.328 / sqrt(Re_L) (eq. (6.34), which follows the local coefficient
        # of eq. (6.33)). Example 6.3 is a worked case; the transition remarks in sec. 6.1 are the
        # source of the validity note below.
        lienhard_heat_transfer(
            "sec. 6.2, eq. (6.34) (local eq. (6.33)), p. 292; Example 6.3, pp. 292-293; "
            "transition remarks sec. 6.1, p. 276",
            accessed=ENGINEERING_ACCESSED,
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"Re_L": 47619.0},
            expected=0.00609,
            rel_tol=0.001,
            note="Worked Example 6.3 of the reference prints Re_L = 47 619 and C_f = 0.00609; "
            "the tolerance covers its three-digit rounding.",
        ),
        VerificationCase(
            inputs={"Re_L": 47619.0},
            expected=0.006085663565733899,
            rel_tol=1e-12,
            note="50-digit mpmath evaluation of 1.328 / sqrt(47619), full precision of the "
            "Example 6.3 case.",
        ),
        VerificationCase(
            inputs={"Re_L": 10000.0},
            expected=0.01328,
            rel_tol=1e-12,
            note="Hand calculation: 1.328 / 100 = 0.01328.",
        ),
        VerificationCase(
            inputs={"Re_L": 4.0},
            expected=0.664,
            rel_tol=1e-12,
            note="Hand calculation: 1.328 / 2 = 0.664 (outside the boundary-layer range; an "
            "arithmetic check only).",
        ),
        VerificationCase(
            inputs={"Re_L": 300000.0},
            expected=0.0024245851878895355,
            rel_tol=1e-12,
            note="50-digit mpmath evaluation of 1.328 / sqrt(3e5), near the transition onset.",
        ),
    ),
    assumptions=(
        "Laminar boundary layer on a smooth flat plate at constant free-stream speed, zero "
        "pressure gradient and constant fluid properties; the coefficient is for one wetted "
        "side, averaged over the plate length.",
        "The boundary-layer approximations fail very close to the leading edge, below about "
        "Re_x of 600 there. The laminar result holds only up to the onset of transition, which "
        "the source places between Re_x of 2e5 and 5e5 for ordinary conditions and as low as "
        "3e4 in disturbed flow. The evaluator does not enforce a regime limit; only "
        "Re_L > 0 is required, so the caller must check that the flow is laminar.",
        "Incompressible flow.",
    ),
    tags=("skin friction", "Blasius", "flat plate", "boundary layer", "laminar", "drag"),
)
