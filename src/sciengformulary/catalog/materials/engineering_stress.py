"""Engineering (Nominal) Stress: sigma_n = F / A0."""

from sciengformulary.catalog._sources import (
    doe_fundamentals_handbook,
    openstax_university_physics,
)
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(F: float, A0: float) -> float:  # noqa: N803 - symbols as written in the source
    return F / A0


engineering_stress = FormulaSpec(
    id="materials.engineering_stress",
    name="Engineering (Nominal) Stress",
    equation="sigma_n = F / A0",
    description="Axial force divided by the original cross-sectional area.",
    inputs=(
        VariableSpec(
            name="F",
            symbol="F",
            description="Axial force, tension positive",
            dimension="M L T^-2",
            si_unit="N",
        ),
        VariableSpec(
            name="A0",
            symbol="A_0",
            description="Original (undeformed) cross-sectional area",
            dimension="L^2",
            si_unit="m^2",
        ),
    ),
    output=VariableSpec(
        name="sigma_n",
        symbol=r"\sigma_n",
        description="Engineering stress",
        dimension="M L^-1 T^-2",
        si_unit="Pa",
    ),
    evaluator=_evaluate,
    references=(
        # The source names it tensile stress, F_perp / A.
        openstax_university_physics(
            1,
            "12-3-stress-strain-and-elastic-modulus",
            "sec. 12.3, eq. (12.34)",
        ),
        # The handbook defines stress as force per cross-sectional area; the 'original area'
        # qualifier in the assumptions rests on the OpenStax reference, not this one.
        doe_fundamentals_handbook(
            "DOE-HDBK-1017/1-93",
            "Module 2 Properties of Metals, 'Stress' summary p. 6; eq. (2-4), p. 12",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"F": 1000.0, "A0": 0.0001},
            expected=10000000.0,
            rel_tol=1e-12,
            note="Hand calculation: 1000 / 1e-4 = 1e7 Pa.",
        ),
    ),
    assumptions=(
        "Force uniformly distributed over the section, away from load points and notches.",
        "A0 is the area measured before loading, so once necking reduces the section the value "
        "falls below the true stress.",
    ),
    tags=("stress", "nominal stress", "engineering stress", "tensile test"),
)
