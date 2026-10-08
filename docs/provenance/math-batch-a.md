# Provenance: mathematics batch A

Sanitized record of how the mathematics formulas added in batch A were found, checked and
licensed. It lists source revisions, licensing decisions, accepted and rejected candidates,
reference locators and verification outcomes. It contains no source text.

## Sources and licensing decisions

| Source | Revision | License decision | Role |
|---|---|---|---|
| Lean mathlib4 (`MATHLIB`) | commit 4a3cff2c9216262b3e173547a543e524f5d6be6e (2026-10-08) | Apache-2.0 (repository LICENSE; every cited file carries the Apache 2.0 header) | supporting reference (formal statements; proofs not re-checked here) |
| P. Selinger, Matrix Theory and Linear Algebra (`SELINGER_LA`) | 1st ed., revision Dal 2018 A; source commit d74bc3a9751b10db8a292eb2f73d4bf1f70de996 | CC BY 4.0 (adapts Lyryx Learning and K. Kuttler, CC BY 3.0); relations restated, no text or figures reused | supporting reference (textbook) |
| NIST/SEMATECH e-Handbook of Statistical Methods (`NIST_HANDBOOK`) | pages accessed 2026-10-08 | NIST work; cited, not copied | supporting reference (probability distributions) |
| SymPy (`SYMPY`) | release 1.14.0, commit 16fa855354eb7bcabd3fe10993841e03b1382692 | BSD-3-Clause; cited files outside the MIT/PyDy exception directories | discovery only; never counted as support |

Excluded for this batch: NIST DLMF (bulk copying restricted), OpenStax Calculus and MIT OCW
(non-commercial share-alike), MathWorld, Wikipedia. A library implementation alone never made
a candidate verified; every accepted formula cites a formal statement, a textbook or a NIST
handbook page that states the relation.

## Outcome

- Scalar candidates in the manifest: 92; deferred (non-scalar): 19.
- Technical gate: DUPLICATE 2, UNVERIFIED 5, VERIFIED 84, VERIFIED_PARTIAL 1.
- Implemented in this batch: 35.
- AMBIGUOUS and UNVERIFIED candidates are being revisited (see the table below); they are not
  in the catalog.

## Implemented formulas

Each expected value was computed independently of the shipped evaluator (exact integer or
Fraction arithmetic, mpmath at 50+ digits, brute-force enumeration, or a worked example in the
cited textbook) and is checked on every import and in CI.

