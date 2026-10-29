"""Lynxtronics - a toolkit for electrical and electronics engineers.

Sub-modules
-----------
units       SI prefix parsing and engineering-notation formatting
basic       Ohm's law, power, series/parallel networks, dividers
passives    Resistor colour codes, E-series values, RC/RL/LC calculations
ac          RMS, reactance, impedance, power factor, three-phase
power       Voltage drop, cable sizing helpers, transformers, energy cost
filters     RC/RL filters, Butterworth, op-amp stages
semi        LED resistors, zener regulators, BJT bias
digital     Base conversion, two's complement, ADC/DAC, truth tables
signal      DFT, RMS, Nyquist, windowing
embedded    PWM, timer prescalers, baud rate error, pull-up sizing
control     PID controller, first-order and second-order responses
"""

from . import ac, basic, control, digital, embedded, filters, passives, power, semi, signal, units

__version__ = "0.1.0"
__all__ = [
    "__version__",
    "ac",
    "basic",
    "control",
    "digital",
    "embedded",
    "filters",
    "passives",
    "power",
    "semi",
    "signal",
    "units",
]
