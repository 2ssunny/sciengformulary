"""Structures formulas."""

from sciengformulary.catalog.structures.angle_of_twist import angle_of_twist
from sciengformulary.catalog.structures.axial_deformation import axial_deformation
from sciengformulary.catalog.structures.bending_stress import bending_stress
from sciengformulary.catalog.structures.cantilever_tip_deflection import cantilever_tip_deflection
from sciengformulary.catalog.structures.rectangle_second_moment_of_area import (
    rectangle_second_moment_of_area,
)
from sciengformulary.catalog.structures.simply_supported_center_deflection import (
    simply_supported_center_deflection,
)
from sciengformulary.catalog.structures.solid_circle_polar_moment_of_area import (
    solid_circle_polar_moment_of_area,
)
from sciengformulary.catalog.structures.torsional_shear_stress import torsional_shear_stress
from sciengformulary.core import FormulaSpec

FORMULAS: tuple[FormulaSpec, ...] = (
    axial_deformation,
    rectangle_second_moment_of_area,
    solid_circle_polar_moment_of_area,
    bending_stress,
    torsional_shear_stress,
    angle_of_twist,
    cantilever_tip_deflection,
    simply_supported_center_deflection,
)
