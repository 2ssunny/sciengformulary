"""Chezy Open-Channel Velocity: V = C * sqrt(R_h * S)."""

import math

from sciengformulary.catalog._domain import finite_result, non_negative, positive
from sciengformulary.catalog._sources import usgs_report
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(
    C: float,  # noqa: N803
    R_h: float,  # noqa: N803
    S: float,  # noqa: N803
) -> float:
    positive("C", C)
    positive("R_h", R_h)
    non_negative("S", S)
    return finite_result(C * math.sqrt(R_h * S))


chezy_velocity = FormulaSpec(
    id="fluids.chezy_velocity",
    name="Chezy Open-Channel Velocity",
    equation="V = C * sqrt(R_h * S)",
    description=(
        "Mean velocity of steady uniform open-channel flow from the Chezy resistance "
        "coefficient, the hydraulic radius and the slope of the energy grade line."
    ),
    inputs=(
        VariableSpec(
            name="C",
            symbol="C",
            description="Chezy resistance coefficient (dimensional)",
            dimension="L^(1/2) T^-1",
            si_unit="m^(1/2)/s",
        ),
        VariableSpec(
            name="R_h",
            symbol="R",
            description="Hydraulic radius (flow area divided by wetted perimeter)",
            dimension="L",
            si_unit="m",
        ),
        VariableSpec(
            name="S",
            symbol="S",
            description="Slope of the energy grade line (equal to the bed slope in uniform flow)",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="V",
        symbol="V",
        description="Mean flow velocity",
        dimension="L T^-1",
        si_unit="m/s",
    ),
    evaluator=_evaluate,
    references=(
        # The source prints V = C sqrt(R S) with S the energy slope (eq. (3), p. B7). The
        # steady, uniform-flow sentence on p. B3 introduces the Manning form of the same
        # resistance law, so it is cited below only for the flow condition, not for this equation.
        usgs_report(
            "Determination of the Manning Coefficient From Measured Bed Roughness in Natural "
            "Channels",
            ("J. T. Limerinos",),
            "Water-Supply Paper 1898-B",
            1970,
            "https://pubs.usgs.gov/wsp/1898b/report.pdf",
            "p. B7, eq. (3)",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"C": 26.153, "R_h": 5.0, "S": 0.001},
            expected=1.8492963648371776,
            rel_tol=1e-12,
            note="50-digit mpmath value of 26.153 * sqrt(0.005); an independent library agrees.",
        ),
        VerificationCase(
            inputs={"C": 50.0, "R_h": 2.5, "S": 0.0004},
            expected=1.5811388300841898,
            rel_tol=1e-12,
            note="Hand check: R_h * S = 0.001, so V = 50 * sqrt(0.001) = 1.58113883...",
        ),
        VerificationCase(
            inputs={"C": 26.153, "R_h": 5.0, "S": 0.0},
            expected=0.0,
            rel_tol=1e-12,
            abs_tol=1e-15,
            note="Edge case of zero slope, where the velocity is zero by hand.",
        ),
    ),
    assumptions=(
        "Steady, uniform open-channel flow. The source states this condition for the Manning "
        "equation (p. B3), the same resistance law with C = R_h^(1/6) / n; it is applied here "
        "to the Chezy form as well.",
        "C is a dimensional coefficient (m^(1/2)/s) and must be supplied in SI units together "
        "with R_h in metres and V in m/s; the relation is not unit-free.",
        "S is the slope of the energy grade line, which equals the bed slope in uniform flow.",
        "C and R_h must be positive and S not negative, otherwise ValueError is raised; "
        "S = 0 returns zero velocity.",
    ),
    tags=("Chezy", "open channel", "uniform flow", "hydraulic radius", "energy slope"),
)
