# Provenance: engineering batch E1 (solids, fluids, thermal)

Sanitized record of how this engineering batch was found, checked and licensed. Candidates were
discovered in open-source engineering libraries; a library never counted as support. Each
implemented formula cites an authoritative source opened during verification. No source text.

## Sources cited by the implemented formulas

| Source | Implemented formulas citing it |
|---|---|
| J. H. Lienhard V, J. H. Lienhard IV: A Heat Transfer Textbook | 42 |
| Massachusetts Institute of Technology: Beam Displacements | 6 |
| U.S. Geological Survey: Water-Supply Paper 1898-B | 3 |
| National Institute of Standards and Technology: CODATA Value: Stefan-Boltzmann constant | 2 |
| Massachusetts Institute of Technology: Trusses | 2 |
| Massachusetts Institute of Technology: Introduction to Elasticity | 1 |
| NASA Glenn Research Center: Torque (Moment) | 1 |
| Massachusetts Institute of Technology: Laminated Composite Plates | 1 |
| National Institute of Standards and Technology: NIST Chemistry WebBook, NIST Standard Reference Database Number 69 | 1 |

Rights notes: textbooks and reports are cited, never copied. OpenStax is excluded (its pages
forbid ingestion into AI systems). MIT OCW notes (Roylance) are CC BY-NC-SA and only cited.
Standards (ISO 5167, ASME MFC, IEC, ASHRAE) and their coefficient tables are not used.

## Counts

- Candidates: 138 scalar + 9 deferred (non-scalar, kept for a future schema).
- Candidate gates: AMBIGUOUS 5, DUPLICATE 24, UNVERIFIED 58, VERIFIED 51.
- Formula records from verification: 116 (AMBIGUOUS 4, DUPLICATE 3, UNVERIFIED 58, VERIFIED 51).
- Implemented: 50; verified and held: 1; verified, implementation pending: 0.
- Candidates not yet verified (awaiting verification): 0.

## Implemented formulas

