"""AC circuit analysis and three-phase relations."""

from __future__ import annotations

import cmath
import math


def rms_sine(peak: float) -> float:
    """RMS value of a sine wave from its peak."""
    return peak / math.sqrt(2)


def peak_from_rms(rms: float) -> float:
    return rms * math.sqrt(2)


def impedance_series_rlc(r: float, l: float, c: float, f: float) -> complex:
    """Complex impedance of a series RLC network."""
    w = 2 * math.pi * f
    return complex(r, w * l - 1.0 / (w * c))


def impedance_parallel(*z: complex) -> complex:
    """Equivalent impedance of parallel complex impedances."""
    return 1.0 / sum(1.0 / x for x in z)


def polar(z: complex) -> tuple[float, float]:
    """(magnitude, angle in degrees)."""
    return abs(z), math.degrees(cmath.phase(z))


def power_triangle(v_rms: float, i_rms: float, phi_deg: float) -> dict:
    """Real (W), reactive (VAR), apparent (VA) power and power factor."""
    phi = math.radians(phi_deg)
    s = v_rms * i_rms
    return {"P": s * math.cos(phi), "Q": s * math.sin(phi), "S": s, "pf": math.cos(phi)}


def pf_correction_capacitor(p: float, pf_old: float, pf_new: float, v: float, f: float = 50) -> float:
    """Capacitance (F) needed to raise power factor from pf_old to pf_new.

    p is real power in watts, v is the RMS line voltage across the capacitor.
    """
    q_old = p * math.tan(math.acos(pf_old))
    q_new = p * math.tan(math.acos(pf_new))
    return (q_old - q_new) / (2 * math.pi * f * v ** 2)


def three_phase_power(v_line: float, i_line: float, pf: float = 1.0) -> dict:
    """Balanced three-phase real, reactive and apparent power."""
    s = math.sqrt(3) * v_line * i_line
    return {"P": s * pf, "Q": s * math.sqrt(1 - pf ** 2), "S": s}


def line_to_phase_voltage(v_line: float) -> float:
    """Phase voltage of a star-connected balanced system."""
    return v_line / math.sqrt(3)


def synchronous_speed(f: float, poles: int) -> float:
    """Synchronous speed of an AC machine in rpm."""
    return 120 * f / poles


def slip(n_sync: float, n_rotor: float) -> float:
    """Induction machine slip as a fraction."""
    return (n_sync - n_rotor) / n_sync