| Formula id | Supporting references (locator) | Discovered in | Cases | Oracles |
|---|---|---|---|---|
| `mathematics.angle_between_vectors_3d` | P. Selinger: 1st ed., rev. Dal 2018 A, sec. 2.6, proposition relating the dot product to the angle (source label prop:dot-product-angle); P. Selinger: 1st ed., rev. Dal 2018 A, sec. 2.7, geometric definition of the cross product (source label def:cross-product-geometric); The mathlib Community: def InnerProductGeometry.angle | SELINGER_LA | 7 | independent oracle (exact / high precision) |
| `mathematics.arithmetic_series_sum_first_integers` | The mathlib Community: theorem Finset.sum_range_id_mul_two | MATHLIB | 5 | direct sum |
| `mathematics.bayes_posterior_probability` | The mathlib Community: theorem ProbabilityTheory.cond_eq_inv_mul_cond_mul; National Institute of Standards and Technology: sec. 8.1.10, Bayes formula | MATHLIB | 4 | mpmath 50 digits |
| `mathematics.beta_function` | The mathlib Community: lemma Complex.betaIntegral_eq_Gamma_mul_div; National Institute of Standards and Technology: sec. 1.3.6.6.17, Beta Distribution: beta function | MATHLIB, SYMPY | 5 | mpmath 50 digits |
| `mathematics.binomial_coefficient` | The mathlib Community: theorem Nat.choose_eq_factorial_div_factorial; The mathlib Community: theorem Finset.card_powersetCard | MATHLIB, SYMPY | 5 | brute force / itertools.combinations count + exact factorial ratio / itertools.product brute force + exact factorial ratio |
| `mathematics.binomial_probability_mass` | The mathlib Community: lemma ProbabilityTheory.binomial_real_singleton; National Institute of Standards and Technology: sec. 1.3.6.6.18, Binomial Distribution: probability mass function | MATHLIB, SYMPY | 5 | mpmath 50 digits |
| `mathematics.catalan_number` | The mathlib Community: theorem succ_mul_catalan_eq_centralBinom; The mathlib Community: def Nat.centralBinom; The mathlib Community: theorem treesOfNumNodesEq_card_eq_catalan | MATHLIB, SYMPY | 5 | brute force / exact integer recurrence / explicit binary-tree enumeration + itertools Dyck words |
| `mathematics.cauchy_probability_density` | The mathlib Community: def ProbabilityTheory.cauchyPDFReal; National Institute of Standards and Technology: sec. 1.3.6.6.3, Cauchy Distribution: probability density function | MATHLIB, SYMPY | 4 | mpmath 50 digits |
| `mathematics.combinations_with_repetition` | The mathlib Community: theorem Nat.multichoose_eq; The mathlib Community: theorem Sym.card_sym_eq_multichoose | MATHLIB, SYMPY | 5 | brute force / itertools.product nondecreasing tuples |
| `mathematics.cramer_rule_2x2_x` | P. Selinger: 1st ed., rev. Dal 2018 A, sec. 7.7, Cramer's rule theorem (source label thm:cramers-rule); P. Selinger: 1st ed., rev. Dal 2018 A, sec. 7.5, theorem: invertible iff determinant non-zero (source label thm:determinant-invertible); P. Selinger: 1st ed., rev. Dal 2018 A, sec. 7.6, formula for the inverse of a 2x2 matrix (source label eqn:inverse-2-by-2); The mathlib Community: theorem Matrix.mulVec_cramer | SELINGER_LA | 4 | independent oracle (exact / high precision) |
| `mathematics.cramer_rule_2x2_y` | P. Selinger: 1st ed., rev. Dal 2018 A, sec. 7.7, Cramer's rule theorem (source label thm:cramers-rule); P. Selinger: 1st ed., rev. Dal 2018 A, sec. 7.5, theorem: invertible iff determinant non-zero (source label thm:determinant-invertible); P. Selinger: 1st ed., rev. Dal 2018 A, sec. 7.6, formula for the inverse of a 2x2 matrix (source label eqn:inverse-2-by-2); The mathlib Community: theorem Matrix.mulVec_cramer | SELINGER_LA | 4 | independent oracle (exact / high precision) |
| `mathematics.derangement_count` | The mathlib Community: theorem numDerangements_sum; The mathlib Community: theorem card_derangements_eq_numDerangements | MATHLIB, SYMPY | 5 | brute force / brute force: itertools.permutations(range(0)) yields one empty tuple / exact Fraction + integer recurrence / itertools.permutations brute force + exact Fraction sum |
| `mathematics.determinant_2x2` | P. Selinger: 1st ed., rev. Dal 2018 A, sec. 7.1, Def. 7.1; The mathlib Community: theorem Matrix.det_fin_two_of | MATHLIB, SELINGER_LA | 3 | independent oracle (exact / high precision) |
| `mathematics.determinant_3x3` | P. Selinger: 1st ed., rev. Dal 2018 A, sec. 7.1, Def. 7.3; The mathlib Community: theorem Matrix.det_fin_three | SELINGER_LA | 4 | independent oracle (exact / high precision) |
| `mathematics.distance_between_points_3d` | P. Selinger: 1st ed., rev. Dal 2018 A, sec. 2.5, definition of the distance between points (source label def:distance-between-points); The mathlib Community: theorem EuclideanSpace.dist_eq | SELINGER_LA | 4 | independent oracle (exact / high precision) |
| `mathematics.distance_point_to_plane` | P. Selinger: 1st ed., rev. Dal 2018 A, sec. 3.2, worked example on the shortest distance to a plane (source label exa:shortest-distance-plane); P. Selinger: 1st ed., rev. Dal 2018 A, sec. 3.2, definition of the standard equation of a plane (source label def:standard-equation-plane); P. Selinger: 1st ed., rev. Dal 2018 A, sec. 2.6, definition of the projection (source label def:projection) | SELINGER_LA | 4 | independent oracle (exact / high precision) |
| `mathematics.exponential_cumulative_distribution` | The mathlib Community: lemma ProbabilityTheory.cdf_expMeasure_eq; National Institute of Standards and Technology: sec. 1.3.6.6.7, Exponential Distribution: cumulative distribution function | MATHLIB | 4 | mpmath 50 digits |
| `mathematics.exponential_probability_density` | The mathlib Community: lemma ProbabilityTheory.exponentialPDF_eq; National Institute of Standards and Technology: sec. 1.3.6.6.7, Exponential Distribution: probability density function | MATHLIB, SYMPY | 3 | mpmath 50 digits |
| `mathematics.fibonacci_binet` | The mathlib Community: theorem Real.coe_fib_eq; The mathlib Community: def Nat.fib | MATHLIB, SYMPY | 5 | exact integer recurrence / exact integer recurrence + mpmath Binet |
| `mathematics.finite_geometric_series_sum` | The mathlib Community: theorem geom_sum_eq | MATHLIB | 7 | exact Fraction direct summation / exact Fraction direct summation + mpmath fsum |
| `mathematics.gamma_probability_density` | The mathlib Community: def ProbabilityTheory.gammaPDFReal; National Institute of Standards and Technology: sec. 1.3.6.6.11, Gamma Distribution: probability density function | MATHLIB, SYMPY | 5 | mpmath 50 digits |
| `mathematics.geometric_probability_mass_failures` | The mathlib Community: lemma ProbabilityTheory.geometricMeasure_real_singleton | MATHLIB | 3 | mpmath 50 digits |
| `mathematics.heron_triangle_area` | The mathlib Community: theorem Theorems100.heron | MATHLIB | 4 | exact Fraction radicand + mpmath sqrt / exact radicand / exact radicand 3 / exact radicand 720 |
| `mathematics.infinite_geometric_series_sum` | The mathlib Community: theorem hasSum_geometric_of_abs_lt_one; The mathlib Community: theorem summable_geometric_iff_norm_lt_one | MATHLIB | 5 | exact Fraction / exact Fraction + mpmath nsum / exact Fraction partial sum + mpmath 60-digit nsum / mpmath nsum + exact Fraction |
| `mathematics.k_permutations` | The mathlib Community: theorem Nat.descFactorial_eq_div; The mathlib Community: theorem Fintype.card_embedding_eq | MATHLIB | 5 | brute force / itertools.product distinct-tuple count |
| `mathematics.law_of_cosines_side` | The mathlib Community: theorem EuclideanGeometry.dist_sq_eq_dist_sq_add_dist_sq_sub_two_mul_dist_mul_dist_mul_cos_angle; The mathlib Community: def EuclideanGeometry.angle | MATHLIB | 5 | mpmath 50-digit |
| `mathematics.law_of_sines_side` | The mathlib Community: theorem EuclideanGeometry.dist_eq_dist_mul_sin_angle_div_sin_angle; The mathlib Community: theorem EuclideanGeometry.sin_angle_mul_dist_eq_sin_angle_mul_dist; The mathlib Community: def EuclideanGeometry.angle | MATHLIB | 5 | mpmath 50-digit |
| `mathematics.logarithm_change_of_base` | The mathlib Community: def Real.logb; The mathlib Community: theorem Real.logb_eq_iff_rpow_eq | MATHLIB | 6 | exact / mpmath 50-digit / mpmath 50-digit ln(x)/ln(b) / mpmath 50-digit with b = mpf(1.001 as float) |
| `mathematics.n_ball_volume` | The mathlib Community: theorem EuclideanSpace.volume_ball; The mathlib Community: theorem InnerProductSpace.volume_ball; The mathlib Community: lemma InnerProductSpace.volume_ball_of_dim_even | MATHLIB | 7 | exact  / mpmath 50-digit Gamma form / mpmath Gamma form |
| `mathematics.parallelepiped_volume` | P. Selinger: 1st ed., rev. Dal 2018 A, sec. 2.7, proposition on the box product and volume (source label prop:box-product); The mathlib Community: theorem triple_product_eq_det | SELINGER_LA | 4 | independent oracle (exact / high precision) |
| `mathematics.poisson_probability_mass` | The mathlib Community: lemma ProbabilityTheory.poissonMeasure_real_singleton; National Institute of Standards and Technology: sec. 1.3.6.6.19, Poisson Distribution: probability mass function | MATHLIB, SYMPY | 4 | mpmath 50 digits |
| `mathematics.quadratic_discriminant` | The mathlib Community: def discrim; The mathlib Community: theorem quadratic_eq_zero_iff | MATHLIB | 5 | fractions.Fraction exact |
| `mathematics.sphere_volume` | The mathlib Community: lemma EuclideanSpace.volume_ball_fin_three; The mathlib Community: theorem EuclideanSpace.volume_ball | MATHLIB | 5 | exact  / mpmath / mpmath (r = mpf(0.1 as float)) / mpmath 50-digit |
| `mathematics.triangle_area_from_vertices_3d` | P. Selinger: 1st ed., rev. Dal 2018 A, sec. 2.7, worked example on the area of a triangle (source label exa:area-triangle); P. Selinger: 1st ed., rev. Dal 2018 A, sec. 2.7, geometric definition of the cross product (source label def:cross-product-geometric) | SELINGER_LA | 4 | independent oracle (exact / high precision) |
| `mathematics.triangle_median_length` | The mathlib Community: theorem EuclideanGeometry.dist_sq_add_dist_sq_eq_two_mul_dist_midpoint_sq_add_half_dist_sq | MATHLIB | 4 | exact Fraction radicand 25 + sqrt / exact radicand / exact radicand 12 |

