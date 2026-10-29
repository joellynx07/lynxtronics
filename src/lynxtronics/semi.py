"""Semiconductor design helpers."""

from __future__ import annotations

from .passives import nearest_standard


def led_resistor(v_supply: float, v_led: float, i_led: float, series: str = "E24") -> dict:
    """Current-limiting resistor for an LED.

    Returns the exact value, the nearest standard value and its power dissipation.
    """
    exact = (v_supply - v_led) / i_led
    std = nearest_standard(exact, series)
    actual_i = (v_supply - v_led) / std
    return {"exact": exact, "standard": std, "current": actual_i, "power": actual_i ** 2 * std}


def zener_resistor(v_in: float, v_z: float, i_load: float, i_zener_min: float = 0.005) -> dict:
    """Series resistor for a zener shunt regulator."""
    r = (v_in - v_z) / (i_load + i_zener_min)
    return {"resistor": r, "power_resistor": ((v_in - v_z) ** 2) / r,
            "power_zener": v_z * i_zener_min}


def bjt_switch_base_resistor(v_drive: float, i_collector: float, beta: float = 100,
                             vbe: float = 0.7, overdrive: float = 5) -> float:
    """Base resistor to saturate a BJT used as a switch."""
    i_base = i_collector / beta * overdrive
    return (v_drive - vbe) / i_base


def mosfet_dissipation(i_d: float, rds_on: float) -> float:
    """Conduction loss of a MOSFET in watts."""
    return i_d ** 2 * rds_on


def diode_bridge_dc(v_rms: float, v_diode: float = 0.7) -> float:
    """Peak DC output of a full-wave bridge rectifier."""
    return v_rms * 2 ** 0.5 - 2 * v_diode


def ripple_voltage(i_load: float, f_line: float, c: float) -> float:
    """Approximate ripple of a full-wave rectifier with a reservoir capacitor."""
    return i_load / (2 * f_line * c)


def heatsink_required(p_diss: float, t_junction_max: float, t_ambient: float,
                      r_jc: float, r_cs: float = 0.5) -> float:
    """Maximum heatsink-to-ambient thermal resistance (C/W)."""
    return (t_junction_max - t_ambient) / p_diss - r_jc - r_cs


def linear_regulator_loss(v_in: float, v_out: float, i_load: float) -> float:
    """Power wasted as heat in a linear regulator."""
    return (v_in - v_out) * i_load
