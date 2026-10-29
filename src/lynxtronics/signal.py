"""Small, dependency-free signal processing helpers."""

from __future__ import annotations

import cmath
import math
from collections.abc import Sequence


def rms(samples: Sequence[float]) -> float:
    """Root-mean-square of a sampled signal."""
    return math.sqrt(sum(x * x for x in samples) / len(samples))


def mean(samples: Sequence[float]) -> float:
    return sum(samples) / len(samples)


def sine_wave(freq: float, fs: float, n: int, amplitude: float = 1.0, phase: float = 0.0) -> list[float]:
    """Generate n samples of a sine wave."""
    return [amplitude * math.sin(2 * math.pi * freq * k / fs + phase) for k in range(n)]


def nyquist(fs: float) -> float:
    """Nyquist frequency for a sampling rate."""
    return fs / 2


def min_sampling_rate(f_max: float, margin: float = 2.5) -> float:
    """Practical minimum sampling rate for a signal bandwidth."""
    return margin * f_max


def hann(n: int) -> list[float]:
    """Hann window coefficients."""
    return [0.5 - 0.5 * math.cos(2 * math.pi * k / (n - 1)) for k in range(n)]


def dft(samples: Sequence[float]) -> list[complex]:
    """Naive O(n^2) discrete Fourier transform."""
    n = len(samples)
    return [sum(samples[t] * cmath.exp(-2j * math.pi * k * t / n) for t in range(n)) for k in range(n)]


def spectrum(samples: Sequence[float], fs: float) -> list[tuple[float, float]]:
    """Single-sided amplitude spectrum as (frequency, amplitude) pairs."""
    n = len(samples)
    x = dft(samples)
    return [(k * fs / n, (1 if k in (0, n // 2) else 2) * abs(x[k]) / n) for k in range(n // 2 + 1)]


def dominant_frequency(samples: Sequence[float], fs: float) -> float:
    """Frequency (Hz) of the strongest non-DC component."""
    spec = spectrum(samples, fs)
    return max(spec[1:], key=lambda p: p[1])[0]


def moving_average(samples: Sequence[float], window: int) -> list[float]:
    """Simple moving average filter."""
    out = []
    for i in range(len(samples)):
        chunk = samples[max(0, i - window + 1): i + 1]
        out.append(sum(chunk) / len(chunk))
    return out


def thd(fundamental: float, harmonics: Sequence[float]) -> float:
    """Total harmonic distortion as a fraction."""
    return math.sqrt(sum(h * h for h in harmonics)) / fundamental