## Not implemented

| Candidate | Gate | Evidence basis | Discovered in | Status / reason |
|---|---|---|---|---|
| `mathematics.angle_between_line_and_plane` | VERIFIED | INDEPENDENT_REFERENCE | SELINGER_LA | PHASE2B_DONE |
| `mathematics.angle_between_lines_3d` | VERIFIED | INDEPENDENT_REFERENCE | SELINGER_LA | PHASE2B_DONE |
| `mathematics.bell_number` | VERIFIED | INDEPENDENT_REFERENCE | SYMPY | PHASE2B_DONE |
| `mathematics.beta_probability_density` | VERIFIED | INDEPENDENT_REFERENCE | SYMPY | PHASE2B_DONE |
| `mathematics.birthday_distinct_probability` | VERIFIED | INDEPENDENT_REFERENCE | MATHLIB | PHASE2B_DONE |
| `mathematics.characteristic_polynomial_2x2` | VERIFIED | INDEPENDENT_REFERENCE | SELINGER_LA | PHASE2B_DONE |
| `mathematics.chi_squared_probability_density` | VERIFIED | INDEPENDENT_REFERENCE | SYMPY | PHASE2B_DONE |
| `mathematics.circle_area` | VERIFIED | INDEPENDENT_REFERENCE | MATHLIB | PHASE2B_DONE |
| `mathematics.complementary_error_function` | UNVERIFIED | IMPLEMENTATION_ONLY | SYMPY | PHASE2B_DONE |
| `mathematics.cramer_rule_3x3_x1` | VERIFIED | INDEPENDENT_REFERENCE | SELINGER_LA | PHASE2B_DONE |
| `mathematics.distance_between_points_2d` | VERIFIED | INDEPENDENT_REFERENCE | SELINGER_LA | PHASE2B_DONE |
| `mathematics.distance_point_to_line_3d` | VERIFIED | INDEPENDENT_REFERENCE | SELINGER_LA | PHASE2B_DONE |
| `mathematics.dot_product_3d` | VERIFIED | INDEPENDENT_REFERENCE | SELINGER_LA | PHASE2B_DONE |
| `mathematics.dot_product_from_magnitudes_and_angle` | VERIFIED | INDEPENDENT_REFERENCE | SELINGER_LA | PHASE2B_DONE |
| `mathematics.double_factorial` | VERIFIED | INDEPENDENT_REFERENCE | SYMPY | PHASE2B_DONE |
| `mathematics.eigenvalues_2x2_larger_real` | VERIFIED | INDEPENDENT_REFERENCE | SELINGER_LA | PHASE2B_DONE |
| `mathematics.error_function` | UNVERIFIED | IMPLEMENTATION_ONLY | SYMPY | PHASE2B_DONE |
| `mathematics.falling_factorial` | VERIFIED | INDEPENDENT_REFERENCE | SYMPY | PHASE2B_DONE |
| `mathematics.gamma_function` | VERIFIED | INDEPENDENT_REFERENCE | SYMPY | PHASE2B_DONE |
| `mathematics.gamma_half_integer` | VERIFIED | INDEPENDENT_REFERENCE | MATHLIB | PHASE2B_DONE |
| `mathematics.gaussian_integral` | VERIFIED | INDEPENDENT_REFERENCE | MATHLIB | PHASE2B_DONE |
| `mathematics.generalized_exponential_integral` | UNVERIFIED | IMPLEMENTATION_ONLY | SYMPY | PHASE2B_DONE |
| `mathematics.geometric_probability_mass_trials` | VERIFIED | INDEPENDENT_REFERENCE | SYMPY | PHASE2B_DONE |
| `mathematics.gumbel_max_probability_density` | VERIFIED | INDEPENDENT_REFERENCE | SYMPY | PHASE2B_DONE |
| `mathematics.harmonic_number` | VERIFIED_PARTIAL | INDEPENDENT_REFERENCE | SYMPY | PHASE2B_DONE |
| `mathematics.hyperbolic_sine` | VERIFIED | INDEPENDENT_REFERENCE | SYMPY | PHASE2B_DONE |
| `mathematics.hypergeometric_probability_mass` | UNVERIFIED | IMPLEMENTATION_ONLY | SYMPY | PHASE2B_DONE |
| `mathematics.laplace_probability_density` | VERIFIED | INDEPENDENT_REFERENCE | SYMPY | PHASE2B_DONE |
| `mathematics.lognormal_probability_density` | VERIFIED | INDEPENDENT_REFERENCE | SYMPY | PHASE2B_DONE |
| `mathematics.lower_incomplete_gamma` | VERIFIED | INDEPENDENT_REFERENCE | SYMPY | PHASE2B_DONE |
| `mathematics.negative_binomial_probability_mass` | UNVERIFIED | IMPLEMENTATION_ONLY | SYMPY | PHASE2B_DONE |
| `mathematics.normal_cumulative_distribution` | VERIFIED | INDEPENDENT_REFERENCE | SYMPY | PHASE2B_DONE |
| `mathematics.normal_probability_density` | DUPLICATE | REFERENCE_LOCATED_UNCONFIRMED | MATHLIB, SYMPY | duplicate of `mathematics.normal_probability_density` |
| `mathematics.parallelogram_area_3d_vectors` | VERIFIED | INDEPENDENT_REFERENCE | SELINGER_LA | PHASE2B_DONE |
| `mathematics.parallelogram_area_from_sides_and_angle` | VERIFIED | INDEPENDENT_REFERENCE | SELINGER_LA | PHASE2B_DONE |
| `mathematics.pareto_probability_density` | VERIFIED | INDEPENDENT_REFERENCE | MATHLIB, SYMPY | PHASE2B_DONE |
| `mathematics.plane_equation_constant` | VERIFIED | INDEPENDENT_REFERENCE | SELINGER_LA | PHASE2B_DONE |
| `mathematics.pythagorean_hypotenuse` | VERIFIED | INDEPENDENT_REFERENCE | MATHLIB | PHASE2B_DONE |
| `mathematics.quadratic_root_plus` | VERIFIED | INDEPENDENT_REFERENCE | MATHLIB | PHASE2B_DONE |
| `mathematics.rayleigh_probability_density` | VERIFIED | INDEPENDENT_REFERENCE | SYMPY | PHASE2B_DONE |
| `mathematics.reciprocal_triangular_number_sum` | VERIFIED | INDEPENDENT_REFERENCE | MATHLIB | PHASE2B_DONE |
| `mathematics.regularized_incomplete_beta` | VERIFIED | INDEPENDENT_REFERENCE | SYMPY | PHASE2B_DONE |
| `mathematics.right_triangle_altitude_geometric_mean` | VERIFIED | INDEPENDENT_REFERENCE | MATHLIB | PHASE2B_DONE |
| `mathematics.right_triangle_angle_from_legs` | VERIFIED | INDEPENDENT_REFERENCE | MATHLIB | PHASE2B_DONE |
| `mathematics.rising_factorial` | VERIFIED | INDEPENDENT_REFERENCE | SYMPY | PHASE2B_DONE |
| `mathematics.scalar_projection_3d` | VERIFIED | INDEPENDENT_REFERENCE | SELINGER_LA | PHASE2B_DONE |
| `mathematics.sinc_unnormalized` | VERIFIED | INDEPENDENT_REFERENCE | SYMPY | PHASE2B_DONE |
| `mathematics.stewart_cevian_length` | VERIFIED | INDEPENDENT_REFERENCE | MATHLIB | PHASE2B_DONE |
| `mathematics.stirling_factorial_approximation` | DUPLICATE | REFERENCE_LOCATED_UNCONFIRMED | MATHLIB | duplicate of `mathematics.stirling_factorial_approximation` |
| `mathematics.stirling_number_first_kind_unsigned` | VERIFIED | INDEPENDENT_REFERENCE | SYMPY | PHASE2B_DONE |
| `mathematics.stirling_number_second_kind` | VERIFIED | INDEPENDENT_REFERENCE | SYMPY | PHASE2B_DONE |
| `mathematics.student_t_probability_density` | VERIFIED | INDEPENDENT_REFERENCE | SYMPY | PHASE2B_DONE |
| `mathematics.sum_of_squares_first_integers` | VERIFIED | INDEPENDENT_REFERENCE | MATHLIB | PHASE2B_DONE |
| `mathematics.total_probability_two_events` | VERIFIED | INDEPENDENT_REFERENCE | MATHLIB | PHASE2B_DONE |
| `mathematics.upper_incomplete_gamma` | VERIFIED | INDEPENDENT_REFERENCE | SYMPY | PHASE2B_DONE |
| `mathematics.vector_magnitude_3d` | VERIFIED | INDEPENDENT_REFERENCE | SELINGER_LA | PHASE2B_DONE |
| `mathematics.weibull_probability_density` | VERIFIED | INDEPENDENT_REFERENCE | SYMPY | PHASE2B_DONE |

