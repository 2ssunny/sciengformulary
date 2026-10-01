# Contributing

People, Python programs, and AI agents use the formulas in SciEng Formulary to
make scientific and engineering decisions, so correctness and applicability
matter more than coverage. **Every formula in the catalog must have at least one
real, independently verified scientific or engineering reference, and at least
one numerical verification case.** A formula that has not been verified stays
out of the catalog. There is no "reference pending" mode.

> ## Never invent bibliographic metadata
>
> Do not make up **authors, titles, years, editions, publishers, journals,
> volumes, issues, pages, section numbers, equation numbers, standard numbers,
> report numbers, ISBNs, DOIs, URLs, access dates**, or any other metadata.
>
> - Record only what you read in the source itself or in a reliable
>   bibliographic record (publisher page, library catalog, DOI record).
> - If you cannot verify an exact page, section, equation number, DOI, URL, or
>   locator, leave that field as `None`. Correct but less specific metadata is
>   better than precise-looking metadata that is made up.
> - The source must support **the actual relationship and its applicability**.
>   A source that only uses similar terminology is not enough.
> - If the source uses different notation, check that it is mathematically
>   equivalent, and note the difference in a comment next to the reference.
>
> This applies equally to human and AI-agent contributors.

## Citation style: IEEE

IEEE is the only citation style used in this project. References are stored as
structured `ReferenceSpec` fields, and the IEEE citation is generated from them
with `format_ieee()`. Do not store a pre-formatted citation string as the data,
and do not store citation numbers such as `[1]`. Numbering belongs to whatever
document renders the list.

Personal author names are stored in IEEE name form (initials, then surname), for
example `"J. D. Anderson"`.

## Source quality

Use the highest-priority source you can verify:

1. Standards, government, and technical organizations (NASA, NIST, FAA, ESA,
   ISO, ASTM, ...).
2. Established scientific and engineering textbooks from reputable publishers.
3. Peer-reviewed journal or conference papers.
4. Official university teaching material.

**Not acceptable as the cited source:** Wikipedia, blogs, random websites,
forums, AI-generated pages, search-result snippets, and unsourced summaries.
These can help you find a source, but you must then open the real source and
verify the formula there.

### Supported `source_type` values and required fields

| `source_type` | Required | Notes |
|---|---|---|
| `book` | `title`, `authors` or `organization`, `publisher`, `year` | `edition`, `place`, `locator` (e.g. `"sec. 3.4"`) when verified |
| `journal_article` | `title`, `authors`, `journal`, `year` | `volume`, `issue`, `pages`, `doi` when verified |
| `standard` | `title`, `standard_number`, `organization` | `year` when the document states it; no personal authors |
| `technical_report` | `title`, `authors` or `organization` | `report_number` only if the report actually has one |
| `official_web` | `title`, `organization`, `url`, `accessed` | `accessed` is `"YYYY-MM-DD"`; `year` = stated publication/update year |
| `course_material` | `title`, `authors` or `organization` (lecturer/institution) | `year` when stated |

Validation also rejects unknown source types, empty strings (use `None`
instead), `authors` that is not a tuple, malformed DOIs or URLs, future access
dates, citation numbering in titles, and identifiers used on the wrong type
(e.g. `journal` on a book).

## Adding a formula

1. **Pick the domain** under `src/sciengformulary/catalog/` (`aerodynamics`,
   `structures`, `fluids`, `thermodynamics`, `materials`, `orbital`).
2. **Create one file** named after the formula, e.g. `lift_force.py`.
3. **Define one `FormulaSpec`** in it, in a variable with the same name as the file:

   ```python
   from sciengformulary.core import FormulaSpec, ReferenceSpec, VariableSpec, VerificationCase


   def _evaluate(q: float, S: float, C_L: float) -> float:  # noqa: N803
       return q * S * C_L


   lift_force = FormulaSpec(
       id="aerodynamics.lift_force",  # <domain>.<file name>
       name="Lift Force",
       equation="L = q * S * C_L",
       inputs=(VariableSpec(...), ...),
       output=VariableSpec(...),
       evaluator=_evaluate,
       references=(
           ReferenceSpec(
               source_type="book",
               title=...,      # exactly as printed in the source
               authors=(...),  # e.g. ("A. B. Surname",)
               publisher=...,
               year=...,
               locator=...,    # only if verified, e.g. "sec. 3.4, eq. (3.12)"
           ),
       ),
       verification_cases=(
           VerificationCase(
               inputs={"q": 1000.0, "S": 2.0, "C_L": 0.5},
               expected=1000.0,  # worked out by hand, never by calling _evaluate
               rel_tol=1e-12,
               note="Hand calculation: 1000 * 2 * 0.5 = 1000.",
           ),
       ),
       description="...",
       assumptions=("...",),
       tags=("...",),
   )
   ```

4. **Register it** by importing it in the domain's `__init__.py` and adding it to
   that domain's `FORMULAS` tuple:

   ```python
   from sciengformulary.catalog.aerodynamics.lift_force import lift_force

   FORMULAS: tuple[FormulaSpec, ...] = (
       dynamic_pressure,
       lift_force,
   )
   ```

   It is then available as `formulas.get("aerodynamics.lift_force")`.

