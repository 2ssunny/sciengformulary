"""Churchill-Bernstein Correlation for a Cylinder in Crossflow.

Nu_D = 0.3 + 0.62 Re_D^(1/2) Pr^(1/3) / (1 + (0.4/Pr)^(2/3))^(1/4)
       * (1 + (Re_D/282000)^(5/8))^(4/5).
"""

from sciengformulary.catalog._domain import finite_result, positive
from sciengformulary.catalog._sources import ENGINEERING_ACCESSED, lienhard_heat_transfer
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase

_PECLET_MIN = 0.2


def _evaluate(Re_D: float, Pr: float) -> float:  # noqa: N803 - symbols as written in the source
    positive("Re_D", Re_D)
    positive("Pr", Pr)
    if Re_D * Pr < _PECLET_MIN:
        raise ValueError(
            f"Re_D * Pr (the Peclet number) must be at least {_PECLET_MIN}, got {Re_D * Pr!r}."
        )
    # Some libraries (for example the Python "ht" package) quote Re_D * Pr > 0.4 from the
    # original paper; the textbook states 0.2 and that is used here.
    prandtl_factor = (1.0 + (0.4 / Pr) ** (2.0 / 3.0)) ** 0.25
    reynolds_factor = (1.0 + (Re_D / 282000.0) ** (5.0 / 8.0)) ** 0.8
    return finite_result(
        0.3 + 0.62 * Re_D**0.5 * Pr ** (1.0 / 3.0) / prandtl_factor * reynolds_factor
    )


churchill_bernstein_cylinder_nusselt = FormulaSpec(
    id="heat_transfer.churchill_bernstein_cylinder_nusselt",
    name="Churchill-Bernstein Cylinder Crossflow Correlation",
    equation=(
        "Nu_D = 0.3 + 0.62 * Re_D^(1/2) * Pr^(1/3) / (1 + (0.4 / Pr)^(2/3))^(1/4) "
        "* (1 + (Re_D / 282000)^(5/8))^(4/5)"
    ),
    description=(
        "Average Nusselt number of a single long circular cylinder in a uniform crossflow, "
        "fitted over the whole range of available data for Re_D Pr of at least 0.2. "
        "It is an external-flow correlation, not a pipe-flow one."
    ),
    inputs=(
        VariableSpec(
            name="Re_D",
            symbol="Re_D",
            description="Reynolds number based on the cylinder diameter and free-stream speed",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="Pr",
            symbol="Pr",
            description="Prandtl number, with Re_D * Pr at least 0.2",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="Nu_D",
        symbol="Nu_D",
        description="Average Nusselt number h D / k based on the cylinder diameter",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        lienhard_heat_transfer("sec. 7.6, eq. (7.65), pp. 390-391", accessed=ENGINEERING_ACCESSED),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"Re_D": 6071.0, "Pr": 0.7},
            expected=40.637085941249744,
            rel_tol=1e-12,
            note="Evaluated with 50-digit arithmetic (mpmath); an independent library agrees.",
        ),
        VerificationCase(
            inputs={"Re_D": 100000.0, "Pr": 7.0},
            expected=507.5910225632826,
            rel_tol=1e-12,
            note="High Reynolds number with a water-like Prandtl number; 50-digit arithmetic.",
        ),
        VerificationCase(
            inputs={"Re_D": 0.28571428571428575, "Pr": 0.7},
            expected=0.5581686439080673,
            rel_tol=1e-12,
            note="Boundary Re_D * Pr = 0.2 (Re_D = 0.2 / 0.7); 50-digit arithmetic.",
        ),
    ),
    assumptions=(
        "Single long circular cylinder normal to a uniform stream, with the average Nusselt "
        "number over the whole circumference.",
        "Re_D * Pr (the Peclet number) must be at least 0.2; the evaluator raises ValueError "
        "below that. The textbook gives a different relation for smaller Peclet numbers.",
        "All properties are evaluated at the film temperature, the mean of the wall and free-"
        "stream temperatures.",
        "The textbook notes that the correlation underpredicts by about 20 % for 4e4 < Re_D < 4e5.",
        "Dimensionless; valid in any consistent unit system.",
    ),
    tags=("Nusselt number", "cylinder", "crossflow", "Churchill-Bernstein", "external flow"),
)
