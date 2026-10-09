# OpenStax provenance audit

Audit date: 2026-10-09. Scope: the 57 catalog formulas that cite OpenStax *University Physics*
(Volumes 1 to 3). Result: 39 formulas gained at least one independent reference, one wrong
locator was corrected, three wording errors were corrected, and 15 formulas still rest on
OpenStax alone. Every OpenStax reference was kept, because it records where the relation was
first taken from.

No equation, evaluator, variable, unit, tolerance or verification case was changed.

## Background

The OpenStax pages now state that the books are licensed CC BY-NC-SA 4.0 and that using them
for training, or for ingestion into a large-language-model or generative-AI offering, needs
OpenStax's written permission (checked 2026-10-09). This catalog is built to be consumed by
people, programs and AI agents, so it should not depend on OpenStax text, and every
relation should be supported by a source that can be cited without that restriction.

Equations, variable definitions and numerical values are facts and may be restated. The way a
source explains them (sentences, figures, worked-example narrative) is not reusable, and
CONTRIBUTING.md already requires original wording.

## Method

1. No OpenStax page, and no cached copy of one, was opened during the audit. OpenStax locators
   and any wording overlap therefore could not be checked here and are listed for human review.
2. Technical check of each formula: equation, evaluator, units and dimensions, assumptions,
   and an independent recomputation of every verification case with exact or high-precision
   arithmetic (never the evaluator).
3. Citation versus copied content, inside this repository only: each case note and prose
   field was classified as an ordinary citation (reference record, restated equation, numbers
   from a worked example) or as a possible copied expression.
4. Search for an independent source for each relation, in this order: NASA Glenn Beginner's
   Guide (one page per 10 s, robots.txt honoured), NASA technical reports whose NTRS rights
   determination is `GOV_PUBLIC_USE_PERMITTED`, the NACA 1135 compilation, NIST publications,
   Lienhard and Lienhard *A Heat Transfer Textbook* (free PDF, equations restated only), the
   U.S. Standard Atmosphere 1976, and DOE Fundamentals Handbooks. Not used: OpenStax,
   Wikipedia, MathWorld, LibreTexts, HyperPhysics, paywalled or pirated copies, and MIT OCW
   for new citations.
5. Remediation (this change): the alternatives were added after the existing references with
   the locator found in the audit; a code comment records any algebraic step, and a
   `Derived result:` assumption was added where the new source is the only non-OpenStax support
   for the relation and does not print it in the catalog's form.

Rights status of the added sources:

| Source | Status |
|---|---|
| NASA Glenn Beginner's Guide pages | Existing `nasa_glenn` builder; page opened 2026-10-09 |
| NTRS reports (NASA TM-87572, NASA-CR-188300, NASA/CR-2005-213034, U.S. Standard Atmosphere 1976) | NTRS rights determination `GOV_PUBLIC_USE_PERMITTED`, no third-party material flagged |
| Lienhard and Lienhard, 6th ed. | Existing builder; free PDF of a copyrighted book, equations restated only |
| DOE Fundamentals Handbooks (DOE-HDBK-1010-92, 1012/1-92, 1017/1-93, 1019/1-93) | CONDITIONAL, see open questions |

## Results by formula

Columns: "OpenStax-only before" says whether the relation had no other source (44 formulas cited
nothing but OpenStax; 9 more cited only a CODATA constant page, which supports the constant and
not the relation). "Technical check" is the independent check; all verification cases
reproduced. Locators are those read in the alternative source (page numbers are printed page
numbers).

