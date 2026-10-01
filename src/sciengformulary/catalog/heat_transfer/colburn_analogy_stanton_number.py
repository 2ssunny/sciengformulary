"""Colburn Analogy: St = (C_f / 2) * Pr^(-2/3)."""

from sciengformulary.catalog._sources import lienhard_heat_transfer
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(C_f: float, Pr: float) -> float:  # noqa: N803 - symbols as written in the source
    return 0.5 * C_f * Pr ** (-2.0 / 3.0)


colburn_analogy_stanton_number = FormulaSpec(
    id="heat_transfer.colburn_analogy_stanton_number",
    name="Colburn Analogy",
    equation="St = (C_f / 2) * Pr^(-2/3)",
    description=(
        "Estimate of the Stanton number from the skin-friction coefficient, extending Reynolds' "
        "analogy to Prandtl numbers other than one."
    ),
    inputs=(
        VariableSpec(
            name="C_f",
            symbol="C_f",
            description="Skin-friction coefficient",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="Pr",
            symbol="Pr",
            description="Prandtl number",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="St",
        symbol="St",
        description="Stanton number",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # The source writes St = (C_f / 2) Pr^(-2/3) = (f / 8) Pr^(-2/3) for pipes.
        lienhard_heat_transfer("sec. 7.3, eq. (7.36)"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"C_f": 0.004, "Pr": 0.7},
            expected=0.0025368685764074307,
            rel_tol=1e-12,
            note="Independent 40-digit decimal evaluation of 0.002 * 0.7^(-2/3).",
        ),
    ),
    assumptions=(
        "Empirical analogy between heat and momentum transfer; it applies to skin friction, "
        "not to form drag, so it fails where the flow separates.",
        "Reduces to St = C_f / 2 (Reynolds analogy) at Pr = 1.",
    ),
    tags=("Colburn analogy", "Reynolds analogy", "Stanton number", "skin friction"),
)
