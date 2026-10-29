"""Practical electrical-installation helpers.

These are first-pass engineering estimates. Always follow your local wiring
regulations and have installations checked by a qualified person.
"""

from __future__ import annotations

import math

# Resistivity at 20 C in ohm*m
RESISTIVITY = {"copper": 1.68e-8, "aluminium": 2.82e-8}

STANDARD_BREAKERS = [6, 10, 13, 16, 20, 25, 32, 40, 50, 63, 80, 100, 125]


def wire_resistance(length_m: float, area_mm2: float, material: str = "copper") -> float:
    """Resistance (ohm) of a conductor of given length and cross-section."""
    return RESISTIVITY[material] * length_m / (area_mm2 * 1e-6)


def voltage_drop(current: float, length_m: float, area_mm2: float,
                 material: str = "copper", phases: int = 1) -> float:
    """Voltage drop (V) over a cable run. length_m is the one-way length."""
    r = wire_resistance(length_m, area_mm2, material)
    factor = 2 if phases == 1 else math.sqrt(3)
    return factor * current * r


def min_cable_area(current: float, length_m: float, v_supply: float, max_drop_pct: float = 3,
                   material: str = "copper", phases: int = 1) -> float:
    """Smallest cross-section (mm^2) keeping voltage drop under a percentage."""
    max_drop = v_supply * max_drop_pct / 100
    factor = 2 if phases == 1 else math.sqrt(3)
    return factor * current * RESISTIVITY[material] * length_m / (max_drop * 1e-6)


def breaker_size(load_current: float, margin: float = 1.25) -> int:
    """Pick the next standard breaker rating above load_current * margin."""
    needed = load_current * margin
    for rating in STANDARD_BREAKERS:
        if rating >= needed:
            return rating
    raise ValueError("Load exceeds the standard breaker table")


def load_current(power_w: float, voltage: float, pf: float = 1.0, phases: int = 1) -> float:
    """Line current for a given real power."""
    if phases == 1:
        return power_w / (voltage * pf)
    return power_w / (math.sqrt(3) * voltage * pf)


def transformer_currents(kva: float, v_primary: float, v_secondary: float, phases: int = 1) -> tuple:
    """Full-load (primary, secondary) currents of a transformer."""
    k = 1 if phases == 1 else math.sqrt(3)
    return kva * 1000 / (k * v_primary), kva * 1000 / (k * v_secondary)


def transformer_efficiency(p_out: float, core_loss: float, copper_loss: float) -> float:
    """Efficiency as a fraction."""
    return p_out / (p_out + core_loss + copper_loss)


def energy_cost(power_w: float, hours: float, tariff_per_kwh: float) -> float:
    """Cost of running a load for a number of hours."""
    return power_w / 1000 * hours * tariff_per_kwh


def battery_runtime(capacity_ah: float, voltage: float, load_w: float,
                    efficiency: float = 0.85, depth_of_discharge: float = 0.8) -> float:
    """Estimated battery or UPS runtime in hours."""
    usable_wh = capacity_ah * voltage * efficiency * depth_of_discharge
    return usable_wh / load_w


def solar_array_size(daily_kwh: float, sun_hours: float, system_efficiency: float = 0.75) -> float:
    """Required PV array size in kWp."""
    return daily_kwh / (sun_hours * system_efficiency)
