"""Resistance of a Uniform Conductor: R = rho_e * L / A."""

from sciengformulary.catalog._sources import (
    lienhard_heat_transfer,
    openstax_university_physics,
)
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(
    rho_e: float,
    L: float,  # noqa: N803
    A: float,  # noqa: N803
) -> float:
    return rho_e * L / A


conductor_resistance = FormulaSpec(
    id="electrical.conductor_resistance",
    name="Resistance of a Uniform Conductor",
    equation="R = rho_e * L / A",
    description="Resistance of a uniform wire or bar from its resistivity and dimensions.",
    inputs=(
        VariableSpec(
            name="rho_e",
            symbol=r"\rho",
            description="Electrical resistivity of the material",
            dimension="M L^3 T^-3 I^-2",
            si_unit="ohm*m",
        ),
        VariableSpec(
            name="L",
            symbol="L",
            description="Conductor length",
            dimension="L",
            si_unit="m",
        ),
        VariableSpec(
            name="A",
            symbol="A",
            description="Cross-sectional area",
            dimension="L^2",
            si_unit="m^2",
        ),
    ),
    output=VariableSpec(
        name="R",
        symbol="R",
        description="Resistance",
        dimension="M L^2 T^-3 I^-2",
        si_unit="ohm",
    ),
    evaluator=_evaluate,
    references=(
        openstax_university_physics(2, "9-3-resistivity-and-resistance", "sec. 9.3, eq. (9.9)"),
        # The book prints R = L / (gamma A) with electrical conductivity gamma; the resistivity is
        # rho = 1 / gamma.
        lienhard_heat_transfer("sec. 2.3, eqs. (2.17b)-(2.18), p. 63"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"rho_e": 1.68e-08, "L": 100.0, "A": 1e-06},
            expected=1.68,
            rel_tol=1e-12,
            note="Hand calculation: 1.68e-8 * 100 / 1e-6 = 1.68 ohm.",
        ),
    ),
    assumptions=(
        "Uniform cross-section and material; current spread uniformly (no skin effect at high "
        "frequency).",
        "Resistivity depends on temperature; use the value at the operating temperature.",
    ),
    tags=("resistance", "resistivity", "wire", "strain gauge", "conductor"),
)