| Formula id | OpenStax-only before? | Alternative added | Technical check | Flags |
|---|---|---|---|---|
| mechanics.angular_momentum_rigid_body | yes (no other reference) | none | Correct | still OpenStax-only |
| mechanics.centripetal_acceleration | yes (no other reference) | none | Correct | still OpenStax-only |
| mechanics.circular_motion_period | yes (no other reference) | none | Correct | case note cites a worked example; still OpenStax-only |
| mechanics.constant_acceleration_position | yes (no other reference) | NASA Glenn "Ballistic Flight Equations", Motion section; NASA Glenn "Rocket Translation", Velocity and Acceleration sections (derived; see Derived result assumption) | Correct | - |
| mechanics.constant_acceleration_speed_squared | yes (no other reference) | NASA Glenn "Ballistic Flight Equations", Motion section (derived; see Derived result assumption) | Correct | case note cites a worked example |
| mechanics.constant_acceleration_velocity | yes (no other reference) | NASA Glenn "Ballistic Flight Equations", Motion section; NASA Glenn "Newton's Laws of Motion", Newton's Second Law section (derived; see Derived result assumption) | Correct | case note cites a worked example |
| mechanics.critical_damping_coefficient | yes (no other reference) | none | Correct | still OpenStax-only |
| mechanics.damped_angular_frequency | yes (no other reference) | none | Correct; description wording ("slightly below") corrected | still OpenStax-only |
| mechanics.forced_vibration_amplitude | yes (no other reference) | none | Correct | still OpenStax-only |
| mechanics.gravitational_force | no (other source already cited) | DOE-HDBK-1010-92, Module 3 'Force and Motion', Newton's Laws of Motion, eq. (3-2), p. 2 (CP-03) | Correct | - |
| mechanics.gravitational_potential_energy | yes (no other reference) | DOE-HDBK-1010-92, Module 5 'Energy, Work, and Power', Potential Energy, eq. (5-1), p. 2 (CP-05) | Correct; description wording ("Change in") corrected | case note cites a worked example |
| mechanics.impulse_of_constant_force | yes (no other reference) | NASA Glenn "Newton's Laws of Motion", Newton's Second Law section; DOE-HDBK-1010-92, Module 3 'Force and Motion', Momentum Principles, eqs. (3-4) to (3-6), pp. 5-6 (CP-03) (derived; see Derived result assumption) | Correct | - |
| mechanics.kinetic_friction_force | yes (no other reference) | DOE-HDBK-1010-92, Module 4 'Application of Newton's Laws', Types of Force: Friction, eq. (4-6), p. 19 (CP-04) | Correct | - |
| mechanics.linear_drag_falling_speed | yes (no other reference) | none | Correct | still OpenStax-only |
| mechanics.natural_angular_frequency | yes (no other reference) | none | Correct | still OpenStax-only |
| mechanics.parallel_axis_moment_of_inertia | yes (no other reference) | none | Correct | still OpenStax-only |
| mechanics.rotational_kinetic_energy | yes (no other reference) | none | Correct | case note cites a worked example; still OpenStax-only |
| mechanics.static_friction_limit | yes (no other reference) | DOE-HDBK-1010-92, Module 4 'Application of Newton's Laws', Types of Force: Friction, eq. (4-5), p. 19 (CP-04) | Correct | possible copied prose: assumptions[1] |
| mechanics.tangential_speed | yes (no other reference) | none | Correct | still OpenStax-only |
| mechanics.translational_kinetic_energy | yes (no other reference) | DOE-HDBK-1010-92, Module 5 'Energy, Work, and Power', Kinetic Energy, eq. (5-2), p. 2 (CP-05) | Correct | case note cites a worked example |
| mechanics.weight | yes (no other reference) | DOE-HDBK-1010-92, Module 4 'Application of Newton's Laws', Force and Weight, eq. (4-2), p. 2 (CP-04); NASA Glenn "Free Falling Objects", Falling through Vacuum, weight equation | Correct | case note cites a worked example |
| electrical.ohms_law_voltage | yes (no other reference) | Lienhard, sec. 2.3, eq. (2.18), p. 63 | Correct | - |
| electrical.conductor_resistance | yes (no other reference) | Lienhard, sec. 2.3, eqs. (2.17b)-(2.18), p. 63 | Correct | - |
| fluids.hydrostatic_pressure_difference | yes (no other reference) | U.S. Standard Atmosphere 1976 (NTRS), sec. 1.2.2, eq. (4), p. 6 (derived; see Derived result assumption) | Correct | possible copied prose: description |
| fluids.mass_flow_rate | no (other source already cited) | none needed | Correct | - |
| fluids.poiseuille_volume_flow_rate | yes (no other reference) | Lienhard, sec. 7.2, eqs. (7.14)-(7.15), p. 358 (derived; see Derived result assumption) | Correct | possible copied prose: assumptions[1] |
| fluids.stokes_drag_force | yes (no other reference) | Lienhard, sec. 11.10, footnote 24, p. 692 | Correct | possible copied prose: assumptions[0] |
| heat_transfer.plane_wall_conduction_rate | no (other source already cited) | none (existing Lienhard locator corrected) | Correct; Lienhard locator corrected; declared K vs Celsius case flagged | - |
| heat_transfer.photon_energy | yes (relation; other refs are constants only) | Lienhard, sec. 10.5, p. 582 (derived; see Derived result assumption) | Correct; domain placement only noted | - |
| heat_transfer.blackbody_emissive_power | yes (relation; other refs are constants only) | Lienhard, sec. 1.3, eq. (1.28), p. 30 | Correct; truncated sigma constant flagged (3.3e-11 rel.) | - |
| heat_transfer.net_radiative_exchange | yes (relation; other refs are constants only) | Lienhard, sec. 1.3, eqs. (1.34)-(1.35), p. 33 | Correct; truncated sigma constant flagged (3.3e-11 rel.) | - |
| heat_transfer.wien_peak_wavelength | yes (relation; other refs are constants only) | Lienhard, sec. 1.3, eq. (1.29), p. 30 | Correct; truncated b constant flagged (6.4e-11 rel.) | - |
| materials.engineering_stress | yes (no other reference) | DOE-HDBK-1017/1-93, Module 2 Properties of Metals, 'Stress' summary p. 6; eq. (2-4), p. 12 | Correct | possible copied prose: assumptions[1] |
| materials.engineering_strain | yes (no other reference) | DOE-HDBK-1017/1-93, Module 2 Properties of Metals, eq. (2-2), p. 7; eq. (2-5), p. 12 | Correct | - |
| materials.uniaxial_hookes_law | yes (no other reference) | DOE-HDBK-1017/1-93, Module 2 Properties of Metals, 'Young's Modulus', eqs. (2-6)-(2-7), p. 12 | Correct | - |
| materials.thermal_strain | yes (no other reference) | NASA TM-87572, sec. 5 'Results and Discussion', p. 5 (derived; see Derived result assumption) | Correct | weak support |
| nuclear.radioactive_decay | yes (no other reference) | DOE-HDBK-1019/1-93, Module 1 Radioactivity, eq. (1-4), p. 31 (also (1-5), p. 32) | Correct | possible copied prose: assumptions[1] |
| nuclear.half_life | yes (no other reference) | DOE-HDBK-1019/1-93, Module 1 Radioactivity, eq. (1-6), p. 32 | Correct | - |
| nuclear.activity | yes (no other reference) | DOE-HDBK-1019/1-93, Module 1 Radioactivity, eq. (1-3), p. 31 | Correct | - |
| orbital.specific_orbital_energy | yes (no other reference) | NASA/CR-2005-213034, eq. (12), p. 19 | Correct | possible copied prose: description |
| orbital.elliptical_orbit_specific_energy | yes (no other reference) | NASA/CR-2005-213034, eq. (19), p. 20 | Correct | - |
| orbital.semi_major_axis_from_apsides | yes (no other reference) | NASA/CR-2005-213034, eq. (6), p. 16 | Correct | - |
| orbital.orbital_period | yes (no other reference) | NASA/CR-2005-213034, eq. (10), p. 16; eq. (25), p. 20 (derived; see Derived result assumption) | Correct | - |
| orbital.gravitational_parameter_from_surface_gravity | yes (no other reference) | U.S. Standard Atmosphere 1976 (NTRS), sec. 1.2.3, eq. (17), p. 8 (derived; see Derived result assumption) | Correct | - |
| thermodynamics.mean_molecular_translational_kinetic_energy | yes (relation; other refs are constants only) | none | Correct | still OpenStax-only |
| thermodynamics.monatomic_ideal_gas_internal_energy | yes (relation; other refs are constants only) | none | Correct | still OpenStax-only |
| thermodynamics.maxwell_speed_distribution | yes (relation; other refs are constants only) | none | Correct | still OpenStax-only; partial sources (mode, mean speed) not added |
| thermodynamics.mean_molecular_speed | yes (relation; other refs are constants only) | U.S. Standard Atmosphere 1976 (NTRS), sec. 1.3.7, eq. (46), p. 17; Lienhard, sec. 11.10, eq. (11.101), p. 686 | Correct | - |
| thermodynamics.rms_molecular_speed | yes (relation; other refs are constants only) | none | Correct | still OpenStax-only |
| thermodynamics.mean_free_path | yes (no other reference) | U.S. Standard Atmosphere 1976 (NTRS), sec. 1.3.8, eq. (47), p. 17; Lienhard, sec. 11.10, eq. (11.102), p. 686 | Correct; assumption wording ("T must be absolute", no T input) corrected | - |
| thermodynamics.isothermal_work | yes (no other reference) | DOE-HDBK-1012/1-92, Module 1, eq. (1-43), p. 98; work as the area under the P-V curve, p. 98; NASA Glenn "Work Done by a Gas", page body, 'Equations' (derived; see Derived result assumption) | Correct; coarse OpenStax locator (section only) | - |
| thermodynamics.isothermal_entropy_change | yes (no other reference) | DOE-HDBK-1012/1-92, Module 1, 'Entropy', eqs. (1-18)-(1-19), p. 22; Lienhard, sec. 1.2, eq. (1.6), p. 9; eq. (1.4), p. 8; NASA Glenn "Second Law - Entropy", page body, first displayed equation | Correct | - |
| thermodynamics.isentropic_temperature_ratio | no (other source already cited) | none needed | Correct | - |
| thermodynamics.heat_engine_efficiency | yes (no other reference) | DOE-HDBK-1012/1-92, Module 1, 'Carnot Cycle', eq. (1-23), p. 73 | Correct | - |
| thermodynamics.carnot_efficiency | yes (no other reference) | DOE-HDBK-1012/1-92, Module 1, 'Carnot Cycle', eq. (1-23), p. 73 | Correct | - |
| thermodynamics.carnot_refrigerator_cop | yes (no other reference) | NASA-CR-188300, p. 57; DOE-HDBK-1012/1-92, Module 1, eq. (1-23), p. 73 plus reversal argument | Correct | - |
| thermodynamics.sensible_heat | yes (no other reference) | DOE-HDBK-1012/1-92, Module 1, 'Heat', eq. (1-17), p. 21; Lienhard, sec. 1.2, eqs. (1.2b), (1.2c), (1.3), p. 7 | Correct | - |

