# Community chemistry contribution: finalization review

Review date: 2026-10-11. Official baseline: `v1.1.0`, commit
`a199bca4b719b9843928c7435fc12e51304cee49`. PR integration base: `develop`,
`50ea23d400d1992d8656a3cf878ee59be99642a1`.

The baseline has 320 formulas in 12 domains. This contribution adds 95 formulas:
all 84 proposed by [@jwchin06](https://github.com/jwchin06), plus 11 formulas from
the existing E3 integration. The resulting catalog has 415 formulas in 18 domains.
No contributed ID was rejected, omitted or replaced. The contributor's optional
`chemistry_tools.py` and its helper-dependent tests are outside this PR's scope.

## Domain inventory

| Domain | v1.1.0 | Community | Existing E3 | Final |
|---|---:|---:|---:|---:|
| aerodynamics | 35 | 0 | 0 | 35 |
| chemical_equilibrium | 0 | 12 | 0 | 12 |
| chemical_kinetics | 0 | 8 | 0 | 8 |
| chemistry | 0 | 22 | 2 | 24 |
| chromatography | 0 | 9 | 0 | 9 |
| electrical | 2 | 0 | 0 | 2 |
| electrochemistry | 0 | 5 | 2 | 7 |
| fluids | 22 | 0 | 0 | 22 |
| heat_transfer | 51 | 0 | 0 | 51 |
| materials | 15 | 0 | 0 | 15 |
| mathematics | 91 | 0 | 0 | 91 |
| mechanics | 23 | 0 | 0 | 23 |
| nuclear | 3 | 0 | 0 | 3 |
| orbital | 29 | 0 | 0 | 29 |
| propulsion | 12 | 0 | 0 | 12 |
| spectroscopy | 0 | 16 | 0 | 16 |
| structures | 17 | 0 | 0 | 17 |
| thermodynamics | 20 | 12 | 7 | 39 |
| **Total** | **320** | **84** | **11** | **415** |

The additional E3 IDs are:

- `chemistry.air_fuel_ratio_from_equivalence_ratio`
- `chemistry.equivalence_ratio_from_mixture_fraction`
- `electrochemistry.tafel_current_density`
- `electrochemistry.thermal_voltage`
- `thermodynamics.ideal_gas_mixture_chemical_potential`
- `thermodynamics.kp_kc_conversion`
- `thermodynamics.nasa7_enthalpy`
- `thermodynamics.nasa7_entropy`
- `thermodynamics.nasa7_heat_capacity`
- `thermodynamics.nasa9_heat_capacity`
- `thermodynamics.pressure_equilibrium_constant`

Their candidate IDs and prior verification/provenance decisions are recorded in
the local `ingestion/manifests/e3-electrical-chemistry-buildings.jsonl` manifest.
[The durable contribution manifest](community-chemistry.json) records all 95 IDs,
their origin and retained bibliography, and SHA-256 hashes of the 84 original
contributor source files. Source hashes describe the supplied files before import
cleanup, not the final reformatted modules.

## Reference, constants and compatibility checks

- All 320 baseline formula dictionaries, including IEEE-rendered references,
  match the official release. Existing evaluator files and the `ReferenceSpec`
  schema/public API are unchanged. The branch already inherited version 1.1.0
  from `main`; finalization does not bump the version.
- All 84 original formulas retain their equations, variables, units, assumptions,
  numerical cases and relationship-specific bibliographic records. Cleanup removes
  unused imports, formats new files and follows the catalog's established convention
  for scientific argument symbols (`I`, `l`).
- The reported consolidation is reproducible: 68 inline `ReferenceSpec` calls were
  removed across 61 of the contributed files. Non-BIPM reference dictionaries are
  identical to the original extension. Nineteen supporting BIPM records deliberately
  use the shared [SI defining-constants page](https://www.bipm.org/en/measurement-units/si-defining-constants)
  instead of the extension's SI Brochure PDF record. This changes those reference
  dictionaries/IEEE strings, but not their relationship references or results.
- All 415 serialized dictionaries match the integration state captured before final
  cleanup. Shared builders live in `catalog/_sources.py`; numerical constants live
  in `catalog/_constants.py`. Planck and Boltzmann constants are reused. The newly
  added exact constants are Avogadro's constant, elementary charge and light speed;
  `R = N_A k_B` and `F = N_A e` are calculated once from them.
- ID uniqueness and module discovery are checked by the existing catalog validator.
  Public lookup and keyword search, including all 95 additions, are also exercised
  by the contribution regression tests. Importing every catalog module succeeds.
- No duplicate IDs were found. Boiling-point elevation and freezing-point depression
  share the algebra `i K b` but represent distinct transitions and solvent constants.
  The pressure equilibrium constant and standard reaction Gibbs energy are inverse
  relations with different outputs. Constant-pressure work is distinct from the
  existing reversible isothermal work law. The chemistry sign convention and
  concentration/activity standard states are explicit.

## DOE error and excluded electrical work

The failing import was `electrical.active_power_from_power_factor`, followed by
the other unregistered E3 electrical modules. Both `DOE-HDBK-1011/3-92` and
`DOE-HDBK-1011/1-92` were missing from the shared source table; `electric_power`
also passed an unsupported `accessed` keyword. None of these modules/tests is in
the v1.1.0 or develop baseline: this is an incomplete local E3 integration, not
a regression in an existing upstream electrical formula.

The smallest shared-builder fix adds the two real Electrical Science volume
records and an optional access-date override. The official DOE title pages verify
the 1992 date, report numbers and volume titles:
[Volume 1](https://www.energy.gov/sites/default/files/2026-04/DOE-HDBK-1011-92_VOL1.pdf),
[Volume 3](https://www.energy.gov/sites/default/files/2026-04/DOE-HDBK-1011-92_VOL3.pdf).
Existing DOE records keep their original access dates. The held electrical tests
pass after the fix (67 tests). Eight unregistered electrical formula files and
their test module were preserved outside the checkout for a separate contribution;
they are not silently registered or included in the chemistry formula count.

## Scientific checks and their limits

The review examines the declared equations, evaluators, dimensions, SI units,
physical assumptions and domain checks of the 95 additions. All 168 numerical
cases in the original 84-formula contribution were independently recomputed
from the declared equations with high-precision arithmetic, without calling their
evaluators to generate expected values. All reproduce the recorded expectations
within their declared tolerances. Existing E3 tests independently check the
additional 11 formulas.

Fresh source checks concentrate on the missing DOE bibliography, SI constants,
NASA RP-1311 polynomial/equivalence-ratio forms, fuel-cell voltage relations,
Harvey's activity/extraction/chromatography conventions and Macmillan's reduced
mass relation. These complement the contributor's existing source records; they
are not a claim that every one of the 45 distinct contributed relationship-source
URLs was reopened during finalization. Automated catalog validation establishes
structural and numerical consistency, not scientific applicability or copyright
clearance for arbitrary use.

Independent regression tests cover invalid/nonfinite inputs, weak-electrolyte
mass balance and extreme concentration ratios, salt mass action, Gibbs/Nernst
consistency, SI Beer-Lambert conversion, second-order half-life composition,
extraction and the van Deemter minimum. No validity thresholds were invented;
coefficient fits and approximate models retain their stated applicability limits.

## Contribution permission and source-content review

The maintainer identified the contributor as **@jwchin06**, authorized this public
acknowledgment, and explicitly confirmed the contributor's consent to distribute
their original code under **Apache-2.0** in the finalization chat on 2026-10-11.
This records the maintainer's confirmation, not an independently obtained signed
contributor agreement. No co-author identity or email address is invented.

The original inventory has 61 OpenStax-supported formulas, 18 supported by David
Harvey/LibreTexts and five with other relationship sources. All legitimate
citations are retained. The imported material consists of equation implementations,
variable/unit metadata, short model assumptions and independently calculated
numerical checks. No textbook chapters, figures, tables, downloaded PDFs or
worked-example narratives are included; no copied third-party implementation was
identified in the reviewed code.

This distinction matters because:

- [OpenStax Chemistry 2e's current attribution block](https://openstax.org/books/chemistry-2e/pages/1-introduction)
  specifies CC BY-NC-SA and additional restrictions on content ingestion. It is
  not an Apache-2.0 source-code license. Its scientific relationships are cited;
  this PR does not relicense the textbook's expressive content.
- [Harvey's activity chapter](https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Analytical_Chemistry_2.1_by_David_Harvey/Analytical_Chemistry_2.1_(Harvey)/06%3A_Equilibrium_Chemistry/6.09%3A_Activity_Effects)
  identifies CC BY-NC-SA 4.0. Its source-specific conventions are documented in
  original wording; no activity-coefficient table is imported.
- [Macmillan's Reduced Mass review](https://www.macmillanlearning.com/studentresources/college/physics/tiplermodernphysics6e/classial_concept_review/chapter_4_ccr_29_reduced_mass.pdf)
  is publicly accessible but does not grant an Apache license. Only the reduced-mass
  relationship is restated in a short independent implementation.

The [U.S. Copyright Office's explanation of protected subject matter](https://www.copyright.gov/help/faq/faq-protect.html)
distinguishes facts/ideas/methods from their expression. That supports the review's
classification, but does not establish the provenance of every sentence or provide
a license to copy source text. Shared reference builders do not resolve that issue.

**Non-blocking maintainer follow-up:** inspect the short descriptive prose against
the restricted sources and consider independent primary references for formulas
currently supported only by OpenStax/LibreTexts. No specific infringing material
has been identified. The PR is submitted as a Draft to make this remaining source
provenance review visible; it is not represented as ready to merge. Optional
docstring expansion and chemistry convenience helpers are outside the blocking
scope.

## Final validation

Local final validation used Python 3.13.9. A local Python 3.10 installation was
not available; the repository's Python 3.10 catalog/test job remains the CI check
for the minimum supported interpreter.

| Check | Final result |
|---|---|
| Targeted chemistry/E3/source tests | 84 passed, 1,600 subtests passed |
| `python -m unittest discover -s tests -v` against the installed wheel | 1,499 run: 1,498 passed, 1 skipped, 0 errors/failures |
| `python -m pytest -q -rs` against the installed wheel | 1,498 passed, 1 skipped, 10,468 subtests passed |
| Clean-installed `python -I -m sciengformulary.validation` outside the checkout | 415 formulas, 18 domains, 1,146 numerical cases passed; 0 validation problems |
| Reference structure and IEEE formatting (included in catalog validation) | 676 reference instances passed |
| Independent original-contribution equation recomputation | 168/168 cases reproduced |
| Existing `ruff check src tests` (Ruff 0.12.0) | Passed |
| `git diff --check` | Passed |
| `python -m build` (isolated Hatchling build) | One wheel and one sdist, version 1.1.0 |
| `python -m twine check --strict dist/*` | Both distributions passed |
| Package-content inspection | Wheel: 452 files; sdist: 455 files; no excluded artifacts |
| Clean wheel installation and public API/import smoke check | 415 formulas; 439 catalog modules imported; version and JSON serialization checked |
| Held, excluded electrical E3 tests after source-builder correction | 67 passed, 115 subtests passed |

The single skip is the pre-existing abstract base test in
`tests/test_orbital_e2_other.py`, not a disabled chemistry test. Both the full
unittest suite and full pytest suite ran once on the final source state. The
Windows sandbox initially blocked ensurepip's temporary files for the clean
environment; recreating that environment with the permitted filesystem access
resolved it. No test or validation rule was weakened.

The repository has no configured Ruff CI job or Ruff rule set. The existing
Ruff 0.12.0 check passes. An exploratory Ruff 0.17.0 invocation enables broader
defaults and reports stylistic findings already widespread in the release
(1,104 source findings in v1.1.0; 1,171 in this integration, a difference of
41 implicit-string-concatenation and 26 scientific-symbol `noqa` findings).
Changing the repository's lint policy or rewriting upstream formatting is outside
this contribution. No lint configuration was changed to make checks pass.
