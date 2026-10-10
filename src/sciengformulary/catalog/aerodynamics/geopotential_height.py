"""Geopotential Height from Geometric Height."""

from sciengformulary.catalog._domain import finite, finite_result, positive
from sciengformulary.catalog._sources import nasa_technical_report
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(R_E: float, h: float) -> float:  # noqa: N803
    positive("R_E", R_E)
    finite("h", h)
    if h <= -R_E:
        raise ValueError(f"h must be greater than -R_E (above the centre of the Earth), got {h!r}.")
    # H = R_E h / (R_E + h), evaluated as a ratio of the smaller to the larger magnitude so
    # that neither the product R_E * h nor the sum R_E + h overflows for a finite result.
    if h < 0:
        return finite_result(h * (R_E / (R_E + h)))
    small, large = (h, R_E) if h <= R_E else (R_E, h)
    return finite_result(small / (1.0 + small / large))


geopotential_height = FormulaSpec(
    id="aerodynamics.geopotential_height",
    name="Geopotential Height from Geometric Height",
    equation="H = R_E * h / (R_E + h)",
    description=(
        "Geopotential altitude, the height scale that absorbs the weakening of gravity with "
        "altitude under an inverse-square law, in terms of the geometric altitude and an "
        "effective Earth radius. It is the altitude coordinate used by the standard-atmosphere "
        "layer formulas."
    ),
    inputs=(
        VariableSpec(
            name="R_E",
            symbol="R_E",
            description="Effective Earth radius (r0 = 6,356,766 m in the 1976 Standard Atmosphere)",
            dimension="L",
            si_unit="m",
        ),
        VariableSpec(
            name="h",
            symbol="h",
            description="Geometric altitude",
            dimension="L",
            si_unit="m",
        ),
    ),
    output=VariableSpec(
        name="H",
        symbol="H",
        description="Geopotential altitude, in geopotential metres",
        dimension="L",
        si_unit="m",
    ),
    evaluator=_evaluate,
    references=(
        # Stated up to the unit factor: eq. (18) reads H = (g0/g0') r0 Z / (r0 + Z) with the
        # ratio g0/g0' equal to 1 m'/m, which is a statement about units and is dropped here, so
        # H is numerically the value in geopotential metres. Symbols: Z -> h, r0 -> R_E.
        nasa_technical_report(
            "U.S. Standard Atmosphere, 1976",
            (),
            "NASA-TM-X-74335; NOAA-S/T-76-1562",
            1976,
            "https://ntrs.nasa.gov/citations/19770009539",
            "sec. 1.2.3, eq. (18), p. 8 (with eq. (17) and eq. (19)); Table I rows Z = -5000, "
            "p. 51, and Z = 5000, p. 55",
            organization=(
                "National Oceanic and Atmospheric Administration, National Aeronautics and "
                "Space Administration and U.S. Air Force"
            ),
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"R_E": 6356766.0, "h": 11000.0},
            expected=10980.99804546838,
            rel_tol=1e-12,
            note="Standard-atmosphere radius at 11 km; 50-digit mpmath evaluation.",
        ),
        VerificationCase(
            inputs={"R_E": 6356766.0, "h": 5000.0},
            expected=4996.070273568692,
            rel_tol=1e-12,
            note="At 5000 m; Table I of the reference prints 4996 m' on this row (mpmath value).",
        ),
        VerificationCase(
            inputs={"R_E": 6356766.0, "h": 0.0},
            expected=0.0,
            rel_tol=1e-12,
            abs_tol=1e-15,
            note="Boundary case: sea level maps to zero.",
        ),
        VerificationCase(
            inputs={"R_E": 6356766.0, "h": -5000.0},
            expected=-5003.93591325625,
            rel_tol=1e-12,
            note="Below sea level; Table I prints -5004 m' on this row (mpmath value).",
        ),
        VerificationCase(
            inputs={"R_E": 6371000.0, "h": 100000.0},
            expected=98454.64379539483,
            rel_tol=1e-12,
            note="Mean-radius sphere at 100 km; 50-digit mpmath evaluation.",
        ),
    ),
    assumptions=(
        "Gravity follows the inverse-square law g = g0 (r0 / (r0 + Z))^2 (eq. (17) of the "
        "source), so the geopotential per unit mass is integrated in closed form.",
        "The factor g0/g0' = 1 m'/m is a statement about units and is dropped: the result is "
        "in geopotential metres, numerically the same unit system as the inputs.",
        "R_E is an input. The 1976 Standard Atmosphere fixes r0 = 6,356,766 m; a mean or "
        "latitude-dependent Earth radius is an admissible input for other uses.",
        "h must exceed -R_E, since the expression is singular at the centre of the Earth.",
        "The source notes that this definition differs from the 1962 relation by 0.2, 0.4 and "
        "33.3 m at 90, 120 and 700 km.",
    ),
    tags=("geopotential altitude", "standard atmosphere", "altitude"),
)
