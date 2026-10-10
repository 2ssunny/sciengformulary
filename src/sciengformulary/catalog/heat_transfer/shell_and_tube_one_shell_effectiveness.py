"""One-Shell-Pass Shell-and-Tube Effectiveness:
eps = 2 / (1 + C_r + sqrt(1 + C_r^2) * coth(NTU * sqrt(1 + C_r^2) / 2)).
"""

import math

from sciengformulary.catalog._domain import finite, non_negative
from sciengformulary.catalog._sources import ENGINEERING_ACCESSED, lienhard_heat_transfer
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(
    NTU: float,  # noqa: N803
    C_r: float,  # noqa: N803
) -> float:
    non_negative("NTU", NTU)
    if not 0 <= finite("C_r", C_r) <= 1:
        raise ValueError(f"C_r must lie in [0, 1], got {C_r!r}.")
    s = math.sqrt(1 + C_r * C_r)
    # coth(G / 2) = (1 + exp(-G)) / (1 - exp(-G)) with G = NTU * s. Writing t = tanh(G / 2)
    # turns 2 / (1 + C_r + s / t) into 2 t / ((1 + C_r) t + s), which has no division by t
    # and so returns the limit 0 at NTU = 0.
    t = math.tanh(NTU * s / 2)
    return 2 * t / ((1 + C_r) * t + s)


shell_and_tube_one_shell_effectiveness = FormulaSpec(
    id="heat_transfer.shell_and_tube_one_shell_effectiveness",
    name="One-Shell-Pass Shell-and-Tube Effectiveness",
    equation=(
        "eps = 2 / (1 + C_r + sqrt(1 + C_r^2) * (1 + exp(-NTU * sqrt(1 + C_r^2))) "
        "/ (1 - exp(-NTU * sqrt(1 + C_r^2)))); eps = 0 for NTU = 0"
    ),
    description=(
        "Effectiveness of a shell-and-tube heat exchanger with one shell pass and two tube "
        "passes, as a function of the number of transfer units and the capacity-rate ratio."
    ),
    inputs=(
        VariableSpec(
            name="NTU",
            symbol="NTU",
            description="Number of transfer units, U A / C_min",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="C_r",
            symbol="C_r",
            description="Capacity-rate ratio C_min / C_max (0 to 1)",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="eps",
        symbol=r"\varepsilon",
        description="Effectiveness, Q / (C_min * (T_h,in - T_c,in))",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # The source prints 2 / [(1 + R) + sqrt(1 + R^2) coth(Gamma / 2)] with R = Cmin/Cmax
        # and Gamma = NTU sqrt(1 + R^2). The exp form in the equation field is the identity
        # coth(Gamma / 2) = (1 + exp(-Gamma)) / (1 - exp(-Gamma)); the evaluator uses the
        # equivalent tanh form. At NTU = 0 both are 0/0 (coth is unbounded); the limit of
        # eps as NTU tends to 0 is 0, which is the derived branch.
        lienhard_heat_transfer(
            "sec. 3.3, Table 3.1 (one shell pass, two tube passes), p. 125",
            accessed=ENGINEERING_ACCESSED,
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"NTU": 5.0, "C_r": 0.7},
            expected=0.6834977044311439,
            rel_tol=1e-12,
            note="50-digit mpmath evaluation of the exponential form.",
        ),
        VerificationCase(
            inputs={"NTU": 1.0, "C_r": 0.0},
            expected=0.6321205588285577,
            rel_tol=1e-12,
            note="C_r = 0 reduces the formula to 1 - exp(-NTU) = 1 - exp(-1); 50-digit mpmath.",
        ),
        VerificationCase(
            inputs={"NTU": 2.0, "C_r": 1.0},
            expected=0.5568096679436695,
            rel_tol=1e-12,
            note="Balanced flow, C_r = 1; 50-digit mpmath evaluation.",
        ),
    ),
    assumptions=(
        "Derived result: at NTU = 0 the stated form is undefined (coth is unbounded). The "
        "limit of the effectiveness as NTU tends to 0 is 0, and the evaluator returns it at "
        "NTU = 0. The evaluator uses the identity coth(x) = 1 / tanh(x) written as "
        "2 t / ((1 + C_r) t + sqrt(1 + C_r^2)) with t = tanh(NTU sqrt(1 + C_r^2) / 2).",
        "Steady operation, no heat loss to the surroundings, negligible axial conduction.",
        "Constant overall coefficient U and constant specific heats of both streams.",
        "One shell pass and two tube passes (the source's configuration); the source's label "
        "is used, not the more general two-or-more-tube-pass wording some libraries use.",
        "C_r = C_min / C_max, so 0 <= C_r <= 1, and NTU >= 0 with NTU = U A / C_min; "
        "otherwise ValueError is raised.",
        "Dimensionless: no unit system enters.",
    ),
    tags=("heat exchanger", "effectiveness", "shell and tube", "effectiveness-NTU"),
)
