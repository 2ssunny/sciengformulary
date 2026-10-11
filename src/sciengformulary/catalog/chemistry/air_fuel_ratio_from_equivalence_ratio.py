"""Air-Fuel Ratio from Equivalence Ratio: AFR = AFR_st / phi."""

from sciengformulary.catalog._domain import finite_result, positive
from sciengformulary.catalog._sources import nasa_rp_1311
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(
    AFR_st: float,  # noqa: N803
    phi: float,
) -> float:
    positive("AFR_st", AFR_st)
    positive("phi", phi)
    return finite_result(AFR_st / phi)


air_fuel_ratio_from_equivalence_ratio = FormulaSpec(
    id="chemistry.air_fuel_ratio_from_equivalence_ratio",
    name="Air-Fuel Ratio from Equivalence Ratio",
    equation="AFR = AFR_st / phi",
    description=(
        "Actual air-fuel mass ratio of a mixture from the stoichiometric air-fuel mass ratio "
        "and the equivalence ratio."
    ),
    inputs=(
        VariableSpec(
            name="AFR_st",
            symbol=r"AFR_{st}",
            description="Stoichiometric air-fuel mass ratio (mass of air per mass of fuel)",
            dimension="1",
            si_unit="kg/kg",
        ),
        VariableSpec(
            name="phi",
            symbol=r"\phi",
            description=(
                "Equivalence ratio, the fuel-to-air ratio relative to stoichiometric; "
                "below 1 is lean, above 1 is rich"
            ),
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="AFR",
        symbol="AFR",
        description="Actual air-fuel mass ratio (mass of air per mass of fuel)",
        dimension="1",
        si_unit="kg/kg",
    ),
    evaluator=_evaluate,
    references=(
        # Derived result: the report defines phi as the actual fuel-to-air weight ratio f/a
        # divided by the stoichiometric one, (f/a)_st (eq. 9.19). The air-fuel ratio is the
        # reciprocal, AFR = a/f, so f/a = phi (f/a)_st gives AFR = AFR_st / phi.
        nasa_rp_1311("eq. (9.19), p. 43 (PDF p. 49)"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"AFR_st": 17.12, "phi": 0.8},
            expected=21.4,
            rel_tol=1e-12,
            note="Exact rational arithmetic: 17.12 / 0.8 = 21.4 (lean, phi below 1).",
        ),
        VerificationCase(
            inputs={"AFR_st": 17.12, "phi": 1.0},
            expected=17.12,
            rel_tol=1e-12,
            note="A stoichiometric mixture (phi = 1) returns the stoichiometric ratio.",
        ),
        VerificationCase(
            inputs={"AFR_st": 14.7, "phi": 2.0},
            expected=7.35,
            rel_tol=1e-12,
            note="Exact arithmetic: 14.7 / 2 = 7.35 (rich, phi above 1).",
        ),
    ),
    assumptions=(
        "Derived result: AFR = AFR_st / phi follows from the definition of the equivalence "
        "ratio as the fuel-to-air weight ratio divided by its stoichiometric value (NASA "
        "RP-1311 eq. 9.19) and AFR being the reciprocal of the fuel-to-air ratio; the report "
        "does not print the air-fuel form.",
        "phi is the engineering equivalence ratio based on the fuel-to-air weight ratio, not "
        "the oxidation-state ratio r used elsewhere in the same report.",
        "Mass basis: AFR and AFR_st are masses of air (or oxidizer) per mass of fuel; a molar "
        "ratio would need a molar stoichiometric ratio instead.",
        "AFR_st and phi must be positive and finite, otherwise ValueError is raised (phi = 0 "
        "is pure air, with an unbounded air-fuel ratio).",
    ),
    tags=("air-fuel ratio", "equivalence ratio", "combustion", "stoichiometry", "NASA"),
)
