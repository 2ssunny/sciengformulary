"""Von Mises Equivalent Stress (Principal Stresses)."""

import math

from sciengformulary.catalog._sources import roylance
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(sigma_1: float, sigma_2: float, sigma_3: float) -> float:
    return math.sqrt(
        0.5 * ((sigma_1 - sigma_2) ** 2 + (sigma_2 - sigma_3) ** 2 + (sigma_3 - sigma_1) ** 2)
    )


von_mises_stress_principal = FormulaSpec(
    id="materials.von_mises_stress_principal",
    name="Von Mises Equivalent Stress (Principal Stresses)",
    equation="sigma_vm = sqrt(((s1 - s2)^2 + (s2 - s3)^2 + (s3 - s1)^2) / 2)",
    description=(
        "Scalar equivalent stress from the three principal stresses, used to compare a multiaxial "
        "stress state with the uniaxial yield stress of a ductile material."
    ),
    inputs=(
        VariableSpec(
            name="sigma_1",
            symbol=r"\sigma_1",
            description="First principal stress",
            dimension="M L^-1 T^-2",
            si_unit="Pa",
        ),
        VariableSpec(
            name="sigma_2",
            symbol=r"\sigma_2",
            description="Second principal stress",
            dimension="M L^-1 T^-2",
            si_unit="Pa",
        ),
        VariableSpec(
            name="sigma_3",
            symbol=r"\sigma_3",
            description="Third principal stress",
            dimension="M L^-1 T^-2",
            si_unit="Pa",
        ),
    ),
    output=VariableSpec(
        name="sigma_vm",
        symbol=r"\sigma_{vm}",
        description="Von Mises equivalent stress",
        dimension="M L^-1 T^-2",
        si_unit="Pa",
    ),
    evaluator=_evaluate,
    references=(
        roylance("Yield and Plastic Flow", "mit3_11f99_yield", 2001, "p. 5"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"sigma_1": 100000000.0, "sigma_2": 0.0, "sigma_3": 0.0},
            expected=100000000.0,
            rel_tol=1e-12,
            note=(
                "Uniaxial tension: the equivalent stress equals the applied stress (the module's "
                "own check)."
            ),
        ),
        VerificationCase(
            inputs={"sigma_1": 50000000.0, "sigma_2": 0.0, "sigma_3": -50000000.0},
            expected=86602540.37844387,
            rel_tol=1e-12,
            note="Pure shear of magnitude k = 50 MPa: equivalent stress sqrt(3) k.",
        ),
    ),
    assumptions=(
        "Isotropic, pressure-insensitive (ductile) material: hydrostatic stress does not "
        "change the result.",
        "Order of the principal stresses does not matter.",
        "The yield criterion compares this value with the uniaxial yield stress; it is not "
        "suitable for brittle materials.",
    ),
    tags=("von Mises", "equivalent stress", "yield criterion", "distortion energy"),
)
