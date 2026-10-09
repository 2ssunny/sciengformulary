"""Thrust-to-Weight Ratio: TW = F / (m * g0)."""

from sciengformulary.catalog._domain import finite_result, positive
from sciengformulary.catalog._sources import ENGINEERING_ACCESSED, nasa_glenn
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(F: float, m: float, g0: float) -> float:  # noqa: N803 - symbols as in the source
    positive("F", F)
    positive("m", m)
    positive("g0", g0)
    return finite_result(F / (m * g0))


thrust_to_weight_ratio = FormulaSpec(
    id="propulsion.thrust_to_weight_ratio",
    name="Thrust-to-Weight Ratio",
    equation="TW = F / (m * g0)",
    description=(
        "Ratio of thrust to the reference weight m * g0 of the vehicle. For a vehicle in a "
        "force balance it equals the acceleration divided by gravity. It compares thrust with "
        "weight rather than with propellant flow (propulsion.specific_impulse) or chamber force "
        "(propulsion.thrust_coefficient)."
    ),
    inputs=(
        VariableSpec(
            name="F",
            symbol="F",
            description="Thrust",
            dimension="M L T^-2",
            si_unit="N",
        ),
        VariableSpec(
            name="m",
            symbol="m",
            description="Vehicle mass",
            dimension="M",
            si_unit="kg",
        ),
        VariableSpec(
            name="g0",
            symbol="g_0",
            description="Standard gravity used to define the reference weight (9.80665 m/s^2)",
            dimension="L T^-2",
            si_unit="m/s^2",
        ),
    ),
    output=VariableSpec(
        name="TW",
        symbol="F/W",
        description="Thrust-to-weight ratio",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # Stated: F/W is the thrust-to-weight ratio and W = m * g (F/W = a/g for a force
        # balance); g is set to the standard value g0 as the reference weight. The page quotes
        # g as 9.8 m/s^2 or 32.2 ft/s^2; g0 is an input here.
        nasa_glenn(
            "Thrust to Weight Ratio",
            "thrust-to-weight-ratio",
            2025,
            locator="Thrust to Weight Ratio",
            accessed=ENGINEERING_ACCESSED,
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"F": 34000.0, "m": 1000.0, "g0": 9.80665},
            expected=3.467035124124956,
            rel_tol=1e-12,
            note="50-digit mpmath evaluation of 34000 / (1000 * 9.80665).",
        ),
        VerificationCase(
            inputs={"F": 9806.65, "m": 1000.0, "g0": 9.80665},
            expected=1.0,
            rel_tol=1e-12,
            note="Edge case: thrust equal to the reference weight 1000 * 9.80665 N gives 1.",
        ),
        VerificationCase(
            inputs={"F": 1200000.0, "m": 50000.0, "g0": 9.80665},
            expected=2.4473189111470277,
            rel_tol=1e-12,
            note="50-digit mpmath evaluation of 1.2e6 / (5e4 * 9.80665), a launch vehicle.",
        ),
    ),
    assumptions=(
        "Weight is evaluated as m * g0 (the sea-level reference), the usual convention for "
        "quoting thrust-to-weight ratios, not the local weight.",
        "Constant mass; the ratio changes as propellant is consumed.",
        "F, m and g0 must be positive (a coasting vehicle with zero thrust is outside the "
        "domain of this entry).",
    ),
    tags=("thrust to weight", "T/W", "performance", "propulsion"),
)
