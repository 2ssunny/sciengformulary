# SciEng Formulary

SciEng Formulary is a curated, machine-readable library of verified scientific and
engineering formulas for humans, Python programs, and AI agents.

Every formula carries:

- its equation;
- input variables and the output variable, each with a dimension and a reference SI
  unit;
- assumptions and applicability limits, written so you can tell when **not** to use it;
- one or more authoritative references, rendered in IEEE style;
- an executable Python evaluator;
- numerical verification cases that the evaluator must reproduce.

It is meant for engineers, scientists and students, and for the programs, AI agents and
CAD/CAE/analysis workflows that need a formula they can look up, check and evaluate:

```text
scientific or engineering question
  -> search for a formula
  -> inspect its variables and assumptions
  -> inspect its authoritative references
  -> evaluate it
  -> use the result in any downstream workflow
```

The package uses only the Python standard library.

## Installation

Once SciEng Formulary is published on PyPI (it has not been released yet):

```bash
pip install sciengformulary
```

Until then, install it from a clone; see [Development](#development).

## Quick start

```python
from sciengformulary import formulas

f = formulas.get("aerodynamics.dynamic_pressure")
print(f.equation)                    # q = 0.5 * rho * V^2
print(f.input_names)                 # ('rho', 'V')
print(f.assumptions[0])              # when the formula applies
print(f.references[0].format_ieee()) # verified source, IEEE style

result = f.evaluate(rho=1.225, V=120.0)  # 8820.0 (Pa, for SI inputs)
```

More of the API:

```python
formulas.list()                       # every formula, sorted by id
formulas.search("normal shock")       # deterministic keyword search
f.verification_cases                  # known input/output cases
f.verify()                            # re-run them; raises ValueError on a mismatch
f.to_dict()                           # all metadata, including structured references
                                      # and verification cases, as JSON-ready data
```

A formula can also be imported directly:

```python
from sciengformulary.catalog.aerodynamics import dynamic_pressure
```

## What is in the catalog

Version 0.1.0 contains 123 formulas, organised by knowledge domain:

| Domain | Formulas | Examples |
|---|---|---|
| `aerodynamics` | 14 | lift and drag, induced drag, isentropic flow ratios, normal-shock relations |
| `electrical` | 2 | Ohm's law, conductor resistance |
| `fluids` | 8 | hydrostatics, mass flow, Reynolds number, Pitot airspeed, Poiseuille flow |
| `heat_transfer` | 24 | conduction, convection correlations, radiation, lumped capacity, LMTD |
| `materials` | 15 | true stress and strain, elastic constants, von Mises, fracture, Weibull |
| `mathematics` | 2 | normal probability density, Stirling's approximation |
| `mechanics` | 21 | kinematics, friction, energy, momentum, vibration |
| `nuclear` | 3 | radioactive decay, half-life, activity |
| `orbital` | 5 | orbital energy, Kepler's third law, semi-major axis |
| `propulsion` | 2 | rocket thrust, specific impulse |
| `structures` | 8 | axial deformation, bending stress, torsion, beam deflections |
| `thermodynamics` | 19 | ideal gas, kinetic theory, entropy, Carnot limits, specific heats |

Only formulas that have been checked against an authoritative source are included.
Candidates that could not be verified, or whose sources disagree, are left out rather
than added with a weaker guarantee.

## How formulas are verified

A formula is checked in two different ways.

**References and human review establish that the formula is right.**

- Every formula has at least one authoritative `ReferenceSpec`: a standards body or
  government technical organisation (NASA, NIST, NACA reports), an established
  textbook, a peer-reviewed paper, or official university teaching material. A
  `FormulaSpec` without one cannot be constructed.
- References are stored as structured fields (authors, organisation, title, year, URL,
  locator, ...). IEEE is the only citation style; `format_ieee()` renders it.
- Locators (section, equation, figure) point at where the relationship was checked.
  Reviewers open the source and confirm the equation, its notation and its assumptions.

**Verification cases establish that the code is right.**

- Every formula has at least one `VerificationCase`: inputs, an expected result
  determined independently of the evaluator (a published worked example or table, or an
  independent calculation from the published equation), and a tolerance.
- `verify()` checks that the evaluator reproduces every case. It runs when each formula
  is constructed and again in CI.
- A passing case shows that the Python code implements the declared equation. It does
  not show that the equation is scientifically correct or applies to your problem.

Check the whole installed catalog at any time:

```bash
python -m sciengformulary.validation
```

## Units

- Evaluators do no unit conversion. **You are responsible for passing every input in one
  consistent unit system**; the result comes out in the matching unit of that system.
- Each variable's `si_unit` is its canonical reference SI representation, and
  `dimension` gives its base dimensions (M, L, T, Theta, N, I).
- Empirical formulas whose coefficients only hold in particular units say so in their
  assumptions.
- Formulas that need physical constants (Boltzmann, Planck, Stefan-Boltzmann, G,
  standard gravity) use the CODATA 2022 values in SI units, so their other inputs must
  be in SI units.

## Development

```bash
git clone https://github.com/2ssunny/sciengformulary.git
cd sciengformulary
pip install -e .
python -m sciengformulary.validation
```

## Repository structure

```text
src/sciengformulary/
├─ __init__.py          # `formulas` registry instance
├─ validation.py        # whole-catalog checks (python -m sciengformulary.validation)
├─ core/
│  ├─ reference.py      # ReferenceSpec (structured source, IEEE rendering)
│  ├─ verification.py   # VerificationCase (known input/output case)
│  ├─ variable.py       # VariableSpec
│  ├─ spec.py           # FormulaSpec
│  └─ registry.py       # FormulaRegistry: get / list / search
└─ catalog/             # one package per knowledge domain, one file per formula
   ├─ _sources.py       # shared bibliographic records
   ├─ _constants.py     # CODATA constants with their NIST references
   ├─ aerodynamics/
   ├─ ...
   └─ thermodynamics/
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the source-quality, anti-fabrication,
verification-case and units rules, and [RELEASING.md](RELEASING.md) for how releases
are published.

## License

Licensed under the Apache License 2.0.
See [LICENSE](LICENSE).