5. **Fill in every field that applies:**
   - `equation`: symbolic form, using the same symbols as the inputs.
   - `inputs` / `output`: each `VariableSpec` with `name` (the keyword argument),
     `symbol` (ASCII LaTeX, e.g. `\rho`), `description`, `dimension` (base
     dimensions M, L, T, Theta, N, I, e.g. `"M L^-3"`, or `"1"` if dimensionless)
     and `si_unit` (e.g. `"kg/m^3"`, or `"-"` if dimensionless).
   - `assumptions`: when the formula is valid and when it is not (flow regime,
     linear-elastic range, small angles, ideal gas, ...). Only state limits the
     reference supports. Leave out thresholds you cannot verify.
   - `references`: at least one `ReferenceSpec` (see above).
   - `verification_cases`: at least one `VerificationCase` (see below).
   - Keep metadata strings ASCII so they print safely in a Windows console.

6. **Follow the example** in
   [`catalog/aerodynamics/dynamic_pressure.py`](src/sciengformulary/catalog/aerodynamics/dynamic_pressure.py).

## Verification cases

Every `FormulaSpec` needs at least one `VerificationCase`: a set of inputs, the
expected output, a tolerance, and a note. When the formula is constructed, and
again in CI, `FormulaSpec.verify()` runs each case through the evaluator and
fails if the result is outside the tolerance.

**What a passing case shows, and what it does not.** A case answers one
question: *does the Python evaluator correctly implement the declared equation
for known inputs?* It does not show that the equation is a correct scientific or
engineering law, or that it applies to a given problem. That is established by
the references, by human review of the source, and by review of the assumptions.
CI never proves a formula scientifically.

**Where `expected` comes from.** Determine it independently of the evaluator
under test. **Never produce `expected` by calling the evaluator**, or by copying
what it printed: a case built that way passes even when the code is wrong.
In order of preference:

1. A worked example in an authoritative source. Say so in `note`, and make sure
   that source is one of the formula's `references`. Do not invent worked
   examples or their locations; the anti-fabrication rules above apply.
2. A value calculated independently from the published equation (by hand, or
   with exact arithmetic such as `fractions.Fraction`).
3. A simple hand-checked case. For simple formulas, transparent arithmetic in the
   `note` is enough, e.g. `"Hand calculation: 0.5 * 1.225 * 14400 = 8820."`
4. An independent, trusted implementation, where appropriate. Name it in `note`.

Using the numbers from a published worked example is fine. Do not copy its
explanation into `note` or code comments.

**Rules for a case:**

- `inputs` has exactly the formula's input names: nothing missing, nothing extra.
- `inputs` values and `expected` are finite `int` or `float` values.
- `rel_tol` and `abs_tol` are non-negative and passed to `math.isclose`. Use a
  tight tolerance (e.g. `rel_tol=1e-12`) for plain arithmetic. Loosen it only
  when `expected` itself is rounded (e.g. a worked example printed to four
  significant figures), and explain why in `note`.
- Set `abs_tol` when `expected` is zero or close to it; a relative tolerance alone
  cannot match zero.
- `note` says where `expected` came from.

## Original wording and copyright

Write descriptions and assumptions in your own words. Do not copy explanatory
prose, figures, tables, worked examples, or other presentation from formula
sheets, textbooks, or websites. An equation itself and its variable definitions
are fine to restate. The way a source explains them is not.

## Course formula sheets

Course formula sheets are welcome as **input**: use them to find which formulas,
notation, subject coverage, and variable relationships to add. Adding them is a
verification workflow, not transcription:

1. **Extract** candidate formulas and their notation from the sheet.
2. **Research** an independent, authoritative source (priority list above) for
   each one.
3. **Verify** that the source states the same relationship (allowing for notation
   differences) and the conditions under which it applies.
4. **Review**: a human or agent reviewer checks the source and metadata.
5. **Implement** only the formulas that passed verification, each with its
   references and at least one independently determined verification case.

The formula sheet may itself be cited as `course_material` where appropriate.
Being used as input does not automatically make it the sole authority.
Prefer to verify against an independent source as well.

## Review: what machines check and what humans check

**Machine validation** runs when the package is imported and in the
`validate-catalog` GitHub Actions check on every pull request. It checks:

- structure and required fields of every `FormulaSpec` and `ReferenceSpec`;
- that every formula has at least one reference;
- registration: each formula is in its domain's `FORMULAS` tuple, under the
  right domain, and no `FormulaSpec` in the catalog is left unregistered;
- unique formula ids, and evaluator parameters that match the input names;
- that each reference can be rendered with `format_ieee()`, and each formula
  can be serialized with `to_dict()`;
- that every formula has at least one verification case, each case's inputs
  match the formula's inputs exactly, and the evaluator reproduces every
  case's `expected` value within its tolerance.

**Human review** is still required. Machine validation cannot tell whether:

- the source really exists;
- it actually supports the equation as implemented;
- the assumptions and applicability limits are correct;
- the locator and the other metadata are accurate;
- a verification case's `expected` value really was determined independently
  of the evaluator.

Reviewers should open the cited source, or ask the author for the exact
location, and confirm these points before approving. "Verified" means a reviewer
did this. No flag in the code can say a formula is verified, so do not add one.

## Other rules

- Evaluators do plain arithmetic with no unit conversion. Write them so that any
  consistent unit system works, and say so in the assumptions if a formula only
  holds in specific units (e.g. empirical correlations).
- Formula ids must be unique and follow `<domain>.<snake_case_name>`.
- Do not bypass validation (e.g. with `object.__setattr__` on a frozen spec).
- Keep the library free of third-party runtime dependencies: standard library only.
