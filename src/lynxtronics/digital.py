"""Digital electronics helpers."""

from __future__ import annotations

import itertools
from typing import Callable


def to_base(n: int, base: int) -> str:
    """Integer to string in base 2-36."""
    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if n == 0:
        return "0"
    sign, n = ("-" if n < 0 else ""), abs(n)
    out = []
    while n:
        n, r = divmod(n, base)
        out.append(digits[r])
    return sign + "".join(reversed(out))


def from_base(text: str, base: int) -> int:
    return int(text, base)


def twos_complement(value: int, bits: int) -> str:
    """Two's-complement binary string of a signed integer.

    >>> twos_complement(-5, 8)
    '11111011'
    """
    if not -(1 << (bits - 1)) <= value < (1 << (bits - 1)):
        raise ValueError("Value does not fit in the given bit width")
    return format(value & ((1 << bits) - 1), f"0{bits}b")


def from_twos_complement(text: str) -> int:
    bits = len(text)
    n = int(text, 2)
    return n - (1 << bits) if text[0] == "1" else n


def gray_code(n: int) -> int:
    return n ^ (n >> 1)


def adc_resolution(vref: float, bits: int) -> float:
    """Volts per LSB."""
    return vref / (2 ** bits)


def adc_to_voltage(code: int, vref: float, bits: int) -> float:
    return code * adc_resolution(vref, bits)


def voltage_to_code(v: float, vref: float, bits: int) -> int:
    return min(int(v / adc_resolution(vref, bits)), 2 ** bits - 1)


def snr_ideal(bits: int) -> float:
    """Ideal quantisation SNR in dB."""
    return 6.02 * bits + 1.76


def truth_table(func: Callable[..., bool], n_inputs: int) -> list[tuple]:
    """Truth table of a Python function of n boolean inputs.

    Returns rows of (inputs..., output).
    """
    return [(*bits, int(bool(func(*bits)))) for bits in itertools.product((0, 1), repeat=n_inputs)]


def parity(n: int) -> int:
    """Even parity bit for an integer."""
    return bin(n).count("1") % 2
