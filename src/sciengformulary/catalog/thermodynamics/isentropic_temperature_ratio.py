"""Isentropic Temperature-Pressure Relation: T2 / T1 = (p2 / p1)^((gamma - 1) / gamma)."""

from sciengformulary.catalog._sources import naca_report_1135, openstax_university_physics
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(p_ratio: float, gamma: float) -> float:
    return p_ratio ** ((gamma - 1.0) / gamma)


isentropic_temperature_ratio = FormulaSpec(
    id="thermodynamics.isentropic_temperature_ratio",
    name="Isentropic Temperature-Pressure Relation",
    equation="T2 / T1 = (p2 / p1)^((gamma - 1) / gamma)",
    description=(
        "Temperature ratio of an ideal gas compressed or expanded isentropically between two "
        "pressures."
    ),
    inputs=(
        VariableSpec(
            name="p_ratio",
            symbol="p_2/p_1",
            description="Pressure ratio p2 / p1",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="gamma",
            symbol=r"\gamma",
            description="Ratio of specific heats c_p / c_v",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="T_ratio",
        symbol="T_2/T_1",
        description="Temperature ratio T2 / T1",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # The source states p/p_t = (T/T_t)^(gamma/(gamma-1)) along an isentrope; any two states on
        # it obey the same power law.
        naca_report_1135("eq. (35)"),
        openstax_university_physics(
            2,
            "3-6-adiabatic-processes-for-an-ideal-gas",
            "sec. 3.6, eq. (3.13)",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"p_ratio": 10.0, "gamma": 1.4},
            expected=1.93069772888325,
            rel_tol=1e-12,
            note="Independent 40-digit decimal evaluation of 10^(0.4/1.4).",
        ),
    ),
    assumptions=(
        "Isentropic (reversible adiabatic) process: no heat transfer and no friction; real "
        "compressors need an efficiency correction.",
        "Ideal (thermally perfect) gas: p = rho R T holds; not near condensation or at very "
        "high pressure.",
        "Calorically perfect gas: constant specific heats, so gamma is constant over the "
        "temperature range.",
    ),
    tags=("isentropic", "adiabatic", "compressor", "pressure ratio", "Brayton"),
)
