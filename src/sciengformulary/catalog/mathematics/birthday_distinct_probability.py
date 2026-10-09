"""Birthday Problem: Probability All Distinct: P = m * (m - 1) * ... * (m - n + 1) / m^n."""

import math

from sciengformulary.catalog._sources import mathlib
from sciengformulary.catalog._domain import integer
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase

# Largest n, and largest number of bits in m**n, for which the probability is computed exactly
# with integers; beyond that a series for the logarithm is used.
_EXACT_LIMIT = 10_000
_EXACT_BITS = 5_000_000


def _evaluate(m: float, n: float) -> float:
    m = integer("m", m, minimum=1)
    n = integer("n", n, minimum=0)
    if n > m:
        return 0.0  # pigeonhole: two people must share a day
    if n <= 1:
        return 1.0
    if n <= _EXACT_LIMIT and n * m.bit_length() <= _EXACT_BITS:
        # m (m - 1) ... (m - n + 1) / m^n with exact integers; int / int is correctly rounded.
        return math.perm(m, n) / m**n
    # Since log(1 - x) <= -x, log P <= -n (n - 1) / (2 m). Below -745.2 the result is smaller
    # than half the smallest positive float and rounds to 0.0.
    if n * (n - 1) * 5 > 7452 * m:
        return 0.0
    # Otherwise y = (n - 1) / m < 0.15 and m > 6.7e4 (or m is huge and y tiny). Euler-Maclaurin
    # summation of log P = sum_{i=0}^{n-1} f(i), f(x) = log(1 - x/m), whose i = 0 term is 0:
    #   integral_0^(n-1) f(x) dx = -m * sum_{k>=2} y^k / (k (k - 1)),
    #   + f(n - 1) / 2 = log(1 - y) / 2,
    #   + (f'(n - 1) - f'(0)) / 12 = -y^2 / (12 (n - 1) (1 - y)),
    # where the next correction is of order (n - 1) / m^4 and is dropped.
    last = n - 1
    y = last / m
    power = 1.0  # y^(k - 1)
    series = 0.0
    for k in range(2, 80):
        power *= y
        term = last * power / (k * (k - 1))  # m * y^k / (k (k - 1)) without the huge m
        series += term
        if term <= 1e-18 * series:
            break
    else:
        raise ArithmeticError("the series for the birthday probability did not converge.")
    log_probability = -series + 0.5 * math.log1p(-y) - y * y / (12.0 * last * (1.0 - y))
    return math.exp(log_probability)


birthday_distinct_probability = FormulaSpec(
    id="mathematics.birthday_distinct_probability",
    name="Birthday Problem: Probability All Distinct",
    equation="P = m * (m - 1) * ... * (m - n + 1) / m^n",
    description=(
        "Probability that n people (or items), each assigned independently and uniformly to one of "
        "m equally likely days (or bins), all get different days. The numerator is the falling "
        "factorial of m with n factors; the probability is 0 when n > m."
    ),
    inputs=(
        VariableSpec(
            name="m",
            symbol="m",
            description="Number of equally likely days or bins",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="n",
            symbol="n",
            description="Number of people or items",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="P",
        symbol="P",
        description="Probability that all n assignments are distinct",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # Mathlib: the uniform (counting) probability on functions Fin n -> Fin m gives a set s
        # the probability #s / #(Fin n -> Fin m), for all n and m. Step: take s = the injective
        # functions (all birthdays distinct); an injective function is an embedding, which is the
        # equivalence the file's own proof of birthday_measure uses.
        mathlib(
            "Archive/Wiedijk100Theorems/BirthdayProblem.lean#L44",
            "theorem Theorems100.Fin.measure_apply",
        ),
        # The number of embeddings of an n-element type into an m-element type is the descending
        # factorial m (m - 1) ... (m - n + 1), zero exactly when n > m.
        mathlib(
            "Mathlib/Data/Fintype/CardEmbedding.lean#L40",
            "theorem Fintype.card_embedding_eq",
        ),
        # The number of all functions is m^n; the quotient is the equation above.
        mathlib("Mathlib/Data/Fintype/BigOperators.lean#L199", "theorem Fintype.card_fun"),
        # Instance check of the general formula: 23 people and 365 days give a probability below
        # 1/2 (and 22 people above 1/2).
        mathlib(
            "Archive/Wiedijk100Theorems/BirthdayProblem.lean#L49",
            "theorem Theorems100.birthday_measure",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"m": 365, "n": 23},
            expected=0.4927027656760146,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Exact Fraction descending-factorial quotient; below 1/2, as in the source's "
                "instance for 23 people."
            ),
        ),
        VerificationCase(
            inputs={"m": 365, "n": 22},
            expected=0.5243046923374499,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Exact Fraction quotient; above 1/2, as in the source's instance for 22 people.",
        ),
        VerificationCase(
            inputs={"m": 365, "n": 60},
            expected=0.005877339134652057,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Exact Fraction quotient for a small probability.",
        ),
        VerificationCase(
            inputs={"m": 3, "n": 3},
            expected=0.2222222222222222,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Brute-force enumeration of all 27 assignments: 6 injective, so 2/9.",
        ),
        VerificationCase(
            inputs={"m": 5, "n": 3},
            expected=0.48,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Brute-force enumeration of all 125 assignments: 60 injective, so 0.48.",
        ),
        VerificationCase(
            inputs={"m": 3, "n": 4},
            expected=0.0,
            rel_tol=0.0,
            abs_tol=1e-15,
            note="More people than days: brute force finds no injective assignment.",
        ),
        VerificationCase(
            inputs={"m": 4, "n": 0},
            expected=1.0,
            rel_tol=0.0,
            abs_tol=1e-15,
            note="No people: the empty assignment is injective, so P = 1.",
        ),
    ),
    assumptions=(
        "m is the number of equally likely days (or bins), m >= 1, and n the number of people (or "
        "items), n >= 0; both must be whole numbers (integral floats are accepted), otherwise "
        "ValueError is raised.",
        "All m^n assignments are equally likely, i.e. each person independently picks a day "
        "uniformly. For the classical problem m = 365 and leap days or seasonal effects are "
        "ignored.",
        "P = 0.0 for n > m (pigeonhole) and P = 1.0 for n = 0 or n = 1. The probability that at "
        "least two people share a day is 1 - P.",
        "Derived result: Mathlib states the counting probability for functions Fin n -> Fin m and "
        "the counts of embeddings and of functions separately; the formula here assembles them "
        "(distinct assignments are the injective functions). The assembled formula was checked by "
        "enumerating every assignment for small m and n and against the 23/22 instance of the "
        "source.",
        "For n up to 10000 (and m**n below about five million bits) the quotient of exact "
        "integers is rounded once, so the result is correctly rounded. Otherwise an "
        "Euler-Maclaurin series for the logarithm is used; measured: relative error below 2e-13 "
        "against 60+ digit mpmath on 404 (m, n) pairs (the series branch: m from 6.7e4 to 1e40 "
        "with n from 10001 up to the point where the probability underflows, about 38.6*sqrt(m); "
        "and m from 2^600 to 2^100000 with n from 60 to 10000 where m**n exceeds five million "
        "bits). Outside that range accuracy is not characterised. Probabilities below about "
        "5e-324 are returned as 0.0.",
    ),
    tags=(
        "birthday problem",
        "birthday paradox",
        "collision probability",
        "falling factorial",
        "probability",
        "combinatorics",
    ),
)
