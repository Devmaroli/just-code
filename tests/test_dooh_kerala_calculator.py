#!/usr/bin/env python3
"""Unit tests for the Kerala DOOH financial calculator."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import dooh_kerala_calculator as calc  # noqa: E402


class TestDutyStack(unittest.TestCase):
    def test_preferred_hs_economic_duty(self):
        d = calc.import_landed_multiplier(conservative=False)
        # 10% BCD + 1% AIDC + 1.1% SWS = 12.1%
        self.assertAlmostEqual(d["bcd"], 0.10)
        self.assertAlmostEqual(d["aidc"], 0.01)
        self.assertAlmostEqual(d["sws"], 0.011)
        self.assertAlmostEqual(d["economic_duty_on_cif"], 0.121)

    def test_conservative_hs_higher_bcd(self):
        d = calc.import_landed_multiplier(conservative=True)
        self.assertAlmostEqual(d["bcd"], 0.20)
        self.assertGreater(d["economic_duty_on_cif"], 0.20)


class TestTariff(unittest.TestCase):
    def test_non_telescopic_top_slab(self):
        self.assertEqual(calc.lt7a_energy_rate(4212), 9.40)

    def test_low_slab(self):
        self.assertEqual(calc.lt7a_energy_rate(80), 6.05)

    def test_outdoor_power_positive(self):
        bill = calc.monthly_power_bill(12.0, 15.0, 18.0, 0.65)
        self.assertGreater(bill, 30_000)
        self.assertLess(bill, 80_000)


class TestModel(unittest.TestCase):
    def test_base_is_profitable(self):
        result = calc.compute(calc.CalculatorConfig())
        self.assertEqual(len(result.sites), 6)
        self.assertGreater(result.capex_total_inr, 8_000_000)
        self.assertLess(result.capex_total_inr, 30_000_000)
        self.assertIsNotNone(result.payback_months)
        self.assertGreater(result.ebitda_monthly_inr, 0)

    def test_target_payback_inside_12_16_months(self):
        preset = calc.scenario_presets("target")
        result = calc.compute(
            calc.CalculatorConfig(
                occupancy=preset["occupancy"],
                programmatic_fill=preset["programmatic_fill"],
                scenario="target",
                fob_usd_per_sqm=preset["fob_usd_per_sqm"],
                sales_commission=preset["sales_commission"],
                amc_rate=preset["amc_rate"],
                outdoor_slots_per_face=preset["outdoor_slots_per_face"],
            )
        )
        self.assertIsNotNone(result.payback_months)
        self.assertGreaterEqual(result.payback_months, 10)
        self.assertLessEqual(result.payback_months, 16)

    def test_zero_occupancy_still_has_programmatic_and_negative_ebitda(self):
        result = calc.compute(calc.CalculatorConfig(occupancy=0.0, programmatic_fill=0.0, scenario="zero"))
        self.assertEqual(result.revenue_gross_monthly_inr, 0.0)
        self.assertLess(result.ebitda_monthly_inr, 0)
        self.assertIsNone(result.payback_months)

    def test_city_revenue_keys(self):
        result = calc.compute(calc.CalculatorConfig())
        self.assertEqual(set(result.revenue_by_city), {"Kochi", "Kozhikode", "Kannur"})
        self.assertGreater(result.revenue_by_city["Kochi"], result.revenue_by_city["Kannur"])

    def test_igst_excluded_from_economic_capex(self):
        result = calc.compute(calc.CalculatorConfig())
        self.assertGreater(result.capex_cash_inr, result.capex_total_inr)

    def test_higher_occupancy_shortens_payback(self):
        low = calc.compute(calc.CalculatorConfig(occupancy=0.60, scenario="low"))
        high = calc.compute(calc.CalculatorConfig(occupancy=0.90, scenario="high"))
        self.assertIsNotNone(low.payback_months)
        self.assertIsNotNone(high.payback_months)
        self.assertLess(high.payback_months, low.payback_months)

    def test_json_roundtrip_keys(self):
        result = calc.compute(calc.CalculatorConfig())
        payload = calc.result_to_json(result)
        self.assertIn("ebitda_monthly_inr", payload)
        self.assertIn("payback_months", payload)
        json.dumps(payload)


class TestCli(unittest.TestCase):
    def test_cli_base_exit_zero(self):
        proc = subprocess.run(
            [sys.executable, os.path.join(ROOT, "dooh_kerala_calculator.py"), "--scenario", "base"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("KERALA DOOH NETWORK", proc.stdout)
        self.assertIn("EBITDA", proc.stdout)

    def test_cli_json(self):
        proc = subprocess.run(
            [sys.executable, os.path.join(ROOT, "dooh_kerala_calculator.py"), "--json", "--occupancy", "0.7"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertEqual(payload["occupancy"], 0.7)
        self.assertEqual(len(payload["sites"]), 6)


if __name__ == "__main__":
    unittest.main()
