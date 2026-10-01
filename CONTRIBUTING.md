# Contributing

Formulas in this library are used by AI agents to make engineering decisions, so
correctness and applicability matter more than coverage. Only add formulas taken
from a reliable engineering source (textbook, standard, course formula sheet), and
state the conditions under which they hold.

## Adding a formula

1. **Pick the domain** under `src/auto_3dx_formulas/catalog/` (`aerodynamics`,
   `structures`, `fluids`, `thermodynamics`, `materials`, `orbital`).
2. **Create one file** named after the formula, e.g. `lift_force.py`.
3. **Define one `FormulaSpec`** in it, with a variable of the same name as the file:

   ```python
   from auto_3dx_formulas.core import FormulaSpec, VariableSpec


   def _evaluate(q: float, S: float, C_L: float) -> float:  # noqa: N803
       return q * S * C_L


   lift_force = FormulaSpec(
       id="aerodynamics.lift_force",  # <domain>.<file name>
       name="Lift Force",
       equation="L = q * S * C_L",
       inputs=(VariableSpec(...), ...),
       output=VariableSpec(...),
       evaluator=_evaluate,
       description="...",
       assumptions=("...",),
       references=("Author, Title, edition, section/eq. no.",),
       tags=("...",),
   )
   ```

4. **Register it** by importing it in the domain's `__init__.py` and adding it to
   that domain's `FORMULAS` tuple:

   ```python
   from auto_3dx_formulas.catalog.aerodynamics.lift_force import lift_force

   FORMULAS: tuple[FormulaSpec, ...] = (
       dynamic_pressure,
       lift_force,
   )
   ```

   It is then available as `formulas.get("aerodynamics.lift_force")`.

5. **Fill in every field that applies:**
   - `equation` — symbolic form, using the same symbols as the inputs.
   - `inputs` / `output` — each `VariableSpec` with `name` (the keyword argument),
     `symbol` (ASCII LaTeX, e.g. `\rho`), `description`, `dimension` (base
     dimensions M, L, T, Theta, N, I, e.g. `"M L^-3"`, or `"1"` if dimensionless)
     and `si_unit` (e.g. `"kg/m^3"`, or `"-"` if dimensionless).
   - Keep metadata strings ASCII so they print safely in a Windows console.
   - `assumptions` — when the formula is valid and when it is not
     (flow regime, linear-elastic range, small angles, ideal gas, ...).
   - `references` — the source, when available. Never invent a citation; leave
     the tuple empty instead.

6. **Follow the example** in
   [`catalog/aerodynamics/dynamic_pressure.py`](src/auto_3dx_formulas/catalog/aerodynamics/dynamic_pressure.py).

## Rules of thumb

- Evaluators do plain arithmetic with no unit conversion. Write them so that any
  consistent unit system works, and say so in the assumptions if a formula only
  holds in specific units (e.g. empirical correlations).
- The evaluator's parameter names must match the input `name`s exactly; this is
  checked when the package is imported.
- Formula ids must be unique and follow `<domain>.<snake_case_name>`.
- Keep the library free of CATIA / auto-3dx dependencies.
