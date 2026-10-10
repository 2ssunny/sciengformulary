"""Laminar Pipe Darcy Friction Factor: f_D = 64 / Re."""

from sciengformulary.catalog._domain import finite_result, positive
from sciengformulary.catalog._sources import ENGINEERING_ACCESSED, lienhard_heat_transfer
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase

# Convention, not a printed limit: the source applies its turbulent correlations from
# Re_D = 2300 upward (p. 369), and 2300 is taken here as the conventional onset of turbulence.
_RE_LAMINAR_MAX = 2300.0


def _evaluate(Re: float) -> float:  # noqa: N803
    positive("Re", Re)
    if Re > _RE_LAMINAR_MAX:
        raise ValueError(
            f"Re must not exceed 2300, the conventional onset of turbulence, got {Re!r}."
        )
    return finite_result(64.0 / Re)


laminar_darcy_friction_factor = FormulaSpec(
    id="fluids.laminar_darcy_friction_factor",
    name="Laminar Pipe Darcy Friction Factor",
    equation="f_D = 64 / Re",
    description=(
        "Darcy friction factor of fully developed laminar flow in a circular pipe, which "
        "depends only on the diameter-based Reynolds number."
    ),
    inputs=(
        VariableSpec(
            name="Re",
            symbol="Re_D",
            description="Reynolds number based on pipe diameter and average speed",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="f_D",
        symbol="f",
        description="Darcy-Weisbach friction factor",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # The laminar branch of the source's friction-factor chart is labelled f = 64 / Re_D.
        lienhard_heat_transfer("sec. 7.3, Fig. 7.6, p. 370", accessed=ENGINEERING_ACCESSED),
        # Independent route: the Hagen-Poiseuille profile (7.14) with u_max = 2 u_av (7.15)
        # gives a pressure gradient -dp/dx = 8 mu u_av / R^2, i.e. delta_p = 32 mu L u_av / D^2.
        # Inserted in the friction-factor definition (7.33) this gives f = 64 / Re_D.
        lienhard_heat_transfer(
            "sec. 7.2, eqs. (7.14)-(7.15), p. 358; sec. 7.3, eq. (7.33), p. 367",
            accessed=ENGINEERING_ACCESSED,
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"Re": 128.0},
            expected=0.5,
            rel_tol=1e-12,
            note="Exact by hand: 64 / 128 = 0.5.",
        ),
        VerificationCase(
            inputs={"Re": 2000.0},
            expected=0.032,
            rel_tol=1e-12,
            note="Exact by hand: 64 / 2000 = 0.032.",
        ),
        VerificationCase(
            inputs={"Re": 2300.0},
            expected=0.02782608695652174,
            rel_tol=1e-12,
            note="Upper end of the accepted range; 50-digit mpmath value of 64 / 2300.",
        ),
        VerificationCase(
            inputs={"Re": 1.0},
            expected=64.0,
            rel_tol=1e-12,
            note="Exact by hand: 64 / 1 = 64.",
        ),
    ),
    assumptions=(
        "Fully developed, steady, incompressible laminar flow of a Newtonian fluid in a "
        "circular pipe; independent of wall roughness. Darcy convention (f_D = 4 f_Fanning).",
        "Re must be positive and at most 2300, otherwise ValueError is raised. The limit 2300 "
        "is a convention for the onset of turbulence, not a laminar limit printed by the "
        "source: the source applies its turbulent correlations from Re_D = 2300 upward (p. 369) "
        "and prints no numerical upper limit for laminar flow.",
        "Derived result: f = 64 / Re also follows from the Hagen-Poiseuille velocity profile "
        "and the definition of the friction factor, as noted next to the reference.",
        "Not valid in the entrance region, where the flow is not yet fully developed.",
    ),
    tags=("friction factor", "laminar", "Hagen-Poiseuille", "pipe flow", "Darcy-Weisbach"),
)
