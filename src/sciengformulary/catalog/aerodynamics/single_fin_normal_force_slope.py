"""Subsonic Normal-Force Slope of a Single Fin (Diederich), from Barrowman's method."""

import math

from sciengformulary.catalog._domain import finite, finite_result, positive
from sciengformulary.catalog._sources import nasa_technical_report
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(Cla: float, AR: float, Gc: float, A_f: float, A_ref: float) -> float:  # noqa: N803
    positive("Cla", Cla)
    positive("AR", AR)
    if abs(finite("Gc", Gc)) >= math.pi / 2:
        raise ValueError(f"Gc must satisfy |Gc| < pi/2 radians, got {Gc!r}.")
    positive("A_f", A_f)
    positive("A_ref", A_ref)
    cos_sweep = math.cos(Gc)
    fin_parameter = 2.0 * math.pi * AR / (Cla * cos_sweep)
    # F_D * sqrt(1 + (2 / F_D)^2) = hypot(F_D, 2). Dividing F_D by (2 + hypot) before the
    # multiplications avoids a false overflow of (2 / F_D)^2 for a very small F_D.
    slope = (
        Cla * cos_sweep * (A_f / A_ref) * (fin_parameter / (2.0 + math.hypot(fin_parameter, 2.0)))
    )
    return finite_result(slope)


single_fin_normal_force_slope = FormulaSpec(
    id="aerodynamics.single_fin_normal_force_slope",
    name="Subsonic Normal-Force Slope of a Single Fin (Diederich)",
    equation=(
        "CN_alpha1 = Cla * FD * (A_f / A_ref) * cos(Gc) / (2 + FD * sqrt(1 + (2 / FD)^2)),  "
        "FD = 2 * pi * AR / (Cla * cos(Gc))"
    ),
    description=(
        "Slope of the normal-force coefficient with angle of attack for one thin fin in "
        "subsonic flow, from Diederich's planform correlation parameter and the "
        "two-dimensional section lift slope. Part of Barrowman's method for the stability "
        "of finned slender vehicles; the coefficient is referred to the reference area "
        "A_ref. Fin-set multiplication and fin-body interference are not included."
    ),
    inputs=(
        VariableSpec(
            name="Cla",
            symbol="C_{N alpha 0}",
            description=(
                "Two-dimensional section normal-force slope, 2*pi/beta for thin-airfoil "
                "theory with the Gothert/Prandtl compressibility correction"
            ),
            dimension="1",
            si_unit="1/rad",
        ),
        VariableSpec(
            name="AR",
            symbol="AR",
            description=(
                "Aspect ratio of the exposed fin. The source does not define it; this module "
                "uses AR = 2 s^2 / A_f, with s the span and A_f the area of one panel (twice "
                "s^2 / A_f), and the tests and verification cases use that convention"
            ),
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="Gc",
            symbol="Gamma_c",
            description="Sweep angle of the mid-chord line",
            dimension="1",
            si_unit="rad",
        ),
        VariableSpec(
            name="A_f",
            symbol="A_f",
            description="Planform area of one exposed fin panel",
            dimension="L^2",
            si_unit="m^2",
        ),
        VariableSpec(
            name="A_ref",
            symbol="A_r",
            description="Reference area, typically the body cross-section",
            dimension="L^2",
            si_unit="m^2",
        ),
    ),
    output=VariableSpec(
        name="CN_alpha1",
        symbol="C_{N alpha,1}",
        description="Normal-force coefficient slope of one fin, referred to A_ref",
        dimension="1",
        si_unit="1/rad",
    ),
    evaluator=_evaluate,
    references=(
        # Stated: eq. (3-1) is evaluated as printed, with F_D from (3-2) and (3-4) and the
        # section slope C_N,alpha0 = 2 pi (thin airfoil) or 2 pi / beta (Gothert) from (3-5);
        # (3-6) is the same relation after substituting these (checked in the tests).
        # Symbols: C_N,alpha0 -> Cla, Gamma_c -> Gc, A_r -> A_ref.
        nasa_technical_report(
            "The Practical Calculation of the Aerodynamic Characteristics of Slender Finned "
            "Vehicles",
            ("J. S. Barrowman",),
            "NASA/TM-2001-209983",
            1967,
            "https://ntrs.nasa.gov/citations/20010047838",
            "sec. 3.11, eq. (3-1) with (3-2), (3-4), (3-5) and (3-6), p. 3",
            organization=(
                "NASA Goddard Space Flight Center (reissue of a March 1967 Catholic "
                "University of America master's dissertation)"
            ),
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={
                "Cla": 6.283185307179586,
                "AR": 2.2222222222222228,
                "Gc": 0.2914567944778671,
                "A_f": 0.009,
                "A_ref": 0.012667686977437444,
            },
            expected=1.959269389119581,
            rel_tol=1e-11,
            note=(
                "Fin with root chord 0.12 m, tip chord 0.06 m and span s = 0.1 m (one-panel "
                "area A_f = 0.009 m^2) on a 0.0635 m body radius at beta = 1; AR is entered "
                "with the convention AR = 2 s^2 / A_f = 2.2222 (s^2 / A_f would be 1.1111); "
                "50-digit mpmath evaluation of eq. (3-6)."
            ),
        ),
        VerificationCase(
            inputs={"Cla": 7.255197456936872, "AR": 1.0, "Gc": 0.3, "A_f": 0.004, "A_ref": 0.0125},
            expected=0.479192122133112,
            rel_tol=1e-11,
            note=(
                "Mach 0.5 (beta = sqrt(0.75)); AR = 1 is entered directly, as a number rather "
                "than from a planform (under AR = 2 s^2 / A_f it means s^2 = 0.002 m^2); "
                "50-digit mpmath evaluation of (3-6)."
            ),
        ),
        VerificationCase(
            inputs={"Cla": 6.283185307179586, "AR": 0.01, "Gc": 0.0, "A_f": 0.001, "A_ref": 0.01},
            expected=0.0015707865094405707,
            rel_tol=1e-11,
            note=(
                "Boundary case: very low aspect ratio, zero sweep; AR = 0.01 is entered "
                "directly (under AR = 2 s^2 / A_f it means s^2 = 5e-6 m^2); 50-digit mpmath, "
                "eq. (3-6)."
            ),
        ),
    ),
    assumptions=(
        "Barrowman's method: subsonic flow, thin fins and small angle of attack, using "
        "thin-airfoil theory for the section and Diederich's correlation for the planform. "
        "The slope is for one fin of a three- or four-fin set; supersonic fins need the "
        "source's separate strip theory, which is not included.",
        "The source lists AR only as the aspect ratio of the exposed fin and prints no formula "
        "for it, so the AR convention is not fixed by the source. This module's verification "
        "case with a planform uses AR = 2 s^2 / A_f, where s is the span and A_f the area of "
        "one panel. The other common convention, AR = s^2 / A_f, is half of that and, for the "
        "same fin, changes the result by a factor of up to 2 (1.7 for the first verification "
        "case; the slope is nearly proportional to AR at low aspect ratio). Use one "
        "convention consistently and check it against the source's own examples before "
        "comparing results.",
        "Cla is an input so that the compressibility correction 2*pi/beta, with "
        "beta = sqrt(1 - M^2) for subsonic Mach number M, stays explicit.",
        "Gc is the mid-chord sweep angle in radians with |Gc| < pi/2; lengths are consistent, "
        "with A_f and A_ref in the same area unit. The reference area is the one the "
        "coefficient is referred to, typically the body cross-section.",
    ),
    tags=("fin", "normal force", "Diederich", "Barrowman", "rocket aerodynamics", "subsonic"),
)
