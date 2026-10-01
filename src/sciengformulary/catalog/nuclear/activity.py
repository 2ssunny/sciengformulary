"""Radioactive Activity: A = lambda * N."""

from sciengformulary.catalog._sources import openstax_university_physics
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(
    decay_constant: float,
    N: float,  # noqa: N803
) -> float:
    return decay_constant * N


activity = FormulaSpec(
    id="nuclear.activity",
    name="Radioactive Activity",
    equation="A = lambda * N",
    description="Decay rate of a radioactive sample.",
    inputs=(
        VariableSpec(
            name="decay_constant",
            symbol=r"\lambda",
            description="Decay constant",
            dimension="T^-1",
            si_unit="1/s",
        ),
        VariableSpec(
            name="N",
            symbol="N",
            description="Number of undecayed nuclei",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="A",
        symbol="A",
        description="Activity (decays per unit time)",
        dimension="T^-1",
        si_unit="Bq",
    ),
    evaluator=_evaluate,
    references=(
        openstax_university_physics(3, "10-3-radioactive-decay", "sec. 10.3, eq. (10.17)"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"decay_constant": 0.1, "N": 1000.0},
            expected=100.0,
            rel_tol=1e-12,
            note="Hand calculation: 0.1 * 1000 = 100 decays/s.",
        ),
    ),
    assumptions=(
        "Single radionuclide; for chains, sum the activities of each member.",
    ),
    tags=("activity", "becquerel", "decay rate", "nuclear"),
)
