# Kerala DOOH Network — End-to-End Execution Blueprint

**Pilot topology:** Kochi (1 dual-face outdoor unipole at Edappally/Kakkanad + 2 indoor MUPI kiosks at Lulu Mall and Forum Mall) · Kozhikode (1 dual-face outdoor unipole at Thondayad Bypass + 1 indoor MUPI at HiLite Mall) · Kannur (1 indoor MUPI at Secura Centre / Capitol Mall).

**Display spec:** Outdoor P3.91 (or P4) SMD LED, die-cast aluminium, IP65/IP66, ≥ 5,500 nits with auto-dimming, conformal-coated PCBs. Indoor: dual-sided 55-inch 2,500–3,000 nit commercial 4K, 8 mm toughened glass kiosk.

**Software:** NovaStar Taurus TB30/TB60 + cloud CMS (PiSignage or VNNOX) + offline cache + Hivestack / Lemma programmatic tags.

Figures in Module 4 are produced by `dooh_kerala_calculator.py`. Statutory amounts are **working planning rates** as of 2026; confirm the live gazette / council schedule before paying.

---

## MODULE 1 — Administrative, Regulatory & Compliance Roadmap

### 1.1 Legal spine

| Instrument | What it controls | Portal / office |
| --- | --- | --- |
| Kerala Municipality Act, 1994, ss. 271–272 | Advertisement tax + written permission of the Secretary before any display | Corporation Town Planning / Revenue |
| Kerala Municipality Building Rules, 2019 | Unipole treated as a building / advertising sign; structural drawings | IBPMS: https://buildingpermit.lsgkerala.gov.in |
| Kerala Industrial Single Window Clearance Boards Act (K-SWIFT) | Parallel departmental clearances for the enterprise (KSEB, Electrical Inspectorate, Fire, Municipality) | https://kswift.kerala.gov.in |
| Control of National Highways (Land and Traffic) Act, 2002 + IRC:46-1972 | No commercial hoarding **inside NH RoW**; setbacks beyond RoW | NHAI Project Director (NH 66) / PWD Roads |
| Electricity Act 2003 + Kerala Electricity Supply Code 2014 | LT connection, metering, duty | https://wss.kseb.in |
| CEA Safety Regulations + Kerala Electrical Inspectorate | Scheme approval / sanction for energisation of advertising installations | https://ceisuraksha.ceikerala.gov.in |

Kochi Corporation’s 2012 advertisement bye-law still matters operationally: Secretary permission is mandatory on public **and** private land; hoardings generally **≥ 1 m** from thoroughfares; LED boards have historically been restricted from screening films (still / slide-style creatives were the bye-law default). In 2025 the Corporation began a designated-site LED programme and the Town Planning Committee is reviewing digital boards that encroach footpaths. **Do not install on footpath, median, or carriageway. Prefer private plots outside RoW, or Corporation-tendered designated sites.**

### 1.2 K-SWIFT + municipal application (step by step)

**Step 0 — Constitute the applicant.** Private limited company with PAN, GSTIN (Kerala registration), IEC (for imports), and a local authorised signatory. Open a current account with an AD code for ICEGATE.

**Step 1 — K-SWIFT registration.** Create an individual login, then an enterprise profile, at https://kswift.kerala.gov.in. Run the “identify clearances” wizard. Tick Municipality (building permit + trade/advertisement), KSEB (new LT), Electrical Inspectorate, and Fire & Rescue (mall kiosks). K-SWIFT is a router — it does **not** replace the Secretary’s s. 272 permission.

**Step 2 — Building permit (IBPMS).** File through https://buildingpermit.lsgkerala.gov.in (also linked from Kochi Corporation: http://kochicorporation.lsgkerala.gov.in). Upload:

1. Site plan (1:200) with NH/SH edge, RoW, setbacks, existing trees, KSEB lines.
2. Structural drawings + certificate (see `docs/legal/STRUCTURAL_STABILITY_CERTIFICATE.md`).
3. Soil report (two boreholes) for outdoor sites.
4. Proof of title / consent (sale deed, tax receipt, possessor’s NOC).
5. AAI NOCAS print for Kochi if the tip of the unipole is in CIAL obstacle-limitation surfaces: https://nocas2.aai.aero/nocas/
6. Lightning and earthing schematic.