Summary: 39 formulas gained references (10 mechanics, 29 in other domains). Formulas gaining
each source: DOE handbooks 19, Lienhard 12, NASA Glenn pages 7 (6 distinct pages), U.S. Standard
Atmosphere 1976 4, NASA/CR-2005-213034 4, NASA TM-87572 1, NASA-CR-188300 1 (some formulas gained
more than one source).

## Corrections made

- `heat_transfer.plane_wall_conduction_rate`: the Lienhard locator read "sec. 2.3, eq. (2.16)".
  Equation (2.16) is on p. 62 in sec. 2.2, and the scalar law is eq. (1.9), sec. 1.3, p. 13
  (checked in the PDF). The locator now reads "sec. 1.3, eq. (1.9), p. 13; sec. 2.2, eq. (2.16),
  p. 62".
- `thermodynamics.mean_free_path`: assumption "T must be absolute" removed; the formula has no
  temperature input. The assumption now says n is the molecule number density (n = p / (k T)).
- `mechanics.gravitational_potential_energy`: the description said "Change in"; the output is
  the potential energy relative to the datum.
- `mechanics.damped_angular_frequency`: "slightly below" is true only for light damping; the
  description now says the frequency falls to zero as damping approaches its critical value.

## Needs human review

### 1. OpenStax locators (all 57 formulas)

