"""Dynamic pressure: q = 0.5 * rho * V^2."""

from sciengformulary.core import FormulaSpec, ReferenceSpec, VariableSpec, VerificationCase

# One multiply-and-square: the evaluator should agree with the hand result to rounding error.
EXACT_ARITHMETIC_REL_TOL = 1e-12


def _evaluate(rho: float, V: float) -> float:  # noqa: N803 - V is the textbook symbol
    return 0.5 * rho * V**2


dynamic_pressure = FormulaSpec(
    id="aerodynamics.dynamic_pressure",
    name="Dynamic Pressure",
    equation="q = 0.5 * rho * V^2",
    description=(
        "Pressure-like quantity carried by a moving fluid: half its density times the square "
        "of its speed. Aerodynamic forces on a body scale with it, which is why it appears in "
        "the definitions of the lift and drag coefficients."
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
    references=(
        # The source writes the flow velocity as u: q = rho * u^2 / 2, the same relation.
        ReferenceSpec(
            source_type="official_web",
            title="Dynamic Pressure",
            organization="NASA Glenn Research Center",
            year=2024,
            locator="Derivation and Flow of Gas sections",
            url="https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/dynamic-pressure/",
            accessed="2026-10-01",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"rho": 1.225, "V": 120.0},
            expected=8820.0,
            rel_tol=EXACT_ARITHMETIC_REL_TOL,
            note="Hand calculation in SI units: 0.5 * 1.225 * 120^2 = 0.5 * 1.225 * 14400 "
            "= 8820 Pa.",
        ),
        VerificationCase(
            inputs={"rho": 2.0, "V": 10.0},
            expected=100.0,
            rel_tol=EXACT_ARITHMETIC_REL_TOL,
            note="Hand calculation with binary-exact values: 0.5 * 2 * 10^2 = 100.",
        ),
    ),
    assumptions=(
        "rho and V are taken at the same point in the flow; use freestream values for the "
        "freestream dynamic pressure.",
        "q is a defined property of any moving flow and can be used in compressible or viscous "
        "flow, but total pressure = static pressure + q (Bernoulli) holds only when density "
        "is constant (incompressible flow).",
        "No unit conversion is applied: inputs must be in consistent units (SI inputs "
        "give q in Pa).",
    ),
    tags=("q", "freestream", "kinetic energy per unit volume", "bernoulli", "airspeed"),
)
