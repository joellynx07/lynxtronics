"""Microcontroller and embedded-systems calculators."""

from __future__ import annotations


def pwm_duty(on_time: float, period: float) -> float:
    """Duty cycle as a percentage."""
    return 100 * on_time / period


def pwm_average_voltage(vcc: float, duty_pct: float) -> float:
    return vcc * duty_pct / 100


def timer_settings(f_cpu: float, f_target: float, timer_bits: int = 16,
                   prescalers: tuple = (1, 8, 64, 256, 1024)) -> dict:
    """Find prescaler and compare value for a periodic timer interrupt.

    Picks the combination with the smallest frequency error.
    """
    best = None
    for p in prescalers:
        ocr = round(f_cpu / (p * f_target)) - 1
        if 0 <= ocr < 2 ** timer_bits:
            actual = f_cpu / (p * (ocr + 1))
            err = abs(actual - f_target) / f_target * 100
            if best is None or err < best["error_pct"]:
                best = {"prescaler": p, "compare": ocr, "actual_hz": actual, "error_pct": err}
    if best is None:
        raise ValueError("No prescaler fits; widen the options or use a bigger timer")
    return best


def uart_baud_error(f_cpu: float, baud: int, oversample: int = 16) -> dict:
    """UBRR value and percentage error for an AVR-style UART divider."""
    ubrr = round(f_cpu / (oversample * baud)) - 1
    actual = f_cpu / (oversample * (ubrr + 1))
    return {"ubrr": ubrr, "actual_baud": actual, "error_pct": (actual - baud) / baud * 100}


def i2c_pullup_range(vcc: float, bus_capacitance: float, rise_time: float = 1e-6,
                     i_sink: float = 3e-3, v_ol: float = 0.4) -> tuple[float, float]:
    """(min, max) pull-up resistor for an I2C bus. Defaults suit 400 kHz fast mode."""
    r_min = (vcc - v_ol) / i_sink
    r_max = rise_time / (0.8473 * bus_capacitance)
    return r_min, r_max


def adc_counts_to_temperature_ntc(counts: int, bits: int, r_fixed: float, r0: float,
                                  t0_c: float, beta: float) -> float:
    """Temperature (C) from an NTC thermistor divider (thermistor on the low side)."""
    import math
    full = 2 ** bits
    r_ntc = r_fixed * counts / (full - counts)
    t0 = t0_c + 273.15
    inv_t = 1 / t0 + math.log(r_ntc / r0) / beta
    return 1 / inv_t - 273.15


def spi_transfer_time(bytes_count: int, clock_hz: float) -> float:
    """Time in seconds to shift a number of bytes over SPI."""
    return bytes_count * 8 / clock_hz


def battery_life_hours(capacity_mah: float, active_ma: float, sleep_ua: float,
                       duty_cycle: float) -> float:
    """Battery life of a duty-cycled device in hours."""
    avg_ma = active_ma * duty_cycle + (sleep_ua / 1000) * (1 - duty_cycle)
    return capacity_mah / avg_ma


def debounce_samples(bounce_ms: float, sample_period_ms: float) -> int:
    """Number of consecutive equal samples needed to debounce a button."""
    return int(bounce_ms / sample_period_ms) + 1