**Step 3 — Advertisement permission (s. 272).** Separate application to the Corporation Secretary (Town Planning Standing Committee file). Attach the building permit (or acknowledgement), tax challan, RFID/identification as required by bye-law, and a content policy (no tobacco, no film screening if still banned, auto-dimming affidavit).

City portals:

| City | Civic body | Working entry points |
| --- | --- | --- |
| Kochi | Kochi Municipal Corporation | http://kochicorporation.lsgkerala.gov.in · Citizen service / IBPMS |
| Kozhikode | Kozhikode Municipal Corporation | https://kozhikodecorporation.lsgkerala.gov.in |
| Kannur | Kannur Municipal Corporation | https://kannurcorporation.lsgkerala.gov.in |

**Step 4 — Pay advertisement tax before the permission is signed.** The Secretary cannot grant s. 272 permission if tax is unpaid (s. 272(2)(ii)).

### 1.3 Advertisement tax — formula (Class A vs Class B)

The Kerala Municipality Act does **not** freeze a statewide rupee rate. Each Council notifies a schedule with Government approval. Until you hold the current resolution, budget with the formula below and treat the rates as a **planning envelope** (verify at the Revenue counter; they change by council resolution).

```
Annual tax (₹) = Display area (sq.m) × Zone rate (₹/sq.m/year) × Type factor
```

| Zone | Typical roads in this pilot | Planning rate (static illuminated) | Type factor for digital / LED |
| --- | --- | ---: | ---: |
| Class A | Kochi Edappally bypass, Kakkanad InfoPark corridor, MG Road / Banerji Road class roads | ₹2,500 / sq.m / year | **2.0** → ₹5,000 / sq.m / year |
| Class B | Kozhikode Thondayad, Kannur mall precincts, secondary arterials | ₹1,500 / sq.m / year | **2.0** → ₹3,000 / sq.m / year |

Worked outdoor Kochi dual-face: 32 sq.m × 2 faces × ₹5,000 = **₹3,20,000 / year** (₹26,667 / month).  
Worked outdoor Kozhikode dual-face: 32 × 2 × ₹3,000 = **₹1,92,000 / year**.  
Indoor MUPI (two 55-inch faces ≈ 1.05 sq.m each, treated as illuminated indoor): budget ₹14,400–₹24,000 / year per kiosk.

Illuminated / digital multipliers of 1.5×–2.5× are the industry pattern in Kerala municipal schedules. If the live bye-law prices digital as a lump-sum licence instead of per sq.m, pay the lump sum and keep the per-sq.m figure as a sensitivity in the calculator (`ad_tax_annual_inr` on each `SiteSpec`).

### 1.4 PWD and NHAI (NH 66, state highways, Thondayad, Edappally)

**Inside National Highway RoW: commercial hoardings are prohibited.** MoRTH circulars (including 16 May 2002 and the 2016 reminder) and the Control of National Highways (Land and Traffic) Rules, 2002, treat advertisement structures on NH land as encroachments. Kerala High Court directions (including *D.B. Binu v. State of Kerala* on the Edappally–Vyttila stretch) require Secretaries and NHAI Project Directors to remove illegal boards.

**Siting rule for this pilot:** take a **private plot outside the notified RoW**, then apply IRC:46-1972 / NBC signage rules:

| Rule | Number |
| --- | --- |
| Minimum setback from edge of carriageway | **10 m** (IRC:46). Kerala outdoor-ad policy submissions to the High Court have also used **50 m from road/footpath edge** for certain categories — design to the **stricter** of IRC 10 m and the local PWD/NATPAC condition on the NOC. |
| Distance from junction, bridge, or railway crossing | **100 m** (50 m in built-up urban sections if PWD agrees in writing). |
| Distance from an official traffic sign | **50 m** along the road. |
| Area vs setback (IRC) | Advertisement area ≤ **0.3 sq.m per metre of setback**. A 64 sq.m dual-face equivalent needs a generous setback or an explicit PWD/NHAI relaxation; this is why designated Corporation sites or deep private plots matter. |
| Median / footpath / green strip | **Zero**. Do not bid these. |

