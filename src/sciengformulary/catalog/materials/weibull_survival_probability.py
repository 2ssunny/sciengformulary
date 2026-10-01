"""Weibull Survival Probability: P_s = exp(-(sigma / sigma_0)^m)."""

import math

from sciengformulary.catalog._sources import roylance
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(sigma: float, sigma_0: float, m: float) -> float:
    return math.exp(-((sigma / sigma_0) ** m))


weibull_survival_probability = FormulaSpec(
    id="materials.weibull_survival_probability",
    name="Weibull Survival Probability",
    equation="P_s = exp(-(sigma / sigma_0)^m)",
    description=(
        "Probability that a brittle specimen survives a stress, in the two-parameter Weibull model."
    ),
    inputs=(
        VariableSpec(
            name="sigma",
            symbol=r"\sigma",
            description="Applied stress",
            dimension="M L^-1 T^-2",
            si_unit="Pa",
        ),
        VariableSpec(
            name="sigma_0",
            symbol=r"\sigma_0",
            description="Characteristic strength (survival probability 1/e)",
            dimension="M L^-1 T^-2",
            si_unit="Pa",
        ),
        VariableSpec(
            name="m",
            symbol="m",
            description="Weibull modulus",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="P_s",
        symbol="P_s",
        description="Survival probability",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        roylance("Statistics of Fracture", "mit3_11f99_stat-1", 2001, "eq. (6)"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"sigma": 0.8, "sigma_0": 1.0, "m": 10.0},
            expected=0.8981895233920782,
            rel_tol=1e-12,
            note="Independent 40-digit decimal evaluation of exp(-0.8^10).",
        ),
        VerificationCase(
            inputs={"sigma": 75.0, "sigma_0": 75.0, "m": 10.0},
            expected=0.36787944117144233,
            rel_tol=1e-12,
            note="At sigma = sigma_0 the survival probability is 1/e for any m.",
        ),
    ),
    assumptions=(
        "sigma_0 and m are fitted for the same specimen volume and stress state as the "
        "component; size effects need the volume-scaled form, which is not implemented.",
        "Uniform stress; brittle failure controlled by the most severe flaw.",
    ),
    tags=("Weibull", "brittle fracture", "reliability", "ceramics", "statistics"),
)
