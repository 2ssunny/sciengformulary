"""Conduction Shape Factor, Sphere Near an Isothermal Plane: S = 4 pi R / (1 - R / (2 h))."""

import math

from sciengformulary.catalog._domain import finite_result, positive
from sciengformulary.catalog._sources import ENGINEERING_ACCESSED, lienhard_heat_transfer
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase

_MAX_RADIUS_RATIO = 0.8


def _evaluate(R: float, h: float) -> float:  # noqa: N803 - symbol as written in the source
    positive("R", R)
    positive("h", h)
    if R / h >= _MAX_RADIUS_RATIO:
        raise ValueError(f"R / h must be below {_MAX_RADIUS_RATIO}, got R={R!r} and h={h!r}.")
    return finite_result(4.0 * math.pi * R / (1.0 - R / (2.0 * h)))


shape_factor_buried_sphere = FormulaSpec(
    id="heat_transfer.shape_factor_buried_sphere",
    name="Conduction Shape Factor, Sphere Near an Isothermal Plane",
    equation="S = 4 * pi * R / (1 - R / (2 * h))",
    description=(
        "Conduction shape factor between an isothermal sphere buried in a large solid and the "
        "isothermal plane surface of that solid; the heat rate is Q = S k (T_sphere - T_plane). "
        "It tends to the isolated-sphere value 4 pi R when the sphere is deep."
    ),
    inputs=(
        VariableSpec(
            name="R",
            symbol="R",
            description="Radius of the sphere, positive",
            dimension="L",
            si_unit="m",
        ),
        VariableSpec(
            name="h",
            symbol="h",
            description="Distance from the plane surface to the centre of the sphere",
            dimension="L",
            si_unit="m",
        ),
    ),
    output=VariableSpec(
        name="S",
        symbol="S",
        description="Conduction shape factor (Q = S k dT)",
        dimension="L",
        si_unit="m",
    ),
    evaluator=_evaluate,
    references=(
        # The source states the factor in terms of the sphere radius R; other compilations use
        # the diameter D = 2R and write 2 pi D / (1 - D / (4 Z)) with Z the depth of the
        # centre, which is the same expression. The source's table text does not restate that
        # h is measured to the sphere centre; the deep-burial limit 4 pi R and the image
        # solution both require it.
        lienhard_heat_transfer("sec. 5.7, Table 5.4 item 7, p. 246", accessed=ENGINEERING_ACCESSED),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"R": 0.5, "h": 100.0},
            expected=6.298932638776527,
            rel_tol=1e-12,
            note="Deep burial: 4 pi 0.5 / (1 - 0.5 / 200) evaluated with 50-digit arithmetic.",
        ),
        VerificationCase(
            inputs={"R": 0.79, "h": 1.0},
            expected=16.408979810485533,
            rel_tol=1e-12,
            note="Just inside the stated limit R / h < 0.8; 50-digit arithmetic (mpmath).",
        ),
    ),
    assumptions=(
        "Steady conduction with uniform conductivity; the sphere and the plane surface are each "
        "isothermal and the medium is otherwise very large.",
        "Stated by the source for R / h < 0.8, where h is the depth of the sphere centre below "
        "the plane; the evaluator raises ValueError at R / h >= 0.8.",
        "The expression is a first-order approximation (the leading image-sphere correction to "
        "the isolated-sphere value 4 pi R), not the exact solution. Against the exact "
        "image-sphere series it is low by about 0.06 % at R / h = 0.3, 0.6 % at 0.5, 3 % at "
        "0.7 and 6 % at 0.8 (checked with 40-digit mpmath arithmetic).",
        "Any consistent length unit; the shape factor has the dimension of length.",
    ),
    tags=("conduction", "shape factor", "sphere", "buried", "semi-infinite medium"),
)