**NH 66 NOC workflow**

1. Identify the chainage on the latest NHAI alignment (Edappally / Koonammavu side for Kochi; Ramanattukara–Thondayad for Kozhikode if the plot touches NH).
2. If the plot is **outside RoW**, apply to the **NHAI Project Director, PIU Kozhikode / PIU Kochi** for a no-objection on traffic-safety grounds, with IRC:46 checklist, sight-line drawing, and brightness affidavit. Use NHAI LMS / PIU email as directed by the PIU.
3. If any cable, crane swing, or stay enters RoW, stop — that is an encroachment application and will fail.
4. For **State Highway / PWD** roads (Thondayad Bypass sections not handed to NHAI): apply to the Executive Engineer, PWD Roads, with the same pack plus District Road Safety Council NOC.

### 1.5 KMBR, wind 39 m/s (140 km/h), soil, lightning

IS 875 Part 3 basic wind speed for Kochi, Kozhikode, Thiruvananthapuram, and Kannur region: **Vb = 39 m/s ≈ 140 km/h**. Design example is in the structural certificate template.

Mandatory outdoor pack:

1. Structural design in STAAD/ETABS, steel per IS 800, foundation per IS 456.
2. Geotech: two boreholes, SPT, water table. Coastal / canal sites (Edappally) → raft or piles, not isolated footings in high water table.
3. Importance factor k1 ≥ 1.06; seismic Zone III (IS 1893).
4. Lightning protection IS/IEC 62305 Level III; earth **≤ 2 Ω**.
5. Annual monsoon recertification by 15 May.

### 1.6 KSEB power — LT-VII(A), not LT-VII(C)

**LT-VII(C)** is for cinema, multiplex, auditorium, stadium. A roadside LED plant is **LT-VII(A) Commercial**. Indoor mall taps ride the mall’s commercial connection via sub-meter.

**KSERC tariff used in the calculator** (Gazette order w.e.f. 05 December 2024, three-phase LT-VII(A)):

| Component | Rate |
| --- | --- |
| Fixed charge | **₹190 / kW / month** (three-phase) |
| Energy (non-telescopic) | 0–100 u: ₹6.05 · 0–200: ₹6.80 · 0–300: ₹7.50 · 0–500: ₹8.15 · **above 500: ₹9.40 / kWh** |
| Electricity duty | **10% of energy charges** (Kerala Electricity Duty Act, 1963) |
| Planning fuel / FPPCA buffer | ₹0.50 / kWh |

Outdoor dual-face at 24 kW connected, 65% load factor, 18 h/day lands in the top slab (~8,400 kWh/month) → about **₹96,000 / month** per unipole including duty (see calculator). Sanction **25 kW** dual-face / **15 kW** single-face.

