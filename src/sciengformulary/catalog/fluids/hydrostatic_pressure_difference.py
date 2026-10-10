"""Hydrostatic Pressure Difference: delta_p = rho * g * h."""

from sciengformulary.catalog._sources import (
    openstax_university_physics,
    us_standard_atmosphere_1976,
)
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(rho: float, g: float, h: float) -> float:
    return rho * g * h


hydrostatic_pressure_difference = FormulaSpec(
    id="fluids.hydrostatic_pressure_difference",
    name="Hydrostatic Pressure Difference",
    equation="delta_p = rho * g * h",
    description=(
        "Pressure rise over a vertical depth h in a motionless fluid of uniform density. It "
        "equals the weight of the overlying fluid column divided by the column's cross-section."
    ),
    inputs=(
        VariableSpec(
            name="rho",
            symbol=r"\rho",
            description="Fluid density",
            dimension="M L^-3",
            si_unit="kg/m^3",
        ),
        VariableSpec(
            name="g",
            symbol="g",
            description="Gravitational acceleration",
            dimension="L T^-2",
            si_unit="m/s^2",
        ),
        VariableSpec(
            name="h",
            symbol="h",
            description="Vertical depth below the reference level",
            dimension="L",
            si_unit="m",
        ),
    ),
    output=VariableSpec(
        name="delta_p",
        symbol=r"\Delta p",
        description="Pressure at depth h minus pressure at the reference level",
        dimension="M L^-1 T^-2",
        si_unit="Pa",
    ),
    evaluator=_evaluate,
    references=(
        # The source writes p = p0 + rho h g; delta_p = p - p0.
        openstax_university_physics(1, "14-1-fluids-density-and-pressure", "sec. 14.1, eq. (14.4)"),
        # The source prints the differential form dP = -g rho dZ with Z upward; integrating over a
        # depth h at constant rho and g gives delta_p = rho g h.
        us_standard_atmosphere_1976("sec. 1.2.2, eq. (4), p. 6"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"rho": 1000.0, "g": 9.81, "h": 10.0},
            expected=98100.0,
            rel_tol=1e-12,
            note="Hand calculation: 1000 * 9.81 * 10 = 98100 Pa.",
        ),
    ),
    assumptions=(
        "Fluid at rest (hydrostatic) with constant density between the two levels; "
        "compressible columns such as the atmosphere need density as a function of height.",
        "h is measured vertically downward from the reference level.",
        "Derived result: obtained by integrating the cited hydrostatic relation dP = -g rho dZ "
        "over a depth h at constant density and gravity; the source prints the differential form.",
    ),
    tags=("hydrostatics", "pressure head", "manometer", "depth", "fluid statics"),
)
