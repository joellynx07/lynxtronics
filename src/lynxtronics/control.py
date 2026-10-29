"""Control-systems helpers."""

from __future__ import annotations

import math


class PID:
    """Discrete PID controller with output clamping and anti-windup.

    >>> pid = PID(kp=2.0, ki=0.5, kd=0.1, out_min=-10, out_max=10)
    >>> round(pid.update(setpoint=1.0, measurement=0.0, dt=0.1), 3)
    2.05
    """

    def __init__(self, kp: float, ki: float = 0.0, kd: float = 0.0,
                 out_min: float = float("-inf"), out_max: float = float("inf")):
        self.kp, self.ki, self.kd = kp, ki, kd
        self.out_min, self.out_max = out_min, out_max
        self._integral = 0.0
        self._prev_error: float | None = None

    def reset(self) -> None:
        self._integral = 0.0
        self._prev_error = None

    def update(self, setpoint: float, measurement: float, dt: float) -> float:
        error = setpoint - measurement
        derivative = 0.0 if self._prev_error is None else (error - self._prev_error) / dt
        candidate = self._integral + error * dt
        output = self.kp * error + self.ki * candidate + self.kd * derivative
        if self.out_min <= output <= self.out_max:
            self._integral = candidate  # only integrate when not saturated
        self._prev_error = error
        return max(self.out_min, min(self.out_max, output))


def first_order_step(k: float, tau: float, t: float) -> float:
    """Step response of K/(tau*s + 1) at time t."""
    return k * (1 - math.exp(-t / tau))


def settling_time_first_order(tau: float, band: float = 0.02) -> float:
    """Time for a first-order system to settle within +/- band."""
    return -tau * math.log(band)


def second_order_params(wn: float, zeta: float) -> dict:
    """Overshoot, peak time and settling time of an underdamped second-order system."""
    if not 0 < zeta < 1:
        raise ValueError("Formulas apply to underdamped systems (0 < zeta < 1)")
    wd = wn * math.sqrt(1 - zeta ** 2)
    return {
        "overshoot_pct": 100 * math.exp(-math.pi * zeta / math.sqrt(1 - zeta ** 2)),
        "peak_time": math.pi / wd,
        "settling_time_2pct": 4 / (zeta * wn),
    }


def ziegler_nichols_pid(ku: float, tu: float) -> dict:
    """Classic Ziegler-Nichols PID gains from ultimate gain and period."""
    kp = 0.6 * ku
    return {"kp": kp, "ki": 2 * kp / tu, "kd": kp * tu / 8}


def simulate_first_order(pid: PID, k: float, tau: float, setpoint: float,
                         dt: float = 0.01, steps: int = 500) -> list[float]:
    """Simulate a PID loop around a first-order plant. Returns the output trace."""
    y, trace = 0.0, []
    for _ in range(steps):
        u = pid.update(setpoint, y, dt)
        y += dt * (-y + k * u) / tau
        trace.append(y)
    return trace
