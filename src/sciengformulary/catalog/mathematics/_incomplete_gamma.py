"""Series and continued-fraction kernels shared by the incomplete gamma formulas."""

import math

# Iteration cap for the series and the continued fraction; reaching it raises ArithmeticError.
MAX_ITERATIONS = 10_000
_EPSILON = 1e-17
# Lentz guard against a zero denominator.
_TINY = 1e-300


def gamma_series_sum(s: float, x: float) -> float:
    """Return sum_{k>=0} x^k / (s (s + 1) ... (s + k)), so gamma(s, x) = x^s e^(-x) * sum.

    Converges quickly for x < s + 1 because every term ratio x / (s + k) is below 1 there.
    """
    term = 1.0 / s
    total = term
    for n in range(1, MAX_ITERATIONS + 1):
        term *= x / (s + n)
        total += term
        if term < total * _EPSILON:
            return total
    raise ArithmeticError(
        f"incomplete gamma series did not converge in {MAX_ITERATIONS} terms (s={s!r}, x={x!r})."
    )


def gamma_continued_fraction(s: float, x: float) -> float:
    """Return the continued fraction F with Gamma(s, x) = x^s e^(-x) * F (x > 0).

    F = 1 / (x + 1 - s - 1 (1 - s) / (x + 3 - s - 2 (2 - s) / (x + 5 - s - ...))), evaluated
    with the modified Lentz method. It converges quickly for x >= s + 1.
    """
    # (x - s) is exact when x and s are close, which is where x + 1 - s would lose the 1.
    b = (x - s) + 1.0
    if b == 0.0:
        raise ArithmeticError(
            f"incomplete gamma continued fraction is degenerate (s={s!r}, x={x!r})."
        )
    c = 1.0 / _TINY
    d = 1.0 / b
    value = d
    for n in range(1, MAX_ITERATIONS + 1):
        a = -n * (n - s)
        b += 2.0
        d = a * d + b
        if abs(d) < _TINY:
            d = _TINY
        c = b + a / c
        if abs(c) < _TINY:
            c = _TINY
        d = 1.0 / d
        delta = d * c
        value *= delta
        if abs(delta - 1.0) < _EPSILON:
            return value
    raise ArithmeticError(
        "incomplete gamma continued fraction did not converge in "
        f"{MAX_ITERATIONS} terms (s={s!r}, x={x!r})."
    )


# Euler-Mascheroni constant.
_EULER_GAMMA = 0.57721566490153286061
# Bernoulli numbers B_2 ... B_12, for the Euler-Maclaurin tail of the zeta sums below.
_BERNOULLI = (1 / 6, -1 / 30, 1 / 42, -1 / 30, 5 / 66, -691 / 2730)
_ZETA_CUTOFF = 20
_ZETA_ORDERS = 64
# The log-gamma series below is used only for shapes below this value.
SMALL_SHAPE_LIMIT = 0.5
# Below this shape exp(s * y) - 1 equals s * y to double precision for every |y| <= 745.
_TINY_SHAPE = 1e-100


def _zeta(order: int) -> float:
    """Return the Riemann zeta function at an integer ``order`` >= 2.

    The first terms are summed directly and the rest of the series is added by the
    Euler-Maclaurin formula (Bernoulli terms up to B_12); the error is below 1e-19.
    """
    total = 1.0 + sum(n**-order for n in range(2, _ZETA_CUTOFF))
    n = float(_ZETA_CUTOFF)
    total += n ** (1 - order) / (order - 1) + 0.5 * n**-order
    rising = float(order)  # order * (order + 1) * ... * (order + 2j - 2)
    factorial = 2.0  # (2j)!
    for j, bernoulli in enumerate(_BERNOULLI, start=1):
        total += bernoulli / factorial * rising * n ** (-order - 2 * j + 1)
        rising *= (order + 2 * j - 1) * (order + 2 * j)
        factorial *= (2 * j + 1) * (2 * j + 2)
    return total


_ZETA_VALUES = tuple(_zeta(order) for order in range(2, _ZETA_ORDERS + 1))


def _log_gamma_one_plus_per_shape(s: float) -> float:
    """Return ln Gamma(1 + s) / s for 0 < s <= 0.5, as -gamma + sum zeta(k) (-1)^k s^(k-1) / k.

    Evaluated term by term in the shape itself, so the small value ln Gamma(1 + s) is never
    obtained by rounding 1 + s (which would lose its leading digits when s is small).
    """
    total = -_EULER_GAMMA
    power = s
    sign = 1.0
    for order, zeta in enumerate(_ZETA_VALUES, start=2):
        total += sign * zeta * power / order
        power *= s
        sign = -sign
        if power < 1e-22:
            break
    return total


def _expm1_per_shape(s: float, y: float) -> float:
    """Return (exp(s * y) - 1) / s without losing digits for small s (|y| <= 745 or so)."""
    if s < _TINY_SHAPE:
        return y
    return math.expm1(s * y) / s


def small_shape_upper_gamma(s: float, x: float) -> float:
    """Return Gamma(s, x) for 0 < s < 1 and 0 < x < 1 without cancellation.

    Gamma(s, x) = Gamma(s) - x^s / s - x^s * sum_{k>=1} (-x)^k / (k! (s + k)), and
    Gamma(s) - x^s / s = ((Gamma(1 + s) - 1) - (x^s - 1)) / s is evaluated as
    (Gamma(1 + s) - 1) / s - expm1(s ln x) / s, each of the two parts accurate to rounding.
    For x below 1/4 their difference is at least about 0.8, whatever s is, so nothing
    cancels. Raises ArithmeticError if the result is not positive.
    """
    log_x = math.log(x)
    if s < SMALL_SHAPE_LIMIT:
        gamma_part = _expm1_per_shape(s, _log_gamma_one_plus_per_shape(s))
    else:
        gamma_part = (math.gamma(1.0 + s) - 1.0) / s
    power_part = _expm1_per_shape(s, log_x)
    term = 1.0
    tail = 0.0
    for k in range(1, 40):
        term *= -x / k
        tail += term / (s + k)
        if abs(term) < 1e-20:
            break
    result = gamma_part - power_part - math.exp(s * log_x) * tail
    if not result > 0.0:
        raise ArithmeticError(f"incomplete gamma evaluation failed (s={s!r}, x={x!r}).")
    return result


def exp_in_range(exponent: float) -> float:
    """Return exp(exponent), raising OverflowError with a clear message above the float range."""
    try:
        return math.exp(exponent)
    except OverflowError as error:
        raise OverflowError("the result is outside the floating-point range.") from error


def gamma_in_range(s: float) -> float:
    """Return Gamma(s), raising OverflowError with a clear message above the float range."""
    try:
        return math.gamma(s)
    except OverflowError as error:
        raise OverflowError(
            f"Gamma({s!r}) is outside the floating-point range, so the result is too."
        ) from error
