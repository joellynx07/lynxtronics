"""Command-line interface: `lynx <command> ...`"""

from __future__ import annotations

import argparse

from . import __version__, basic, filters, passives, power, semi
from .units import fmt, parse


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="lynx", description="Lynxtronics engineering calculators")
    p.add_argument("--version", action="version", version=f"lynxtronics {__version__}")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("ohm", help="Ohm's law: give two of v, i, r (e.g. v=12 r=4.7k)")
    s.add_argument("pairs", nargs=2)

    s = sub.add_parser("parallel", help="Parallel resistance, e.g. lynx parallel 1k 2.2k 4.7k")
    s.add_argument("values", nargs="+")

    s = sub.add_parser("divider", help="Voltage divider: vin r1 r2")
    s.add_argument("vin"), s.add_argument("r1"), s.add_argument("r2")
 
    s = sub.add_parser("led", help="LED resistor: supply vled current")
    s.add_argument("supply"), s.add_argument("vled"), s.add_argument("current")

    s = sub.add_parser("cutoff", help="RC cutoff frequency: r c")
    s.add_argument("r"), s.add_argument("c")

    s = sub.add_parser("resonance", help="LC resonance: l c")
    s.add_argument("l"), s.add_argument("c")

    s = sub.add_parser("color", help="Decode resistor bands, e.g. lynx color brown black red gold")
    s.add_argument("bands", nargs="+")

    s = sub.add_parser("vdrop", help="Voltage drop: current length_m area_mm2")
    s.add_argument("current"), s.add_argument("length"), s.add_argument("area")
    return p


def main(argv: list[str] | None = None) -> None:
    a = _build_parser().parse_args(argv)
    if a.cmd == "ohm":
        kw = {k: parse(v) for k, v in (x.split("=") for x in a.pairs)}
        res = basic.ohms_law(**kw)
        print(f"V = {fmt(res['v'], 'V')}\nI = {fmt(res['i'], 'A')}\n"
              f"R = {fmt(res['r'], 'Ω')}\nP = {fmt(res['p'], 'W')}")
    elif a.cmd == "parallel":
        print(fmt(basic.parallel(parse(v) for v in a.values), "Ω"))
    elif a.cmd == "divider":
        print(fmt(basic.voltage_divider(parse(a.vin), parse(a.r1), parse(a.r2)), "V"))
    elif a.cmd == "led":
        r = semi.led_resistor(parse(a.supply), parse(a.vled), parse(a.current))
        print(f"Exact: {fmt(r['exact'], 'Ω')}  Use: {fmt(r['standard'], 'Ω')}  "
              f"Current: {fmt(r['current'], 'A')}  Power: {fmt(r['power'], 'W')}")
    elif a.cmd == "cutoff":
        print(fmt(filters.rc_cutoff(parse(a.r), parse(a.c)), "Hz"))
    elif a.cmd == "resonance":
        print(fmt(passives.resonant_frequency(parse(a.l), parse(a.c)), "Hz"))
    elif a.cmd == "color":
        ohms, tol = passives.decode_resistor(a.bands)
        print(f"{fmt(ohms, 'Ω')} ±{tol}%")
    elif a.cmd == "vdrop":
        d = power.voltage_drop(parse(a.current), parse(a.length), parse(a.area))
        print(fmt(d, "V"))


if __name__ == "__main__":
    main()
