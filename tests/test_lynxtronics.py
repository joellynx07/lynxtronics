import math

import pytest

from lynxtronics import (
    ac,
    basic,
    control,
    digital,
    embedded,
    filters,
    passives,
    power,
    semi,
    signal,
)
from lynxtronics.units import fmt, parse


def test_parse_and_fmt():
    assert parse("4.7k") == 4700
    assert math.isclose(parse("100nF"), 1e-7)
    assert parse(5) == 5.0
    assert fmt(4700, "Ω") == "4.7 kΩ"
    assert fmt(0.000001, "F") == "1 µF"
    with pytest.raises(ValueError):
        parse("abc")


def test_ohms_law():
    r = basic.ohms_law(v=12, r=4)
    assert r["i"] == 3 and r["p"] == 36
    with pytest.raises(ValueError):
        basic.ohms_law(v=1)


def test_networks():
    assert basic.parallel([100, 100]) == 50
    assert basic.series([1, 2, 3]) == 6
    assert basic.voltage_divider(10, 1000, 1000) == 5
    assert basic.max_power_transfer(10, 5) == (5, 5.0)


def test_resistor_codes():
    assert passives.decode_resistor(["brown", "black", "red", "gold"]) == (1000.0, 5)
    assert passives.decode_resistor(["yellow", "violet", "black", "black", "brown"]) == (470.0, 1)
    assert passives.encode_resistor(4700) == ["yellow", "violet", "red", "gold"]
    assert passives.nearest_standard(4300, "E12") == 4700


def test_reactive():
    assert math.isclose(passives.resonant_frequency(1e-3, 1e-6), 5032.9, rel_tol=1e-3)
    assert math.isclose(passives.reactance_c(1e-6, 1000), 159.15, rel_tol=1e-3)
    assert math.isclose(passives.time_constant_rc(1e3, 1e-6), 1e-3)


def test_ac():
    assert math.isclose(ac.rms_sine(325.27), 230, rel_tol=1e-3)
    p = ac.power_triangle(230, 10, 0)
    assert p["P"] == 2300 and p["Q"] == 0
    assert ac.synchronous_speed(50, 4) == 1500
    assert math.isclose(ac.slip(1500, 1440), 0.04)
    assert ac.pf_correction_capacitor(10_000, 0.7, 0.95, 230) > 0


def test_power():
    assert power.breaker_size(14) == 20
    assert math.isclose(power.voltage_drop(10, 20, 2.5), 2 * 10 * 1.68e-8 * 20 / 2.5e-6)
    assert power.min_cable_area(16, 30, 230) > 0
    assert math.isclose(power.energy_cost(1000, 5, 1.2), 6.0)


def test_filters():
    assert math.isclose(filters.rc_cutoff(1000, 1e-6), 159.15, rel_tol=1e-3)
    assert math.isclose(filters.rc_lowpass_gain(1000, 1e-6, 159.15), 0.7071, rel_tol=1e-3)
    assert filters.inverting_gain(10e3, 1e3) == -10
    assert filters.non_inverting_gain(9e3, 1e3) == 10
    assert filters.butterworth_order(1000, 2000, 3, 40) == 7


def test_semi():
    r = semi.led_resistor(5, 2, 0.02)
    assert math.isclose(r["exact"], 150)
    assert r["standard"] == 150
    assert semi.bjt_switch_base_resistor(5, 0.1) > 0


def test_digital():
    assert digital.twos_complement(-5, 8) == "11111011"
    assert digital.from_twos_complement("11111011") == -5
    assert digital.to_base(255, 16) == "FF"
    assert digital.gray_code(2) == 3
    assert math.isclose(digital.adc_resolution(5, 10), 5 / 1024)
    assert digital.truth_table(lambda a, b: a and b, 2)[-1] == (1, 1, 1)


def test_signal():
    s = signal.sine_wave(50, 1000, 200)
    assert math.isclose(signal.rms(s), 1 / math.sqrt(2), rel_tol=1e-2)
    assert signal.dominant_frequency(signal.sine_wave(100, 1000, 100), 1000) == 100
    assert signal.nyquist(8000) == 4000


def test_embedded():
    t = embedded.timer_settings(16_000_000, 1000)
    assert t["error_pct"] < 0.01
    u = embedded.uart_baud_error(16_000_000, 9600)
    assert u["ubrr"] == 103
    lo, hi = embedded.i2c_pullup_range(3.3, 100e-12)
    assert lo < hi
    assert embedded.pwm_duty(1, 4) == 25
    assert math.isclose(embedded.adc_counts_to_temperature_ntc(512, 10, 10_000, 10_000, 25, 3950), 25, abs_tol=0.01)


def test_control():
    pid = control.PID(2.0, 0.5, 0.1, -10, 10)
    assert math.isclose(pid.update(1.0, 0.0, 0.1), 2.05)
    trace = control.simulate_first_order(control.PID(2, 5, 0), k=1, tau=0.5, setpoint=1.0)
    assert math.isclose(trace[-1], 1.0, abs_tol=0.02)
    assert math.isclose(control.first_order_step(1, 1, 1), 1 - math.exp(-1))
    assert control.second_order_params(10, 0.5)["overshoot_pct"] == pytest.approx(16.3, abs=0.1)


def test_cli(capsys):
    from lynxtronics.cli import main
    main(["parallel", "1k", "1k"])
    assert capsys.readouterr().out.strip() == "500 Ω"
    main(["color", "brown", "black", "red", "gold"])
    assert "1 kΩ" in capsys.readouterr().out