## Deferred (does not fit the scalar FormulaSpec)

Kept in `math-batch-a.deferred.jsonl` next to this file for a future schema; nothing here is
in the catalog.

| Candidate | Kind | Proposed future schema |
|---|---|---|
| `MATHLIB-043-determinant_3x3_general` | MATRIX_VECTOR | Matrix-valued input schema (n x n array) with scalar output. |
| `MATHLIB-044-cauchy_schwarz` | MATRIX_VECTOR | Inequality/constraint schema over vector inputs (bound checker), not FormulaSpec. |
| `MATHLIB-045-taylor_lagrange_remainder` | SYMBOLIC_IDENTITY | Function-valued inputs plus existential/bound schema (error-bound helper), not FormulaSpec. |
| `MATHLIB-046-gamma_reflection` | SYMBOLIC_IDENTITY | Identity/consistency-check schema (two expressions asserted equal) used in verification suites. |
| `MATHLIB-047-legendre_duplication` | SYMBOLIC_IDENTITY | Identity/consistency-check schema. |
| `SYMPY-037-maxwell_pdf` | SCALAR_NUMERIC |  |
| `SYMPY-043-fourier_transform_convention` | SYMBOLIC_IDENTITY | Needs a function-valued/operator schema (transform pairs with convention metadata), not scalar inputs. |
| `SYMPY-044-matrix_determinant` | MATRIX_VECTOR | Needs matrix-valued inputs; a fixed 2x2/3x3 scalar-expanded variant could be v1 but is a different relation. |
| `SYMPY-045-linear_constant_coeff_ode` | ODE_PDE | ODE solution families need a symbolic/ODE schema; individual scalar solutions (e.g. damped oscillator) already live in mechanics. |
| `SYMPY-046-partial_bell_polynomial` | MATRIX_VECTOR | Variable-length sequence input; needs vector-input schema. |
| `SYMPY-047-beta_function_identities` | SYMBOLIC_IDENTITY | Identity schema (lhs == rhs for all admissible inputs) or use as verification cases of mathematics.beta_function. |
| `SELINGER_LA-003` | MATRIX_VECTOR | Needs a matrix-valued input schema (MatrixSpec with shape n x n) plus integer index inputs. |
| `SELINGER_LA-004` | MATRIX_VECTOR | Variable-size matrix input; recursive definition is an ALGORITHM-style formula. |
| `SELINGER_LA-008` | MATRIX_VECTOR | General-n Cramer's rule needs matrix + vector inputs and integer index. |
| `SELINGER_LA-012` | MATRIX_VECTOR | Needs variable-length vector input and/or vector output. |
| `SELINGER_LA-017` | MATRIX_VECTOR | Vector-valued output; needs a vector output schema. |
| `SELINGER_LA-018` | MATRIX_VECTOR | Vector output; could be split into three scalar component formulas but that is artificial. |
| `SELINGER_LA-030` | MATRIX_VECTOR | Matrix input, set-valued output; would need matrix schema and multi-output. |
| `SELINGER_LA-031` | SYMBOLIC_IDENTITY | Identity/property schema (or use as property-based tests for dot_product_3d). |