None of these could be checked. Confirm that each section and equation number exists, supports
the stated assumptions, and matches the notation noted in the code comments.

- mechanics.angular_momentum_rigid_body: Vol. 1, sec. 11.2, eq. (11.9)
- mechanics.centripetal_acceleration: Vol. 1, sec. 4.4, eq. (4.27)
- mechanics.circular_motion_period: Vol. 1, sec. 4.4
- mechanics.constant_acceleration_position: Vol. 1, sec. 3.4, eq. (3.13)
- mechanics.constant_acceleration_speed_squared: Vol. 1, sec. 3.4, eq. (3.14)
- mechanics.constant_acceleration_velocity: Vol. 1, sec. 3.4, eq. (3.12)
- mechanics.critical_damping_coefficient: Vol. 1, sec. 15.5
- mechanics.damped_angular_frequency: Vol. 1, sec. 15.5, eq. (15.26)
- mechanics.forced_vibration_amplitude: Vol. 1, sec. 15.6, eq. (15.29)
- mechanics.gravitational_force: Vol. 1, sec. 13.1, eq. (13.1)
- mechanics.gravitational_potential_energy: Vol. 1, sec. 8.1, eq. (8.5)
- mechanics.impulse_of_constant_force: Vol. 1, sec. 9.2, eq. (9.5)
- mechanics.kinetic_friction_force: Vol. 1, sec. 6.2, eq. (6.2)
- mechanics.linear_drag_falling_speed: Vol. 1, sec. 6.4
- mechanics.natural_angular_frequency: Vol. 1, sec. 15.1, eq. (15.9)
- mechanics.parallel_axis_moment_of_inertia: Vol. 1, sec. 10.5, eq. (10.20)
- mechanics.rotational_kinetic_energy: Vol. 1, sec. 10.4, eq. (10.18)
- mechanics.static_friction_limit: Vol. 1, sec. 6.2, eq. (6.1)
- mechanics.tangential_speed: Vol. 1, sec. 10.3
- mechanics.translational_kinetic_energy: Vol. 1, sec. 7.2, eq. (7.6)
- mechanics.weight: Vol. 1, sec. 5.4, eq. (5.9)
- electrical.ohms_law_voltage: Vol. 2, sec. 9.4, eq. (9.11)
- electrical.conductor_resistance: Vol. 2, sec. 9.3, eq. (9.9)
- fluids.hydrostatic_pressure_difference: Vol. 1, sec. 14.1, eq. (14.4)
- fluids.mass_flow_rate: Vol. 1, sec. 14.5, eq. (14.15)
- fluids.poiseuille_volume_flow_rate: Vol. 1, sec. 14.7, eq. (14.19)
- fluids.stokes_drag_force: Vol. 1, sec. 6.4, eq. (6.6)
- heat_transfer.plane_wall_conduction_rate: Vol. 2, sec. 1.6, eq. (1.9)
- heat_transfer.photon_energy: Vol. 3, sec. 6.2, eq. (6.13)
- heat_transfer.blackbody_emissive_power: Vol. 3, sec. 6.1, eq. (6.4)
- heat_transfer.net_radiative_exchange: Vol. 2, sec. 1.6, eq. (1.10)
- heat_transfer.wien_peak_wavelength: Vol. 3, sec. 6.1, eq. (6.1)
- materials.engineering_stress: Vol. 1, sec. 12.3, eq. (12.34)
- materials.engineering_strain: Vol. 1, sec. 12.3, eq. (12.35)
- materials.uniaxial_hookes_law: Vol. 1, sec. 12.3, eq. (12.36)
- materials.thermal_strain: Vol. 2, sec. 1.3, eq. (1.2)
- nuclear.radioactive_decay: Vol. 3, sec. 10.3, eq. (10.11)
- nuclear.half_life: Vol. 3, sec. 10.3, eqs. (10.13)-(10.15)
- nuclear.activity: Vol. 3, sec. 10.3, eq. (10.17)
- orbital.specific_orbital_energy: Vol. 1, sec. 13.3, eq. (13.5)
- orbital.elliptical_orbit_specific_energy: Vol. 1, sec. 13.5
- orbital.elliptical_orbit_specific_energy: Vol. 1, sec. 13.4, eq. (13.9)
- orbital.semi_major_axis_from_apsides: Vol. 1, sec. 13.5
- orbital.orbital_period: Vol. 1, sec. 13.5, eq. (13.11)
- orbital.gravitational_parameter_from_surface_gravity: Vol. 1, sec. 13.2, eq. (13.2)
- thermodynamics.mean_molecular_translational_kinetic_energy: Vol. 2, sec. 2.2, eq. (2.6)
- thermodynamics.monatomic_ideal_gas_internal_energy: Vol. 2, sec. 2.2, eq. (2.7)
- thermodynamics.maxwell_speed_distribution: Vol. 2, sec. 2.4, eq. (2.15)
- thermodynamics.mean_molecular_speed: Vol. 2, sec. 2.4, eq. (2.16)
- thermodynamics.rms_molecular_speed: Vol. 2, sec. 2.2, eq. (2.8)
- thermodynamics.mean_free_path: Vol. 2, sec. 2.2, eq. (2.10)
- thermodynamics.isothermal_work: Vol. 2, sec. 3.2
- thermodynamics.isothermal_entropy_change: Vol. 2, sec. 4.6, eq. (4.8)
- thermodynamics.isentropic_temperature_ratio: Vol. 2, sec. 3.6, eq. (3.13)
- thermodynamics.heat_engine_efficiency: Vol. 2, sec. 4.2, eq. (4.2)
- thermodynamics.carnot_efficiency: Vol. 2, sec. 4.5, eq. (4.5)
- thermodynamics.carnot_refrigerator_cop: Vol. 2, sec. 4.5, eq. (4.6)
- thermodynamics.sensible_heat: Vol. 2, sec. 1.4, eq. (1.5)

