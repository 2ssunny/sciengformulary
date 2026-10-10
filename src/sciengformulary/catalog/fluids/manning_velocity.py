"""Manning Open-Channel Velocity (SI units): V = (1 / n) * R_h^(2/3) * S^(1/2)."""

import math

from sciengformulary.catalog._domain import finite_result, non_negative, positive
from sciengformulary.catalog._sources import usgs_report
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(
    n: float,
    R_h: float,  # noqa: N803
    S: float,  # noqa: N803
) -> float:
    positive("n", n)
    positive("R_h", R_h)
    non_negative("S", S)
    return finite_result(R_h ** (2.0 / 3.0) * math.sqrt(S) / n)


manning_velocity = FormulaSpec(
    id="fluids.manning_velocity",
    name="Manning Open-Channel Velocity",
    equation="V = (1 / n) * R_h^(2/3) * S^(1/2)",
    description=(
        "Mean velocity of steady uniform open-channel flow from the Manning roughness "
        "coefficient, the hydraulic radius and the slope of the energy grade line, in SI units."
    ),
    inputs=(
        VariableSpec(
            name="n",
            symbol="n",
            description="Manning roughness coefficient, its numerical value in SI units",
            dimension="T L^(-1/3)",
            si_unit="s/m^(1/3)",
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
        # The source prints the Manning equation V = 1.486 R^(2/3) S^(1/2) / n only in English
        # units (eq. (1), p. B3, where it also states the steady, uniform-flow condition), the
        # Chezy equation V = C sqrt(R S) and the metric relation C = R^(1/6) / n. Derived
        # result: substituting the metric C into the Chezy equation gives
        # V = R^(2/3) S^(1/2) / n, the SI form implemented here (the SI constant is 1; the
        # printed 1.486 is 1 / 0.3048^(1/3) = 1.48592 to its four digits).
        usgs_report(
            "Determination of the Manning Coefficient From Measured Bed Roughness in Natural "
            "Channels",
            ("J. T. Limerinos",),
            "Water-Supply Paper 1898-B",
            1970,
            "https://pubs.usgs.gov/wsp/1898b/report.pdf",
            "p. B3, eq. (1) (English units); p. B7, eq. (3) and p. B8, eq. (6) with the "
            "substitution paragraph and the English-unit result that follows it",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"n": 0.03, "R_h": 0.2859, "S": 0.005236},
            expected=1.046778195811897,
            rel_tol=1e-12,
            note="50-digit mpmath value; an independent library example agrees.",
        ),
        VerificationCase(
            inputs={"n": 0.013, "R_h": 0.5, "S": 0.001},
            expected=1.5323923806378643,
            rel_tol=1e-12,
            note="50-digit mpmath value; equals the Chezy form with C = R_h^(1/6) / n.",
        ),
        VerificationCase(
            inputs={"n": 1.0, "R_h": 1.0, "S": 1.0},
            expected=1.0,
            rel_tol=1e-12,
            note="Exact by hand: every factor equals one.",
        ),
        VerificationCase(
            inputs={"n": 0.03, "R_h": 0.5, "S": 0.0},
            expected=0.0,
            rel_tol=1e-12,
            abs_tol=1e-15,
            note="Edge case of zero slope, where the velocity is zero by hand.",
        ),
    ),
    assumptions=(
        "Derived result: the SI form follows from substituting the metric Chezy coefficient "
        "C = R_h^(1/6) / n into the Chezy equation; the source prints the Manning equation "
        "only in English units with the constant 1.486.",
        "SI units only: R_h in metres, V in m/s and n as its customary value in s/m^(1/3). "
        "The relation is empirical and not dimensionally homogeneous; the English-unit form "
        "needs the factor 1.486 and feet.",
        "Steady, uniform open-channel flow, the condition under which the source states the "
        "equation was developed.",
        "n and R_h must be positive and S not negative, otherwise ValueError is raised; "
        "S = 0 returns zero velocity.",
    ),
    tags=("Manning", "open channel", "uniform flow", "roughness coefficient", "hydraulic radius"),
)
