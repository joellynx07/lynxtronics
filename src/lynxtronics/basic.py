"""Fundamental DC circuit relations."""

from __future__ import annotations

from collections.abc import Iterable


def ohms_law(v: float | None = None, i: float | None = None, r: float | None = None) -> dict:
    """Solve Ohm's law given any two of voltage (V), current (A), resistance (ohm).

    >>> ohms_law(v=12, r=4)["i"]
    3.0
    """
    given = [x is not None for x in (v, i, r)]
    if sum(given) != 2:
        raise ValueError("Provide exactly two of v, i, r")
    if v is None:
        v = i * r
    elif i is None:
        i = v / r
    else:
        r = v / i
    return {"v": v, "i": i, "r": r, "p": v * i}


def power(v: float | None = None, i: float | None = None, r: float | None = None) -> float:
    """Electrical power in watts from any two of v, i, r."""
    return ohms_law(v=v, i=i, r=r)["p"]


def series(values: Iterable[float]) -> float:
    """Total resistance (or inductance) of elements in series."""
    return float(sum(values))


def parallel(values: Iterable[float]) -> float:
    """Total resistance (or inductance) of elements in parallel.

    >>> parallel([100, 100])
    50.0
    """
    values = list(values)
    if not values:
        raise ValueError("Need at least one value")
    if any(v == 0 for v in values):
        return 0.0
    return 1.0 / sum(1.0 / v for v in values)


def cap_series(values: Iterable[float]) -> float:
    """Total capacitance of capacitors in series."""
    return parallel(values)


def cap_parallel(values: Iterable[float]) -> float:
    """Total capacitance of capacitors in parallel."""
    return series(values)


def voltage_divider(vin: float, r1: float, r2: float) -> float:
    """Output voltage of a resistive divider (r2 is the bottom resistor)."""
    return vin * r2 / (r1 + r2)


def current_divider(i_total: float, r1: float, r2: float) -> tuple[float, float]:
    """Branch currents (i1, i2) for two parallel resistors."""
    return i_total * r2 / (r1 + r2), i_total * r1 / (r1 + r2)


def thevenin_divider(vin: float, r1: float, r2: float) -> tuple[float, float]:
    """Thevenin equivalent (Vth, Rth) seen at a divider output."""
    return voltage_divider(vin, r1, r2), parallel([r1, r2])


def max_power_transfer(vth: float, rth: float) -> tuple[float, float]:
    """Load resistance and power for maximum power transfer."""
    return rth, vth ** 2 / (4 * rth)