Locators the audit marked as especially uncertain: `thermodynamics.isothermal_work` ("sec. 3.2",
no equation number, and the book form is presumably n R T ln(V2/V1) while the catalog uses the
specific gas constant), and the code comments in `mechanics.damped_angular_frequency`,
`mechanics.forced_vibration_amplitude`, `mechanics.linear_drag_falling_speed` and
`mechanics.gravitational_potential_energy`, which describe how the book writes the relation.

### 2. Possibly copied prose

Compare these repository fields with the OpenStax text. All are low confidence: generic
textbook-style sentences, not distinctive phrasing.

| Field | Reason |
|---|---|
| `mechanics.static_friction_limit` assumptions[1] | Explanatory sentence on static friction balancing the applied force below impending motion |
| `fluids.hydrostatic_pressure_difference` description | "Weight of the column above, per unit area" is a common textbook gloss |
| `fluids.poiseuille_volume_flow_rate` assumptions[1] | Reynolds-number thresholds sentence follows the cited section ("the cited section gives ...") |
| `fluids.stokes_drag_force` assumptions[0] | Linear-versus-quadratic drag sentence reads like a textbook sentence |
| `materials.engineering_stress` assumptions[1] | Original-area and necking remark is a standard textbook remark |
| `nuclear.radioactive_decay` assumptions[1] | Generic "statistical law, large N" phrasing |
| `orbital.specific_orbital_energy` description | Textbook-style sentence on mechanical energy per unit mass and bound orbits |

