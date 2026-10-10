"""Chezy Coefficient from Manning Roughness (SI units): C = R_h^(1/6) / n."""

from sciengformulary.catalog._domain import finite_result, positive
from sciengformulary.catalog._sources import usgs_report
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(
    n: float,
    R_h: float,  # noqa: N803
) -> float:
    positive("n", n)
    positive("R_h", R_h)
    return finite_result(R_h ** (1.0 / 6.0) / n)


chezy_coefficient_from_manning = FormulaSpec(
    id="fluids.chezy_coefficient_from_manning",
    name="Chezy Coefficient from Manning Roughness",
    equation="C = R_h^(1/6) / n",
    description=(
        "Chezy resistance coefficient of an open channel obtained from the Manning roughness "
        "coefficient and the hydraulic radius, in SI units."
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
    ),
    output=VariableSpec(
        name="C",
        symbol="C",
        description="Chezy resistance coefficient",
        dimension="L^(1/2) T^-1",
        si_unit="m^(1/2)/s",
    ),
    evaluator=_evaluate,
    references=(
        # The source prints the metric-units form C = R^(1/6) / n (the Chezy coefficient varies
        # as the sixth root of the hydraulic radius); the symbols are the same up to renaming.
        usgs_report(
            "Determination of the Manning Coefficient From Measured Bed Roughness in Natural "
            "Channels",
            ("J. T. Limerinos",),
            "Water-Supply Paper 1898-B",
            1970,
            "https://pubs.usgs.gov/wsp/1898b/report.pdf",
            "p. B8, eq. (6) ('metric units')",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"n": 0.05, "R_h": 5.0},
            expected=26.15320972023661,
            rel_tol=1e-12,
            note="50-digit mpmath value of 5^(1/6) / 0.05; an independent library example agrees.",
        ),
        VerificationCase(
            inputs={"n": 0.013, "R_h": 0.25},
            expected=61.05388661416152,
            rel_tol=1e-12,
            note="50-digit mpmath value of 0.25^(1/6) / 0.013.",
        ),
        VerificationCase(
            inputs={"n": 0.04, "R_h": 1.0},
            expected=25.0,
            rel_tol=1e-12,
            note="Exact by hand: R_h = 1 m makes the sixth root 1, so C = 1 / 0.04 = 25.",
        ),
    ),
    assumptions=(
        "SI units only: R_h in metres and n as its customary value in s/m^(1/3). The relation "
        "is not dimensionally homogeneous and does not hold in other unit systems.",
        "The English-unit counterpart carries a factor of about 1.486 (as printed in the "
        "source) and must not be mixed with this form.",
        "Applies to the uniform-flow setting of the source's Manning and Chezy equations; "
        "n and R_h must be positive, otherwise ValueError is raised.",
    ),
    tags=("Chezy", "Manning", "open channel", "roughness", "hydraulic radius"),
)