| Formula id | Form | Supporting references (locator) | Discovered in | Cases |
|---|---|---|---|---|
| `fluids.bond_number` | stated | J. H. Lienhard V: Appendix C (nomenclature), p. 772; eq. (9.14) and the sentence after it, p. 496 | FLUIDS_CHEDL | 3 |
| `fluids.chezy_coefficient_from_manning` | stated | J. T. Limerinos: p. B8, eq. (6) ('metric units') | FLUIDS_CHEDL | 3 |
| `fluids.chezy_velocity` | stated | J. T. Limerinos: p. B7, eq. (3) | FLUIDS_CHEDL | 3 |
| `fluids.darcy_weisbach_pressure_drop` | derived | J. H. Lienhard V: sec. 7.3, eq. (7.33), p. 367 | FLUIDS_CHEDL | 3 |
| `fluids.filonenko_smooth_pipe_friction_factor` | stated | J. H. Lienhard V: sec. 7.3, eq. (7.42), p. 369; worked value p. 372 | LIENHARD_AHTT | 3 |
| `fluids.haaland_friction_factor` | stated | J. H. Lienhard V: sec. 7.3, eq. (7.50), p. 373 | FLUIDS_CHEDL | 5 |
| `fluids.laminar_darcy_friction_factor` | derived | J. H. Lienhard V: sec. 7.3, Fig. 7.6, p. 370; J. H. Lienhard V: sec. 7.2, eqs. (7.14)-(7.15), p. 358; sec. 7.3, eq. (7.33), p. 367 | FLUIDS_CHEDL | 4 |
| `fluids.manning_velocity` | derived | J. T. Limerinos: p. B3, eq. (1) (English units); p. B7, eq. (3) and p. B8, eq. (6) with the substitution paragraph and the English-unit result that follows it | FLUIDS_CHEDL | 4 |
| `fluids.smooth_pipe_friction_factor_power_law` | derived | J. H. Lienhard V: sec. 7.3, eq. (7.38), p. 368 | LIENHARD_AHTT | 3 |
| `fluids.strouhal_number` | stated | J. H. Lienhard V: eq. (7.64), p. 387 | FLUIDS_CHEDL | 3 |
| `fluids.weber_number` | stated | J. H. Lienhard V: eq. (9.39) and following definition, p. 510; J. H. Lienhard V: p. 520 (flow-boiling burnout, Katto discussion) | FLUIDS_CHEDL | 3 |
| `heat_transfer.churchill_bernstein_cylinder_nusselt` | stated | J. H. Lienhard V: sec. 7.6, eq. (7.65), pp. 390-391 | HT_CHEDL | 3 |
| `heat_transfer.churchill_chu_horizontal_cylinder_nusselt` | derived | J. H. Lienhard V: sec. 8.4, eq. (8.29), pp. 430-431; J. H. Lienhard V: sec. 8.4, Example 8.4, p. 431 | HT_CHEDL | 4 |
| `heat_transfer.churchill_chu_vertical_plate_nusselt` | stated | J. H. Lienhard V: sec. 8.3, eq. (8.13b), p. 420 | HT_CHEDL | 3 |
| `heat_transfer.colburn_pipe_nusselt` | stated | J. H. Lienhard V: sec. 7.3, eq. (7.39a), p. 368 | HT_CHEDL | 2 |
| `heat_transfer.concentric_cylinder_radiation_exchange` | derived | J. H. Lienhard V: sec. 10.4, Example 10.5, eq. (10.27), p. 570; National Institute of Standards and Technology: 2022 CODATA recommended value | MODELICA_MSL | 2 |
| `heat_transfer.counterflow_effectiveness` | derived | J. H. Lienhard V: sec. 3.3, eq. (3.21), p. 122 | HT_CHEDL | 3 |
| `heat_transfer.crossflow_cmax_mixed_effectiveness` | stated | J. H. Lienhard V: sec. 3.3, Table 3.1 (crossflow, one stream mixed: Cmax mixed, Cmin unmixed), p. 125 | HT_CHEDL | 2 |
| `heat_transfer.crossflow_cmin_mixed_effectiveness` | derived | J. H. Lienhard V: sec. 3.3, Table 3.1 (crossflow, one stream mixed: Cmin mixed, Cmax unmixed), p. 125 | HT_CHEDL | 2 |
| `heat_transfer.cylindrical_wall_thermal_resistance` | stated | J. H. Lienhard V: sec. 2.3, eq. (2.25), p. 69 and Example 2.6, p. 70; J. H. Lienhard V: sec. 5.7, Table 5.4 item 2, p. 246 | HT_CHEDL, MODELICA_MSL | 3 |
| `heat_transfer.eckert_number` | stated | J. H. Lienhard V: sec. 6.5, p. 310 (list of conditions for the laminar flat-plate results) | FLUIDS_CHEDL | 2 |
| `heat_transfer.gnielinski_nusselt` | stated | J. H. Lienhard V: sec. 7.3, eq. (7.41), p. 369; J. H. Lienhard V: sec. 7.3, p. 371 and Example 7.3, p. 372 | HT_CHEDL | 3 |
| `heat_transfer.gnielinski_smooth_tube_nusselt` | stated | J. H. Lienhard V: sec. 7.3, eq. (7.43a), p. 371 | HT_CHEDL | 3 |
| `heat_transfer.graetz_number` | stated | J. H. Lienhard V: sec. 7.2, eq. (7.26), p. 362 | FLUIDS_CHEDL | 2 |
| `heat_transfer.grashof_number` | stated | J. H. Lienhard V: sec. 8.3, eq. (8.9), p. 418 | FLUIDS_CHEDL | 3 |
| `heat_transfer.jakob_number` | stated | J. H. Lienhard V: sec. 8.5, eq. (8.48), p. 441 | FLUIDS_CHEDL | 2 |
| `heat_transfer.laminar_flat_plate_uniform_flux_local_nusselt` | stated | J. H. Lienhard V: sec. 6.5, eq. (6.71), p. 311 | MODELICA_MSL | 2 |
| `heat_transfer.number_of_transfer_units` | stated | J. H. Lienhard V: sec. 3.3, eq. (3.18), p. 122 | HT_CHEDL | 2 |
| `heat_transfer.parallel_flow_effectiveness` | stated | J. H. Lienhard V: sec. 3.3, eq. (3.20), p. 122 | HT_CHEDL | 4 |
| `heat_transfer.parallel_plate_radiation_exchange` | derived | J. H. Lienhard V: sec. 10.4, eqs. (10.23)-(10.25), pp. 568-569; National Institute of Standards and Technology: 2022 CODATA recommended value | MODELICA_MSL | 3 |
| `heat_transfer.peclet_number` | stated | J. H. Lienhard V: sec. 6.5, eq. (6.61), p. 307; J. H. Lienhard V: sec. 7.6, p. 391 | FLUIDS_CHEDL | 2 |
| `heat_transfer.phase_change_exchanger_effectiveness` | stated | J. H. Lienhard V: sec. 3.3, eq. (3.22), p. 126; limit of eqs. (3.20)-(3.21), p. 122 | HT_CHEDL | 3 |
| `heat_transfer.rayleigh_number` | stated | J. H. Lienhard V: sec. 8.3, eq. (8.11), p. 419 | FLUIDS_CHEDL | 2 |
| `heat_transfer.schmidt_number` | stated | J. H. Lienhard V: sec. 11.3, eq. (11.27), p. 632 | FLUIDS_CHEDL | 2 |
| `heat_transfer.shape_factor_buried_sphere` | stated | J. H. Lienhard V: sec. 5.7, Table 5.4 item 7, p. 246 | HT_CHEDL | 2 |
| `heat_transfer.shell_and_tube_one_shell_effectiveness` | derived | J. H. Lienhard V: sec. 3.3, Table 3.1 (one shell pass, two tube passes), p. 125 | HT_CHEDL | 3 |
| `heat_transfer.sherwood_number` | derived | J. H. Lienhard V: sec. 11.6, eq. (11.69) and Table 11.2, p. 658; named Sherwood number on p. 659 | FLUIDS_CHEDL | 2 |
| `heat_transfer.sieder_tate_turbulent_nusselt` | stated | J. H. Lienhard V: sec. 7.3, eq. (7.40), pp. 368-369 | HT_CHEDL | 2 |
| `mechanics.linear_spring_force` | derived | D. Roylance: section 'Stiffness', eq. (3), p. 5; eq. (7), p. 6 | MODELICA_MSL | 3 |
| `mechanics.torque_from_tangential_force` | stated | NASA Glenn Research Center: Example 1 | MODELICA_MSL | 3 |
| `structures.beam_rotational_stiffness_far_end_fixed` | derived | D. Roylance: eqs. (1)-(4), pp. 1-2; Fig. 6 and the superposition paragraph, p. 9 | PYNITE | 2 |
| `structures.fixed_bar_axial_reaction_linear_load` | derived | D. Roylance: p. 11 (constitutive delta = P L / (A E), compatibility, equilibrium) | PYNITE | 4 |
| `structures.fixed_bar_axial_reaction_point_load` | derived | D. Roylance: p. 11 (constitutive delta = P L / (A E), compatibility, equilibrium) | PYNITE | 3 |
| `structures.fixed_end_moment_applied_couple` | derived | D. Roylance: eqs. (1)-(4), pp. 1-2; Fig. 6 and the superposition paragraph, p. 9 | PYNITE | 4 |
| `structures.fixed_end_moment_partial_linear_load` | derived | D. Roylance: eqs. (1)-(4), pp. 1-2; Fig. 6 and the superposition paragraph, p. 9 | PYNITE | 5 |
| `structures.fixed_end_moment_point_load` | derived | D. Roylance: eqs. (1)-(4), pp. 1-2; Fig. 6 and the superposition paragraph, p. 9 | PYNITE | 4 |
| `structures.fixed_end_reaction_point_load` | derived | D. Roylance: eqs. (1)-(4), pp. 1-2; Fig. 6 and the superposition paragraph, p. 9 | PYNITE | 4 |
| `structures.fixed_guided_beam_lateral_stiffness` | derived | D. Roylance: eqs. (1)-(4), pp. 1-2; Fig. 6 and the superposition paragraph, p. 9 | PYNITE | 2 |
| `structures.plate_flexural_rigidity` | derived | D. Roylance: eq. (2), p. 2 and eq. (24), p. 9 | PYNITE | 3 |
| `thermodynamics.antoine_vapor_pressure` | stated | National Institute of Standards and Technology: 'Phase change data', block 'Antoine Equation Parameters'; J. H. Lienhard V: eq. (11.49), p. 645; fn. 8, p. 646 | THERMO_CHEDL | 3 |

