"""Equivalence Ratio from Mixture Fraction: phi = (Z / (1 - Z)) * ((1 - Z_st) / Z_st)."""

from sciengformulary.catalog._domain import finite, finite_result
from sciengformulary.catalog._sources import nasa_rp_1311
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _open_unit_interval(name: str, value: float) -> float:
    if not 0 < finite(name, value) < 1:
        raise ValueError(f"{name} must lie strictly between 0 and 1, got {value!r}.")
    return value


def _evaluate(
    Z: float,  # noqa: N803
    Z_st: float,  # noqa: N803
) -> float:
    _open_unit_interval("Z", Z)
    _open_unit_interval("Z_st", Z_st)
    return finite_result((Z / (1.0 - Z)) * ((1.0 - Z_st) / Z_st))


equivalence_ratio_from_mixture_fraction = FormulaSpec(
    id="chemistry.equivalence_ratio_from_mixture_fraction",
    name="Equivalence Ratio from Mixture Fraction",
    equation="phi = (Z / (1 - Z)) * ((1 - Z_st) / Z_st)",
    description=(
        "Equivalence ratio of a two-stream fuel and oxidizer mixture from its mixture fraction "
        "(mass fraction of fuel-stream material) and the stoichiometric mixture fraction."
    ),
    inputs=(
        VariableSpec(
            name="Z",
            symbol="Z",
            description="Mixture fraction: mass fraction of the fuel stream in the mixture",
            dimension="1",
            si_unit="kg/kg",
        ),
        VariableSpec(
            name="Z_st",
            symbol=r"Z_{st}",
            description="Stoichiometric mixture fraction (same definition as Z)",
            dimension="1",
            si_unit="kg/kg",
        ),
    ),
    output=VariableSpec(
        name="phi",
        symbol=r"\phi",
        description="Equivalence ratio; below 1 is lean, above 1 is rich",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # Derived result: the report defines phi = (f/a) / (f/a)_st with f/a the fuel-to-air
        # weight ratio (eq. 9.19). For a mixture of a pure-fuel stream and a pure-oxidizer
        # (air) stream with fuel-stream mass fraction Z, f/a = Z / (1 - Z), and likewise
        # (f/a)_st = Z_st / (1 - Z_st); substituting gives the relation above. If the streams
        # are diluted with a fixed composition, f/a = c Z / (1 - Z) with one constant c, which
        # cancels in the ratio, so the final relation holds for such streams too.
        nasa_rp_1311("eq. (9.19), p. 43 (PDF p. 49)"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"Z": 0.04, "Z_st": 0.055},
            expected=0.7159090909090909,
            rel_tol=1e-12,
            note="Exact rational arithmetic: (0.04 / 0.96) * (0.945 / 0.055) (lean).",
        ),
        VerificationCase(
            inputs={"Z": 0.055, "Z_st": 0.055},
            expected=1.0,
            rel_tol=1e-12,
            note="Z equal to Z_st is the stoichiometric mixture, so phi = 1.",
        ),
        VerificationCase(
            inputs={"Z": 0.2, "Z_st": 0.0552},
            expected=4.278985507246377,
            rel_tol=1e-12,
            note="Exact rational arithmetic: (0.2 / 0.8) * (0.9448 / 0.0552) (rich).",
        ),
    ),
    assumptions=(
        "Derived result: phi = [Z / (1 - Z)] [(1 - Z_st) / Z_st] follows by writing the "
        "fuel-to-air weight ratio of NASA RP-1311 eq. 9.19 as Z / (1 - Z), which holds when the "
        "fuel stream is pure fuel and the oxidizer stream is pure oxidizer; for streams of "
        "fixed composition (e.g. diluted) the ratio f/a differs by a constant factor that "
        "cancels in phi. The report does not print this form.",
        "Z is the mass fraction of the fuel stream, fuel-stream mass over the total mass of "
        "fuel stream plus oxidizer stream, and Z_st is the same quantity for the "
        "stoichiometric mixture. This is a two-stream mixing definition; it is not the "
        "element-based (Bilger) mixture fraction, which is a different quantity.",
        "phi is the engineering equivalence ratio based on the fuel-to-air weight ratio.",
        "Z and Z_st must lie strictly between 0 and 1, otherwise ValueError is raised.",
    ),
    tags=("equivalence ratio", "mixture fraction", "combustion", "stoichiometry", "NASA"),
)
