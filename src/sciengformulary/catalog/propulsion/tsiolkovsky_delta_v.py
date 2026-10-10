"""Tsiolkovsky Rocket Equation (Velocity Increment): delta_v = c * ln(m0 / mf)."""

import math

from sciengformulary.catalog._domain import finite_result, positive
from sciengformulary.catalog._sources import nasa_technical_report
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(c: float, m0: float, mf: float) -> float:
    positive("c", c)
    positive("m0", m0)
    positive("mf", mf)
    if mf > m0:
        raise ValueError(f"mf must not exceed m0, got m0={m0!r}, mf={mf!r}.")
    ratio = m0 / mf
    if not math.isfinite(ratio):
        # For a mass ratio beyond the float range, ln(m0) - ln(mf) still gives the logarithm.
        log_ratio = math.log(m0) - math.log(mf)
    elif ratio < 2.0:
        # ln(m0 / mf) = log1p((m0 - mf) / mf); m0 - mf is exact for mf <= m0 <= 2 mf, so the
        # logarithm keeps its accuracy when mf is within a few ulps of m0.
        log_ratio = math.log1p((m0 - mf) / mf)
    else:
        log_ratio = math.log(ratio)
    return finite_result(c * log_ratio)


tsiolkovsky_delta_v = FormulaSpec(
    id="propulsion.tsiolkovsky_delta_v",
    name="Tsiolkovsky Rocket Equation (Velocity Increment)",
    equation="delta_v = c * ln(m0 / mf)",
    description=(
        "Ideal velocity increment of a rocket from its effective exhaust velocity and the "
        "ratio of initial to final mass, with no external forces. This is the inverse form "
        "of propulsion.rocket_equation_final_mass, which gives the burnout mass from a "
        "velocity increment. For the exhaust velocity itself see "
        "propulsion.effective_exhaust_velocity."
    ),
    inputs=(
        VariableSpec(
            name="c",
            symbol="c",
            description="Effective exhaust velocity",
            dimension="L T^-1",
            si_unit="m/s",
        ),
        VariableSpec(
            name="m0",
            symbol="m_0",
            description="Initial mass (before the burn)",
            dimension="M",
            si_unit="kg",
        ),
        VariableSpec(
            name="mf",
            symbol="m_f",
            description="Final (burnout) mass",
            dimension="M",
            si_unit="kg",
        ),
    ),
    output=VariableSpec(
        name="delta_v",
        symbol=r"\Delta v",
        description="Velocity increment",
        dimension="L T^-1",
        si_unit="m/s",
    ),
    evaluator=_evaluate,
    references=(
        # Derived: the report gives final mass / initial mass = exp(-delta_v / c); taking the
        # logarithm of the reciprocal gives delta_v = c * ln(m0 / mf).
        nasa_technical_report(
            "An Analytical Optimization of Electric Propulsion Orbit Transfer Vehicles",
            ("S. R. Oleson",),
            "NASA CR-191129",
            1993,
            "https://ntrs.nasa.gov/citations/19930017871",
            "p. 3 (text before eq. 3) and eq. (5)",
        ),
        # Stated with a loss factor: v_bo = C_vc * g * (I_s)_oa * ln(1 / (1 - R_p)), where
        # 1 / (1 - R_p) = m0 / mf and C_vc corrects for gravity and drag. With C_vc = 1 and
        # c = g * I_s (eq. (1-31a)) this is the equation above.
        nasa_technical_report(
            "Design of Liquid Propellant Rocket Engines",
            ("D. K. Huzel", "D. H. Huang"),
            "NASA SP-125",
            1967,
            "https://ntrs.nasa.gov/citations/19710019929",
            "sec. 1.3, eq. (1-30), p. 11",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"c": 3000.0, "m0": 1000.0, "mf": 500.0},
            expected=2079.441541679836,
            rel_tol=1e-12,
            note="50-digit mpmath evaluation of 3000 * ln 2 (the mass halves).",
        ),
        VerificationCase(
            inputs={"c": 4400.0, "m0": 5000.0, "mf": 1200.0},
            expected=6279.311964816641,
            rel_tol=1e-12,
            note="50-digit mpmath evaluation of 4400 * ln(5000/1200), propellant fraction 0.76.",
        ),
        VerificationCase(
            inputs={"c": 3000.0, "m0": 800.0, "mf": 800.0},
            expected=0.0,
            rel_tol=1e-12,
            abs_tol=1e-15,
            note="Edge case: no propellant burned, ln 1 = 0.",
        ),
    ),
    assumptions=(
        "Derived result: the cited report states final mass / initial mass = "
        "exp(-delta_v / c); taking the logarithm gives delta_v = c * ln(m0 / mf). The second "
        "reference prints the same relation with a trajectory-loss factor C_vc that equals 1 "
        "when gravity and drag losses are ignored.",
        "No gravity, drag or thrust-direction losses, and a constant effective exhaust velocity.",
        "c, m0 and mf must be positive with mf <= m0 (a mass gain is not a rocket burn).",
    ),
    tags=("rocket equation", "delta-v", "Tsiolkovsky", "mass ratio", "propulsion"),
)