**Application checklist (https://wss.kseb.in)**

1. Online LT new connection, ₹50 application fee.
2. Proof of identity, ownership/consent, GSTIN.
3. Sanctioned load calculation: LED 600–800 W/sq.m peak × area × faces × 0.8 diversity + controller 0.5 kW + lighting 0.2 kW.
4. Test report from a licensed electrical contractor; ELCB, SPD, earthing drawing.
5. Security deposit and service-line estimate per KSERC cost data.
6. Electrical Inspectorate: advertising / neon-class installations and connected load in this range go through https://ceisuraksha.ceikerala.gov.in for scheme approval and sanction for energisation (Kannur Inspectorate explicitly lists neon sign boards).
7. Meter: three-phase static meter, **ToD-capable**, so that if KSEB extends ToD to this LT commercial node you do not replace hardware. Dual-tariff / ToD is not universally applied to LT-VII(A) today; specify it in the application as a future-proof requirement.

Mall indoor: 0.55 kW, 14 h, 20% mall markup → about **₹2,100 / month** per kiosk.

---

## MODULE 2 — Hardware Sourcing & Procurement

### 2.A China OEM (Shenzhen cluster)

| OEM | URL | Why they are on this shortlist |
| --- | --- | --- |
| Unilumin | https://www.unilumin.com | Ushin / Usurface outdoor, IP66, marine coating options |
| Absen | https://www.absen.com | A-series outdoor advertising, strong India service footprint |
| Leyard / Planar | https://www.leyard.com | Custom high-brightness outdoor |
| LianTronics | https://www.liantronics.com | High-reliability outdoor cabinets |
| Apexls | http://www.apexls.com | Custom kiosks and outdoor panels; typically keener FOB |

**Commercial posture:** `base` scenario prices **USD 650 / sq.m FOB** (flagship IP66, 5,500 nits, spare kit). `target` scenario prices **USD 330 / sq.m FOB** (volume A-series / Apexls CKD with the same IP and coating spec — only award if FAT in `docs/procurement/QC_AND_IMPORT_CHECKLIST.md` passes). Do not buy “P3.91 outdoor” without salt-spray data.

**HS codes and duty (planning)**

Complete advertising video walls are **Heading 8528**. Prefer **CTH 8528 52 00** (monitors capable of connecting to an ADP machine / player) where CESTAT / CAAR support exists for LED monitor tiles. Customs may reclass to **8528 59 00** (“other monitors”, **20% BCD**). Do not use 8531 (indicator panels) for video walls.

Duty stack on 8528 52 00 used in the calculator:

```
BCD  = 10% of CIF
AIDC = 10% of BCD
SWS  = 10% of (BCD + AIDC)
IGST = 18% of (CIF + BCD + AIDC + SWS)
Economic cost (ITC of IGST claimed) = BCD + AIDC + SWS = 12.1% of CIF
Cash at port                      = 12.1% + IGST ≈ 32.3% of CIF
```

Run `--conservative-hs` to force 20% BCD. File an advance ruling (CAAR Mumbai) if the first container is > USD 80,000.

**Logistics:** FCL 40' Shekou / Yantian / Nansha → **INCOK, ICTT Vallarpadam** (DP World). CHA files BE on https://www.icegate.gov.in. Port: https://www.cochinport.gov.in · terminal: https://www.dpworld.com/en/ports-terminals/india/ictt/services. Do not destuff in rain.

### 2.B India stockists and kiosk fabricators

| Vendor | URL | Use |
| --- | --- | --- |
| Vishwanjali Technology | https://www.vishwanjali.com | Cabinet assembly, indoor/outdoor LED |
| Elpro Technologies | https://www.elprotech.in | Standees and indoor/outdoor kiosks |
| Matrix Digital Corporation | https://www.matrixdisplaysystem.com | Modules, PSU, die-cast cabinets |
| Pixel LED India | https://www.pixelledindia.com | Receiving cards, NovaStar, emergency modules |
| Mean Well India | https://www.meanwell.in | HLG/ELG weatherproof PSU |

**Split buy:** import LED modules + receiving cards; fabricate unipoles and MUPI shells in Kochi (IS 2062 steel, Akzo/Jotun C5-M paint system); buy Mean Well locally for 7-year replacement. Hold a spare kit in a **dry Kochi warehouse**, never on the unipole walkway.

Controllers: NovaStar Taurus **TB60** outdoor, **TB30** indoor. CMS: https://pisignage.com or VNNOX https://www.vnnox.com. Programmatic: https://www.hivestack.com · https://lemmatechnologies.com.

---

## MODULE 3 — Site Leasing & Mall Pitch

### 3.1 Pitch deck for HiLite, Lulu, Forum, Gokulam, Secura (12 slides)

1. **Cover** — Kerala coastal DOOH, six-node pilot, Kochi HQ.
2. **Why this mall** — catchment (Lulu: regional + tourist; HiLite: Malabar affluent; Secura/Capitol: Kannur city).
3. **Product** — dual-face 55" 3,000 nit, 8 mm glass, 1.2 × 1.2 m footprint, silent, no audio by default.
4. **Look & feel** — Spectrum of night/day renders in the actual atrium (commission a local 3D artist; do not pitch generic Shenzhen photos).
5. **Mall inventory** — 12% reserved loop for mall events (Clause 8 of the MoU).
6. **Safety** — ELCB, SPD, toughened glass, fire-load letter, night install window.
7. **Power** — sub-meter, 20% cap on markup, no phantom HVAC lump sum.
8. **Commercial** — hybrid: Minimum Guarantee + 18% of kiosk gross, whichever higher.
9. **Content standards** — no tobacco, brightness caps, proof-of-play portal login for the mall GM.
10. **Insurance** — ₹2 Cr public liability, mall as additional insured.
11. **Case references** — Indian mall DOOH comps (keep honest; Kochi digital is still young).
12. **Ask** — 36-month licence, 18-month lock-in, 3-month deposit, LOI in 21 days.

Outdoor landowner pitch is shorter: private plot, outside RoW, 18% or hybrid with ₹80,000 / ₹45,000 floor, monsoon indemnity, crane access four times a year.

Full clause set: [`docs/legal/SITE_LEASE_AND_MOU.md`](legal/SITE_LEASE_AND_MOU.md).

### 3.2 Deal physics (why hybrid)

A Lulu kiosk at ₹8,500 × 12 slots × 75% occupancy yields ~₹81,000 / month. A ₹75,000 fixed rent leaves almost nothing after power and CMS. Hybrid floors (₹20,000–₹40,000 indoor, ₹45,000–₹80,000 outdoor) plus 18% of gross keep the mall/owner whole in a good month without killing the pilot. The calculator’s `--lease-model hybrid|fixed|revshare` switches this live.

---

## MODULE 4 — Financial Model & ROI

Inventory assumption: **10-second spots in a 100-second loop** = 10 slots per outdoor face × 2 faces = 20 outdoor slots; indoor 6 slots × 2 faces = 12 slots.

Rate card (as specified):

| Inventory | ₹ / slot / month |
| --- | ---: |
| Kochi outdoor | 50,000 |
| Kozhikode outdoor | 30,000 |
| Mall MUPI (all three cities) | 8,500 |

Theoretical 100% direct capacity = **₹20.08 lakh / month**.

### 4.1 CAPEX — `base` (premium import, USD 650/sq.m, dual-face)

Economic CAPEX **₹1.95 Cr**. IGST cash at port **₹15.1 lakh** (ITC). Cash build **₹2.10 Cr**.

| Line | ₹ |
| --- | ---: |
| Outdoor LED FOB (4 faces × 32 sq.m) | 69,88,800 |
| Freight + insurance + ICTT | 4,80,000 |
| BCD + AIDC + SWS | 9,03,725 |
| Unipole, foundation, soil, PE | 40,94,000 |
| Electrical, SPD, lightning | 7,56,000 |
| KSEB 3-ph connection | 5,50,000 |
| NovaStar + player + 4G | 4,62,000 |
| K-SWIFT / municipal / PWD year-1 | 5,00,000 |
| Outdoor install + 72 h burn-in | 4,50,000 |
| Indoor 55" pairs (4 kiosks) | 8,80,000 |
| MUPI fabrication | 7,40,000 |
| Indoor player + install | 4,00,000 |
| CMS + Lemma/Hivestack hook | 2,50,000 |
| Spares warehouse | 6,30,000 |
| Contingency 8% | 14,46,762 |
| **Economic total** | **1,95,31,287** |

### 4.2 OPEX and revenue — `base` (75% occupancy, 35% programmatic fill of unsold at 55% of direct CPM)

| | ₹ / month |
| --- | ---: |
| Fixed (hybrid leases, KSEB, tax, CMS, 4.5% AMC, ops ₹60k, insurance ₹15k) | 7,68,434 |
| Sales commission 10% | 1,60,264 |
| **OPEX** | **9,28,698** |
| Direct sold | 15,06,000 |
| Programmatic | 96,635 |
| **Gross revenue** | **16,02,635** |
| Kochi / Kozhikode / Kannur | 9.61 L / 5.60 L / 0.81 L |
| **EBITDA** | **6,73,937** |
| Net operating margin | **42.1%** |
| Simple payback | **29.0 months** |
| Annual ROI on economic CAPEX | **41.4%** |
| Direct occupancy breakeven | **22%** |

Outdoor KSEB is the second-largest site cost after lease (~₹96,000 / unipole / month). Auto-dimming is a P&L control, not just a safety feature.

### 4.3 `target` stack — 12–16 month payback (15.9 months in the calculator)

The specified rate card **cannot** repay a USD 650/sq.m dual-face import in 16 months without occupancy and hardware changes. The `target` scenario is the execution path that does:

1. Volume OEM / CKD FOB **USD 330 / sq.m** with the same FAT (not a spec downgrade on IP or nits).
2. **90%** direct occupancy (two national retainers + local jewellery / education / healthcare / QSRs pre-sold before energisation).
3. In-house sales, commission **6%**.
4. AMC **3.5%** (own technician + Pixel LED / Mean Well India spares).

Result: economic CAPEX **₹1.54 Cr**, gross revenue **₹18.57 lakh / month**, EBITDA **₹9.69 lakh / month**, margin **52.2%**, payback **15.9 months**, annual ROI **75.7%**.

### 4.4 Programmatic

Unsold loop time is offered to Hivestack / Lemma at **55% of the direct slot CPM**. Fill 35% (`base`) or 45% (`target`) of unsold. Do not cannibalise direct by opening programmatic until occupancy is below 85% or the slot is inside 72 hours of play. Proof-of-play logs are the audit trail for both mall revenue-share and SSPs.

GST 18% on advertising (SAC 9983) is treated as a pass-through and is **not** inside EBITDA.

---

## MODULE 5 — Technical Deployment & Weather Hardening

Kerala’s design enemies are **salt (Kochi backwaters, Kozhikode coast), 3,000 mm rain, 90% RH, and 39 m/s gusts**, not desert heat.

### 5.1 Cabinets and coating

| Choice | Spec |
| --- | --- |
| Cabinet | Die-cast aluminium, not iron. Iron rusts through a monsoon even with powder coat. |
| Gasket | EPDM, continuous, no splices at corners. |
| Fasteners | A4 / 316 stainless, anti-seize on threads. |
| Paint | ISO 12944 C5-M, zinc-rich primer + epoxy + PU, DFT ≥ 240 µm on the unipole. |
| PCB coat | **Silicone (SR)** IPC-CC-830, not acrylic. Acrylic micro-cracks in salt air. |
| Modules | Rear-service, IP65, conformal-coated driver ICs, potting on power plugs. |
| Drains | Two weep holes per cabinet, insect mesh, never silicone-sealed shut. |

Indoor kiosks: 8 mm toughened glass, powder-coated aluminium frame, hidden 120 mm fans with G4 filters, condensate path away from PSUs. Mall AC is not a substitute for a sealed player enclosure.

### 5.2 Electrical safety

1. TT earthing, two pits minimum, **≤ 2 Ω**, 3 m apart, inspected every April and September.
2. **Class II SPD** (Type 2, 40 kA 8/20) at the LT incomer; Type 3 at the player.
3. **ELCB / RCCB 100 mA** incoming, 30 mA on socket/player circuit.
4. Lightning IS/IEC 62305 Level III, down-conductor not shared with data screen.
5. Mean Well HLG, derate 20% below nameplate in 40 °C cabinet.
6. No outdoor transformers in Corporation limits (Kerala Electrical Inspectorate guidelines). Stay on KSEB LT.

### 5.3 Controllers, CMS, failover

```
Brand MP4 ──► PiSignage / VNNOX cloud ──► HTTPS ──► TB60 (outdoor) / TB30 (indoor)
                                              │
                                              ├─ 4G primary (Jio) + 4G failover (Airtel)
                                              ├─ local SSD: last-known 100-second loop (6 creatives)
                                              └─ watchdog: if cloud > 90 s unreachable → play /offline/loop/
```

Failover logic (implement in the player agent):

1. Heartbeat to CMS every 30 s.
2. If 3 consecutive misses, freeze the current playlist from local cache; do **not** show a black frame or an OS desktop.
3. If cache is empty, play a licensed public-service still (monsoon helpline / 112) — never a competitor or political creative.
4. When the link returns, do not interrupt a 10-second spot; splice at the next loop boundary.
5. Proof-of-play continues locally (CSV + hash) and uploads in catch-up; this is what Lemma/Hivestack and mall auditors will demand.

Brightness: light sensor on the **north** face, 5,500 nits cap day, 600 nits after 22:00, 15% per minute ramp. Log nits with proof-of-play.

NovaStar: https://www.novastar.tech · PiSignage: https://pisignage.com · VNNOX: https://www.vnnox.com.

---

## MODULE 6 — Automated Execution Script

The calculator is `dooh_kerala_calculator.py` at the repository root (Python 3.10+, stdlib only).

```bash
python3 dooh_kerala_calculator.py --scenario base
python3 dooh_kerala_calculator.py --scenario target
python3 dooh_kerala_calculator.py --scenario conservative --conservative-hs
python3 dooh_kerala_calculator.py --occupancy 0.8 --lease-model revshare --outdoor-faces 1
python3 dooh_kerala_calculator.py --json --out /tmp/dooh.json
python3 -m unittest tests.test_dooh_kerala_calculator -v
```

| Flag | Effect |
| --- | --- |
| `--scenario base\|target\|optimistic\|conservative` | Occupancy, programmatic fill, FOB, commission, AMC |
| `--occupancy 0–1` | Direct sold share of loop |
| `--programmatic-fill 0–1` | Share of *unsold* inventory sent to SSPs |
| `--kochi-slot` `--kozhikode-slot` `--mall-slot` | Rate card |
| `--lease-model hybrid\|fixed\|revshare` | 18% / floors |
| `--outdoor-faces 1\|2` | Single vs dual unipole |
| `--fob-usd` | LED FOB |
| `--commission` | Sales commission |
| `--usd-inr` | FX |
| `--conservative-hs` | 20% BCD under 8528 59 00 |

Formulas (same as the script):

```
kWh          = kW_connected × load_factor × hours/day × 30
energy       = kWh × LT-VII(A) non-telescopic slab rate
power_bill   = energy + (190 × sanction_kW) + 0.10×energy + 0.50×kWh
site_revenue = occupancy×slots×price + (1−occupancy)×slots×price×prog_fill×0.55
lease        = max(minimum_guarantee, 0.18 × site_revenue)   # hybrid
EBITDA       = Σ site_revenue − leases − power − tax − CMS − AMC − ops − insurance − commission
payback      = economic_CAPEX / monthly_EBITDA
ROI_annual   = 12 × EBITDA / economic_CAPEX
```

---

## 90-day mobilisation (outdoor first)

| Week | Action |
| --- | --- |
| 1–2 | Incorporate, GST, IEC, K-SWIFT login, shortlist two Kochi plots **outside NH RoW**, issue mall LOIs |
| 3–4 | Geotech + topographic survey + IRC setback drawing; file IBPMS + s. 272; start KSEB WSS |
| 5–6 | FAT at OEM or India assembler; book 40' to Vallarpadam; Structural Engineer certificate |
| 7–8 | Inspectorate scheme; unipole fabrication in Kochi; mall kiosk mock-up sign-off |
| 9–10 | Foundation + earth pits before monsoon (do not open foundations after 1 June) |
| 11–12 | Cabinet hang, 72 h burn-in, CMS + programmatic tag, first paid loop |

If the calendar hits June before foundations are cast, **slip outdoor to September** and go live on the four indoor kiosks first. A half-built unipole in a Kerala monsoon is a High Court case waiting to happen.

---

## Document map

| File | Role |
| --- | --- |
| `docs/legal/SITE_LEASE_AND_MOU.md` | Full clause set (hybrid rent, KSEB, 12% mall loop, monsoon indemnity) |
| `docs/legal/STRUCTURAL_STABILITY_CERTIFICATE.md` | IS 875 39 m/s sign-off |
| `docs/procurement/QC_AND_IMPORT_CHECKLIST.md` | FAT, salt spray, ICEGATE |
| `dooh_kerala_calculator.py` | Live P&L |

Rates cited: KSERC LT-VII(A) Gazette 05-Dec-2024; Kerala Electricity Duty Act 1963 (10%); IS 875 Part 3 Vb 39 m/s; IRC:46-1972; Kerala Municipality Act ss. 271–272; CBIC heading 8528. Confirm before money moves.
