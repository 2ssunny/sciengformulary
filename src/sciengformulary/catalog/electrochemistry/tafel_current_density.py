"""Tafel Current Density: j = j0 * exp(alpha * n_e * F * eta / (R * T))."""

import math

from sciengformulary.catalog._constants import (
    FARADAY_CONSTANT,
    FARADAY_CONSTANT_REFERENCE,
    MOLAR_GAS_CONSTANT,
    MOLAR_GAS_CONSTANT_REFERENCE,
)
from sciengformulary.catalog._domain import (
    finite_result,
    integer,
    non_negative,
    positive,
)
from sciengformulary.catalog._sources import doe_fuel_cell_handbook, nist_si_brochure
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(j0: float, alpha: float, n_e: float, eta: float, T: float) -> float:  # noqa: N803
    positive("j0", j0)
    positive("alpha", alpha)
    integer("n_e", n_e, minimum=1)
    non_negative("eta", eta)
    positive("T", T)
    exponent = alpha * n_e * FARADAY_CONSTANT * eta / (MOLAR_GAS_CONSTANT * T)
    try:
        growth = math.exp(exponent)
    except OverflowError:
        raise OverflowError(
            f"exp({exponent!r}) is outside the floating-point range; the overpotential is far "
            "too large for the Tafel equation to be meaningful."
        ) from None
    return finite_result(j0 * growth)


tafel_current_density = FormulaSpec(
    id="electrochemistry.tafel_current_density",
    name="Tafel Current Density",
    equation="j = j0 * exp(alpha * n_e * F * eta / (R * T))",
    description=(
        "Current density of an electrode reaction in the Tafel regime from the exchange "
        "current density and the activation overpotential."
    ),
    inputs=(
        VariableSpec(
            name="j0",
            symbol="j_0",
            description="Exchange current density",
            dimension="I L^-2",
            si_unit="A/m^2",
        ),
        VariableSpec(
            name="alpha",
            symbol=r"\alpha",
            description="Electron transfer coefficient of the electrode reaction",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="n_e",
            symbol="n",
            description="Number of electrons transferred (whole number, at least 1)",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="eta",
            symbol=r"\eta",
            description="Activation overpotential (voltage loss), not negative",
            dimension="M L^2 T^-3 I^-1",
            si_unit="V",
        ),
        VariableSpec(
            name="T",
            symbol="T",
            description="Absolute temperature",
            dimension="Theta",
            si_unit="K",
        ),
    ),
    output=VariableSpec(
        name="j",
        symbol="j",
        description="Current density",
        dimension="I L^-2",
        si_unit="A/m^2",
    ),
    evaluator=_evaluate,
    references=(
        # Derived result: the handbook prints the activation polarization as
        # eta_act = (RT / (alpha n F)) ln(i / i_o) (2-20) and the intercept-slope form
        # eta_act = a + b ln i (2-21). Solving (2-20) for i gives i = i_o exp(alpha n F eta / RT).
        # The handbook writes i for the current density and i_o for the exchange current density.
        doe_fuel_cell_handbook("eqs. (2-20) and (2-21), p. 2-12 (PDF p. 65)"),
        # R and F are the exact products N_A k and N_A e of the SI-2019 defining constants;
        # the CODATA 2022 records for R and F give their values.
        nist_si_brochure("sec. 2.2, Table 1 (the seven defining constants), p. 4 (PDF p. 20)"),
        MOLAR_GAS_CONSTANT_REFERENCE,
        FARADAY_CONSTANT_REFERENCE,
    ),
    verification_cases=(
        VerificationCase(
            inputs={"j0": 0.001, "alpha": 0.5, "n_e": 1.0, "eta": 0.1, "T": 298.15},
            expected=0.0070012396400441195,
            rel_tol=1e-12,
            note="50-digit mpmath value of the exponential with the exact SI constants (oracle).",
        ),
        VerificationCase(
            inputs={"j0": 0.02, "alpha": 0.5, "n_e": 2.0, "eta": 0.0, "T": 333.15},
            expected=0.02,
            rel_tol=1e-12,
            note="Zero overpotential makes the exponential 1, so j equals j0.",
        ),
        VerificationCase(
            inputs={"j0": 0.0005, "alpha": 0.3, "n_e": 2.0, "eta": 0.25, "T": 333.15},
            expected=0.09292192950427813,
            rel_tol=1e-12,
            note="50-digit mpmath value, two electrons, with the exact SI constants (oracle).",
        ),
    ),
    assumptions=(
        "Derived result: the printed Tafel equation (2-20) for the overpotential is inverted "
        "to give the current density.",
        "Validity from the source: the Tafel equation is a semi-empirical approximation for "
        "activation overpotentials of roughly 50-100 mV and above (high overpotential, one "
        "direction of the reaction only). It is not enforced as a limit because the source "
        "gives only a rough threshold; at eta = 0 the formula returns j0, which is not the "
        "net current of the reaction.",
        "The source treats eta as a voltage loss, so eta must be finite and not negative; "
        "otherwise ValueError is raised.",
        "j0 and T must be positive and finite, alpha positive and finite, and n_e a whole "
        "number of at least 1; otherwise ValueError is raised. The source gives no upper "
        "bound for alpha. A result outside the float range raises OverflowError.",
        "j and j0 refer to the same area basis and are in one current-density unit. R = N_A k_B "
        "and F = N_A e (exact SI-2019 values) are fixed in the evaluator in SI units: eta in "
        "volts and T in kelvin.",
    ),
    tags=("Tafel equation", "activation polarization", "exchange current density", "fuel cell"),
)
