"""Bond Number: Bo = g * (rho_l - rho_g) * L^2 / sigma."""

from sciengformulary.catalog._domain import finite_result, non_negative, positive
from sciengformulary.catalog._sources import ENGINEERING_ACCESSED, lienhard_heat_transfer
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(
    g: float,
    rho_l: float,
    rho_g: float,
    L: float,  # noqa: N803
    sigma: float,
) -> float:
    positive("g", g)
    positive("rho_l", rho_l)
    non_negative("rho_g", rho_g)
    if rho_l <= rho_g:
        raise ValueError(f"rho_l must exceed rho_g, got rho_l={rho_l!r}, rho_g={rho_g!r}.")
    positive("L", L)
    positive("sigma", sigma)
    return finite_result(g * (rho_l - rho_g) * L**2 / sigma)


bond_number = FormulaSpec(
    id="fluids.bond_number",
    name="Bond Number",
    equation="Bo = g * (rho_l - rho_g) * L^2 / sigma",
    description=(
        "Ratio of buoyancy, from gravity acting on the density difference, to the "
        "surface-tension force across a liquid-gas or liquid-vapour interface."
    ),
    inputs=(
        VariableSpec(
            name="g",
            symbol="g",
            description="Gravitational acceleration",
            dimension="L T^-2",
            si_unit="m/s^2",
        ),
        VariableSpec(
            name="rho_l",
            symbol=r"\rho_l",
            description="Density of the heavier (liquid) phase",
            dimension="M L^-3",
            si_unit="kg/m^3",
        ),
        VariableSpec(
            name="rho_g",
            symbol=r"\rho_g",
            description="Density of the lighter (gas or vapour) phase",
            dimension="M L^-3",
            si_unit="kg/m^3",
        ),
        VariableSpec(
            name="L",
            symbol="L",
            description="Characteristic length chosen by the user",
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
        name="Bo",
        symbol="Bo",
        description="Bond number",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # The nomenclature list prints Bo = L^2 g (rho_f - rho_g) / sigma, which is the equation
        # here with the heavier phase (rho_f in the source) named rho_l. Eq. (9.14) and the
        # sentence after it name Pi_2 = L / sqrt(sigma / (g (rho_f - rho_g))) the square root of
        # the Bond number, consistent with it.
        lienhard_heat_transfer(
            "Appendix C (nomenclature), p. 772; eq. (9.14) and the sentence after it, p. 496",
            accessed=ENGINEERING_ACCESSED,
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"g": 9.80665, "rho_l": 1000.0, "rho_g": 1.2, "L": 2.0, "sigma": 0.0589},
            expected=665187.2339558573,
            rel_tol=1e-12,
            note="50-digit mpmath value; an independent library example gives the same number.",
        ),
        VerificationCase(
            inputs={"g": 9.80665, "rho_l": 1000.0, "rho_g": 0.0, "L": 0.001, "sigma": 0.072},
            expected=0.13620347222222223,
            rel_tol=1e-12,
            note="Edge case with zero gas density; 50-digit mpmath value.",
        ),
        VerificationCase(
            inputs={"g": 9.80665, "rho_l": 998.0, "rho_g": 1.0, "L": 0.0005, "sigma": 0.072},
            expected=0.03394871545138889,
            rel_tol=1e-12,
            note="Small Bond number, surface tension dominant; 50-digit mpmath value.",
        ),
    ),
    assumptions=(
        "The source defines the Bond number in its nomenclature list as L^2 g (rho_f - rho_g) "
        "/ sigma and calls the group Pi_2 of eq. (9.14) its square root, which agrees.",
        "rho_l must exceed rho_g (liquid heavier than the surrounding gas), matching the "
        "source's density difference rho_f - rho_g; otherwise ValueError is raised.",
        "L is the characteristic length of the problem; authors differ on the length scale "
        "(for example the capillary length), so use the one the correlation in use specifies.",
        "Dimensionless: any consistent unit system gives the same value.",
    ),
    tags=("Bond number", "Eotvos number", "surface tension", "buoyancy", "dimensionless group"),
)
