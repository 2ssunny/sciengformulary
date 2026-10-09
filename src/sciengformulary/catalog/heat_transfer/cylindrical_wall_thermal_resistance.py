"""Cylindrical Wall Thermal Resistance: R_t = ln(r_o / r_i) / (2 * pi * k * L)."""

import math

from sciengformulary.catalog._domain import finite_result, positive
from sciengformulary.catalog._sources import ENGINEERING_ACCESSED, lienhard_heat_transfer
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(
    r_o: float,
    r_i: float,
    k: float,
    L: float,  # noqa: N803 - symbol as written in the source
) -> float:
    positive("r_i", r_i)
    positive("r_o", r_o)
    positive("k", k)
    positive("L", L)
    if r_o <= r_i:
        raise ValueError(f"r_o must exceed r_i, got r_o={r_o!r} and r_i={r_i!r}.")
    # log1p keeps full precision for a thin wall, where r_o / r_i is close to 1.
    return finite_result(math.log1p((r_o - r_i) / r_i) / (2.0 * math.pi * k * L))


cylindrical_wall_thermal_resistance = FormulaSpec(
    id="heat_transfer.cylindrical_wall_thermal_resistance",
    name="Cylindrical Wall Thermal Resistance",
    equation="R_t = ln(r_o / r_i) / (2 * pi * k * L)",
    description=(
        "Conduction resistance of the wall of a hollow cylinder (a pipe or tube wall) to radial "
        "heat flow; the radial counterpart of the plane-wall resistance L / (k A), whose area "
        "changes with radius."
    ),
    inputs=(
        VariableSpec(
            name="r_o",
            symbol="r_o",
            description="Outer radius of the wall, larger than r_i",
            dimension="L",
            si_unit="m",
        ),
        VariableSpec(
            name="r_i",
            symbol="r_i",
            description="Inner radius of the wall, positive",
            dimension="L",
            si_unit="m",
        ),
        VariableSpec(
            name="k",
            symbol="k",
            description="Thermal conductivity of the wall material, positive",
            dimension="M L T^-3 Theta^-1",
            si_unit="W/(m*K)",
        ),
        VariableSpec(
            name="L",
            symbol="L",
            description="Length of the cylinder along its axis, positive",
            dimension="L",
            si_unit="m",
        ),
    ),
    output=VariableSpec(
        name="R_t",
        symbol="R_t",
        description="Thermal resistance of the wall to radial conduction",
        dimension="M^-1 L^-2 T^3 Theta",
        si_unit="K/W",
    ),
    evaluator=_evaluate,
    references=(
        # The source writes the conduction term of the resistance chain through a tube
        # (eq. 2.25) and prints it explicitly in Example 2.6.
        lienhard_heat_transfer(
            "sec. 2.3, eq. (2.25), p. 69 and Example 2.6, p. 70", accessed=ENGINEERING_ACCESSED
        ),
        # Table 5.4 item 2 gives the shape factor per unit length 2 pi / ln(r_o / r_i) of a
        # thick cylinder wall, with R_t = 1 / (k S): the same relation.
        lienhard_heat_transfer("sec. 5.7, Table 5.4 item 2, p. 246", accessed=ENGINEERING_ACCESSED),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"r_o": 0.5, "r_i": 0.45, "k": 20.0, "L": 10.0},
            expected=8.384323436827047e-05,
            rel_tol=1e-12,
            note="ln(0.5 / 0.45) / (2 pi 20 10) evaluated with 50-digit arithmetic (mpmath).",
        ),
        VerificationCase(
            inputs={"r_o": 1.001, "r_i": 1.0, "k": 1.0, "L": 1.0},
            expected=0.00015907541863224015,
            rel_tol=1e-12,
            note="Thin wall, close to the plane-wall value 0.001 / (2 pi); 50-digit arithmetic.",
        ),
        VerificationCase(
            inputs={"r_o": 0.0058, "r_i": 0.0025, "k": 0.074, "L": 1.0},
            expected=1.8099942911435594,
            rel_tol=1e-12,
            note=(
                "Radii and conductivity of the insulated tube of the textbook's Example 2.6; "
                "value from 50-digit arithmetic (mpmath)."
            ),
        ),
    ),
    assumptions=(
        "Steady, one-dimensional radial conduction with constant thermal conductivity and no "
        "internal heat generation.",
        "Long cylinder: heat flow through the end faces is neglected. The inner and outer "
        "surfaces are isothermal.",
        "Radii r_o > r_i > 0; any consistent length and conductivity units give the resistance "
        "in the matching units (K/W in SI). The ratio r_o / r_i is dimensionless, so diameters "
        "give the same logarithm.",
        "This is the wall-conduction resistance only. Convective films on the surfaces add "
        "their own resistances in series.",
    ),
    tags=("conduction", "thermal resistance", "cylinder", "pipe wall", "radial"),
)