## Not implemented

| Candidate / formula | Gate | Discovered in | Reason / source needed |
|---|---|---|---|
| `aerodynamics.critical_pressure_ratio` | DUPLICATE | FLUIDS_CHEDL | duplicate of `aerodynamics.isentropic_pressure_ratio (special case M=1)` |
| `aerodynamics.drag_force` | DUPLICATE | MODELICA_MSL | duplicate of `aerodynamics.drag_force` |
| `aerodynamics.mach_number` | DUPLICATE | FLUIDS_CHEDL | duplicate of `aerodynamics.mach_number` |
| `electrical.capacitive_reactance` | UNVERIFIED | MODELICA_MSL | Needs a circuits source stating X_C = 1/(omega C) for a sinusoidally driven ideal capacitor. NIST SP 330 (opened) gives only the unit definitions (farad = C/V). Textbook needed: OpenStax University Physics vol 2 (AC circ |
| `electrical.dc_machine_back_emf` | UNVERIFIED | MODELICA_MSL | Needs an electric-machines source for the ideal commutator machine relations V_emf = k omega and tau = k I with the same constant (power balance). Textbook needed: Fitzgerald, Kingsley & Umans, Electric Machinery, or Cha |
| `electrical.dc_machine_electromagnetic_torque` | UNVERIFIED | MODELICA_MSL | As for electrical.dc_machine_back_emf (tau = k I with the same SI constant, from V I = tau omega). Sign convention of the library (cut torque = -k i) not adopted. Textbook needed: Fitzgerald/Kingsley/Umans or Chapman. Op |
| `electrical.electric_power` | VERIFIED | MODELICA_MSL | verified only against a unit definition; held for a stronger source (planned: DOE Electrical Science handbook in batch E3) |
| `electrical.magnetic_permeance_hollow_cylinder_axial` | UNVERIFIED | MODELICA_MSL | Needs a magnetic-circuit source for reluctance/permeance of a prismatic (annular-sector) tube: G_m = mu_0 mu_r A / l with A = alpha (r_o^2 - r_i^2)/2. No allowed free source stating magnetic-circuit permeance found. Orig |
| `electrical.magnetic_permeance_hollow_cylinder_radial` | UNVERIFIED | MODELICA_MSL | Needs a source for the radial-flux permeance G_m = mu_0 mu_r alpha l / ln(r_o/r_i), a derived integral of the magnetic-circuit relation over a radial path. Same gap as the axial/prismatic items: Roters (1941) or a magnet |
| `electrical.magnetic_reluctance_prismatic` | UNVERIFIED | MODELICA_MSL | Needs a source for R_m = l / (mu_0 mu_r A) (or G_m = 1/R_m) of a uniform prismatic tube with no fringing. Same gap: Roters (1941) or a magnetic-circuit text. Candidate also notes mu_0 constant choice (4 pi 1e-7 vs CODATA |
| `electrical.ohms_law_voltage` | DUPLICATE | MODELICA_MSL | duplicate of `electrical.ohms_law_voltage` |
| `electrical.resistance_temperature_coefficient` | UNVERIFIED | MODELICA_MSL | Needs a source stating R(T) = R_ref (1 + alpha (T - T_ref)). A NIST SP 250-91 hit defines a temperature-dependent coefficient differently (not opened or used). Textbook needed: OpenStax University Physics vol 2 (resistiv |
| `electrical.synchronous_speed` | UNVERIFIED | FLUIDS_CHEDL | Needs a machine text stating N_s = 120 f / p (rpm, f in Hz, p poles). The library cites a web page (All About Circuits) which is not in the allowed source list. Textbook needed: Chapman, Electric Machinery Fundamentals,  |
| `fluids.archimedes_number` | UNVERIFIED | FLUIDS_CHEDL | Not in Lienhard (full-text keyword search, 800 pp.), not on the NASA Glenn Similarity Parameters page (only Re and Mach printed), not in OpenStax University Physics vol. 1 sections 14.5-14.6. Needs Perry's Chemical Engin |
| `fluids.blasius_friction_factor` | UNVERIFIED | FLUIDS_CHEDL | Lienhard prints only the different smooth-pipe power law f/4 = 0.046 Re^-0.2 (p. 368, listed as a separate NEW candidate); Blasius's 0.3164 Re^-1/4 is not printed in any opened source. Needs Blasius (1913, VDI Forschungs |
| `fluids.capillary_number` | UNVERIFIED | FLUIDS_CHEDL | Not in Lienhard (full-text keyword search, 800 pp.), not on the NASA Glenn Similarity Parameters page (only Re and Mach printed), not in OpenStax University Physics vol. 1 sections 14.5-14.6. Lienhard mentions capillary  |
| `fluids.cavitation_number` | UNVERIFIED | FLUIDS_CHEDL | Not in Lienhard (full-text keyword search, 800 pp.), not on the NASA Glenn Similarity Parameters page (only Re and Mach printed), not in OpenStax University Physics vol. 1 sections 14.5-14.6. Needs Cengel & Cimbala, Perr |
| `fluids.chen_friction_factor` | UNVERIFIED | FLUIDS_CHEDL | Only Haaland (7.50) and Filonenko (7.42) are printed by Lienhard. Needs Chen, Ind. Eng. Chem. Fundam. 18(3), 296-297 (1979) (not freely available; original not opened). |
| `fluids.churchill_1977_friction_factor` | UNVERIFIED | FLUIDS_CHEDL | Lienhard cites other Churchill correlations only. Needs Churchill, Chem. Eng. 84(24), 91-92 (1977) (original not opened, not free). |
| `fluids.darcy_weisbach_head_loss` | UNVERIFIED | FLUIDS_CHEDL | needs a non-OpenStax authoritative source; OpenStax removed 2026-10-09: the book now states CC BY-NC-SA 4.0 and forbids ingestion into LLM/generative AI without written permission. |
| `fluids.dean_number` | UNVERIFIED | FLUIDS_CHEDL | Not in Lienhard (full-text keyword search, 800 pp.), not on the NASA Glenn Similarity Parameters page (only Re and Mach printed), not in OpenStax University Physics vol. 1 sections 14.5-14.6. Needs Catchpole & Fulford (1 |
| `fluids.ideal_constriction_mass_flow_rate` | UNVERIFIED | FLUIDS_CHEDL | needs a non-OpenStax authoritative source; OpenStax removed 2026-10-09: the book now states CC BY-NC-SA 4.0 and forbids ingestion into LLM/generative AI without written permission. |
| `fluids.euler_number` | UNVERIFIED | FLUIDS_CHEDL | Not in Lienhard (full-text keyword search, 800 pp.), not on the NASA Glenn Similarity Parameters page (only Re and Mach printed), not in OpenStax University Physics vol. 1 sections 14.5-14.6. Needs Perry, Cengel & Cimbal |
| `fluids.froude_number_squared` | AMBIGUOUS | FLUIDS_CHEDL | Convention differs between supporting source (squared) and manifest (root). Either ship the squared form under its own id with Lienhard p. 157 as support (record formula above) or obtain a source printing V/sqrt(gL) (e.g |
| `fluids.fully_rough_friction_factor` | UNVERIFIED | FLUIDS_CHEDL | Lienhard Fig. 7.6 caption says rough-wall curves follow eq. (7.50) (Haaland) and eq. (7.48) gives only roughness-Reynolds-number ranges; it does not print f = (-2 log10(eps/(3.7 D)))^-2. Needs von Karman (1930), Rennels  |
| `fluids.hooper_two_k_loss_coefficient` | UNVERIFIED | FLUIDS_CHEDL | Needs Hooper, Chem. Eng. 88(17), 96-100 (1981) / Crane TP-410 with the K1, K_inf table (not free; original not opened). Fitting constants cannot be verified at all without it. |
| `fluids.knudsen_number` | UNVERIFIED | FLUIDS_CHEDL | Not in Lienhard (full-text keyword search, 800 pp.), not on the NASA Glenn Similarity Parameters page (only Re and Mach printed), not in OpenStax University Physics vol. 1 sections 14.5-14.6. Needs a rarefied-gas text (P |
| `fluids.loss_coefficient_basis_change` | UNVERIFIED | FLUIDS_CHEDL | Relation K2 = K1 (D2/D1)^4 follows from equal pressure drop dp = K rho V^2/2 on each basis plus continuity A1 V1 = A2 V2 (OpenStax eq. 14.14), but the definition of the loss coefficient K itself is printed in no opened s |
| `fluids.minor_loss_head` | UNVERIFIED | FLUIDS_CHEDL | Loss coefficient K defined by dp = K rho V^2/2 (head K V^2/2g) is not printed in any opened source (Lienhard prints only the pipe case f L/D, eq. 7.33). Needs Crane TP-410 / Cengel & Cimbala / White (not free). Mathemati |
| `fluids.minor_loss_pressure_drop` | UNVERIFIED | FLUIDS_CHEDL | Same gap as minor_loss_head: the K definition for fittings is not in an opened source. Identical in form to fluids.darcy_weisbach_pressure_drop (verified) with K = f L/D. |
| `fluids.nozzle_expansibility_factor` | UNVERIFIED | FLUIDS_CHEDL | ISO 5167-3 / ASME MFC-3M expansibility relation is held (standards text not allowed). Isentropic nozzle expansion could be derived from NACA Report 1135 but the ISO 'epsilon' definition would still need the standard. |
| `fluids.ohnesorge_number` | UNVERIFIED | FLUIDS_CHEDL | Not in Lienhard (full-text keyword search, 800 pp.), not on the NASA Glenn Similarity Parameters page (only Re and Mach printed), not in OpenStax University Physics vol. 1 sections 14.5-14.6. Needs Perry, Ohnesorge (1936 |
| `fluids.orifice_expansibility_factor` | UNVERIFIED | FLUIDS_CHEDL | ISO 5167-2 / ASME MFC-3M coefficients 0.351, 0.256, 0.93 are held (standards text not allowed); empirical, cannot be verified from an allowed source. |
| `fluids.orifice_loss_coefficient_from_discharge_coefficient` | UNVERIFIED | FLUIDS_CHEDL | Derived from ISO 5167-2 permanent-loss relations and discharge coefficient definition (held). Needs ISO 5167-2 or a free flow-measurement text. |
| `fluids.orifice_permanent_pressure_loss` | UNVERIFIED | FLUIDS_CHEDL | ISO 5167-2 permanent pressure loss formula is held (standards text not allowed). |
| `fluids.pipe_loss_coefficient_from_friction_factor` | UNVERIFIED | FLUIDS_CHEDL | K = f L/D is the Darcy-Weisbach relation (7.33) rewritten as dp/(rho V^2/2), but the name/definition 'loss coefficient K' appears in no opened source. Maintainers may accept it as derived from verified fluids.darcy_weisb |
| `fluids.power_number` | UNVERIFIED | FLUIDS_CHEDL | Not in Lienhard (full-text keyword search, 800 pp.), not on the NASA Glenn Similarity Parameters page (only Re and Mach printed), not in OpenStax University Physics vol. 1 sections 14.5-14.6. Needs a mixing text (Perry,  |
| `fluids.pump_specific_speed` | UNVERIFIED | FLUIDS_CHEDL | Dimensional (rpm, m^3/s, m) convention from HI 1.3 (standard, not allowed). Needs a free pump text or the standard to fix units and the best-efficiency-point definition. |
| `fluids.reader_harris_gallagher_discharge_coefficient` | AMBIGUOUS | FLUIDS_CHEDL | license hold |
| `fluids.reynolds_number` | DUPLICATE | FLUIDS_CHEDL | duplicate of `fluids.reynolds_number` |
| `fluids.serghides_friction_factor` | UNVERIFIED | FLUIDS_CHEDL | Needs Serghides, Chem. Eng. 91(5), 63-64 (1984) (not free; original not opened). |
| `fluids.sudden_contraction_loss_coefficient_rennels` | UNVERIFIED | FLUIDS_CHEDL | Needs Rennels & Hudson, Pipe Flow (Wiley, 2012; not free) for the coefficients 0.0696, 0.622, 0.215, 0.785. |
| `fluids.sudden_expansion_loss_coefficient` | UNVERIFIED | FLUIDS_CHEDL | Borda-Carnot K = (1 - d1^2/d2^2)^2 follows from a momentum balance with a loss coefficient on the small-pipe velocity, but no opened source prints it (OpenStax vol. 1 has no control-volume momentum treatment). Needs Renn |
| `fluids.swamee_jain_friction_factor` | UNVERIFIED | FLUIDS_CHEDL | Needs Swamee & Jain, J. Hydraul. Div. ASCE 102(5), 657-664 (1976) (not free; original not opened). Lienhard prints Haaland instead. |
| `fluids.velocity_of_approach_factor` | UNVERIFIED | FLUIDS_CHEDL | needs a non-OpenStax authoritative source; OpenStax removed 2026-10-09: the book now states CC BY-NC-SA 4.0 and forbids ingestion into LLM/generative AI without written permission. |
| `heat_transfer.air_cooled_machine_heat_transfer_coefficient` | UNVERIFIED | MODELICA_MSL | Dimensional rule-of-thumb h = 7.8 v^0.78 not in Lienhard; needs Fischer, Elektrische Maschinen (Hanser, 2017), not freely available. |
| `heat_transfer.annular_fin_efficiency` | UNVERIFIED | HT_CHEDL | Lienhard sec. 4.5 (p. 180) gives annular/circular fin efficiency only as Schneider's charts (Fig. 4.13), not the Bessel closed form; straight insulated-tip fin eta_f = tanh(mL)/(mL) is stated (eq. 4.53, p. 174) and could |
| `heat_transfer.biot_number` | DUPLICATE | FLUIDS_CHEDL | duplicate of `heat_transfer.biot_number` |
| `heat_transfer.churchill_sphere_free_convection_nusselt` | AMBIGUOUS | HT_CHEDL | Different correlation from the one implemented. Either rename and ship Lienhard eq. (8.33), or obtain Churchill's chapter in the Heat Exchanger Design Handbook (not freely available) for the library form. |
| `heat_transfer.convective_heat_flux` | DUPLICATE | MODELICA_MSL | duplicate of `heat_transfer.convective_heat_flux` |
| `heat_transfer.crossflow_unmixed_effectiveness_approx` | UNVERIFIED | HT_CHEDL | Library form 1 - exp[(NTU^0.22/C_r)(exp(-C_r NTU^0.78) - 1)] is not in Lienhard; Table 3.1 (p. 125) gives a DIFFERENT two-range approximation for both-unmixed crossflow (R > 0.3 and NTU > 1, else 1 - exp{[exp(-R^1.15 NTU |
| `heat_transfer.dittus_boelter_nusselt` | AMBIGUOUS | HT_CHEDL | Source conflict: coefficient (0.023 vs 0.0243) and cooling branch (n = 0.3) unsupported; Re range for (7.39b) not stated. Coordinator to decide: ship textbook 0.0243/Pr^0.4 heating-only form, or obtain Rohsenow Handbook  |
| `heat_transfer.hausen_laminar_entry_nusselt` | UNVERIFIED | HT_CHEDL | Hausen 3.66 + 0.0668 Gz/(1 + 0.04 Gz^(2/3)) not found in Lienhard sec. 7.2; textbook instead gives curve fits eqs. (7.28)-(7.29) (p. 362) for the isothermal-wall thermal entry (possible new candidates). Need Hausen 1943  |
| `heat_transfer.laminar_pipe_h_uniform_wall_temperature` | DUPLICATE | HT_CHEDL | duplicate of `heat_transfer.laminar_pipe_h_uniform_wall_temperature` |
| `heat_transfer.log_mean_temperature_difference` | DUPLICATE | HT_CHEDL | duplicate of `heat_transfer.log_mean_temperature_difference` |
| `heat_transfer.net_radiative_exchange` | DUPLICATE | MODELICA_MSL | duplicate of `heat_transfer.net_radiative_exchange` |
| `heat_transfer.nusselt_number` | DUPLICATE | FLUIDS_CHEDL | duplicate of `heat_transfer.nusselt_number` |
| `heat_transfer.petukhov_kirillov_popov_nusselt` | UNVERIFIED | HT_CHEDL | Lienhard eq. (7.35) (p. 367) gives the Petukhov-type form with denominator 1 + 12.7 sqrt(f/8)(Pr^(2/3) - 1) (constant 1, Pr >~ 0.7, smooth pipe) - NOT the C = 1.07 + 900/Re - 0.63/(1 + 10 Pr) variant. Need Petukhov 1970  |
| `heat_transfer.plane_wall_thermal_resistance` | DUPLICATE | MODELICA_MSL | duplicate of `heat_transfer.plane_wall_thermal_resistance` |
| `heat_transfer.prandtl_number` | DUPLICATE | FLUIDS_CHEDL | duplicate of `heat_transfer.prandtl_number` |
| `heat_transfer.sieder_tate_laminar_nusselt` | UNVERIFIED | HT_CHEDL | 1.86 (Gz)^(1/3)(mu_b/mu_w)^0.14 not found in Lienhard sec. 7.2 (keyword search found no 1.86). Need Sieder & Tate 1936 (ACS, paywalled). |
| `heat_transfer.stanton_number` | DUPLICATE | FLUIDS_CHEDL | duplicate of `heat_transfer.stanton_number` |
| `heat_transfer.thermal_diffusivity` | DUPLICATE | FLUIDS_CHEDL | duplicate of `heat_transfer.thermal_diffusivity` |
| `heat_transfer.turbulent_flat_plate_mean_nusselt` | UNVERIFIED | HT_CHEDL | Schlichting/VDI form 0.037 Re^0.8 Pr / (1 + 2.443 Re^-0.1 (Pr^(2/3) - 1)) not in Lienhard; sec. 6.9 eq. (6.120) (p. 334) gives a different laminar+transition+turbulent average for gases with Pr^0.6. Need VDI Heat Atlas ( |
| `materials.shear_modulus_from_youngs_modulus` | DUPLICATE | PYNITE | duplicate of `materials.shear_modulus_from_youngs_modulus` |
| `mechanics.equivalent_inertia_translating_mass` | UNVERIFIED | MODELICA_MSL | Needs a statement of the kinetic-energy equivalence J_eq = m R^2 for rolling without slip (1/2 m v^2 = 1/2 J w^2 with v = w R). Textbook needed: any dynamics text or OpenStax University Physics vol 1 (rotational kinetic  |
| `mechanics.gear_ratio_output_speed` | UNVERIFIED | MODELICA_MSL | As written, omega_out = omega_in / i_g with i_g defined as omega_in / omega_out is a definition; independent content is the no-slip mesh condition r_in omega_in = r_out omega_out (i_g = r_out / r_in = N_out / N_in). Need |
| `mechanics.gear_ratio_output_torque` | UNVERIFIED | MODELICA_MSL | Needs a source for the lossless-gear torque relation tau_out = i_g tau_in (power conservation tau_in omega_in = tau_out omega_out). Textbook needed: Shigley or Norton (gear trains), or OpenStax University Physics vol 1 ( |
| `mechanics.incline_gravity_component` | UNVERIFIED | MODELICA_MSL | Needs a statics/dynamics text stating that the component of weight along an incline is m g sin(theta). NASA Glenn 'Forces in a Climb' (opened) resolves forces on a vertical/horizontal axis and never states the along-path |
| `mechanics.rolling_resistance_force` | UNVERIFIED | MODELICA_MSL | Needs a vehicle-dynamics source for F = C_r m g cos(theta) with a stated validity (speed-independent coefficient). No allowed free source located (NASA TM/NTRS tyre reports give measured coefficients, not this relation). |
| `mechanics.tangential_speed` | DUPLICATE | MODELICA_MSL | duplicate of `mechanics.tangential_speed` |
| `mechanics.viscous_damper_force` | UNVERIFIED | MODELICA_MSL | Needs a source stating the linear viscous damper law F = c v (force proportional to relative velocity). Roylance 'Linear Viscoelasticity' (mit3_11f99_visco, p. 9) prints only the stress-strain-rate analogue sigma = eta d |
| `mechanics.viscous_damper_power_loss` | UNVERIFIED | MODELICA_MSL | Needs P = F v (mechanical power) plus the damper law F = c v; neither stated in an allowed source opened. Derived step P = c v^2 is trivial once both are sourced. Textbook needed: any dynamics text or OpenStax University |
| `structures.angle_of_twist` | DUPLICATE | PYNITE | duplicate of `structures.angle_of_twist` |
| `structures.axial_deformation` | DUPLICATE | PYNITE | duplicate of `structures.axial_deformation` |
| `structures.fixed_shaft_torque_reaction` | DUPLICATE | PYNITE | duplicate of `DUPLICATE (same functional form) of structures.fixed_bar_axial_reaction_point_load in this group.` |
| `structures.plastic_moment_capacity` | UNVERIFIED | PYNITE | Needs a plastic-analysis source defining the plastic section modulus Z = int /y/ dA about the equal-area axis and stating M_p = f_y Z for a fully plastic section. The Roylance modules read (Yield and Plastic Flow, Beam D |
| `structures.wide_flange_yield_surface_ratio` | UNVERIFIED | PYNITE | Empirical fitted interaction surface cited by the library as 'Matrix Structural Analysis, 2nd Edition', Eq. 10.18; the book (authors/publisher not stated in the library file) was not opened and is not freely available. T |
| `thermodynamics.clausius_clapeyron_pressure_ratio` | AMBIGUOUS | THERMO_CHEDL | Source prints only the differential form, only for sublimation (h_sf), only in a footnote, with no statement of the ideal-vapor / negligible condensed-volume assumptions and no integrated form. Vaporization version, assu |
| `thermodynamics.compressor_discharge_temperature` | UNVERIFIED | FLUIDS_CHEDL | Needs a source defining compressor isentropic efficiency eta_s = (T2s - T1)/(T2 - T1) with T2s from the catalogued isentropic relation (derivable in one step). NASA Glenn Brayton-cycle pages (searched) do not define it.  |
| `thermodynamics.ideal_gas_pressure` | DUPLICATE | THERMO_CHEDL | duplicate of `thermodynamics.ideal_gas_pressure` |
| `thermodynamics.isentropic_compression_work` | UNVERIFIED | FLUIDS_CHEDL | Needs a source for the steady-flow isentropic compression work w = (k/(k-1)) Z R T1 [(p2/p1)^((k-1)/k) - 1]/eta_s including the compressibility factor Z. Library cites Couper, Penney & Fair, Chemical Process Equipment (n |
| `thermodynamics.isentropic_efficiency_from_polytropic` | UNVERIFIED | FLUIDS_CHEDL | Needs a source for the polytropic-to-isentropic efficiency relation eta_s = [(p2/p1)^((k-1)/k) - 1] / [(p2/p1)^((k-1)/(k eta_p)) - 1]. Library cites Couper et al.; no free allowed source found. Textbook needed: Saravanam |
| `thermodynamics.isentropic_temperature_ratio` | DUPLICATE | FLUIDS_CHEDL | duplicate of `thermodynamics.isentropic_temperature_ratio` |
| `thermodynamics.isothermal_compression_work` | DUPLICATE | FLUIDS_CHEDL | duplicate of `thermodynamics.isothermal_work` |
| `thermodynamics.polytropic_exponent_from_efficiency` | UNVERIFIED | FLUIDS_CHEDL | Needs a source for n = k eta_p / (1 - k (1 - eta_p)). Library cites Couper et al.; no free allowed source found. Textbook needed: Saravanamuttoo or a compressor-thermodynamics text relating polytropic exponent to polytro |
| `thermodynamics.stagnation_temperature` | DUPLICATE | FLUIDS_CHEDL | duplicate of `thermodynamics.stagnation_temperature` |
| `thermodynamics.watson_vaporization_enthalpy_scaling` | UNVERIFIED | THERMO_CHEDL | Needs the original Watson correlation h_fg(T) = h_fg(T_ref) ((1 - T/T_c)/(1 - T_ref/T_c))^0.38 and its stated exponent range. Lienhard AHTT (searched) does not contain it; library gives no primary reference. Textbook nee |

## Deferred (does not fit the scalar FormulaSpec)

| Candidate | Kind | Proposed future schema |
|---|---|---|
| `E1_CHEDL_014` | IMPLICIT | Needs an implicit-equation spec (residual + bracketed root solve) or a special-function dependency for Lambert W. |
| `E1_CHEDL_015` | IMPLICIT | Implicit; same schema need as Colebrook. |
| `E1_CHEDL_089` | ALGORITHM | Requires a quadrature-backed evaluator (scalar in/out but integral + Bessel I0); could ship once a numeric-integration helper is allowed. |
| `E1_CHEDL_097` | MATRIX_VECTOR | Needs a vector (mole-fraction array) input type; binary scalar specialisation is v1-compatible. |
| `MODELICA_MSL:mechanics_rolling_resistance_regularised_sign` | ALGORITHM | Piecewise/option-selected model would need an enum 'method' input and branch metadata. |
| `PYNITE:structures_frame_local_stiffness_matrix` | MATRIX_VECTOR | Matrix-valued output schema (shape, DOF ordering, sign convention) required. |
| `PYNITE:structures_geometric_stiffness_matrix` | MATRIX_VECTOR | Matrix output; pair with elastic matrix for buckling eigenproblem (also needs eigen schema). |
| `PYNITE:structures_beam_segment_internal_moment` | SCALAR_NUMERIC | Function-of-position output with convention metadata; low catalog value as a standalone scalar formula. |
| `PYNITE:structures_plane_stress_constitutive_matrix` | MATRIX_VECTOR | Matrix output. The embedded G = E/(2(1+nu)) duplicates materials.shear_modulus_from_youngs_modulus. |
