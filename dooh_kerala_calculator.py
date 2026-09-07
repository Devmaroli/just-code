#!/usr/bin/env python3
"""Kerala DOOH Network Financial Calculator.

Computes CAPEX, monthly OPEX, city-wise revenue, EBITDA, net operating
margin, payback period, and annual ROI for a Digital Out-Of-Home screen
network across Kochi, Kozhikode, and Kannur.

Default topology (6 display nodes):
  * Kochi:     1 outdoor unipole + 2 indoor dual-sided MUPI kiosks
  * Kozhikode: 1 outdoor unipole + 1 indoor dual-sided MUPI kiosk
  * Kannur:    1 indoor dual-sided MUPI kiosk

Tariffs and duty stacks used here match the accompanying blueprint
(docs/KERALA_DOOH_BLUEPRINT.md). Rates are working planning figures;
confirm KSERC, CBIC, and municipal schedules before committing capital.

Usage:
  python3 dooh_kerala_calculator.py
  python3 dooh_kerala_calculator.py --scenario target
  python3 dooh_kerala_calculator.py --occupancy 0.85 --scenario optimistic
  python3 dooh_kerala_calculator.py --json --out /tmp/dooh.json
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass, field
from typing import Dict, List, Optional


# ---------------------------------------------------------------------------
# Planning constants (INR unless noted). Keep in sync with the blueprint.
# ---------------------------------------------------------------------------

INR_PER_USD = 84.0

# KSERC LT-VII(A) Commercial (three-phase), Gazette order w.e.f. 05-Dec-2024.
# Energy slabs are non-telescopic: the entire monthly consumption is billed
# at the slab that the total units fall into.
LT7A_FIXED_CHARGE_PER_KW = 190.0  # Rs / kW / month, three-phase
LT7A_ENERGY_SLABS = (
    (100, 6.05),
    (200, 6.80),
    (300, 7.50),
    (500, 8.15),
    (float("inf"), 9.40),
)
KERALA_ELECTRICITY_DUTY_RATE = 0.10  # 10% of energy charges (KED Act, 1963)
FUEL_SURCHARGE_PER_KWH = 0.50  # planning buffer for FPPCA / other levies

# Import duty stack for CTH 8528 52 00 (computer-connectable monitors).
# Conservative case uses 8528 59 00 (other monitors) with 20% BCD.
BCD_PREFERRED = 0.10
BCD_CONSERVATIVE = 0.20
AIDC_ON_BCD = 0.10  # 10% of BCD
SWS_ON_CUSTOMS = 0.10  # 10% of (BCD + AIDC)
IGST_RATE = 0.18

# Outdoor LED: P3.91, 8.0 m x 4.0 m = 32 sq.m per face, 5,500 nits.
# Dual-face is the commercial default: one unipole covers both carriageways.
OUTDOOR_AREA_SQM = 32.0
OUTDOOR_FOB_USD_PER_SQM = 650.0
OUTDOOR_CONNECTED_KW_PER_FACE = 12.0
OUTDOOR_HOURS_PER_DAY = 18.0
OUTDOOR_LOAD_FACTOR = 0.65  # auto-dimming blended utilisation
DEFAULT_OUTDOOR_FACES = 2

# Indoor dual-sided 55-inch MUPI.
INDOOR_CONNECTED_KW = 0.55
INDOOR_HOURS_PER_DAY = 14.0
INDOOR_MALL_MARKUP = 0.20  # mall recovers KSEB + HVAC share

# Commercial inventory: 10-second spots in a 100-second loop = 10 slots/face.
OUTDOOR_SLOTS_PER_FACE = 10
INDOOR_FACES_PER_KIOSK = 2
INDOOR_SLOTS_PER_FACE = 6

KOCHI_OUTDOOR_SLOT_INR = 50_000.0
KOZHIKODE_OUTDOOR_SLOT_INR = 30_000.0
MALL_SLOT_INR = 8_500.0

# Programmatic (Hivestack / Lemma) fills a share of *unsold* loop time.
DEFAULT_PROGRAMMATIC_FILL = 0.35
PROGRAMMATIC_CPM_DISCOUNT = 0.55  # programmatic realises 55% of direct CPM

GST_ON_ADVERTISING = 0.18  # output GST; modelled as pass-through, not in EBITDA
SALES_COMMISSION_RATE = 0.10
DEFAULT_REVENUE_SHARE = 0.18
AMC_RATE = 0.045
OPS_ADMIN_MONTHLY = 60_000.0
INSURANCE_MONTHLY = 15_000.0
CONTINGENCY_RATE = 0.08

DAYS_PER_MONTH = 30.0
MONTHS_PER_YEAR = 12.0


@dataclass
class SiteSpec:
    site_id: str
    city: str
    name: str
    kind: str  # "outdoor" | "indoor"
    min_lease_inr: float
    ad_tax_annual_inr: float
    slot_price_inr: float
    slots: int
    revenue_share_rate: float = DEFAULT_REVENUE_SHARE


def default_sites(outdoor_faces: int = DEFAULT_OUTDOOR_FACES) -> List[SiteSpec]:
    """Pilot network of six display nodes with commercially viable lease floors.

    High fixed mall rents (₹55k–₹75k) consume indoor yield at ₹8,500/slot.
    Floors below are minimum guarantees; hybrid mode bills max(floor, 18% of site gross).
    """
    outdoor_slots = OUTDOOR_SLOTS_PER_FACE * outdoor_faces
    indoor_slots = INDOOR_FACES_PER_KIOSK * INDOOR_SLOTS_PER_FACE
    kochi_tax = 5_000.0 * OUTDOOR_AREA_SQM * outdoor_faces
    clt_tax = 3_000.0 * OUTDOOR_AREA_SQM * outdoor_faces
    return [
        SiteSpec(
            site_id="KOCHI-OUT-01",
            city="Kochi",
            name="Edappally / Kakkanad outdoor unipole",
            kind="outdoor",
            min_lease_inr=80_000.0,
            ad_tax_annual_inr=kochi_tax,
            slot_price_inr=KOCHI_OUTDOOR_SLOT_INR,
            slots=outdoor_slots,
        ),
        SiteSpec(
            site_id="KOCHI-IN-01",
            city="Kochi",
            name="Lulu Mall MUPI kiosk",
            kind="indoor",
            min_lease_inr=40_000.0,
            ad_tax_annual_inr=24_000.0,
            slot_price_inr=MALL_SLOT_INR,
            slots=indoor_slots,
        ),
        SiteSpec(
            site_id="KOCHI-IN-02",
            city="Kochi",
            name="Forum Mall MUPI kiosk",
            kind="indoor",
            min_lease_inr=32_000.0,
            ad_tax_annual_inr=24_000.0,
            slot_price_inr=MALL_SLOT_INR,
            slots=indoor_slots,
        ),
        SiteSpec(
            site_id="CLT-OUT-01",
            city="Kozhikode",
            name="Thondayad Bypass outdoor unipole",
            kind="outdoor",
            min_lease_inr=45_000.0,
            ad_tax_annual_inr=clt_tax,
            slot_price_inr=KOZHIKODE_OUTDOOR_SLOT_INR,
            slots=outdoor_slots,
        ),
        SiteSpec(
            site_id="CLT-IN-01",
            city="Kozhikode",
            name="HiLite Mall MUPI kiosk",
            kind="indoor",
            min_lease_inr=28_000.0,
            ad_tax_annual_inr=18_000.0,
            slot_price_inr=MALL_SLOT_INR,
            slots=indoor_slots,
        ),
        SiteSpec(
            site_id="CAN-IN-01",
            city="Kannur",
            name="Secura Centre / Capitol Mall MUPI kiosk",
            kind="indoor",
            min_lease_inr=20_000.0,
            ad_tax_annual_inr=14_400.0,
            slot_price_inr=MALL_SLOT_INR,
            slots=indoor_slots,
        ),
    ]


def resolved_lease(site: SiteSpec, site_revenue: float, lease_model: str) -> float:
    """fixed = floor only; revshare = % of gross; hybrid = max(floor, %)."""
    share = site.revenue_share_rate * site_revenue
    if lease_model == "fixed":
        return site.min_lease_inr
    if lease_model == "revshare":
        return share
    return max(site.min_lease_inr, share)


def lt7a_energy_rate(monthly_kwh: float) -> float:
    """Return the non-telescopic LT-VII(A) energy charge for a monthly kWh total."""
    for ceiling, rate in LT7A_ENERGY_SLABS:
        if monthly_kwh <= ceiling:
            return rate
    return LT7A_ENERGY_SLABS[-1][1]


def monthly_power_bill(connected_kw: float, sanction_kw: float, hours_per_day: float, load_factor: float, mall_markup: float = 0.0) -> float:
    """KSEB LT-VII(A) three-phase monthly bill including electricity duty."""
    kwh = connected_kw * load_factor * hours_per_day * DAYS_PER_MONTH
    energy_rate = lt7a_energy_rate(kwh)
    energy_charge = kwh * energy_rate
    fixed_charge = LT7A_FIXED_CHARGE_PER_KW * sanction_kw
    duty = energy_charge * KERALA_ELECTRICITY_DUTY_RATE
    fuel = kwh * FUEL_SURCHARGE_PER_KWH
    subtotal = energy_charge + fixed_charge + duty + fuel
    return subtotal * (1.0 + mall_markup)


def import_landed_multiplier(conservative: bool) -> Dict[str, float]:
    """Return duty components and the CIF-to-landed (ex-IGST-credit) multiplier.

    IGST is a credit for a GST-registered importer and is excluded from
    economic CAPEX. Cash outflow still includes IGST at clearance.
    """
    bcd = BCD_CONSERVATIVE if conservative else BCD_PREFERRED
    aidc = bcd * AIDC_ON_BCD
    sws = (bcd + aidc) * SWS_ON_CUSTOMS
    customs = bcd + aidc + sws
    igst = (1.0 + customs) * IGST_RATE
    return {
        "bcd": bcd,
        "aidc": aidc,
        "sws": sws,
        "igst": igst,
        "cash_duty_on_cif": customs + igst,
        "economic_duty_on_cif": customs,
    }


@dataclass
class CapexLine:
    item: str
    amount_inr: float
    notes: str = ""


@dataclass
class FinancialResult:
    scenario: str
    occupancy: float
    programmatic_fill: float
    usd_inr: float
    conservative_hs: bool
    sites: List[Dict]
    capex_lines: List[Dict]
    capex_total_inr: float
    capex_cash_inr: float
    opex_fixed_monthly_inr: float
    opex_variable_monthly_inr: float
    opex_total_monthly_inr: float
    revenue_direct_monthly_inr: float
    revenue_programmatic_monthly_inr: float
    revenue_gross_monthly_inr: float
    revenue_by_city: Dict[str, float]
    ebitda_monthly_inr: float
    ebitda_annual_inr: float
    net_operating_margin: float
    payback_months: Optional[float]
    annual_roi: Optional[float]
    theoretical_capacity_monthly_inr: float
    occupancy_breakeven: Optional[float]
    lease_model: str = "hybrid"
    outdoor_faces: int = DEFAULT_OUTDOOR_FACES


def outdoor_hardware_fob_inr(usd_inr: float, faces: int, fob_usd_per_sqm: float) -> float:
    return OUTDOOR_AREA_SQM * fob_usd_per_sqm * usd_inr * faces


def outdoor_sanction_kw(faces: int) -> float:
    """Connected ~12 kW/face; sanction 15 kW single-face or 25 kW dual-face."""
    return 15.0 if faces <= 1 else 25.0


def build_capex(
    n_outdoor: int,
    n_indoor: int,
    usd_inr: float,
    conservative_hs: bool,
    faces: int,
    fob_usd_per_sqm: float = OUTDOOR_FOB_USD_PER_SQM,
) -> List[CapexLine]:
    duty = import_landed_multiplier(conservative_hs)
    fob_one = outdoor_hardware_fob_inr(usd_inr, faces, fob_usd_per_sqm)
    freight_one = 150_000.0 * (1.6 if faces > 1 else 1.0)
    cif_one = fob_one + freight_one
    economic_duty_one = cif_one * duty["economic_duty_on_cif"]
    igst_one = cif_one * (1.0 + duty["bcd"] + duty["aidc"] + duty["sws"]) * IGST_RATE
    structure = 1_780_000.0 * (1.15 if faces > 1 else 1.0)
    electrical = 280_000.0 * (1.35 if faces > 1 else 1.0)
    kseb = 220_000.0 * (1.25 if faces > 1 else 1.0)
    controller = 165_000.0 * (1.4 if faces > 1 else 1.0)
    install = 180_000.0 * (1.25 if faces > 1 else 1.0)
    spares = 420_000.0 * (1.5 if faces > 1 else 1.0)

    lines = [
        CapexLine(
            f"Outdoor LED cabinets (P3.91, {OUTDOOR_AREA_SQM:.0f} sq.m x {faces} face(s), FOB China)",
            fob_one * n_outdoor,
            f"{n_outdoor} unipoles x {faces} face(s) x {OUTDOOR_AREA_SQM:.0f} sq.m x USD {fob_usd_per_sqm:.0f} x INR {usd_inr:.0f}",
        ),
        CapexLine(
            "Sea freight, marine insurance, ICD handling (ICTT Vallarpadam)",
            freight_one * n_outdoor,
            "FCL 40' from Shenzhen/Guangzhou; THC + CHA at Cochin",
        ),
        CapexLine(
            "Customs BCD + AIDC + SWS (economic, IGST excluded)",
            economic_duty_one * n_outdoor,
            f"HS {'85285900 (20% BCD)' if conservative_hs else '85285200 (10% BCD)'}",
        ),
        CapexLine(
            "IGST cash at clearance (GST credit, not economic CAPEX)",
            igst_one * n_outdoor,
            "Recoverable as ITC in the first GST return after import",
        ),
        CapexLine(
            "Unipole structure, foundation, soil test, structural PE",
            structure * n_outdoor,
            "12–15 m MS unipole, IS 2062, coastal paint system, pile/raft",
        ),
        CapexLine(
            "Electrical, earthing pits, Class II SPD, lightning IS/IEC 62305",
            electrical * n_outdoor,
            "LT panel, ELCB, <2 Ohm pits, Cu down-conductor",
        ),
        CapexLine(
            "KSEB LT-VII(A) 3-phase connection (10–25 kW sanction)",
            kseb * n_outdoor,
            "Security deposit + service line + ToD-capable meter + Inspectorate",
        ),
        CapexLine(
            "NovaStar TB60 + industrial player + 4G/5G failover",
            controller * n_outdoor,
            "Taurus TB60, Mean Well PSU spare, dual-SIM router",
        ),
        CapexLine(
            "K-SWIFT / municipal / PWD / NHAI first-year statutory",
            250_000.0 * n_outdoor,
            "Application, building permit, advertisement licence year-1",
        ),
        CapexLine(
            "Outdoor install, crane, commissioning, 72-hour burn-in",
            install * n_outdoor,
            "Night lift window, traffic marshal, NDT on welds",
        ),
        CapexLine(
            "Indoor dual-sided 55-inch 2,500–3,000 nit commercial LCDs",
            220_000.0 * n_indoor,
            "Two 55-inch panels per kiosk, 24x7 rated",
        ),
        CapexLine(
            "MUPI kiosk fabrication (MS/Al + 8 mm toughened glass)",
            185_000.0 * n_indoor,
            "Powder-coated, lockable, concealed cabling, branding shroud",
        ),
        CapexLine(
            "Indoor player, CMS licence year-1 hardware, install",
            100_000.0 * n_indoor,
            "Android/x86 player, 4G, mall electrical tap, civil pad",
        ),
        CapexLine(
            "Shared CMS, Hivestack/Lemma SSP integration, creative studio",
            250_000.0,
            "One-time VAST/VPAID connector + proof-of-play dashboard",
        ),
        CapexLine(
            "Spares (outdoor modules + indoor panels + Mean Well PSU)",
            spares,
            "Held in Kochi warehouse for 24-hour swap SLA",
        ),
    ]
    hardware_ex_igst = sum(l.amount_inr for l in lines if "IGST cash" not in l.item)
    lines.append(
        CapexLine(
            "Contingency (8% of economic CAPEX before IGST)",
            hardware_ex_igst * CONTINGENCY_RATE,
            "Monsoon delay, extra civil, duty reclassification buffer",
        )
    )
    return lines


def site_power_monthly(site: SiteSpec, outdoor_faces: int) -> float:
    if site.kind == "outdoor":
        return monthly_power_bill(
            OUTDOOR_CONNECTED_KW_PER_FACE * outdoor_faces,
            outdoor_sanction_kw(outdoor_faces),
            OUTDOOR_HOURS_PER_DAY,
            OUTDOOR_LOAD_FACTOR,
        )
    return monthly_power_bill(
        INDOOR_CONNECTED_KW,
        max(INDOOR_CONNECTED_KW, 1.0),
        INDOOR_HOURS_PER_DAY,
        0.85,
        mall_markup=INDOOR_MALL_MARKUP,
    )


@dataclass
class CalculatorConfig:
    occupancy: float = 0.75
    programmatic_fill: float = DEFAULT_PROGRAMMATIC_FILL
    usd_inr: float = INR_PER_USD
    conservative_hs: bool = False
    scenario: str = "base"
    kochi_outdoor_slot: float = KOCHI_OUTDOOR_SLOT_INR
    kozhikode_outdoor_slot: float = KOZHIKODE_OUTDOOR_SLOT_INR
    mall_slot: float = MALL_SLOT_INR
    sales_commission: float = SALES_COMMISSION_RATE
    lease_model: str = "hybrid"
    outdoor_faces: int = DEFAULT_OUTDOOR_FACES
    fob_usd_per_sqm: float = OUTDOOR_FOB_USD_PER_SQM
    outdoor_slots_per_face: int = OUTDOOR_SLOTS_PER_FACE
    amc_rate: float = AMC_RATE
    sites: List[SiteSpec] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.sites:
            self.sites = default_sites(self.outdoor_faces)

    def apply_slot_overrides(self) -> None:
        outdoor_slots = self.outdoor_slots_per_face * self.outdoor_faces
        for site in self.sites:
            if site.kind == "outdoor":
                site.slots = outdoor_slots
                if site.city == "Kochi":
                    site.slot_price_inr = self.kochi_outdoor_slot
                else:
                    site.slot_price_inr = self.kozhikode_outdoor_slot
            else:
                site.slot_price_inr = self.mall_slot


def scenario_presets(name: str) -> Dict:
    name = name.lower().strip()
    if name == "conservative":
        return {
            "occupancy": 0.60,
            "programmatic_fill": 0.20,
            "conservative_hs": True,
            "scenario": "conservative",
        }
    if name == "optimistic":
        return {
            "occupancy": 0.90,
            "programmatic_fill": 0.50,
            "conservative_hs": False,
            "scenario": "optimistic",
        }
    if name == "target":
        # Acceleration stack that lands inside a 12–16 month simple payback.
        return {
            "occupancy": 0.90,
            "programmatic_fill": 0.45,
            "conservative_hs": False,
            "scenario": "target",
            "fob_usd_per_sqm": 330.0,
            "sales_commission": 0.06,
            "amc_rate": 0.035,
            "outdoor_slots_per_face": 10,
        }
    return {
        "occupancy": 0.75,
        "programmatic_fill": DEFAULT_PROGRAMMATIC_FILL,
        "conservative_hs": False,
        "scenario": "base",
    }


def compute(cfg: CalculatorConfig) -> FinancialResult:
    cfg.apply_slot_overrides()
    n_outdoor = sum(1 for s in cfg.sites if s.kind == "outdoor")
    n_indoor = sum(1 for s in cfg.sites if s.kind == "indoor")
    capex_lines = build_capex(
        n_outdoor,
        n_indoor,
        cfg.usd_inr,
        cfg.conservative_hs,
        cfg.outdoor_faces,
        cfg.fob_usd_per_sqm,
    )
    capex_cash = sum(l.amount_inr for l in capex_lines)
    capex_economic = sum(l.amount_inr for l in capex_lines if "IGST cash" not in l.item)

    cms_per_player = 2_200.0
    connectivity_per_site = 1_200.0
    maintenance_monthly = (capex_economic * cfg.amc_rate) / MONTHS_PER_YEAR

    site_rows = []
    revenue_by_city: Dict[str, float] = {}
    theoretical = 0.0
    direct_rev = 0.0
    prog_rev = 0.0
    lease_total = 0.0
    site_power_tax_cms = 0.0

    for site in cfg.sites:
        power = site_power_monthly(site, cfg.outdoor_faces)
        tax_m = site.ad_tax_annual_inr / MONTHS_PER_YEAR
        cms = cms_per_player
        conn = connectivity_per_site

        capacity = site.slot_price_inr * site.slots
        theoretical += capacity
        sold = capacity * cfg.occupancy
        unsold = capacity * (1.0 - cfg.occupancy)
        programmatic = unsold * cfg.programmatic_fill * PROGRAMMATIC_CPM_DISCOUNT
        site_rev = sold + programmatic
        lease = resolved_lease(site, site_rev, cfg.lease_model)
        lease_total += lease
        site_power_tax_cms += power + tax_m + cms + conn
        direct_rev += sold
        prog_rev += programmatic
        revenue_by_city[site.city] = revenue_by_city.get(site.city, 0.0) + site_rev

        site_rows.append(
            {
                "site_id": site.site_id,
                "city": site.city,
                "name": site.name,
                "kind": site.kind,
                "lease_inr": round(lease, 2),
                "min_lease_inr": round(site.min_lease_inr, 2),
                "power_inr": round(power, 2),
                "ad_tax_monthly_inr": round(tax_m, 2),
                "cms_connectivity_inr": round(cms + conn, 2),
                "slots": site.slots,
                "slot_price_inr": site.slot_price_inr,
                "capacity_inr": round(capacity, 2),
                "direct_revenue_inr": round(sold, 2),
                "programmatic_revenue_inr": round(programmatic, 2),
                "site_revenue_inr": round(site_rev, 2),
            }
        )

    opex_fixed = lease_total + site_power_tax_cms + maintenance_monthly + OPS_ADMIN_MONTHLY + INSURANCE_MONTHLY
    gross = direct_rev + prog_rev
    variable = gross * cfg.sales_commission
    opex_total = opex_fixed + variable
    ebitda = gross - opex_total
    margin = (ebitda / gross) if gross else 0.0
    payback = (capex_economic / ebitda) if ebitda > 0 else None
    roi = (ebitda * MONTHS_PER_YEAR / capex_economic) if capex_economic else None

    breakeven = _occupancy_breakeven(cfg, capex_economic)

    return FinancialResult(
        scenario=cfg.scenario,
        occupancy=cfg.occupancy,
        programmatic_fill=cfg.programmatic_fill,
        usd_inr=cfg.usd_inr,
        conservative_hs=cfg.conservative_hs,
        sites=site_rows,
        capex_lines=[asdict(l) for l in capex_lines],
        capex_total_inr=round(capex_economic, 2),
        capex_cash_inr=round(capex_cash, 2),
        opex_fixed_monthly_inr=round(opex_fixed, 2),
        opex_variable_monthly_inr=round(variable, 2),
        opex_total_monthly_inr=round(opex_total, 2),
        revenue_direct_monthly_inr=round(direct_rev, 2),
        revenue_programmatic_monthly_inr=round(prog_rev, 2),
        revenue_gross_monthly_inr=round(gross, 2),
        revenue_by_city={k: round(v, 2) for k, v in revenue_by_city.items()},
        ebitda_monthly_inr=round(ebitda, 2),
        ebitda_annual_inr=round(ebitda * MONTHS_PER_YEAR, 2),
        net_operating_margin=round(margin, 4),
        payback_months=round(payback, 2) if payback is not None else None,
        annual_roi=round(roi, 4) if roi is not None else None,
        theoretical_capacity_monthly_inr=round(theoretical, 2),
        occupancy_breakeven=breakeven,
        lease_model=cfg.lease_model,
        outdoor_faces=cfg.outdoor_faces,
    )


def _occupancy_breakeven(cfg: CalculatorConfig, capex_economic: float) -> Optional[float]:
    """Scan occupancy because hybrid leases make OPEX revenue-dependent."""
    found = None
    for step in range(0, 151):
        probe = step / 100.0
        trial = CalculatorConfig(
            occupancy=probe,
            programmatic_fill=cfg.programmatic_fill,
            usd_inr=cfg.usd_inr,
            conservative_hs=cfg.conservative_hs,
            scenario="probe",
            kochi_outdoor_slot=cfg.kochi_outdoor_slot,
            kozhikode_outdoor_slot=cfg.kozhikode_outdoor_slot,
            mall_slot=cfg.mall_slot,
            sales_commission=cfg.sales_commission,
            lease_model=cfg.lease_model,
            outdoor_faces=cfg.outdoor_faces,
            fob_usd_per_sqm=cfg.fob_usd_per_sqm,
            outdoor_slots_per_face=cfg.outdoor_slots_per_face,
            amc_rate=cfg.amc_rate,
            sites=[SiteSpec(**{**asdict(s)}) for s in cfg.sites],
        )
        # Inline a lightweight P&L without recursing into breakeven.
        trial.apply_slot_overrides()
        ebitda = _ebitda_only(trial, capex_economic)
        if ebitda >= 0:
            found = probe
            break
    return round(found, 4) if found is not None else None


def _ebitda_only(cfg: CalculatorConfig, capex_economic: float) -> float:
    cms_per_player = 2_200.0
    connectivity_per_site = 1_200.0
    maintenance_monthly = (capex_economic * cfg.amc_rate) / MONTHS_PER_YEAR
    lease_total = 0.0
    site_power_tax_cms = 0.0
    gross = 0.0
    for site in cfg.sites:
        power = site_power_monthly(site, cfg.outdoor_faces)
        tax_m = site.ad_tax_annual_inr / MONTHS_PER_YEAR
        capacity = site.slot_price_inr * site.slots
        sold = capacity * cfg.occupancy
        unsold = capacity * (1.0 - cfg.occupancy)
        programmatic = unsold * cfg.programmatic_fill * PROGRAMMATIC_CPM_DISCOUNT
        site_rev = sold + programmatic
        lease_total += resolved_lease(site, site_rev, cfg.lease_model)
        site_power_tax_cms += power + tax_m + cms_per_player + connectivity_per_site
        gross += site_rev
    opex = (
        lease_total
        + site_power_tax_cms
        + maintenance_monthly
        + OPS_ADMIN_MONTHLY
        + INSURANCE_MONTHLY
        + gross * cfg.sales_commission
    )
    return gross - opex


def inr(value: Optional[float]) -> str:
    if value is None:
        return "n/a"
    sign = "-" if value < 0 else ""
    n = abs(value)
    # Indian grouping: 12,34,56,789.00
    whole, frac = f"{n:.2f}".split(".")
    if len(whole) <= 3:
        grouped = whole
    else:
        grouped = whole[-3:]
        rest = whole[:-3]
        parts = []
        while rest:
            parts.append(rest[-2:])
            rest = rest[:-2]
        grouped = ",".join(reversed(parts)) + "," + grouped
    return f"{sign}₹{grouped}.{frac}"


def pct(value: Optional[float]) -> str:
    if value is None:
        return "n/a"
    return f"{value * 100:.1f}%"


def render_text(result: FinancialResult) -> str:
    lines = [
        "=" * 78,
        "KERALA DOOH NETWORK — FINANCIAL MODEL",
        f"Scenario: {result.scenario.upper()}  |  Direct occupancy: {pct(result.occupancy)}"
        f"  |  Programmatic fill of unsold: {pct(result.programmatic_fill)}",
        f"USD/INR: {result.usd_inr:.2f}  |  HS posture: "
        f"{'conservative 85285900' if result.conservative_hs else 'preferred 85285200'}",
        f"Lease model: {result.lease_model}  |  Outdoor faces/unipole: {result.outdoor_faces}",
        "=" * 78,
        "",
        "CAPEX (economic, IGST credited separately)",
        "-" * 78,
    ]
    for row in result.capex_lines:
        if "IGST cash" in row["item"]:
            continue
        lines.append(f"  {row['item']:<58} {inr(row['amount_inr']):>18}")
    lines.append(f"  {'TOTAL ECONOMIC CAPEX':<58} {inr(result.capex_total_inr):>18}")
    igst = next((r["amount_inr"] for r in result.capex_lines if "IGST cash" in r["item"]), 0.0)
    lines.append(f"  {'IGST cash at port (ITC recoverable)':<58} {inr(igst):>18}")
    lines.append(f"  {'TOTAL CASH OUTFLOW AT BUILD':<58} {inr(result.capex_cash_inr):>18}")
    lines += ["", "MONTHLY OPEX", "-" * 78]
    lines.append(f"  {'Fixed (leases, power, tax, CMS, opex staff)':<58} {inr(result.opex_fixed_monthly_inr):>18}")
    lines.append(f"  {'Variable (sales commission)':<58} {inr(result.opex_variable_monthly_inr):>18}")
    lines.append(f"  {'TOTAL MONTHLY OPEX':<58} {inr(result.opex_total_monthly_inr):>18}")
    lines += ["", "MONTHLY REVENUE", "-" * 78]
    lines.append(f"  {'Theoretical 100% direct capacity':<58} {inr(result.theoretical_capacity_monthly_inr):>18}")
    lines.append(f"  {'Direct sold inventory':<58} {inr(result.revenue_direct_monthly_inr):>18}")
    lines.append(f"  {'Programmatic (Hivestack/Lemma on unsold)':<58} {inr(result.revenue_programmatic_monthly_inr):>18}")
    lines.append(f"  {'GROSS MONTHLY REVENUE':<58} {inr(result.revenue_gross_monthly_inr):>18}")
    for city, amount in result.revenue_by_city.items():
        lines.append(f"    {city:<56} {inr(amount):>18}")
    lines += ["", "SITE DETAIL", "-" * 78]
    for s in result.sites:
        lines.append(
            f"  {s['site_id']}  {s['name']}"
        )
        lines.append(
            f"      lease {inr(s['lease_inr'])}  power {inr(s['power_inr'])}  "
            f"rev {inr(s['site_revenue_inr'])}  ({s['slots']} slots @ {inr(s['slot_price_inr'])})"
        )
    lines += ["", "RETURNS", "-" * 78]
    lines.append(f"  {'EBITDA (monthly)':<58} {inr(result.ebitda_monthly_inr):>18}")
    lines.append(f"  {'EBITDA (annual)':<58} {inr(result.ebitda_annual_inr):>18}")
    lines.append(f"  {'Net operating margin':<58} {pct(result.net_operating_margin):>18}")
    payback_txt = f"{result.payback_months:.1f} months" if result.payback_months else "Does not pay back at this occupancy"
    lines.append(f"  {'Simple payback on economic CAPEX':<58} {payback_txt:>18}")
    lines.append(f"  {'Annual ROI on economic CAPEX':<58} {pct(result.annual_roi):>18}")
    lines.append(f"  {'Direct occupancy breakeven':<58} {pct(result.occupancy_breakeven):>18}")
    lines.append("=" * 78)
    return "\n".join(lines) + "\n"


def result_to_json(result: FinancialResult) -> Dict:
    payload = asdict(result)
    return payload


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Kerala DOOH 6-node financial calculator (Kochi, Kozhikode, Kannur).",
    )
    p.add_argument(
        "--scenario",
        choices=("conservative", "base", "optimistic", "target"),
        default="base",
        help="Preset occupancy, programmatic fill, duty posture, and (for target) CKD hardware stack.",
    )
    p.add_argument("--occupancy", type=float, default=None, help="Direct sold occupancy 0–1 (overrides scenario).")
    p.add_argument("--programmatic-fill", type=float, default=None, help="Fill rate of unsold inventory 0–1.")
    p.add_argument("--usd-inr", type=float, default=INR_PER_USD, help="USD to INR conversion for FOB LED.")
    p.add_argument("--conservative-hs", action="store_true", help="Use 20% BCD under CTH 85285900.")
    p.add_argument("--kochi-slot", type=float, default=KOCHI_OUTDOOR_SLOT_INR, help="Kochi outdoor monthly slot INR.")
    p.add_argument("--kozhikode-slot", type=float, default=KOZHIKODE_OUTDOOR_SLOT_INR, help="Kozhikode outdoor monthly slot INR.")
    p.add_argument("--mall-slot", type=float, default=MALL_SLOT_INR, help="Indoor mall monthly slot INR.")
    p.add_argument("--commission", type=float, default=None, help="Sales commission on gross revenue (default 0.10; target scenario uses 0.06).")
    p.add_argument("--fob-usd", type=float, default=None, help="Outdoor LED FOB USD per sq.m (default 650; target scenario uses 330).")
    p.add_argument("--outdoor-slots-per-face", type=int, default=None, help="Sellable 10-second slots per outdoor face (default 10).")
    p.add_argument(
        "--lease-model",
        choices=("hybrid", "fixed", "revshare"),
        default="hybrid",
        help="hybrid = max(minimum guarantee, 18%% of site gross); fixed = guarantee only; revshare = percent only.",
    )
    p.add_argument(
        "--outdoor-faces",
        type=int,
        default=DEFAULT_OUTDOOR_FACES,
        help="1 = single-face unipole; 2 = dual-face (default, both carriageways).",
    )
    p.add_argument("--json", action="store_true", help="Print JSON instead of a formatted table.")
    p.add_argument("--out", default=None, help="Write output to this file path.")
    return p


def config_from_args(args: argparse.Namespace) -> CalculatorConfig:
    preset = scenario_presets(args.scenario)
    occupancy = args.occupancy if args.occupancy is not None else preset["occupancy"]
    prog = args.programmatic_fill if args.programmatic_fill is not None else preset["programmatic_fill"]
    if not 0.0 <= occupancy <= 1.5:
        raise SystemExit("--occupancy must be between 0 and 1.5")
    if not 0.0 <= prog <= 1.0:
        raise SystemExit("--programmatic-fill must be between 0 and 1")
    if args.outdoor_faces not in (1, 2):
        raise SystemExit("--outdoor-faces must be 1 or 2")
    cfg = CalculatorConfig(
        occupancy=occupancy,
        programmatic_fill=prog,
        usd_inr=args.usd_inr,
        conservative_hs=args.conservative_hs or preset["conservative_hs"],
        scenario=preset["scenario"] if args.occupancy is None else f"{preset['scenario']}+custom",
        kochi_outdoor_slot=args.kochi_slot,
        kozhikode_outdoor_slot=args.kozhikode_slot,
        mall_slot=args.mall_slot,
        sales_commission=args.commission if args.commission is not None else preset.get("sales_commission", SALES_COMMISSION_RATE),
        lease_model=args.lease_model,
        outdoor_faces=args.outdoor_faces,
        fob_usd_per_sqm=args.fob_usd if args.fob_usd is not None else preset.get("fob_usd_per_sqm", OUTDOOR_FOB_USD_PER_SQM),
        outdoor_slots_per_face=args.outdoor_slots_per_face if args.outdoor_slots_per_face is not None else preset.get("outdoor_slots_per_face", OUTDOOR_SLOTS_PER_FACE),
        amc_rate=preset.get("amc_rate", AMC_RATE),
    )
    return cfg


def main(argv: Optional[List[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    result = compute(config_from_args(args))
    output = json.dumps(result_to_json(result), indent=2) if args.json else render_text(result)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as handle:
            handle.write(output)
        sys.stderr.write(f"Wrote {args.out}\n")
        return 0
    sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
