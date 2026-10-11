"""Hydrogenic electronic energies in the Bohr model."""

from sciengformulary.catalog._domain import finite_result, integer, positive
from sciengformulary.core import (
    FormulaSpec,
    ReferenceSpec,
    VariableSpec,
    VerificationCase,
)


def _evaluate(E_R: float, Z: float, n: float) -> float:
    positive("E_R", E_R)
    Z = integer("Z", Z, minimum=1)
    n = integer("n", n, minimum=1)
    return finite_result(-E_R * (Z / n) ** 2)


hydrogenic_bohr_energy = FormulaSpec(
    id="spectroscopy.hydrogenic_bohr_energy",
    name="Hydrogenic Bohr Energy",
    equation="E_n = -E_R*Z^2/n^2",
    description="Hydrogenic electronic energies in the Bohr model.",
    inputs=(
        VariableSpec(
            name="E_R",
            symbol="E_R",
            description="Positive Rydberg energy appropriate to the reduced-mass convention",
            dimension="M L^2 T^-2",
            si_unit="J",
        ),
        VariableSpec(
            name="Z", symbol="Z", description="Nuclear charge number", dimension="1", si_unit="-"
        ),
        VariableSpec(
            name="n", symbol="n", description="Principal quantum number", dimension="1", si_unit="-"
        ),
    ),
    output=VariableSpec(
        name="E_n",
        symbol="E_n",
        description="Bound-state electronic energy relative to ionization",
        dimension="M L^2 T^-2",
        si_unit="J",
    ),
    evaluator=_evaluate,
    references=(
        ReferenceSpec(
            source_type="official_web",
            title="6.2 The Bohr Model",
            organization="OpenStax",
            url="https://openstax.org/books/chemistry-2e/pages/6-2-the-bohr-model",
            accessed="2026-10-10",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"E_R": 2.18e-18, "Z": 1, "n": 1},
            expected=-2.18e-18,
            note="Hydrogenic n=1 energy is minus the supplied Rydberg energy.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
        VerificationCase(
            inputs={"E_R": 2.18e-18, "Z": 2, "n": 2},
            expected=-2.18e-18,
            note="Equal Z and n gives the same Z^2/n^2 factor of one.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
    ),
    assumptions=(
        "Single-electron hydrogenic atom or ion; nonrelativistic Bohr/Coulomb energy model.",
        "E_R is supplied rather than hard-coded so its finite-nuclear-mass convention is explicit.",
        "Not a multi-electron atom model; fine structure and QED effects excluded.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "spectroscopy", "hydrogenic bohr energy"),
)
