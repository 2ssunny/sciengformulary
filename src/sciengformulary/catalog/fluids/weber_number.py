"""Weber Number: We = rho * V^2 * L / sigma."""

from sciengformulary.catalog._domain import finite_result, non_negative, positive
from sciengformulary.catalog._sources import ENGINEERING_ACCESSED, lienhard_heat_transfer
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(
    rho: float,
    V: float,  # noqa: N803
    L: float,  # noqa: N803
    sigma: float,
) -> float:
    positive("rho", rho)
    non_negative("V", V)
    positive("L", L)
    positive("sigma", sigma)
    return finite_result(rho * V**2 * L / sigma)


weber_number = FormulaSpec(
    id="fluids.weber_number",
    name="Weber Number",
    equation="We = rho * V^2 * L / sigma",
    description=(
        "Ratio of the inertial force to the surface-tension force for a flow with a free interface."
    ),
    inputs=(
        VariableSpec(
            name="rho",
            symbol=r"\rho",
            description="Density of the flowing fluid",
            dimension="M L^-3",
            si_unit="kg/m^3",
        ),
        VariableSpec(
            name="V",
            symbol="u",
            description="Flow speed",
            dimension="L T^-1",
            si_unit="m/s",
        ),
        VariableSpec(
            name="L",
            symbol="L",
            description="Characteristic length",
            dimension="L",
            si_unit="m",
        ),
        VariableSpec(
            name="sigma",
            symbol=r"\sigma",
            description="Surface tension",
            dimension="M T^-2",
            si_unit="N/m",
        ),
    ),
    output=VariableSpec(
        name="We",
        symbol="We",
        description="Weber number",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # The source writes We_L = rho_g u^2 L / sigma with the vapour density of its boiling
        # context and any characteristic length L; here rho is the density of the flowing fluid.
        lienhard_heat_transfer(
            "eq. (9.39) and following definition, p. 510", accessed=ENGINEERING_ACCESSED
        ),
        # The source also calls G^2 L / (sigma rho_f) a Weber number; with the mass flux
        # G = rho_f u this equals rho_f u^2 L / sigma, the same form.
        lienhard_heat_transfer(
            "p. 520 (flow-boiling burnout, Katto discussion)", accessed=ENGINEERING_ACCESSED
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"rho": 900.0, "V": 0.18, "L": 0.001, "sigma": 0.01},
            expected=2.916,
            rel_tol=1e-12,
            note="Hand calculation: 900 * 0.0324 * 0.001 / 0.01 = 2.916.",
        ),
        VerificationCase(
            inputs={"rho": 1000.0, "V": 5.0, "L": 0.002, "sigma": 0.072},
            expected=694.4444444444445,
            rel_tol=1e-12,
            note="50-digit mpmath value of 1000 * 25 * 0.002 / 0.072.",
        ),
        VerificationCase(
            inputs={"rho": 1000.0, "V": 0.0, "L": 0.002, "sigma": 0.072},
            expected=0.0,
            rel_tol=1e-12,
            abs_tol=1e-15,
            note="Edge case of zero flow speed, where the number is zero by hand.",
        ),
    ),
    assumptions=(
        "Definition of a dimensionless group. The density and length scale must be the ones "
        "the correlation using We specifies.",
        "Other conventions exist (for example the density difference, or a factor 1/2); this "
        "is the form printed by the source.",
        "Dimensionless: any consistent unit system gives the same value. rho, L and sigma "
        "must be positive and V not negative, otherwise ValueError is raised.",
    ),
    tags=("Weber number", "surface tension", "dimensionless group", "similarity"),
)
