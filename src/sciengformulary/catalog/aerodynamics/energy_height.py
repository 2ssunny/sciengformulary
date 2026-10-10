"""Energy Height: h_E = h + V^2 / (2 * g)."""

from sciengformulary.catalog._domain import finite, finite_result, positive
from sciengformulary.catalog._sources import nasa_technical_report
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(h: float, V: float, g: float) -> float:  # noqa: N803
    finite("h", h)
    finite("V", V)
    positive("g", g)
    return finite_result(h + V**2 / (2.0 * g))


energy_height = FormulaSpec(
    id="aerodynamics.energy_height",
    name="Energy Height",
    equation="h_E = h + V^2 / (2 * g)",
    description=(
        "Specific energy of an aircraft relative to the surrounding air, expressed as an "
        "equivalent height: the sum of its kinetic and potential energy per unit weight. It "
        "is the height the aircraft would reach if it converted all of its airspeed into "
        "altitude."
    ),
    inputs=(
        VariableSpec(
            name="h",
            symbol="h",
            description="Altitude",
            dimension="L",
            si_unit="m",
        ),
        VariableSpec(
            name="V",
            symbol="V",
            description="Airspeed relative to the surrounding air mass",
            dimension="L T^-1",
            si_unit="m/s",
        ),
        VariableSpec(
            name="g",
            symbol="g",
            description="Gravitational acceleration",
            dimension="L T^-2",
            si_unit="m/s^2",
        ),
    ),
    output=VariableSpec(
        name="h_E",
        symbol="h_e",
        description="Energy height",
        dimension="L",
        si_unit="m",
    ),
    evaluator=_evaluate,
    references=(
        # Stated: the summary describes the energy height as the sum of the kinetic and
        # potential energies per unit weight of the airplane referenced to the surrounding air
        # mass, and the list of symbols gives h_e = V^2 / 2g + h, with h the altitude above mean
        # sea level. Symbols: h_e -> h_E.
        nasa_technical_report(
            "Longitudinal Stability and Control in Wind Shear With Energy Height Rate Feedback",
            ("J. Gera",),
            "NASA TM-81828",
            1980,
            "https://ntrs.nasa.gov/citations/19800024908",
            "Summary and List of Symbols (energy height h_e = V^2/(2g) + h)",
            organization="NASA Langley Research Center",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"h": 10000.0, "V": 250.0, "g": 9.80665},
            expected=13186.613165556026,
            rel_tol=1e-12,
            note="10 km at 250 m/s; 50-digit mpmath evaluation of h + V^2 / (2 g).",
        ),
        VerificationCase(
            inputs={"h": 0.0, "V": 100.0, "g": 9.80665},
            expected=509.8581064889641,
            rel_tol=1e-12,
            note="Ground level at 100 m/s; 50-digit mpmath evaluation.",
        ),
        VerificationCase(
            inputs={"h": 3000.0, "V": 0.0, "g": 9.80665},
            expected=3000.0,
            rel_tol=1e-12,
            note="Boundary case: at zero airspeed the energy height equals the altitude.",
        ),
    ),
    assumptions=(
        "Gravity is treated as uniform over the altitude range; h is the altitude above mean sea "
        "level.",
        "V is the airspeed relative to the air mass, not the ground speed; in a moving air "
        "mass (wind shear) the two differ.",
        "Any consistent unit system works; g must be positive. A negative altitude is allowed.",
    ),
    tags=("energy height", "specific energy", "flight mechanics"),
)
