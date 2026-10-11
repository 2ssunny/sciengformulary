"""Verified chromatography formula catalog."""

from sciengformulary.catalog.chromatography.baseline_peak_resolution import (
    baseline_peak_resolution,
)
from sciengformulary.catalog.chromatography.baseline_plate_number import (
    baseline_plate_number,
)
from sciengformulary.catalog.chromatography.fundamental_resolution_estimate import (
    fundamental_resolution_estimate,
)
from sciengformulary.catalog.chromatography.plate_height import (
    plate_height,
)
from sciengformulary.catalog.chromatography.retention_factor import (
    retention_factor,
)
from sciengformulary.catalog.chromatography.separation_factor import (
    separation_factor,
)
from sciengformulary.catalog.chromatography.tlc_retardation_factor import (
    tlc_retardation_factor,
)
from sciengformulary.catalog.chromatography.van_deemter_optimum_velocity import (
    van_deemter_optimum_velocity,
)
from sciengformulary.catalog.chromatography.van_deemter_plate_height import (
    van_deemter_plate_height,
)
from sciengformulary.core import (
    FormulaSpec,
)

FORMULAS: tuple[FormulaSpec, ...] = (
    retention_factor,
    separation_factor,
    baseline_peak_resolution,
    baseline_plate_number,
    plate_height,
    fundamental_resolution_estimate,
    van_deemter_plate_height,
    van_deemter_optimum_velocity,
    tlc_retardation_factor,
)
