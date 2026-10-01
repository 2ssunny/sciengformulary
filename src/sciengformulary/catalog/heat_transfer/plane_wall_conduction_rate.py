"""Heat Conduction Through a Plane Wall: Q = k * A * (T_hot - T_cold) / L."""

from sciengformulary.catalog._sources import lienhard_heat_transfer, openstax_university_physics
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(
    k: float,
    A: float,  # noqa: N803
    T_hot: float,  # noqa: N803
    T_cold: float,  # noqa: N803
    L: float,  # noqa: N803
) -> float:
    return k * A * (T_hot - T_cold) / L


plane_wall_conduction_rate = FormulaSpec(
    id="heat_transfer.plane_wall_conduction_rate",
    name="Heat Conduction Through a Plane Wall",
    equation="Q = k * A * (T_hot - T_cold) / L",
    description="Steady conductive heat flow through a flat slab with fixed face temperatures.",
    inputs=(
        VariableSpec(
            name="k",
            symbol="k",
            description="Thermal conductivity",
            dimension="M L T^-3 Theta^-1",
            si_unit="W/(m*K)",
        ),
        VariableSpec(
            name="A",
            symbol="A",
            description="Wall area normal to the heat flow",
            dimension="L^2",
            si_unit="m^2",
        ),
        VariableSpec(
            name="T_hot",
            symbol="T_h",
            description="Temperature of the hotter face",
            dimension="Theta",
            si_unit="K",
        ),
        VariableSpec(
            name="T_cold",
            symbol="T_c",
            description="Temperature of the colder face",
            dimension="Theta",
            si_unit="K",
        ),
        VariableSpec(
            name="L",
            symbol="L",
            description="Wall thickness",
            dimension="L",
            si_unit="m",
        ),
    ),
    output=VariableSpec(
        name="Q",
        symbol="Q",
        description="Heat flow rate from hot to cold face",
        dimension="M L^2 T^-3",
        si_unit="W",
    ),
    evaluator=_evaluate,
    references=(
        # The source writes the slab thickness as d.
        openstax_university_physics(2, "1-6-mechanisms-of-heat-transfer", "sec. 1.6, eq. (1.9)"),
        lienhard_heat_transfer("sec. 2.3, eq. (2.16)"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"k": 34.0, "A": 0.4, "T_hot": 110.0, "T_cold": 50.0, "L": 0.03},
            expected=27200.0,
            rel_tol=1e-12,
            note=(
                "Worked example in Lienhard sec. 1.3 (lead slab): q = 68000 W/m^2 over 0.4 m^2 "
                "gives 27200 W."
            ),
        ),
    ),
    assumptions=(
        "Steady state; constant thermal conductivity.",
        "One-dimensional conduction: the wall is wide compared with its thickness, with no "
        "heat generation inside it.",
        "Temperature differences may use kelvin or degrees Celsius.",
    ),
    tags=("conduction", "plane wall", "slab", "heat loss", "insulation"),
)
