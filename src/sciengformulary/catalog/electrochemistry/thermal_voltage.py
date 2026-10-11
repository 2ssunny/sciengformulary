"""Thermal Voltage: V_T = R * T / F."""

from sciengformulary.catalog._constants import (
    BOLTZMANN_CONSTANT_REFERENCE,
    FARADAY_CONSTANT,
    FARADAY_CONSTANT_REFERENCE,
    MOLAR_GAS_CONSTANT,
    MOLAR_GAS_CONSTANT_REFERENCE,
)
from sciengformulary.catalog._domain import finite_result, positive
from sciengformulary.catalog._sources import doe_fuel_cell_handbook, nist_si_brochure
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase

# R and F are exact products of SI defining constants (catalog/_constants.py):
# R = N_A k and F = N_A e, so R / F = k / e.


def _evaluate(T: float) -> float:  # noqa: N803
    positive("T", T)
    # R / F is about 8.6e-5 V/K; forming it first keeps R * T from overflowing for huge T.
    return finite_result(MOLAR_GAS_CONSTANT / FARADAY_CONSTANT * T)


thermal_voltage = FormulaSpec(
    id="electrochemistry.thermal_voltage",
    name="Thermal Voltage (RT/F)",
    equation="V_T = R * T / F",
    description=(
        "Voltage scale of electrochemical kinetics and equilibria: the molar gas constant times "
        "the temperature over the Faraday constant, about 25.7 mV at 298.15 K."
    ),
    inputs=(
        VariableSpec(
            name="T",
            symbol="T",
            description="Absolute temperature",
            dimension="Theta",
            si_unit="K",
        ),
    ),
    output=VariableSpec(
        name="V_T",
        symbol="V_T",
        description="Thermal voltage RT/F",
        dimension="M L^2 T^-3 I^-1",
        si_unit="V",
    ),
    evaluator=_evaluate,
    references=(
        # Derived result: the group R T / F is the one-electron case (n = 1) of the prefactors
        # RT/(nF) and RT/(alpha n F) printed in the Nernst equations of Table 2-2 and in the
        # Tafel equation (2-20). The handbook does not give the group a name; "thermal voltage"
        # is the name used here.
        doe_fuel_cell_handbook(
            "Table 2-2 (Nernst equations), p. 2-5 (PDF p. 58); eq. (2-20), p. 2-12 (PDF p. 65)"
        ),
        # The exact SI-2019 values of k, N_A and e make R = N_A k and F = N_A e exact, so
        # R T / F = k T / e.
        nist_si_brochure("sec. 2.2, Table 1 (the seven defining constants), p. 4 (PDF p. 20)"),
        BOLTZMANN_CONSTANT_REFERENCE,
        # The evaluator's R and F are the CODATA 2022 values (exact products of defining
        # constants), cited here by their own records.
        MOLAR_GAS_CONSTANT_REFERENCE,
        FARADAY_CONSTANT_REFERENCE,
    ),
    verification_cases=(
        VerificationCase(
            inputs={"T": 298.15},
            expected=0.025692579121085846,
            rel_tol=1e-12,
            note="50-digit mpmath value of k T / e with the exact SI constants (oracle).",
        ),
        VerificationCase(
            inputs={"T": 310.0},
            expected=0.02671373311265005,
            rel_tol=1e-12,
            note="50-digit mpmath value of k T / e with the exact SI constants (oracle).",
        ),
        VerificationCase(
            inputs={"T": 1.0},
            expected=8.617333262145177e-05,
            rel_tol=1e-12,
            note="At 1 K the result is k / e, 8.617333262...e-5 V/K, from the exact constants.",
        ),
    ),
    assumptions=(
        "Derived result: the voltage scale RT/F is the n = 1 case of the prefactor RT/(nF) "
        "that the source prints in its Nernst and Tafel equations; the source does not name it.",
        "R = N_A * k_B = 8.31446261815324 J/(mol K) and F = N_A * e = 96485.33212331001 C/mol "
        "from the exact SI-2019 defining constants (NIST SP 330, Table 1), so the result "
        "equals k_B T / e. They are fixed in the evaluator, in SI units: T in kelvin, result "
        "in volts.",
        "The relation holds for any temperature; T must be positive and finite, otherwise "
        "ValueError is raised.",
    ),
    tags=("thermal voltage", "Nernst", "Faraday constant", "electrochemistry"),
)
