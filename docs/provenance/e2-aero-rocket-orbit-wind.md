# Provenance: engineering batch E2 (aerodynamics, rockets, orbits, wind)

Sanitized record of how this engineering batch was found, checked and licensed. Candidates were
discovered in open-source engineering libraries; a library never counted as support. Each
implemented formula cites an authoritative source opened during verification. No source text.

## Sources cited by the implemented formulas

| Source | Implemented formulas citing it |
|---|---|
| NASA Langley Research Center (The George Washington University, JIAFS): NASA/CR-2005-213034 | 15 |
| NASA Langley Research Center: NASA SP-325 | 12 |
| NASA Goddard Space Flight Center (reissue of a March 1967 Catholic University of America master's dissertation): NASA/TM-2001-209983 | 8 |
| NASA Goddard Space Flight Center: X-643-67-627 | 8 |
| National Oceanic and Atmospheric Administration, National Aeronautics and Space Administration and U.S. Air Force: NASA-TM-X-74335; NOAA-S/T-76-1562 | 5 |
| National Aeronautics and Space Administration: NASA SP-125 | 4 |
| NASA Glenn Research Center: Terminal Velocity Interactive | 3 |
| Ames Research Staff: NACA Rep. 1135 | 3 |
| National Aeronautics and Space Administration: NASA TR R-158 | 3 |
| NASA Glenn Research Center: Specific Impulse | 3 |
| NASA Glenn Research Center: Forces in a Climb | 2 |
| NASA Glenn Research Center: Lift Equation | 2 |
| NASA Lewis Research Center (Sverdrup Technology): NASA CR-191129 | 2 |
| National Aeronautics and Space Administration: NASA SP-8039 | 2 |
| NASA Langley Research Center: NASA TM-81828 | 1 |
| NASA Glenn Research Center: Induced Drag Coefficient | 1 |
| The mathlib Community: mathlib4 | 1 |
| NASA Langley Research Center: NASA TM-85729 | 1 |
| National Aeronautics and Space Administration: NASA TM-79275; DOE/NASA/1059-79/4 | 1 |
| NASA Lewis Research Center: NASA TM X-73433 | 1 |
| NASA Goddard Space Flight Center: NASA TN D-1045 | 1 |
| NASA George C. Marshall Space Flight Center: NASA TM X-53485 | 1 |
| J. H. Lienhard V, J. H. Lienhard IV: A Heat Transfer Textbook | 1 |
| NASA Glenn Research Center: Thrust to Weight Ratio | 1 |
| National Aeronautics and Space Administration: NASA CR-191129 | 1 |

Rights notes: textbooks and reports are cited, never copied. OpenStax is excluded (its pages
forbid ingestion into AI systems). MIT OCW notes (Roylance) are CC BY-NC-SA and only cited.
Standards (ISO 5167, ASME MFC, IEC, ASHRAE) and their coefficient tables are not used.

## Counts

- Candidates: 112 scalar + 27 deferred (non-scalar, kept for a future schema).
- Candidate gates: AMBIGUOUS 5, DUPLICATE 8, UNVERIFIED 41, VERIFIED 58.
- Formula records from verification: 104 (AMBIGUOUS 5, DUPLICATE 1, UNVERIFIED 40, VERIFIED 58).
- Implemented: 58; verified and held: 0; verified, implementation pending: 0.
- Candidates not yet verified (awaiting verification): 1.

## Implemented formulas

| Formula id | Form | Supporting references (locator) | Discovered in | Cases |
|---|---|---|---|---|
| `aerodynamics.barometric_pressure_gradient_layer` | derived | National Oceanic and Atmospheric Administration, National Aeronautics and Space Administration and U.S. Air Force: sec. 1.3.1, eq. (33a), p. 12; Table 4 (layer base heights and gradients), p. 3; eq. (23), p. 10 | AEROSANDBOX | 5 |
| `aerodynamics.barometric_pressure_isothermal_layer` | derived | National Oceanic and Atmospheric Administration, National Aeronautics and Space Administration and U.S. Air Force: sec. 1.3.1, eq. (33b), p. 12; Table 4, p. 3 | AEROSANDBOX | 4 |
| `aerodynamics.climb_gradient` | derived | NASA Glenn Research Center: Vertical and horizontal component equations | AEROSANDBOX | 3 |
| `aerodynamics.conical_transition_center_of_pressure` | derived | J. S. Barrowman: sec. 3.22, eqs. (3-77)-(3-88), pp. 28-29, with (3-65) p. 20 | ROCKETPY | 3 |
| `aerodynamics.conical_transition_normal_force_slope` | derived | J. S. Barrowman: sec. 3.21, eq. (3-65), p. 20 | ROCKETPY | 3 |
| `aerodynamics.density_altitude` | derived | National Oceanic and Atmospheric Administration, National Aeronautics and Space Administration and U.S. Air Force: sec. 1.2.5, eqs. (22), (23), p. 9-10; sec. 1.3.1, eq. (33a), p. 12; sec. 1.3.4, eq. (42), p. 15; Table 4, p. 3 (b = 0: H_b = 0, L = -6.5 K/km', T_M,0 = 288.15 K); Table 10, p. 20; Table I, p. 51 (row Z = -5000 m, H = -5004 m') | AEROSANDBOX | 4 |
| `aerodynamics.energy_height` | stated | J. Gera: Summary and List of Symbols (energy height h_e = V^2/(2g) + h) | AEROSANDBOX | 3 |
| `aerodynamics.geopotential_height` | stated | National Oceanic and Atmospheric Administration, National Aeronautics and Space Administration and U.S. Air Force: sec. 1.2.3, eq. (18), p. 8 (with eq. (17) and eq. (19)); Table I rows Z = -5000, p. 51, and Z = 5000, p. 55 | ROCKETPY | 5 |
| `aerodynamics.induced_drag_force` | derived | NASA Glenn Research Center: Induced Drag Coefficient; NASA Glenn Research Center: Lift Equation; NASA Glenn Research Center: Terminal Velocity Interactive | AEROSANDBOX | 3 |
| `aerodynamics.isentropic_area_mach_ratio` | derived | Ames Research Staff: eq. (80); Tables I and II | AEROSANDBOX | 7 |
| `aerodynamics.isentropic_mass_flow_rate` | derived | Ames Research Staff: eqs. (26), (29b), (30), (43), (44), (46), pp. 615-616; eq. (79) and text, p. 618 | AEROSANDBOX | 4 |
| `aerodynamics.nose_normal_force_slope` | derived | J. S. Barrowman: sec. 3.21, eq. (3-66) (from (3-65)), p. 20-21 | ROCKETPY | 3 |
| `aerodynamics.parachute_radius_from_drag_area` | derived | NASA Glenn Research Center: Terminal Velocity Interactive; The mathlib Community: lemma EuclideanSpace.volume_ball_fin_two | ROCKETPY | 3 |
| `aerodynamics.power_series_nose_center_of_pressure` | derived | J. S. Barrowman: sec. 3.22, eq. (3-89), p. 29 | ROCKETPY | 4 |
| `aerodynamics.sears_haack_wave_drag_area` | stated | J. W. Bantle: sec. 'Bodies Alone', eq. (15), p. 33 (eq. (14) p. 32; eq. (16) p. 33) | AEROSANDBOX | 3 |
| `aerodynamics.single_fin_normal_force_slope` | stated | J. S. Barrowman: sec. 3.11, eq. (3-1) with (3-2), (3-4), (3-5) and (3-6), p. 3 | ROCKETPY | 3 |
| `aerodynamics.slender_body_center_of_pressure_from_volume` | stated | J. S. Barrowman: sec. 3.22, eq. (3-89), p. 29 | ROCKETPY | 3 |
| `aerodynamics.stall_speed` | derived | NASA Glenn Research Center: Lift Equation; NASA Glenn Research Center: small-angle reduction | AEROSANDBOX | 3 |
| `aerodynamics.terminal_velocity_drag_area` | derived | NASA Glenn Research Center: Terminal Velocity Interactive | ROCKETPY | 3 |
| `aerodynamics.trapezoid_mac_spanwise_location` | stated | J. S. Barrowman: sec. 3.12, eq. (3-26), p. 10 (with (3-13), (3-18), (3-24), (3-25)) | ROCKETPY | 4 |
| `aerodynamics.trapezoidal_fin_center_of_pressure` | derived | J. S. Barrowman: sec. 3.12, eqs. (3-13), (3-18), (3-24), (3-26), (3-28), (3-29), (3-30), pp. 7-10 | ROCKETPY | 4 |
| `fluids.laminar_flat_plate_mean_skin_friction` | stated | J. H. Lienhard V: sec. 6.2, eq. (6.34) (local eq. (6.33)), p. 292; Example 6.3, pp. 292-293; transition remarks sec. 6.1, p. 276 | AEROSANDBOX | 5 |
| `fluids.sutherland_viscosity_air` | stated | National Oceanic and Atmospheric Administration, National Aeronautics and Space Administration and U.S. Air Force: sec. 1.3.11, eq. (51), p. 19; Table 2B (constants, p. 2) and p. 4 (S = 110 K, see comment above); Table 10 (sea-level mu0), p. 20 | AEROSANDBOX | 4 |
| `fluids.wind_shear_power_law` | stated | D. A. Spera: Introduction, eq. (1) (p. 1 of the paper) | OPENFAST | 3 |
| `orbital.barker_parabolic_anomaly_from_mean_anomaly` | derived | R. C. Blanchard: eqs. (1.1) second line and (1.2), p. 1 | POLIASTRO | 4 |
| `orbital.barker_parabolic_mean_anomaly` | derived | R. C. Blanchard: eqs. (1.1) second line and (1.2), p. 1 | POLIASTRO | 4 |
| `orbital.bielliptic_total_delta_v` | derived | C. W. Brunner: sec. 2.3.1, p. 16 (text after eq. 10) with eqs. (4)-(9); R. S. Dunning: chap. 1, eqs. (1-29), p. 8, (1-47), p. 13 and (1-51), p. 14 | POLIASTRO | 3 |
| `orbital.circular_orbit_speed` | stated | C. W. Brunner: eqs. (4)-(5), p. 15; R. S. Dunning: chap. 1, 'Circular orbit', eq. (1-51), p. 14 (and eq. 1-18, p. 7) | OREKIT | 3 |
| `orbital.conic_orbit_radius` | derived | C. W. Brunner: eqs. (21)-(22), p. 20; R. S. Dunning: chap. 1, 'Equation of a Conic Section', eq. (1-38), p. 10 | OREKIT | 5 |
| `orbital.eccentric_anomaly_from_true_anomaly` | derived | J. T. Kent: eq. (2), p. 3; C. W. Brunner: eq. (23), p. 20 | OREKIT | 4 |
| `orbital.edelbaum_delta_v` | stated | S. R. Oleson: p. 3, eq. (3), and p. 5 verification example | POLIASTRO | 4 |
| `orbital.flight_path_angle` | derived | C. W. Brunner: eqs. (13), (16), p. 19; R. S. Dunning: chap. 1, eqs. (1-23), (1-31), (1-38), pp. 7-10 | POLIASTRO | 5 |
| `orbital.hohmann_first_impulse` | derived | C. W. Brunner: eqs. (4), (6), (7), (9), pp. 15-16; R. S. Dunning: chap. 1, eqs. (1-29), p. 8, (1-47), p. 13 and (1-51), p. 14 | POLIASTRO | 3 |
| `orbital.hohmann_second_impulse` | derived | C. W. Brunner: eqs. (5), (6), (8), (9), pp. 15-16; R. S. Dunning: chap. 1, eqs. (1-29), p. 8, (1-47), p. 13 and (1-51), p. 14 | POLIASTRO | 3 |
| `orbital.hohmann_transfer_time` | derived | C. W. Brunner: eqs. (6), (10), p. 16; R. S. Dunning: chap. 1, eqs. (1-47) and (1-48), p. 13 | POLIASTRO | 3 |
| `orbital.hyperbolic_asymptote_true_anomaly` | derived | C. W. Brunner: eqs. (21)-(22), p. 20; R. S. Dunning: chap. 1, eq. (1-38), p. 10, and 'Hyperbolic trajectories', eq. (1-35), p. 16 | OREKIT | 3 |
| `orbital.hyperbolic_eccentric_anomaly_from_true_anomaly` | derived | R. C. Blanchard: eq. (1.1), p. 1 | OREKIT | 3 |
| `orbital.hyperbolic_kepler_mean_anomaly` | stated | R. C. Blanchard: eq. (1.1), third line, p. 1 | OREKIT | 3 |
| `orbital.hyperbolic_true_anomaly_from_eccentric_anomaly` | derived | R. C. Blanchard: eq. (1.1), p. 1 | OREKIT | 3 |
| `orbital.j2_nodal_precession_rate` | stated | J. Borsody: analysis item (4), eq. (1), p. 2; oblateness parameter J and semilatus rectum p in the appendix list of symbols; W. R. Bandeen: p. 2, eq. (1) and the 'ideal orbit' example, pp. 2-4 | OREKIT | 5 |
| `orbital.kepler_mean_anomaly_from_eccentric_anomaly` | stated | J. T. Kent: eq. (1), p. 3 (printed page 3); C. W. Brunner: eq. (25), p. 20; R. C. Blanchard: eq. (1.1), p. 1 | OREKIT | 4 |
| `orbital.keplerian_mean_motion` | derived | R. C. Blanchard: eq. (1.1), p. 1; R. S. Dunning: chap. 1, 'Mean and Eccentric Anomaly', eq. (1-66), p. 16 | OREKIT | 3 |
| `orbital.laplace_sphere_of_influence_radius` | stated | C. W. Brunner: eq. (11), p. 19; R. R. Burrows: eq. (11), p. 6 | POLIASTRO | 3 |
| `orbital.mean_motion_semi_major_axis_sensitivity` | derived | R. C. Blanchard: eq. (1.1) (time coefficient sqrt(mu / a^3)) | OREKIT | 2 |
| `orbital.semi_latus_rectum` | derived | C. W. Brunner: eq. (20), p. 20 (and p = h^2 / mu, eq. 18); R. S. Dunning: chap. 1, eq. (1-36), p. 9, and 'p = a(1 - eps^2)' after eq. (1-36a), p. 13 | OREKIT | 3 |
| `orbital.specific_angular_momentum` | derived | C. W. Brunner: eqs. (13), (18), pp. 19-20; R. S. Dunning: chap. 1, eq. (1-23), p. 7, and eq. (1-36), p. 9 | POLIASTRO | 3 |
| `orbital.true_anomaly_from_eccentric_anomaly` | derived | J. T. Kent: eq. (2), p. 3; C. W. Brunner: eq. (23), p. 20 | OREKIT | 4 |
| `orbital.vis_viva_speed` | derived | C. W. Brunner: eqs. (7), (8), (37), p. 16 and p. 23; eqs. (12), (15), (19), pp. 19-20; R. S. Dunning: chap. 1, eq. (1-29), p. 8, and eq. (1-47), p. 13 | POLIASTRO | 4 |
| `propulsion.average_thrust` | stated | NASA Glenn Research Center: Specific Impulse | ROCKETPY | 3 |
| `propulsion.burn_to_throat_area_ratio` | stated | National Aeronautics and Space Administration: sec. 2.1.2, text under eq. (15), p. 10 | ROCKETPY | 3 |
| `propulsion.effective_exhaust_velocity` | stated | NASA Glenn Research Center: Specific Impulse; D. K. Huzel: sec. 1.3, eqs. (1-31) and (1-31a), p. 11 | OREKIT | 3 |
| `propulsion.effective_exhaust_velocity_from_impulse` | stated | NASA Glenn Research Center: Specific Impulse | ROCKETPY | 3 |
| `propulsion.nozzle_expansion_ratio` | derived | D. K. Huzel: sec. 1.2, eq. (1-20), p. 7 (sample calculation 1-2, pp. 8-10); Ames Research Staff: eqs. (44) and (80), pp. 616 and 618 | AEROSANDBOX | 5 |
| `propulsion.regression_rate_from_mass_flow` | derived | National Aeronautics and Space Administration: sec. 2.1, eq. (4), p. 5 | ROCKETPY | 3 |
| `propulsion.rocket_equation_final_mass` | derived | S. R. Oleson: p. 3 (text before eq. 3) and eq. (5) | OPENSTAX_UNIVERSITY_PHYSICS_V1 | 3 |
| `propulsion.thrust_coefficient` | stated | D. K. Huzel: sec. 1.3, eq. (1-33a), p. 12 (definition (1-33) C_f = F/(A_t (p_c)_ns)) | AEROSANDBOX | 4 |
| `propulsion.thrust_to_weight_ratio` | stated | NASA Glenn Research Center: Thrust to Weight Ratio | ROCKETPY | 3 |
| `propulsion.tsiolkovsky_delta_v` | derived | S. R. Oleson: p. 3 (text before eq. 3) and eq. (5); D. K. Huzel: sec. 1.3, eq. (1-30), p. 11 | NASA_CR_191129 | 3 |

## Not implemented

| Candidate / formula | Gate | Discovered in | Reason / source needed |
|---|---|---|---|
| `DUPLICATE` | UNVERIFIED | ROCKETPY | not yet verified |
| `aerodynamics.equivalent_airspeed` | UNVERIFIED | AEROSANDBOX | No NASA/NACA document stating V_E = V sqrt(rho/rho_SL) was opened. The relation follows from equating dynamic pressures (Glenn Dynamic Pressure page, read, defines q = rho u^2/2) but the definition of 'equivalent airspee |
| `aerodynamics.fin_body_interference_factor` | AMBIGUOUS | ROCKETPY | NASA/TM-2001-209983 sec. 3.31, eq. (3-96) (read as an image) prints K_T(B) as a function of tau = (s + r_t)/r_t as a long arctangent expression (referencing refs 7 and 17), not K = 1 + r/(s + r) = 1 + 1/tau. As printed t |
| `aerodynamics.finite_wing_lift_slope_ratio` | UNVERIFIED | AEROSANDBOX | Raymer / USAF DATCOM relation CL_alpha/Cl_alpha = AR/(2 + sqrt(4 + AR^2(1-M^2)/eta^2 + (AR tan Lambda/eta)^2)); not opened (Raymer is copyrighted; DATCOM is a USAF, not NASA, document). Empirical coefficient set; stays U |
| `aerodynamics.fuselage_upsweep_drag_area` | UNVERIFIED | AEROSANDBOX | Raymer Eq. 12.36 empirical fit D/q = 3.83 u^2.5 A_max; copyrighted book not opened. |
| `aerodynamics.ground_effect_induced_drag_ratio` | UNVERIFIED | AEROSANDBOX | Phillips and Hunsaker paper (J. Aircraft) fit D_i,IGE/D_i,OGE = 1 - exp(-4.01 (2h/b)^0.717); AIAA paper not opened; empirical coefficients. |
| `aerodynamics.haack_series_nose_radius` | UNVERIFIED | AEROSANDBOX | The Haack series (r/R = sqrt((theta - sin(2 theta)/2 + C sin^3 theta)/pi)) is not printed in any opened source. NASA TM-85729 prints only the Sears-Haack body shape r = r_max (1 - (2x/l - 1)^2)^(3/4) (a different, closed |
| `aerodynamics.korn_drag_divergence_mach` | UNVERIFIED | AEROSANDBOX | Mason's Configuration Aerodynamics (Virginia Tech course text, copyright not cleared) states the Korn equation; no NASA document opened. Empirical (airfoil technology factor kappa_A). |
| `aerodynamics.landing_airborne_distance_torenbeek` | UNVERIFIED | AEROSANDBOX | Torenbeek, Synthesis of Subsonic Airplane Design (book, not opened). Empirical field-length model. |
| `aerodynamics.liftoff_speed_ratio_torenbeek` | UNVERIFIED | AEROSANDBOX | Torenbeek (book), empirical. |
| `aerodynamics.lock_wave_drag_coefficient` | UNVERIFIED | AEROSANDBOX | Lock's 4th-power law as used by Mason (Cd_wave = 20 (M - M_crit)^4); copyrighted/uncleared course text; empirical constant 20. |
| `aerodynamics.optimal_taper_ratio` | UNVERIFIED | AEROSANDBOX | Nita-Scholz (2012) empirical fit lambda_opt = 0.45 exp(-0.0375 Lambda); stays UNVERIFIED per brief (empirical coefficient set from a paper). |
| `aerodynamics.oswald_efficiency_nita_scholz` | UNVERIFIED | AEROSANDBOX | Nita-Scholz empirical coefficient set; stays UNVERIFIED per brief. |
| `aerodynamics.prandtl_glauert_correction` | AMBIGUOUS | ROCKETPY | NASA/TM-2001-209983 sec. 3.11, eqs. (3-3), (3-4), p. 3 print only the thin-airfoil lift-curve slope 2*pi and its Gothert/Prandtl compressible correction 2*pi/beta, beta = sqrt(1 - M^2) (subsonic). The candidate states Cl |
| `aerodynamics.rail_exit_stall_wind_speed` | UNVERIFIED | ROCKETPY | No source prints this relation. It follows from vector geometry: with the rail inclined theta from horizontal, rocket speed v along the axis and a horizontal wind of speed w blowing against the lean direction, tan(alpha) |
| `aerodynamics.static_margin` | UNVERIFIED | ROCKETPY | Static margin in calibers, SM = (x_cp - x_cg)/d, is not printed in the opened Barrowman thesis (it only defines x_CG and x_cp) and no NASA page defining the caliber measure was opened. RocketPy computes (cm - cp)/(2 r) w |
| `aerodynamics.takeoff_airborne_distance_torenbeek` | UNVERIFIED | AEROSANDBOX | Torenbeek (book), empirical. |
| `aerodynamics.takeoff_ground_roll_torenbeek` | UNVERIFIED | AEROSANDBOX | Torenbeek (book), empirical coefficient 0.72. |
| `duplicate:AEROSANDBOX-019-isentropic_temperature_over_total_temperature` | DUPLICATE | AEROSANDBOX | duplicate of `aerodynamics.isentropic_temperature_ratio` |
| `duplicate:AEROSANDBOX-020-isentropic_pressure_over_total_pressure` | DUPLICATE | AEROSANDBOX | duplicate of `aerodynamics.isentropic_pressure_ratio` |
| `duplicate:AEROSANDBOX-021-isentropic_density_over_total_density` | DUPLICATE | AEROSANDBOX | duplicate of `aerodynamics.isentropic_density_ratio` |
| `duplicate:AEROSANDBOX-030-indicated_airspeed_incompressible` | DUPLICATE | AEROSANDBOX | duplicate of `fluids.pitot_static_airspeed` |
| `duplicate:E2-OREKIT-002-keplerian_period` | DUPLICATE | OREKIT | duplicate of `orbital.orbital_period` |
| `duplicate:E2-OREKIT-019-mass_flow_from_thrust_and_isp` | DUPLICATE | OREKIT | duplicate of `propulsion.specific_impulse` |
| `duplicate:ROCKETPY-123-mass_flow_from_thrust` | DUPLICATE | ROCKETPY | duplicate of `propulsion.specific_impulse` |
| `engineering.aerodynamics.actuator_disk_thrust_coefficient` | UNVERIFIED | OPENFAST | C_T = 4 a F (1 - a) is the momentum-theory thrust coefficient with tip-loss factor F (Ning 2014, Wiley journal, not opened). The NREL AeroDyn manual could not be fetched: nrel.gov does not resolve from this environment a |
| `engineering.aerodynamics.blade_local_solidity` | UNVERIFIED | OPENFAST | sigma_r = B c/(2 pi r): same missing wind-turbine source as the other OpenFAST/AeroDyn candidates. |
| `engineering.aerodynamics.buhl_turbulent_wake_thrust_coefficient` | UNVERIFIED | OPENFAST | Buhl's empirical C_T correction for a > 0.4 (Wind Energy, journal) is named only in a code comment; empirical coefficient set; no NASA/DOE source opened. |
| `engineering.aerodynamics.glauert_skew_momentum_thrust_coefficient` | UNVERIFIED | OPENFAST | Glauert skewed-wake momentum C_T = 4 a F sqrt((1-a)^2 + tan^2 chi0); source not opened. |
| `engineering.aerodynamics.oye_dynamic_inflow_time_constant` | UNVERIFIED | OPENFAST | Oye dynamic-inflow time constants (empirical coefficients) from Branlard's Springer book; not opened. |
| `engineering.aerodynamics.pitt_peters_skewed_wake_correction` | UNVERIFIED | OPENFAST | Pitt-Peters (K = 15 pi/32) skewed-wake correction named only in warning text; no source opened. |
| `engineering.aerodynamics.prandtl_tip_loss_factor` | UNVERIFIED | OPENFAST | Prandtl tip-loss F = (2/pi) acos(exp(-B (R - r)/(2 r /sin phi/))); the AeroDyn manual could not be fetched (nrel.gov unreachable); no NASA wind-turbine document opened states it. |
| `engineering.aerodynamics.tip_speed_ratio` | UNVERIFIED | OPENFAST | lambda = Omega R/V is definitional but no NASA/DOE document stating it was opened (AeroDyn manual unreachable; NTRS searches 'tip speed ratio' gave rotorcraft and fan documents, none opened). |
| `engineering.aerodynamics.wake_skew_angle` | UNVERIFIED | OPENFAST | chi = (1 + 0.6 a) chi0 is an empirical relation cited nowhere in the file. |
| `engineering.aerodynamics.wind_power_flux` | UNVERIFIED | OPENFAST | P_w = 0.5 rho A V^3: the AeroDyn manual could not be fetched. The relation follows from kinetic energy flux (0.5 mdot V^2 with mdot = rho A V, NASA Glenn Mass Flow Rate in the catalog), but the kinetic-energy step would  |
| `engineering.aerodynamics.wind_turbine_power_coefficient` | UNVERIFIED | OPENFAST | C_P = P/(0.5 rho A V^3): same missing wind-turbine source. |
| `engineering.aerodynamics.wind_turbine_thrust_coefficient` | UNVERIFIED | OPENFAST | C_T = T/(0.5 rho A V^2): same missing wind-turbine source. |
| `engineering.aerodynamics.wind_turbine_torque_coefficient` | UNVERIFIED | OPENFAST | C_Q = Q/(0.5 rho A V^2 R): same missing wind-turbine source. |
| `engineering.fluids.api_offshore_wind_profile` | UNVERIFIED | OPENFAST | API offshore wind profile U = U_1h (1 + 0.0573 sqrt(1 + 0.15 U_1h) ln(z/z_ref)): API RP 2A / ISO 19901-1 are standards (not allowed); empirical coefficients; no NASA/DOE document opened. |
| `engineering.fluids.log_law_wind_profile` | AMBIGUOUS | OPENFAST | NASA CR-2288 (Luers), sec. 'Summary of mean wind model', p. 2 (read as an image) prints the neutral logarithmic law as u = (u*/k) ln((Z + Z0)/Z0), i.e. with the height origin shifted by the roughness length (Z measured a |
| `engineering.fluids.log_law_wind_profile_friction_velocity` | AMBIGUOUS | OPENFAST | Same convention issue as log_law_wind_profile: CR-2288 prints u = (u*/k)[ln((Z + Z0)/Z0) + psi(Z/L)]; the candidate's U(z) = U_ref + (u*/kappa) ln(z/z_ref) is the difference of two such expressions (the z0 shifts cancel  |
| `engineering.orbital.hill_sphere_radius` | UNVERIFIED | POLIASTRO | No allowed source states it. Searched: OpenStax vol. 1 secs. 13.3-13.5 (no Hill sphere; 13.6 not opened), NASA/JPL Descanso ch. 2 and NASA CR-2005-213034 (only the Laplace 2/5 form), NTRS and nasa.gov searches (nothing). |
| `orbital.j2_apsidal_precession_rate` | AMBIGUOUS | OREKIT | Source conflict on the sign of the apsidal rate; resolved only by our own derivation. |
| `engineering.orbital.perigee_maintenance_delta_v` | UNVERIFIED | POLIASTRO | Only Vallado, Fundamentals of Astrodynamics and Applications, 4th ed. (2013), p. 885 (as cited by the library) states the small-eccentricity station-keeping estimate; not freely available and not opened. It also depends  |
| `engineering.propulsion.tsiolkovsky_final_mass` | DUPLICATE | OREKIT | duplicate of `m_f = m_0 exp(-delta_v/(g0 I_sp)) is propulsion.rocket_equation_final_mass (verified in group e2_orbital) with c = g0 I_sp, which is itself verified here (propulsion.effective_exhaust_velocity, Glenn Specif |
| `fluids.knudsen_number` | UNVERIFIED | AEROSANDBOX | Kn = lambda/L is a definition; no opened NASA source prints it. Glenn Similarity Parameters (opened) does not list the Knudsen number; NASA CR-6 (Rogers and Wainwright, opened) uses 'Knudsen number based on probe diamete |
| `fluids.mixed_flat_plate_mean_skin_friction` | UNVERIFIED | AEROSANDBOX | Cengel and Cimbala Table 10-4 (copyrighted textbook) for C_f = 0.074 Re^-1/5 - 1742/Re_L; Lienhard (opened) prints Prandtl's local 0.059 Re_x^-1/5 only as a rounded problem statement (Problem 6.46) and White's local ln-l |
| `fluids.turbulent_flat_plate_mean_skin_friction` | UNVERIFIED | AEROSANDBOX | C_f = 0.074 Re_L^-1/5: Lienhard prints Prandtl's local form with the rounded coefficient 0.059 only in Problem 6.46 and the more accurate ln-law (6.102); the mean 0.074 (= 1.25 x 0.0592) is not printed. Cengel (copyright |
| `mechanics.ellipsoid_geocentric_radius` | UNVERIFIED | ROCKETPY | Standard geometry (geodetic latitude on an ellipsoid) but no opened source states it; WGS84 (NIMA TR8350.2) is a DoD document not opened; Wikipedia only in library cites. |
| `mechanics.somigliana_normal_gravity` | UNVERIFIED | ROCKETPY | Somigliana formula with free-air height correction cites Wikipedia only. The height series needs a geodesy source (Heiskanen-Moritz, NGA TR8350.2); not opened. Overlaps mechanics.weight. |
| `orbital.escape_speed` | UNVERIFIED | OPENSTAX_UNIVERSITY_PHYSICS_V1 | needs a non-OpenStax authoritative source; OpenStax removed 2026-10-09: the book now states CC BY-NC-SA 4.0 and forbids ingestion into LLM/generative AI without written permission. |
| `propulsion.actuator_disk_shaft_power` | UNVERIFIED | AEROSANDBOX | P = 0.5 T V (sqrt(T/(0.5 rho V^2 A) + 1) + 1)/eta (momentum theory; cited to MIT unified thermodynamics notes node86, not an allowed source here). No NASA propeller document opened. |
| `propulsion.bates_grain_burn_area` | UNVERIFIED | ROCKETPY | A_b = 2 pi N (R_o^2 - r_i^2 + r_i h) is geometry of an end-and-bore burning cylindrical grain; no opened source prints it (SP-8039 pages read do not give grain geometry). |
| `thermodynamics.mean_free_path_from_viscosity` | UNVERIFIED | AEROSANDBOX | lambda = (mu/p) sqrt(pi R T/2) follows from mu = 0.5 rho c_bar lambda with c_bar = sqrt(8RT/pi) (simple kinetic theory, Vincenti and Kruger book, not opened). The 1976 Standard Atmosphere defines the mean free path from  |

## Deferred (does not fit the scalar FormulaSpec)

| Candidate | Kind | Proposed future schema |
|---|---|---|
| `AEROSANDBOX-004-flat_plate_mean_cf_schlichting_power` | EMPIRICAL | Hold until attribution is confirmed; could become fluids.<name> EMPIRICAL scalar. |
| `AEROSANDBOX-005-cylinder_drag_fit` | EMPIRICAL | Fitted-to-data model; would need a curve-fit schema with data provenance. |
| `AEROSANDBOX-013-sears_haack_drag_from_radius` | SCALAR_NUMERIC | Ship only one Sears-Haack form after reconciling units. |
| `AEROSANDBOX-016-approximate_transonic_wave_drag` | ALGORITHM | Spline/piecewise model; needs a piecewise-model schema. |
| `AEROSANDBOX-024-isa_layer_table_model` | ALGORITHM | Needs a table/piecewise schema; prefer layer constants from US Standard Atmosphere 1976. |
| `AEROSANDBOX-037-balanced_field_length_torenbeek_modified` | EMPIRICAL | Ship only the published (unmodified) Torenbeek form after primary check. |
| `AEROSANDBOX-042-small_srm_propellant_fits` | EMPIRICAL | Propellant-specific data fits; would need a material-data schema. |
| `AEROSANDBOX-044-wind_and_tropopause_fits` | ALGORITHM | Data model; would need dataset schema with provenance. |
| `AEROSANDBOX-045-breguet_range_lead` | SCALAR_NUMERIC | Lead only; take Breguet range/endurance from a primary text, not from this repo. |
| `ROCKETPY-103-parachute_added_mass_porosity_fit` | EMPIRICAL | Hold until the published source is identified. |
| `ROCKETPY-104-terminal_descent_ode` | ODE_PDE | ODE with altitude-dependent density; needs ODE schema. |
| `ROCKETPY-106-fin_flutter_mach_naca_tn4197` | EMPIRICAL | Ship only after the 1.337 constant's unit basis is confirmed against NACA TN 4197. |
| `ROCKETPY-116-barrowman_roll_interference_factors` | SCALAR_NUMERIC | Long closed forms; verify each term against Barrowman before shipping as two scalars. |
| `ROCKETPY-117-barrowman_total_cp` | MATRIX_VECTOR | Variable-length weighted mean; needs sequence inputs. |
| `ROCKETPY-130-isa_layer_model_iso2533` | ALGORITHM | Table/piecewise schema; per-layer formula duplicates 022/023. |
| `E2-OREKIT-004-kepler_equation_elliptic_solve` | IMPLICIT | Implicit-equation schema (root solve with documented starter/tolerance) needed. |
| `E2-OREKIT-006-kepler_equation_hyperbolic_solve` | IMPLICIT | Implicit-equation schema needed. |
| `E2-OREKIT-016-j2_differential_drift_linearized` | ALGORITHM | Multi-input sensitivity model producing time-dependent angle offsets; needs model schema. |
| `E2-OREKIT-022-analytical_and_numerical_propagators` | ALGORITHM | State-vector propagation and frame transforms need vector/time-series schema. |
| `E2-POLIASTRO-014-state_vector_conversions_and_propagators` | MATRIX_VECTOR | Requires vector inputs/outputs schema. |
| `E2-OPENFAST-009-bem_axial_induction_momentum_region` | SCALAR_NUMERIC | Meaningful only inside the BEM residual solve; keep with the BEM ALGORITHM record unless a stand-alone use is wanted. |
| `E2-OPENFAST-016-diabatic_log_wind_profile` | EMPIRICAL |  |
| `E2-OPENFAST-019-iec_extreme_wind_speed_profile` | EMPIRICAL |  |
| `E2-OPENFAST-021-oye_dynamic_inflow_odes` | ODE_PDE | ODE schema needed. |
| `E2-OPENFAST-022-powles_tower_shadow` | EMPIRICAL |  |
| `E2-OPENFAST-023-eames_tower_shadow` | EMPIRICAL |  |
| `E2-OPENFAST-024-steady_bem_solution` | ALGORITHM | Iterative per-node solver with airfoil table lookup. |