For all 57 formulas, also compare the descriptions, variable descriptions and assumptions with
the book for wording overlap.

### 3. Verification-case numbers that may come from OpenStax worked examples

The case notes of `mechanics.circular_motion_period`, `constant_acceleration_speed_squared`,
`constant_acceleration_velocity`, `gravitational_potential_energy`, `rotational_kinetic_energy`,
`translational_kinetic_energy` and `weight` say the inputs follow a worked example of the cited
section. Numbers are facts, but a human should confirm that only the numbers (not the
explanation) were reused. For the 36 formulas outside mechanics the notes do not claim a worked
example, but this could not be excluded without opening the book.

### 4. Formulas still supported only by OpenStax (15)

| Formula | Kind of source needed |
|---|---|
| `mechanics.angular_momentum_rigid_body`, `centripetal_acceleration`, `circular_motion_period`, `parallel_axis_moment_of_inertia`, `rotational_kinetic_energy`, `tangential_speed` | NASA, DOE or NIST primer on rotational kinematics and rigid-body dynamics. DOE-HDBK-1010 states only that circular motion needs a centripetal force, and the NASA Glenn rotation page does not print the equations. NTRS flywheel reports with `GOV_PUBLIC_USE_PERMITTED` exist but were not read |
| `mechanics.critical_damping_coefficient`, `damped_angular_frequency`, `forced_vibration_amplitude`, `natural_angular_frequency` | Mechanical-vibration or engineering-dynamics primer for the single-degree-of-freedom mass-spring-damper. Neither DOE-HDBK-1010 nor the NASA Glenn Guide has it |
| `mechanics.linear_drag_falling_speed` | Source solving m dv/dt = m g - c v. The NASA Glenn drag page covers drag proportional to v^2 only. Alternatively, document the separable-ODE derivation in the description |
| `thermodynamics.mean_molecular_translational_kinetic_energy`, `monatomic_ideal_gas_internal_energy`, `rms_molecular_speed` | Kinetic-theory source printing (3/2) k T, U = (3/2) N k T, or v_rms |
| `thermodynamics.maxwell_speed_distribution` | Source printing the speed density f(v). DOE-HDBK-1019/1 eq. (2-13) gives only the most probable speed and Lienhard eq. (11.101) only the mean speed; these partial sources were not added |

