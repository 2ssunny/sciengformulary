# auto-3dx-formulas

A small, open-source library of engineering formulas, written so that AI agents can
find a formula, check whether it applies, and evaluate it.

Each formula carries its equation, input and output variables with dimensions and
reference units, applicability conditions, and references, along with a plain Python
function that evaluates it.

It is meant to be used alongside auto-3dx 1.0.0:

```text
engineering request
  -> agent searches for and selects a formula
  -> agent checks assumptions and units
  -> agent evaluates the formula
  -> agent uses the result with auto-3dx
```

The library has no dependency on auto-3dx or CATIA, and no third-party dependencies at all.

## Status

Early, version 0.1.0. The catalog currently contains one reference formula
(`aerodynamics.dynamic_pressure`). More formulas will be added over time.

## Installation

From a clone of this repository (Python 3.10+):

```bash
pip install -e .
```

## Usage

```python
from auto_3dx_formulas import formulas

formulas.list()                     # all formulas, sorted by id
formulas.search("dynamic pressure") # keyword search over id, name, description, tags

f = formulas.get("aerodynamics.dynamic_pressure")
f.equation      # 'q = 0.5 * rho * V^2'
f.input_names   # ('rho', 'V')
f.assumptions   # when the formula is valid
f.to_dict()     # all metadata as JSON-serializable data

f.evaluate(rho=1.225, V=120.0)      # 8820.0
```

A formula can also be imported directly:

```python
from auto_3dx_formulas.catalog.aerodynamics import dynamic_pressure

dynamic_pressure.evaluate(rho=1.225, V=120.0)  # 8820.0
```

**Units.** Evaluators do no unit conversion. Pass every input in one consistent unit
system and the result comes out in the matching unit of that system. Each variable
lists its dimension and SI unit for reference. In the example above, inputs in
kg/m^3 and m/s give q = 8820.0 Pa.

## Repository structure

```text
src/auto_3dx_formulas/
├─ __init__.py          # `formulas` registry instance
├─ core/
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

Create one file per formula in the matching domain, define a `FormulaSpec`, and
add it to that domain's `FORMULAS` tuple. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE)
