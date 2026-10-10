"""Laminar Flat-Plate Local Nusselt Number, Uniform Heat Flux: Nu_x = 0.4587 Re_x^(1/2) Pr^(1/3)."""

from sciengformulary.catalog._domain import finite, finite_result, positive
from sciengformulary.catalog._sources import ENGINEERING_ACCESSED, lienhard_heat_transfer
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase

_PR_MIN = 0.7


def _evaluate(Re_x: float, Pr: float) -> float:  # noqa: N803 - symbols as written in the source
    positive("Re_x", Re_x)
    if finite("Pr", Pr) < _PR_MIN:
        raise ValueError(f"Pr must be at least {_PR_MIN} for this correlation, got {Pr!r}.")
    # The textbook prints 0.4587 with Pr >= 0.7. Some libraries (for example the Modelica
    # Standard Library) use 0.453 with 0.6 < Pr < 50 and Re_x < 5e5; the textbook is followed.
    return finite_result(0.4587 * Re_x**0.5 * Pr ** (1.0 / 3.0))


laminar_flat_plate_uniform_flux_local_nusselt = FormulaSpec(
    id="heat_transfer.laminar_flat_plate_uniform_flux_local_nusselt",
    name="Laminar Flat-Plate Local Nusselt Number, Uniform Heat Flux",
    equation="Nu_x = 0.4587 * Re_x^(1/2) * Pr^(1/3)",
    description=(
        "Local Nusselt number at distance x from the leading edge of a flat plate in a laminar "
        "boundary layer when the wall heat flux is uniform. The isothermal-wall counterpart, "
        "with coefficient 0.332, is a separate formula; here the wall temperature varies along "
        "the plate."
    ),
    inputs=(
        VariableSpec(
            name="Re_x",
            symbol="Re_x",
            description="Reynolds number based on the distance x from the leading edge, positive",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="Pr",
            symbol="Pr",
            description="Prandtl number, at least 0.7",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="Nu_x",
        symbol="Nu_x",
        description="Local Nusselt number q_w x / (k (T_w - T_inf))",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        lienhard_heat_transfer("sec. 6.5, eq. (6.71), p. 311", accessed=ENGINEERING_ACCESSED),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"Re_x": 100000.0, "Pr": 0.7},
            expected=128.79373962931666,
            rel_tol=1e-12,
            note="Boundary Pr = 0.7; 0.4587 sqrt(1e5) 0.7^(1/3) with 50-digit arithmetic.",
        ),
        VerificationCase(
            inputs={"Re_x": 200000.0, "Pr": 7.0},
            expected=392.41272732629943,
            rel_tol=1e-12,
            note="Water-like Prandtl number; 50-digit arithmetic (mpmath).",
        ),
    ),
    assumptions=(
        "Steady, laminar, two-dimensional boundary layer on a flat plate with zero pressure "
        "gradient. It does not apply once the boundary layer is turbulent; the caller must "
        "keep Re_x in the laminar range.",
        "Uniform wall heat flux from the leading edge, with no unheated starting length. The "
        "Nusselt number uses the local wall-to-free-stream temperature difference.",
        "Pr >= 0.7, where the source says the expression is within 1 % of the exact solution; "
        "the evaluator raises ValueError below 0.7. Not for liquid metals.",
        "Properties are evaluated at the film temperature. Dimensionless; valid in any "
        "consistent unit system.",
    ),
    tags=("Nusselt number", "flat plate", "boundary layer", "laminar", "uniform heat flux"),
)
