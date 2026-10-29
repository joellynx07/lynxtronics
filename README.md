# Lynxtronics

[![CI](https://github.com/joellynx07/lynxtronics/actions/workflows/ci.yml/badge.svg)](https://github.com/joellynx07/lynxtronics/actions)
[![PyPI](https://img.shields.io/pypi/v/lynxtronics.svg)](https://pypi.org/project/lynxtronics/)
[![Python](https://img.shields.io/pypi/pyversions/lynxtronics.svg)](https://pypi.org/project/lynxtronics/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

**A pure-Python toolkit for electrical and electronics engineers.** Zero dependencies, fully tested,
usable as a library or from the command line.

```bash
pip install lynxtronics
```

## Why Lynxtronics?

Engineers repeat the same calculations every day: resistor values, filter cutoffs, cable sizes,
timer prescalers. Lynxtronics puts them in one importable, documented, tested package.

| Module | What it covers |
|---|---|
| `units` | Parse `4.7k`, `100nF`; format results in engineering notation |
| `basic` | Ohm's law, series/parallel, dividers, Thevenin, max power transfer |
| `passives` | Resistor colour codes, E12/E24 values, reactance, RC/RL/LC, resonance, Q |
| `ac` | RMS, complex impedance, power triangle, power factor correction, three-phase, motor slip |
| `power` | Voltage drop, cable sizing, breaker selection, transformers, energy cost, battery, solar |
| `filters` | RC filters, Butterworth order, op-amp gain and bandwidth, slew rate |
| `semi` | LED resistors, zener regulators, BJT/MOSFET, rectifier ripple, heatsinks |
| `digital` | Base conversion, two's complement, Gray code, ADC/DAC, truth tables |
| `signal` | DFT, spectrum, windowing, moving average, THD, Nyquist |
| `embedded` | PWM, timer prescaler search, UART baud error, I2C pull-ups, NTC thermistor, battery life |
| `control` | PID with anti-windup, step responses, Ziegler-Nichols, loop simulation |

## Quick start

```python
from lynxtronics import basic, filters, semi, embedded
from lynxtronics.units import parse, fmt

# Resistor for a 2 V, 20 mA LED on 5 V
print(semi.led_resistor(5, 2, 0.02))

# RC low-pass cutoff
fc = filters.rc_cutoff(parse("10k"), parse("100nF"))
print(fmt(fc, "Hz"))          # 159 Hz

# 1 kHz timer interrupt on a 16 MHz MCU
print(embedded.timer_settings(16_000_000, 1000))

# PID loop simulation
from lynxtronics.control import PID, simulate_first_order
trace = simulate_first_order(PID(2, 5, 0), k=1, tau=0.5, setpoint=1.0)
```

## Command line

```bash
lynx ohm v=12 r=4.7k
lynx parallel 1k 2.2k 4.7k
lynx divider 12 10k 4.7k
lynx led 5 2 20m
lynx cutoff 10k 100n
lynx resonance 10m 100n
lynx color brown black red gold
lynx vdrop 16 30 2.5
```

## Safety note

Installation helpers in `lynxtronics.power` are first-pass estimates. Always follow your local
wiring regulations and have electrical installations verified by a qualified person.

## Development

```bash
git clone https://github.com/joellynx07/lynxtronics
cd lynxtronics
pip install -e ".[dev]"
pytest
ruff check .
```

## Roadmap

- [ ] Smith chart and transmission-line helpers
- [ ] SPICE netlist generator
- [ ] Optional matplotlib plots (Bode, step response)
- [ ] Battery pack and solar sizing wizards
- [ ] Sphinx documentation site

## Contributing

Pull requests are welcome. Add tests for every new function and keep the package dependency-free.

## License

MIT © Joel Judiah Amoah
