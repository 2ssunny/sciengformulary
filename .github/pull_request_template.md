## Summary

<!-- What does this PR change, and why? -->

## Type of change

- [ ] New or modified formula(s)
- [ ] Core / validation change
- [ ] Documentation or maintenance

## Formulas and references

<!-- For each new or modified formula: its id, the source(s) used, where in the
source the equation is verified, and where each verification case's expected value
came from (worked example, hand calculation, ...). Write "N/A" for non-formula PRs. -->

| Formula id | Reference (IEEE) | Locator verified | Verification case source |
|---|---|---|---|
|  |  |  |  |

## Formula checklist

Mark items that do not apply as N/A (e.g. `- [x] N/A: ...`) for general maintenance PRs.

- [ ] I verified each new or modified formula against the cited source.
- [ ] Each formula has at least one authoritative `ReferenceSpec` (see the source priority in CONTRIBUTING.md).
- [ ] I opened and checked the cited source directly, not only a search snippet or summary.
- [ ] I did not invent bibliographic metadata or locators; unverified fields are left empty.
- [ ] I verified notation differences between the code and the cited source.
- [ ] Assumptions/applicability are written in original wording.
- [ ] I did not copy copyrighted prose, figures, tables, or examples.
- [ ] Each formula has at least one `VerificationCase`.
- [ ] `VerificationCase.expected` was determined independently of the evaluator (never by running it), and each case's `note` says how.
- [ ] Verification cases pass within the stated tolerances.
- [ ] The formula is registered in the correct domain `FORMULAS` tuple.
- [ ] I did not bypass `ReferenceSpec` / `VerificationCase` / `FormulaSpec` validation.

## General checklist

- [ ] The `validate-catalog` check passes.
- [ ] Docs (README / CONTRIBUTING) are updated if behavior or conventions changed.
