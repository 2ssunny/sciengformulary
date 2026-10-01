# SciEng Formulary

Verified scientific and engineering formulas with variables, units, assumptions,
references, and executable evaluators.

SciEng Formulary is a curated, machine-readable formula library. Each formula
carries:

- its equation;
- input variables and the output variable, each with a dimension and a reference
  SI unit;
- assumptions and applicability limits;
- one or more authoritative references, rendered in IEEE style;
- an executable Python evaluator;
- numerical verification cases that the evaluator must reproduce.

It is written for engineers, scientists, and students, and for the Python
programs, AI agents, and CAD/CAE/analysis workflows that need a formula they can
look up, check, and evaluate:

```text
scientific or engineering question
  -> search for a formula
  -> inspect its variables and assumptions
  -> inspect its authoritative references
  -> evaluate it
  -> use the result in any downstream workflow
```

The package uses only the Python standard library.

## Status

Early, version 0.1.0. The catalog currently contains one formula
(`aerodynamics.dynamic_pressure`). More formulas will be added over time.

## Installation

From a clone of this repository (Python 3.10+):

```bash
pip install -e .
```

## Usage

```python
from sciengformulary import formulas

formulas.list()                     # all formulas, sorted by id
formulas.search("dynamic pressure") # keyword search over id, name, description, tags

f = formulas.get("aerodynamics.dynamic_pressure")
f.equation      # 'q = 0.5 * rho * V^2'
f.input_names   # ('rho', 'V')
f.assumptions   # when the formula is valid
f.references[0].format_ieee()  # verified source, as an IEEE citation
f.verification_cases           # known input/output cases
f.verify()      # re-run the cases; raises ValueError on a mismatch
f.to_dict()     # all metadata as JSON-serializable data

f.evaluate(rho=1.225, V=120.0)      # 8820.0
```

A formula can also be imported directly:

```python
from sciengformulary.catalog.aerodynamics import dynamic_pressure

dynamic_pressure.evaluate(rho=1.225, V=120.0)  # 8820.0
```

**Units.** Evaluators do no unit conversion. Pass every input in one consistent unit
system and the result comes out in the matching unit of that system. Each variable
lists its dimension and SI unit for reference. In the example above, inputs in
kg/m^3 and m/s give q = 8820.0 Pa.

## References and verification

A formula is checked in two different ways:

- **References and human review establish that the formula is right.** Every
  formula has at least one authoritative `ReferenceSpec`, stored as structured
  fields and rendered in IEEE style with `format_ieee()`. Reviewers open the
  source and confirm that it supports the equation, its notation, and its
  assumptions. A `FormulaSpec` without a reference cannot be constructed.
- **Verification cases establish that the code is right.** Every formula has at
  least one `VerificationCase`: inputs and an expected result determined
  independently of the evaluator, with a tolerance. `verify()` checks that the
  evaluator reproduces them. This shows the Python code implements the declared
  equation. It does not show that the equation is scientifically correct or
  applicable to your problem.

Formulas from course formula sheets are extracted, checked against an
authoritative source, and reviewed before they are added. They are never copied
over unchecked. The `validate-catalog` GitHub Actions check validates references,
registration, serialization, and every verification case on each pull request.

## Repository structure

```text
src/sciengformulary/
├─ __init__.py          # `formulas` registry instance
├─ core/
│  ├─ reference.py      # ReferenceSpec (structured source, IEEE rendering)
│  ├─ verification.py   # VerificationCase (known input/output case)
│  ├─ variable.py       # VariableSpec
│  ├─ spec.py           # FormulaSpec
│  └─ registry.py       # FormulaRegistry: get / list / search
└─ catalog/             # one package per domain, one file per formula
   ├─ aerodynamics/
   │  └─ dynamic_pressure.py
   ├─ structures/
   ├─ fluids/
   ├─ thermodynamics/
   ├─ materials/
   └─ orbital/
```

## Adding formulas

Create one file per formula in the matching domain, define a `FormulaSpec` with at
least one verified `ReferenceSpec` and at least one `VerificationCase`, and add it
to that domain's `FORMULAS` tuple. See [CONTRIBUTING.md](CONTRIBUTING.md) for the
source-quality, anti-fabrication, and verification-case rules.

## License

Licensed under the Apache License 2.0.
See [LICENSE](LICENSE).
