"""SI prefix parsing and engineering-notation formatting."""

from __future__ import annotations

import math
import re

_PREFIXES = {
    "p": 1e-12, "n": 1e-9, "u": 1e-6, "µ": 1e-6, "m": 1e-3,
    "": 1.0, "k": 1e3, "K": 1e3, "M": 1e6, "G": 1e9, "T": 1e12,
}
_FORMAT_PREFIXES = {
    -12: "p", -9: "n", -6: "µ", -3: "m", 0: "", 3: "k", 6: "M", 9: "G", 12: "T",
}
_PATTERN = re.compile(r"^\s*([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)\s*([pnuµmkKMGT]?)\s*[A-Za-zΩ]*\s*$")


def parse(value: str | float) -> float:
    """Convert '4.7k', '100n', '2.2uF' or a number to a float in base units.

    >>> parse("4.7k")
    4700.0
    >>> parse("100nF")
    1e-07
    """
    if isinstance(value, (int, float)):
        return float(value)
    match = _PATTERN.match(value)
    if not match:
        raise ValueError(f"Cannot parse value: {value!r}")
    number, prefix = match.groups()
    return float(number) * _PREFIXES[prefix]


def fmt(value: float, unit: str = "", digits: int = 3) -> str:
    """Format a number in engineering notation with an SI prefix.

    >>> fmt(4700, "Ω")
    '4.7 kΩ'
    >>> fmt(0.000001, "F")
    '1 µF'
    """
    if value == 0:
        return f"0 {unit}".strip()
    exponent = int(math.floor(math.log10(abs(value)) / 3) * 3)
    exponent = max(-12, min(12, exponent))
    scaled = value / (10 ** exponent)
    text = f"{scaled:.{digits}g}"
    return f"{text} {_FORMAT_PREFIXES[exponent]}{unit}".strip()