Weakly supported (reference added, but the support is thin): `materials.thermal_strain` (one
sentence defining the expansion coefficient as d(strain)/dT), `thermodynamics.isothermal_work`
(DOE and NASA Glenn print the ideal-gas law and work as an area, not the logarithm),
`fluids.stokes_drag_force` (a footnote in Lienhard), `thermodynamics.heat_engine_efficiency`
(DOE prints it in the Carnot-cycle context), `thermodynamics.carnot_refrigerator_cop` (NASA
CR-188300 gives it in a design worksheet, DOE only by a reversal argument), and
`materials.engineering_stress` (the DOE text does not say the original area is used, so that
qualifier rests on OpenStax).

### 5. Truncated constants (flagged, not changed)

- Stefan-Boltzmann constant in `heat_transfer.blackbody_emissive_power` and
  `net_radiative_exchange`: the catalog value 5.670374419e-8 is truncated; the full-precision
  CODATA 2022 value differs by 3.3e-11 relative, so the cases are about 3.2e-11 relative below
  the full-precision result. The case note's "exact arithmetic" is exact for the truncated
  value.
- Wien constant in `heat_transfer.wien_peak_wavelength`: 2.897771955e-3 m K differs from the
  full-precision value by 6.4e-11 relative. The Lienhard book prints it to six digits only.

### 6. Other points noted

- `heat_transfer.plane_wall_conduction_rate`: the variables are declared in kelvin, while the
  case uses degrees Celsius (110 and 50). Only the difference enters, so the result is right,
  but the declared unit and the case disagree.
- `heat_transfer.photon_energy` sits in heat_transfer because it supports radiation; a
  classification question only.
- All new locators, DOE and NTRS URLs and the NTRS-derived author names were taken from the
  audit records and local copies; a reviewer should open each source once.
- The DOE handbooks number two different equations (4-5) in Module 4; the friction law is the
  one in "Types of Force".

## Open rights questions

1. DOE Fundamentals Handbooks (19 formulas): the handbooks carry Distribution Statement A
   (approved for public release) and no copyright notice, but were prepared for DOE with help
   from a contractor. Status CONDITIONAL: usable for citation, but the maintainers should
   decide whether that is enough. Only equations and numbers are restated.
2. Lienhard and Lienhard: a free PDF of a copyrighted book. Citing it and restating equations
   is the same practice as the existing references; confirm the maintainers accept it for the
   12 formulas that now use it.
3. NTRS reports: rights are per document. The four used here carry `GOV_PUBLIC_USE_PERMITTED`;
   two (CR-188300, CR-2005-213034) are contractor or university reports on NTRS, which the
   determination nevertheless covers.
4. MIT OCW: not used for any new citation here (the existing Roylance records are untouched).
5. Whether continuing to cite OpenStax, as historical attribution of where a relation was
   taken from, is acceptable under CC BY-NC-SA 4.0 and the OpenStax AI clause, and whether any
   repository prose counts as an adaptation of the book (see section 2), is a decision for the
   maintainers. If any OpenStax reference is to be removed, the 15 OpenStax-only formulas must
   first get another source.
