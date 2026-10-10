"""Jakob Number: Ja = c_p * (T_sat - T_w) / h_fg."""

from sciengformulary.catalog._domain import finite, finite_result, positive
from sciengformulary.catalog._sources import ENGINEERING_ACCESSED, lienhard_heat_transfer
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(
    c_p: float,
    T_sat: float,  # noqa: N803
    T_w: float,  # noqa: N803
    h_fg: float,
) -> float:
    positive("c_p", c_p)
    finite("T_sat", T_sat)
    finite("T_w", T_w)
    positive("h_fg", h_fg)
    if T_w > T_sat:
        raise ValueError(
            f"T_w must not exceed T_sat for the condensation form, got T_w={T_w!r}, "
            f"T_sat={T_sat!r}."
        )
    return finite_result(c_p * (T_sat - T_w) / h_fg)


jakob_number = FormulaSpec(
    id="heat_transfer.jakob_number",
    name="Jakob Number",
    equation="Ja = c_p * (T_sat - T_w) / h_fg",
    description=(
        "Ratio of the sensible heat of the liquid over the saturation-to-wall temperature "
        "difference to the latent heat of the phase change."
    ),
    inputs=(
        VariableSpec(
            name="c_p",
            symbol="c_p",
            description="Specific heat at constant pressure of the liquid",
            dimension="L^2 T^-2 Theta^-1",
            si_unit="J/(kg*K)",
        ),
        VariableSpec(
            name="T_sat",
            symbol="T_{sat}",
            description="Saturation temperature",
            dimension="Theta",
            si_unit="K",
        ),
        VariableSpec(
            name="T_w",
            symbol="T_w",
            description="Wall temperature (at or below T_sat)",
            dimension="Theta",
            si_unit="K",
        ),
        VariableSpec(
            name="h_fg",
            symbol="h_{fg}",
            description="Latent heat of vaporization",
            dimension="L^2 T^-2",
            si_unit="J/kg",
        ),
    ),
    output=VariableSpec(
        name="Ja",
        symbol="Ja",
        description="Jakob number",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # The source uses this form for film condensation (wall below saturation).
        lienhard_heat_transfer("sec. 8.5, eq. (8.48), p. 441", accessed=ENGINEERING_ACCESSED),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"c_p": 4000.0, "T_sat": 373.15, "T_w": 363.15, "h_fg": 2000000.0},
            expected=0.02,
            rel_tol=1e-12,
            note=(
                "Hand calculation: 4000 * 10 / 2e6 = 0.02; the float difference 373.15 - 363.15 "
                "is 10 to about 6e-15 relative."
            ),
        ),
        VerificationCase(
            inputs={"c_p": 4000.0, "T_sat": 373.15, "T_w": 373.15, "h_fg": 2000000.0},
            expected=0.0,
            rel_tol=1e-12,
            abs_tol=1e-15,
            note="Wall at saturation temperature: no subcooling, so the numerator is zero.",
        ),
    ),
    assumptions=(
        "Condensation convention: the wall is at or below the saturation temperature and the "
        "result is non-negative. T_w greater than T_sat raises ValueError. Boiling texts define "
        "the number with the wall superheat T_w - T_sat instead; this formula does not cover "
        "that form.",
        "c_p is the specific heat of the liquid, not the vapor.",
        "c_p and h_fg must be finite and positive; otherwise ValueError is raised.",
        "Dimensionally homogeneous: c_p, the temperature difference and h_fg in one "
        "consistent unit system.",
    ),
    tags=("Jakob number", "dimensionless group", "phase change", "condensation"),
)
