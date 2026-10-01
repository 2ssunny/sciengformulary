"""Dynamic pressure: q = 0.5 * rho * V^2."""

from auto_3dx_formulas.core import FormulaSpec, VariableSpec


def _evaluate(rho: float, V: float) -> float:  # noqa: N803 - V is the textbook symbol
    return 0.5 * rho * V**2


dynamic_pressure = FormulaSpec(
    id="aerodynamics.dynamic_pressure",
    name="Dynamic Pressure",
    equation="q = 0.5 * rho * V^2",
    description=(
        "Kinetic energy per unit volume of a fluid moving at speed V relative to a body "
        "or reference frame. Used to non-dimensionalize aerodynamic forces, e.g. L = q S C_L."
    ),
    inputs=(
        VariableSpec(
            name="rho",
            symbol=r"\rho",
            description="Fluid density at the point of interest (e.g. freestream)",
            dimension="M L^-3",
            si_unit="kg/m^3",
        ),
        VariableSpec(
            name="V",
            symbol="V",
            description="Flow speed relative to the body (true airspeed for aircraft)",
            dimension="L T^-1",
            si_unit="m/s",
        ),
    ),
    output=VariableSpec(
        name="q",
        symbol="q",
        description="Dynamic pressure",
        dimension="M L^-1 T^-2",
        si_unit="Pa",
    ),
    evaluator=_evaluate,
    assumptions=(
        "rho and V are local values at the same point; use freestream values for "
        "freestream dynamic pressure.",
        "V is true speed relative to the fluid. With equivalent airspeed, use sea-level "
        "density instead of local density.",
        "Valid as a definition at any Mach number, but q equals stagnation minus static "
        "pressure only for incompressible flow (roughly M < 0.3).",
        "No unit conversion is applied: inputs must be in consistent units (SI inputs "
        "give q in Pa).",
    ),
    # Add sources as plain strings, e.g. "Author, Title, edition, section/eq. no.".
    references=(),
    tags=("q", "freestream", "kinetic energy per unit volume", "bernoulli", "airspeed"),
)
