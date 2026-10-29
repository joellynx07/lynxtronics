"""Passive filters and op-amp stages."""

from __future__ import annotations

import math


def rc_cutoff(r: float, c: float) -> float:
    """-3 dB cutoff frequency (Hz) of a first-order RC filter."""
    return 1.0 / (2 * math.pi * r * c)


def rc_lowpass_gain(r: float, c: float, f: float) -> float:
    """Magnitude response of an RC low-pass filter at frequency f."""
    return 1.0 / math.sqrt(1 + (f / rc_cutoff(r, c)) ** 2)


def rc_highpass_gain(r: float, c: float, f: float) -> float:
    fc = rc_cutoff(r, c)
    return (f / fc) / math.sqrt(1 + (f / fc) ** 2)


def gain_db(ratio: float) -> float:
    """Voltage ratio to decibels."""
    return 20 * math.log10(ratio)


def db_to_ratio(db: float) -> float:
    return 10 ** (db / 20)


def butterworth_order(fp: float, fs: float, ap_db: float, as_db: float) -> int:
    """Minimum Butterworth low-pass order for passband/stopband specs."""
    num = math.log10((10 ** (as_db / 10) - 1) / (10 ** (ap_db / 10) - 1))
    return math.ceil(num / (2 * math.log10(fs / fp)))


def inverting_gain(rf: float, rin: float) -> float:
    """Closed-loop gain of an inverting op-amp stage."""
    return -rf / rin


def non_inverting_gain(rf: float, rg: float) -> float:
    """Closed-loop gain of a non-inverting op-amp stage."""
    return 1 + rf / rg


def opamp_bandwidth(gbw: float, gain: float) -> float:
    """Closed-loop bandwidth from the gain-bandwidth product."""
    return gbw / abs(gain)


def slew_limited_frequency(slew_rate: float, vpeak: float) -> float:
    """Full-power bandwidth (Hz). slew_rate in V/s."""
    return slew_rate / (2 * math.pi * vpeak)


def rc_for_cutoff(fc: float, c: float) -> float:
    """Resistor value for a desired cutoff with a chosen capacitor."""
    return 1.0 / (2 * math.pi * fc * c)
