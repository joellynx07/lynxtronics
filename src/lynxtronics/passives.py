"""Resistor colour codes, standard value series and reactive component maths."""

from __future__ import annotations

import math

_COLORS = ["black", "brown", "red", "orange", "yellow", "green", "blue", "violet", "grey", "white"]
_MULT = {**{c: 10 ** i for i, c in enumerate(_COLORS)}, "gold": 0.1, "silver": 0.01}
_TOL = {"brown": 1, "red": 2, "green": 0.5, "blue": 0.25, "violet": 0.1, "grey": 0.05,
        "gold": 5, "silver": 10}

E12 = [1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2]
E24 = [1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.2, 2.4, 2.7, 3.0,
       3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1]


def decode_resistor(bands: list[str]) -> tuple[float, float]:
    """Decode a 4- or 5-band resistor. Returns (ohms, tolerance_percent).

    >>> decode_resistor(["brown", "black", "red", "gold"])
    (1000.0, 5)
    """
    bands = [b.lower() for b in bands]
    if len(bands) == 4:
        digits, mult, tol = bands[:2], bands[2], bands[3]
    elif len(bands) == 5:
        digits, mult, tol = bands[:3], bands[3], bands[4]
    else:
        raise ValueError("Use 4 or 5 bands")
    number = int("".join(str(_COLORS.index(d)) for d in digits))
    return float(number * _MULT[mult]), _TOL[tol]


def encode_resistor(ohms: float, tolerance: float = 5) -> list[str]:
    """Return 4-band colours for a resistance (two significant digits)."""
    if ohms <= 0:
        raise ValueError("Resistance must be positive")
    exp = math.floor(math.log10(ohms)) - 1
    sig = round(ohms / 10 ** exp)
    if sig >= 100:
        sig //= 10
        exp += 1
    tol_name = next(k for k, v in _TOL.items() if v == tolerance)
    mult_name = next(k for k, v in _MULT.items() if math.isclose(v, 10 ** exp))
    return [_COLORS[sig // 10], _COLORS[sig % 10], mult_name, tol_name]


def nearest_standard(value: float, series: str = "E24") -> float:
    """Nearest preferred value from E12 or E24.

    >>> nearest_standard(4300, "E12")
    4700.0
    """
    table = {"E12": E12, "E24": E24}[series.upper()]
    decade = 10 ** math.floor(math.log10(value))
    candidates = [m * decade * f for m in table for f in (1,)] + [10 * decade]
    return float(min(candidates, key=lambda c: abs(math.log(c / value))))


def reactance_c(c: float, f: float) -> float:
    """Capacitive reactance Xc in ohms."""
    return 1.0 / (2 * math.pi * f * c)


def reactance_l(l: float, f: float) -> float:
    """Inductive reactance Xl in ohms."""
    return 2 * math.pi * f * l


def time_constant_rc(r: float, c: float) -> float:
    """RC time constant in seconds."""
    return r * c


def time_constant_rl(r: float, l: float) -> float:
    """RL time constant in seconds."""
    return l / r


def rc_charge_voltage(vs: float, r: float, c: float, t: float) -> float:
    """Capacitor voltage after time t when charging through R."""
    return vs * (1 - math.exp(-t / (r * c)))


def resonant_frequency(l: float, c: float) -> float:
    """LC resonant frequency in Hz."""
    return 1.0 / (2 * math.pi * math.sqrt(l * c))


def q_factor_series(r: float, l: float, c: float) -> float:
    """Quality factor of a series RLC circuit."""
    return math.sqrt(l / c) / r


def inductor_energy(l: float, i: float) -> float:
    """Energy stored in an inductor in joules."""
    return 0.5 * l * i ** 2


def capacitor_energy(c: float, v: float) -> float:
    """Energy stored in a capacitor in joules."""
    return 0.5 * c * v ** 2
