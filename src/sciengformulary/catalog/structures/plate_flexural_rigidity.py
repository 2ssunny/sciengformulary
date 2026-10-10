"""Plate Flexural Rigidity: D = E * t^3 / (12 * (1 - nu^2))."""

from sciengformulary.catalog._domain import finite, finite_result, positive
from sciengformulary.catalog._sources import ENGINEERING_ACCESSED, roylance
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(
    E: float,  # noqa: N803
    t: float,
    nu: float,
) -> float:
    positive("E", E)
    positive("t", t)
    finite("nu", nu)
    if not -1.0 < nu < 0.5:
        raise ValueError(f"nu must lie in (-1, 0.5), got {nu!r}.")
    return finite_result(E * t**3 / (12.0 * (1.0 - nu**2)))


plate_flexural_rigidity = FormulaSpec(
    id="structures.plate_flexural_rigidity",
    name="Plate Flexural Rigidity",
    equation="D = E * t^3 / (12 * (1 - nu^2))",
    description=(
        "Bending stiffness per unit width of a thin, homogeneous, isotropic, linear elastic "
        "plate; it relates the bending moment per unit width to the curvature."
    ),
    inputs=(
        VariableSpec(
            name="E",
            symbol="E",
            description="Young's modulus of the material",
            dimension="M L^-1 T^-2",
            si_unit="Pa",
        ),
        VariableSpec(
            name="t",
            symbol="t",
            description="Plate thickness",
            dimension="L",
            si_unit="m",
        ),
        VariableSpec(
            name="nu",
            symbol=r"\nu",
            description="Poisson's ratio, between -1 and 0.5 (exclusive)",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="D",
        symbol="D",
        description="Flexural rigidity (moment per unit width per unit curvature)",
        dimension="M L^2 T^-2",
        si_unit="N*m",
    ),
    evaluator=_evaluate,
    references=(
        # Eq. (2) gives the plane-stress stiffness matrix of an isotropic ply,
        # D = E / (1 - nu^2) * [[1, nu, 0], [nu, 1, 0], [0, 0, (1 - nu) / 2]], and eq. (24) the
        # laminate bending stiffness D_b = (1/3) * sum over plies of D_k (z_{k+1}^3 - z_k^3),
        # which relates moments per unit width to curvature (eq. (23)). For one homogeneous
        # layer z runs from -t/2 to t/2, so D_b = D t^3 / 12 and its first entry is
        # E t^3 / (12 (1 - nu^2)); the notes do not print this closed form.
        roylance(
            "Laminated Composite Plates",
            "mit3_11f99_laminates",
            2000,
            "eq. (2), p. 2 and eq. (24), p. 9",
            accessed=ENGINEERING_ACCESSED,
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"E": 200000000000.0, "t": 0.01, "nu": 0.3},
            expected=18315.018315018315,
            rel_tol=1e-12,
            note="Hand calculation: 200e9 * 1e-6 / (12 * 0.91) = 200000 / 10.92 = 18315.018 N*m.",
        ),
        VerificationCase(
            inputs={"E": 1000000000.0, "t": 0.1, "nu": 0.0},
            expected=83333.33333333333,
            rel_tol=1e-12,
            note="Zero Poisson ratio: E t^3 / 12 = 1e9 * 1e-3 / 12 = 83333.33 N*m.",
        ),
        VerificationCase(
            inputs={"E": 5000000.0, "t": 0.02, "nu": -0.5},
            expected=4.444444444444445,
            rel_tol=1e-12,
            note="Hand calculation: 5e6 * 8e-6 / (12 * 0.75) = 40 / 9 = 4.4444 N*m (nu < 0).",
        ),
    ),
    assumptions=(
        "Thin plate in classical (Kirchhoff) laminate theory: plane sections remain plane, "
        "small deflections, plane-stress material law, a single homogeneous isotropic layer.",
        "The upper bound nu < 0.5 is the isotropic-material limit mentioned by the source; the "
        "lower bound nu > -1 is where the formula becomes singular. Values outside "
        "(-1, 0.5) raise ValueError, as do non-positive E or t.",
        "Derived result: eq. (24) evaluated for one layer between z = -t/2 and z = t/2 using "
        "the isotropic stiffness matrix of eq. (2); the source does not print the closed form "
        "for a homogeneous plate.",
        "Homogeneous in any consistent unit set (Pa * m^3, which is N*m per unit width).",
    ),
    tags=("plate", "flexural rigidity", "bending stiffness", "Kirchhoff"),
)
