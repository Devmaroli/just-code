#!/usr/bin/env python3
"""Build the building-mounted outdoor cost estimate + SWOT PDF."""

from __future__ import annotations

from pathlib import Path

from weasyprint import CSS, HTML

ROOT = Path(__file__).resolve().parents[1]
OUT_PDF = ROOT / "docs" / "Kerala_DOOH_Cost_Estimate_and_SWOT.pdf"

FONT_SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
FONT_SANS_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
FONT_SANS_ITALIC = "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"

CSS_TEXT = f"""
@font-face {{
  font-family: ReportSans;
  src: url("file://{FONT_SANS}");
  font-weight: 400;
}}
@font-face {{
  font-family: ReportSans;
  src: url("file://{FONT_SANS_BOLD}");
  font-weight: 700;
}}
@font-face {{
  font-family: ReportSans;
  src: url("file://{FONT_SANS_ITALIC}");
  font-style: italic;
}}

:root {{
  --ink: #1b2430;
  --muted: #4a5563;
  --rule: #c5a572;
  --band: #0f3d3e;
  --paper: #f7f3ea;
  --s: #1f6b4a;
  --w: #8a5a12;
  --o: #1a5276;
  --t: #8b2e2e;
}}

* {{ box-sizing: border-box; }}
html, body {{
  margin: 0;
  padding: 0;
  color: var(--ink);
  font-family: ReportSans, "Liberation Sans", sans-serif;
  font-size: 10pt;
  line-height: 1.42;
}}

@page {{
  size: A4;
  margin: 16mm 15mm 18mm 15mm;
  @top-left {{
    content: "Kerala outdoor DOOH  ·  Building-mounted cost pack";
    font-size: 8pt;
    color: #5c6570;
    font-family: ReportSans, sans-serif;
  }}
  @top-right {{
    content: "Confidential working paper";
    font-size: 8pt;
    color: #5c6570;
    font-family: ReportSans, sans-serif;
  }}
  @bottom-left {{
    content: "Cost estimate + SWOT  |  September 2026";
    font-size: 8pt;
    color: #5c6570;
    font-family: ReportSans, sans-serif;
  }}
  @bottom-right {{
    content: "Page " counter(page);
    font-size: 8pt;
    color: #5c6570;
    font-family: ReportSans, sans-serif;
  }}
}}
@page :first {{
  margin: 0;
  @top-left {{ content: none; }}
  @top-right {{ content: none; }}
  @bottom-left {{ content: none; }}
  @bottom-right {{ content: none; }}
}}

.cover {{
  min-height: 297mm;
  background: var(--band);
  color: #f7f3ea;
  padding: 26mm 22mm 20mm 22mm;
  break-after: page;
}}
.cover-kicker {{
  letter-spacing: 0.26em;
  text-transform: uppercase;
  font-size: 8.5pt;
  color: var(--rule);
  margin-bottom: 16mm;
}}
.cover h1 {{
  font-size: 26pt;
  line-height: 1.12;
  margin: 0 0 7mm 0;
  color: #f7f3ea;
  border: none;
  max-width: 155mm;
}}
.cover .sub {{
  font-size: 12pt;
  color: #d7c4a3;
  margin: 0 0 14mm 0;
  max-width: 155mm;
}}
.cover-meta {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 5mm 12mm;
  border-top: 1px solid #2c6a6b;
  padding-top: 7mm;
  font-size: 10pt;
}}
.cover-meta span {{
  display: block;
  color: var(--rule);
  font-size: 7.5pt;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  margin-bottom: 1.2mm;
}}
.cover-kpis {{
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 4mm;
  margin: 14mm 0 0 0;
}}
.cover-kpis div {{
  border: 0.6pt solid #2c6a6b;
  padding: 4mm;
}}
.cover-kpis span {{
  display: block;
  font-size: 7.5pt;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--rule);
}}
.cover-kpis strong {{
  display: block;
  font-size: 13pt;
  margin-top: 1.5mm;
  color: #f7f3ea;
}}
.cover-foot {{
  position: absolute;
  bottom: 16mm;
  left: 22mm;
  right: 22mm;
  font-size: 8pt;
  color: #c9d6d6;
  border-top: 1px solid #2c6a6b;
  padding-top: 5mm;
}}

h1 {{
  color: var(--band);
  font-size: 16pt;
  margin: 0 0 5mm 0;
  padding-bottom: 2.5mm;
  border-bottom: 2px solid var(--rule);
}}
h2 {{
  color: var(--band);
  font-size: 12pt;
  margin: 7mm 0 3mm 0;
  padding-bottom: 1.2mm;
  border-bottom: 0.5pt solid #d8c7a8;
}}
h3 {{
  color: var(--band);
  font-size: 10.5pt;
  margin: 4.5mm 0 2mm 0;
}}
p {{ margin: 0 0 2.8mm 0; }}
ul {{ margin: 0 0 3mm 0; padding-left: 5mm; }}
li {{ margin-bottom: 1.1mm; }}
.section {{ break-before: page; }}
h2 {{ page-break-after: avoid; }}
h3 {{ page-break-after: avoid; }}

table {{
  width: 100%;
  border-collapse: collapse;
  margin: 2mm 0 4.5mm 0;
  font-size: 8.5pt;
}}
thead {{ display: table-header-group; }}
tr {{ page-break-inside: avoid; }}
th {{
  background: var(--band);
  color: #f7f3ea;
  text-align: left;
  padding: 2mm 2.2mm;
}}
td {{
  padding: 1.7mm 2.2mm;
  border-bottom: 0.4pt solid #d7ddd8;
  vertical-align: top;
}}
td.num, th.num {{ text-align: right; }}
tr:nth-child(even) td {{ background: #f4f1e8; }}
tr.total td {{
  background: #0f3d3e !important;
  color: #f7f3ea;
  font-weight: 700;
}}
.note {{
  font-size: 8.3pt;
  color: var(--muted);
  margin: -1mm 0 4mm 0;
}}
.callout {{
  background: var(--band);
  color: #f7f3ea;
  padding: 4.5mm 5.5mm;
  margin: 0 0 5mm 0;
}}
.callout h3 {{
  color: var(--rule);
  margin: 0 0 1.5mm 0;
  font-size: 8.5pt;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}}
.callout p {{ margin: 0; font-size: 9.5pt; }}

.swot {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4mm;
  margin-top: 2mm;
}}
.swot-box {{
  border: 0.7pt solid #d8c7a8;
  padding: 4mm 4.5mm;
  break-inside: avoid;
}}
.swot-box h3 {{
  margin: 0 0 2.5mm 0;
  font-size: 10pt;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}}
.swot-box.s h3 {{ color: var(--s); }}
.swot-box.w h3 {{ color: var(--w); }}
.swot-box.o h3 {{ color: var(--o); }}
.swot-box.t h3 {{ color: var(--t); }}
.swot-box ul {{ padding-left: 4.2mm; margin: 0; font-size: 8.6pt; }}
.swot-box li {{ margin-bottom: 1.6mm; }}

.disclaimer {{
  font-size: 8pt;
  color: var(--muted);
  border-top: 0.6pt solid #d8c7a8;
  padding-top: 3mm;
  margin-top: 5mm;
}}
"""

HTML_DOC = r"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="utf-8"/><title>Kerala Outdoor DOOH — Cost Estimate and SWOT</title></head>
<body>

<section class="cover">
  <div class="cover-kicker">Confidential · Working paper · Planning rates as of September 2026</div>
  <h1>Outdoor digital advertising</h1>
  <p class="sub">Building-mounted LED — detailed cost estimate, rent, regulatory cash, and SWOT for a first Kochi site (Edappally / Kakkanad class sightline).</p>
  <div class="cover-meta">
    <div><span>Model</span>Rent a commercial building. You pay screen + structure + filings. Landlord provides terrace or facade.</div>
    <div><span>Recommended first asset</span>One 8 m × 4 m (32 sq.m) road-facing P3.91 / P4 face, volume OEM, IP65, ≥ 5,500 nits.</div>
    <div><span>Not included in hardware</span>Ground unipole, pile foundation, new KSEB service line, land purchase.</div>
    <div><span>Date</span>07 September 2026 · Kochi · Kozhikode · Kannur</div>
  </div>
  <div class="cover-kpis">
    <div><span>Hardware to switch on</span><strong>₹31 lakh</strong></div>
    <div><span>Admin + tax year-0</span><strong>₹5–8 lakh</strong></div>
    <div><span>Cash to be live</span><strong>₹38–45 lakh</strong></div>
  </div>
  <div class="cover-foot">
    Advertisement tax, stamp duty, KSEB tariff and customs BCD must be confirmed against the live gazette and the Corporation schedule before capital is committed. This is not a legal opinion or a quotation from an OEM.
  </div>
</section>

<section>
  <h1>1. How the cost is split</h1>
  <div class="callout">
    <h3>Read this first</h3>
    <p>Three wallets: (A) one-time screen and structure, (B) monthly rent to the building, (C) government and professional filings. Mall kiosks are a different product and are not costed here. A land unipole is ~₹90 lakh; a rented building cuts that to ~₹31 lakh of hardware because you do not build a 15 m pole or piles.</p>
  </div>
  <table>
    <thead>
      <tr><th>Wallet</th><th>Who</th><th>When</th><th class="num">Planning amount</th></tr>
    </thead>
    <tbody>
      <tr><td>A. Digital screen + building structure + electrics</td><td>You</td><td>Once</td><td class="num">₹29 L economic / ₹31 L cash</td></tr>
      <tr><td>B. Space rent (terrace / facade rights)</td><td>You → landlord</td><td>Monthly</td><td class="num">₹50,000 floor or 18% of ads</td></tr>
      <tr><td>C. Admin, lawyers, engineers, year-1 tax</td><td>You</td><td>Year 0</td><td class="num">₹5–8 L</td></tr>
      <tr><td>D. Landlord deposit</td><td>You (refundable)</td><td>At signing</td><td class="num">3–6 months’ rent (₹1.5–6 L)</td></tr>
      <tr><td>E. Power, CMS, AMC, tax after go-live</td><td>You</td><td>Monthly</td><td class="num">₹75,000–₹90,000 besides rent</td></tr>
      <tr class="total"><td>Cash to be live (A + C + D, recommended site)</td><td>You</td><td>Before first loop</td><td class="num">₹38–45 lakh</td></tr>
    </tbody>
  </table>
  <p class="note">Recommended site = one 32 sq.m face, volume OEM at about USD 330 / sq.m FOB, commercial building, Kochi Class A sightline. IGST paid at Cochin Port is claimed as ITC and is inside the ₹31 L cash figure (~₹2.1 L).</p>
</section>

<section>
  <h1>2. One-time hardware — three formats</h1>
  <p>All figures are economic CAPEX (IGST excluded from the total, shown separately as cash). USD/INR 84. Customs on CTH 8528 52 00: BCD 10% + AIDC + SWS ≈ 12.1% of CIF. Conservative reclass to 8528 59 00 (20% BCD) would add roughly ₹1.0–1.3 L on a single 32 sq.m face.</p>
  <table>
    <thead>
      <tr>
        <th>Cost bucket</th>
        <th class="num">Compact 6×3 m<br/>18 sq.m, 1 face</th>
        <th class="num">Recommended 8×4 m<br/>32 sq.m, 1 face</th>
        <th class="num">Dual-face rooftop<br/>2 × 32 sq.m</th>
      </tr>
    </thead>
    <tbody>
      <tr><td><strong>A. Digital screen</strong> (LED FOB + freight + BCD/AIDC/SWS)</td><td class="num">₹6.9 L</td><td class="num">₹11.6 L</td><td class="num">₹22.6 L</td></tr>
      <tr><td><strong>B. Structure on the building</strong> (steel, anchors, walkway, waterproofing)</td><td class="num">₹4.5 L</td><td class="num">₹6.5 L</td><td class="num">₹9.5 L</td></tr>
      <tr><td><strong>C. Setup</strong> (electrical, SPD, earth, sub-meter, NovaStar, install, licence pack, spares, 8% buffer)</td><td class="num">₹8.3 L</td><td class="num">₹10.9 L</td><td class="num">₹15.7 L</td></tr>
      <tr class="total"><td>Economic total</td><td class="num">₹20 L</td><td class="num">₹29 L</td><td class="num">₹48 L</td></tr>
      <tr><td>IGST at port (GST credit)</td><td class="num">₹1.2 L</td><td class="num">₹2.1 L</td><td class="num">₹4.1 L</td></tr>
      <tr class="total"><td>Cash to switch the screen on</td><td class="num">₹21 L</td><td class="num">₹31 L</td><td class="num">₹52 L</td></tr>
    </tbody>
  </table>
  <p>Premium cabinets (Unilumin / Absen class, ~USD 650 / sq.m) add about <strong>₹10 lakh</strong> on the 32 sq.m single face (economic ~₹39 L, cash ~₹43 L). Not required for site one if factory FAT (IP65, 5,500 nits, salt spray, 72-hour burn-in) is passed.</p>
  <p>Dual-face is worth the extra LED bill only if <em>both</em> directions have paying traffic. Otherwise buy one road-facing face.</p>

  <h2>2.1 Recommended 32 sq.m, one face — line by line</h2>
  <table>
    <thead><tr><th>Split</th><th>Item</th><th class="num">₹</th></tr></thead>
    <tbody>
      <tr><td>Screen</td><td>LED cabinets FOB (32 sq.m × USD 330 × 84)</td><td class="num">8,87,000</td></tr>
      <tr><td>Screen</td><td>Sea freight + insurance to ICTT Vallarpadam</td><td class="num">1,50,000</td></tr>
      <tr><td>Screen</td><td>Customs BCD + AIDC + SWS</td><td class="num">1,25,000</td></tr>
      <tr><td>Structure</td><td>Terrace / facade steel frame, chemical anchors, walkway, waterproofing make-good</td><td class="num">6,50,000</td></tr>
      <tr><td>Setup</td><td>LT panel, Class II SPD, ELCB, earthing ≤ 2 Ω</td><td class="num">1,80,000</td></tr>
      <tr><td>Setup</td><td>Building sub-meter / commercial power tap</td><td class="num">80,000</td></tr>
      <tr><td>Setup</td><td>NovaStar TB60 + industrial player + dual-SIM 4G</td><td class="num">1,65,000</td></tr>
      <tr><td>Setup</td><td>Structural PE certificate + year-1 advertisement licence pack</td><td class="num">1,50,000</td></tr>
      <tr><td>Setup</td><td>Hoist / crane, install, 72-hour burn-in</td><td class="num">1,20,000</td></tr>
      <tr><td>Setup</td><td>Spare modules + Mean Well PSU</td><td class="num">1,80,000</td></tr>
      <tr><td>Setup</td><td>Contingency 8%</td><td class="num">2,15,000</td></tr>
      <tr class="total"><td></td><td>Economic CAPEX</td><td class="num">29,02,000</td></tr>
      <tr><td></td><td>IGST cash at port (ITC)</td><td class="num">2,09,000</td></tr>
      <tr class="total"><td></td><td>Cash to switch on</td><td class="num">31,11,000</td></tr>
    </tbody>
  </table>
  <p class="note">Rounded to the nearest thousand. Hardware licence pack in this table is the OEM/file bundle; full lawyer + tax cash is in Section 4 so it is not double-counted in the ₹38–45 L live figure.</p>
</section>

<section>
  <h1>3. Renting cost (monthly, to the building)</h1>
  <p>This is the lease for the wall or terrace — not the screen. Sign a <strong>hybrid</strong>: minimum guarantee or 18% of that board’s Gross Advertising Revenue, whichever is higher. Register the licence if the term exceeds 11 months (Kerala Stamp Act + Registration Act).</p>
  <table>
    <thead>
      <tr><th>Location quality</th><th class="num">Fixed rent / month</th><th>Revenue share alternative</th><th>Deposit</th></tr>
    </thead>
    <tbody>
      <tr><td><strong>Kochi Class A</strong> — Edappally, Kakkanad, Vyttila, MG / Banerji sightline</td><td class="num">₹70,000–₹1,20,000</td><td>15–18% of board ads</td><td>3–6 months</td></tr>
      <tr><td><strong>Kochi Class B</strong> — good road, weaker sightline</td><td class="num">₹35,000–₹60,000</td><td>12–15%</td><td>3 months</td></tr>
      <tr><td><strong>Kozhikode</strong> — Thondayad / city arterial</td><td class="num">₹40,000–₹80,000</td><td>15–18%</td><td>3–6 months</td></tr>
      <tr><td><strong>Kannur</strong> — commercial building</td><td class="num">₹20,000–₹40,000</td><td>12–15%</td><td>3 months</td></tr>
    </tbody>
  </table>
  <h3>Recommended first contract (Kochi Class A)</h3>
  <table>
    <thead><tr><th>Term</th><th>Detail</th></tr></thead>
    <tbody>
      <tr><td>Model</td><td>Hybrid: <strong>₹50,000 minimum or 18% of ads</strong>, whichever higher, plus GST</td></tr>
      <tr><td>Lock-in</td><td>18 months inside a 36-month licence</td></tr>
      <tr><td>Deposit</td><td>3 months of the minimum (₹1.50 L), interest-free, refundable on make-good</td></tr>
      <tr><td>Power</td><td>Commercial sub-meter; markup on KSEB energy <strong>capped at 20%</strong></td></tr>
      <tr><td>Worked rent at 75% sold</td><td>Revenue ₹3.75 L × 18% = <strong>₹67,500 / month</strong></td></tr>
      <tr><td>Worked rent if unsold</td><td>Floor <strong>₹50,000 / month</strong></td></tr>
    </tbody>
  </table>
  <p>Do not take ₹1.5 lakh fixed rent on a dark screen. If the owner wants equity instead of rent: owner gives space + deposit waived; you put in the ₹31 L hardware; split ads <strong>70/30 or 80/20 in your favour</strong> in year 1.</p>

  <h2>3.1 Other monthly costs (not rent, still yours)</h2>
  <table>
    <thead><tr><th>Item</th><th class="num">32 sq.m, 1 face</th><th class="num">Dual-face rooftop</th></tr></thead>
    <tbody>
      <tr><td>Electricity (building bill + ~20% markup), 18 h, auto-dim</td><td class="num">₹50,000–₹60,000</td><td class="num">~₹1,00,000</td></tr>
      <tr><td>CMS + 4G</td><td class="num">₹3,500</td><td class="num">₹3,500</td></tr>
      <tr><td>Local technician / AMC</td><td class="num">₹8,000–₹12,000</td><td class="num">₹12,000–₹18,000</td></tr>
      <tr><td>Advertisement tax (planning)</td><td class="num">~₹13,000 Class A</td><td class="num">~₹26,000 Class A</td></tr>
      <tr class="total"><td>Total besides rent</td><td class="num">₹75,000–₹90,000</td><td class="num">₹1.4–1.5 L</td></tr>
    </tbody>
  </table>
  <p>All-in monthly (rent + power + tax + upkeep), Kochi Class A, one face: <strong>₹1.2–2.0 lakh</strong> depending on whether the hybrid rent is on the floor or on 18% of a full loop.</p>
</section>

<section>
  <h1>4. Administrative and regulatory cash</h1>
  <p>Renting a building does <strong>not</strong> skip ss. 271–272 of the Kerala Municipality Act. You skip piles and a roadside pole. You still need the Secretary’s written permission, tax, a structural certificate on <em>that building</em>, commercial power, and usually an Inspectorate file. Highway-facing facades still attract PWD / NHAI.</p>

  <h2>4.1 One-time filings and professionals</h2>
  <table>
    <thead><tr><th>Item</th><th class="num">Typical ₹</th><th>Time</th></tr></thead>
    <tbody>
      <tr><td>Company + GSTIN + current account</td><td class="num">20,000–40,000</td><td>2 weeks</td></tr>
      <tr><td>IEC (only if importing LED)</td><td class="num">3,000–10,000</td><td>1–2 weeks</td></tr>
      <tr><td>Advocate: title check + leave-and-licence</td><td class="num">40,000–80,000</td><td>2–3 weeks</td></tr>
      <tr><td>Stamp + registration of 36-month licence (~5% of average annual rent)</td><td class="num">40,000–70,000</td><td>1–2 weeks</td></tr>
      <tr><td>Structural audit of existing building + LED frame design</td><td class="num">75,000–1,50,000</td><td>2–4 weeks</td></tr>
      <tr><td>IBPMS / KMBR drawings + scrutiny</td><td class="num">40,000–1,00,000</td><td>30–60 days</td></tr>
      <tr><td>Advertisement file, miscellaneous Corporation fees</td><td class="num">10,000–25,000</td><td>with s. 272</td></tr>
      <tr><td>Electrical Inspectorate scheme + inspection</td><td class="num">8,000–25,000</td><td>15–30 days</td></tr>
      <tr><td>KSEB commercial sub-meter / load paperwork</td><td class="num">10,000–80,000</td><td>15–45 days</td></tr>
      <tr><td>AAI NOCAS (if roof enters CIAL surfaces)</td><td class="num">15,000–50,000</td><td>15–45 days</td></tr>
      <tr><td>PWD / Road Safety / NHAI pack (if the face addresses a highway)</td><td class="num">15,000–40,000</td><td>30–90 days</td></tr>
      <tr><td>Year-1 public liability (₹2 Cr) + equipment insurance</td><td class="num">20,000–40,000</td><td>1 week</td></tr>
      <tr class="total"><td>Professionals + filings, excluding advertisement tax</td><td class="num">₹3–6 L (use ₹4.5 L)</td><td></td></tr>
      <tr><td>Year-1 advertisement tax — Class A digital 32 sq.m × ₹5,000</td><td class="num"><strong>₹1.60 L</strong></td><td>Pay before permission</td></tr>
      <tr class="total"><td>All-in year-0 regulatory cash</td><td class="num">₹5–8 lakh</td><td>Critical path 8–12 weeks (no NH) or 4–6 months (highway-facing)</td></tr>
    </tbody>
  </table>
  <p class="note">Tax formula used: area (sq.m) × zone rate × digital factor 2.0. Class A planning rate ₹2,500 static → ₹5,000 digital. Class B → ₹3,000 digital (₹96,000 / year on 32 sq.m). Confirm the live council schedule; the Act does not freeze a statewide rupee rate.</p>

  <h2>4.2 Gates that still apply on a rented building</h2>
  <table>
    <thead><tr><th>Gate</th><th>Why it still applies</th><th>If skipped</th></tr></thead>
    <tbody>
      <tr><td>Owner / association NOC</td><td>No right to load terrace or facade</td><td>Removal; you eat the screen</td></tr>
      <tr><td>ss. 271–272 permission + tax</td><td>Private buildings are not exempt</td><td>Fine, seizure, High Court climate</td></tr>
      <tr><td>KMBR / IBPMS</td><td>LED frame is an advertising sign / outdoor display</td><td>Unauthorised addition</td></tr>
      <tr><td>Structural certificate of the building</td><td>32 sq.m LED is a wind sail on someone else’s slab</td><td>Collapse / insurer void</td></tr>
      <tr><td>Electrical Inspectorate</td><td>Advertising / neon-class installations</td><td>No lawful energisation</td></tr>
      <tr><td>Commercial meter</td><td>12 kW cannot sit on domestic LT</td><td>Back-billing, disconnection</td></tr>
      <tr><td>PWD / NHAI</td><td>If the face sells NH 66 or SH traffic</td><td>Hazard notice even on private terrace</td></tr>
      <tr><td>AAI NOCAS</td><td>Extra height near CIAL</td><td>Height cut</td></tr>
    </tbody>
  </table>
  <p><strong>Do not order full FOB cabinets until there is a written owner NOC and a Corporation file number.</strong> Import can beat permission by six weeks; warehouse then costs more than the fee.</p>
</section>

<section>
  <h1>5. Cash to be live and monthly P&amp;L</h1>
  <h2>5.1 Money required before the first paid loop</h2>
  <table>
    <thead><tr><th></th><th class="num">Compact 18 sq.m</th><th class="num">Recommended 32 sq.m, 1 face</th></tr></thead>
    <tbody>
      <tr><td>Screen + structure + electrics (cash, incl. IGST)</td><td class="num">₹21 L</td><td class="num">₹31 L</td></tr>
      <tr><td>Admin, lawyers, engineers, filings, year-1 tax</td><td class="num">₹5–8 L</td><td class="num">₹5–8 L</td></tr>
      <tr><td>Landlord deposit (3–6 months)</td><td class="num">₹1.2–3.6 L</td><td class="num">₹1.5–6.0 L</td></tr>
      <tr class="total"><td>Cash to be live</td><td class="num">₹27–33 L</td><td class="num">₹38–45 L</td></tr>
    </tbody>
  </table>

  <h2>5.2 Kochi Class A — 32 sq.m, 10 slots × ₹50,000</h2>
  <table>
    <thead><tr><th></th><th class="num">50% sold</th><th class="num">75% sold</th><th class="num">90% sold</th></tr></thead>
    <tbody>
      <tr><td>Gross advertising revenue</td><td class="num">₹2.50 L</td><td class="num">₹3.75 L</td><td class="num">₹4.50 L</td></tr>
      <tr><td>Hybrid rent (max of ₹50,000 and 18%)</td><td class="num">₹50,000</td><td class="num">₹67,500</td><td class="num">₹81,000</td></tr>
      <tr><td>Power + tax + CMS + AMC (mid)</td><td class="num">₹82,000</td><td class="num">₹82,000</td><td class="num">₹82,000</td></tr>
      <tr class="total"><td>Left before sales commission and promoter salary</td><td class="num">₹1.18 L</td><td class="num">₹2.26 L</td><td class="num">₹2.87 L</td></tr>
    </tbody>
  </table>
  <p>At 75% sold, simple payback on ₹41 L live cash (mid-range) is about <strong>18 months</strong> before commission. Pre-sell at least half the loop before the crane. Programmatic (Hivestack / Lemma) is for unsold time, not the plan.</p>
  <p>Compare: two Lulu/Forum kiosks at ₹8,500/slot do not cover a small ops team. One Kochi outdoor face on a rented building does, if the sightline is real.</p>
</section>

<section class="section">
  <h1>6. SWOT — outdoor digital advertising (Kerala)</h1>
  <p>Scoped to a <strong>building-mounted outdoor LED</strong> in Kochi / Kozhikode / Kannur — not mall MUPI, not a flex hoarding, not a ground unipole on NH land.</p>
  <div class="swot">
    <div class="swot-box s">
      <h3>Strengths</h3>
      <ul>
        <li>Unit economics dwarf indoor: one 32 sq.m Kochi face at 75% sold leaves ~₹2.3 L/month after rent and power; a mall kiosk at ₹8,500 leaves ~₹0.3–0.4 L.</li>
        <li>Building mount cuts first-site hardware from ~₹90 L (land unipole) to ~₹31 L.</li>
        <li>National and regional brands already buy outdoor; jewellery, auto, education, healthcare and QSR are live categories in Kochi.</li>
        <li>Illegal flex removal and Corporation-designated LED create scarcity of <em>legal</em> digital inventory.</li>
        <li>Programmatic SSPs (Hivestack, Lemma) can fill remainder-of-loop without a second sales team.</li>
        <li>24×7 auto-dimmed presence; proof-of-play logs support both landlord audits and brand IO closes.</li>
        <li>Hybrid rent shares downside with the building owner.</li>
      </ul>
    </div>
    <div class="swot-box w">
      <h3>Weaknesses</h3>
      <ul>
        <li>Permission is political and slow (30–90 days; 4–6 months if highway-facing). Hardware can arrive before the file moves.</li>
        <li>KSEB is the second-largest site cost after rent (~₹50–60k / face / month).</li>
        <li>Coastal monsoon: salt, 3,000 mm rain, 39 m/s design wind; cheap iron frames and acrylic conformal coat will fail.</li>
        <li>Older Kochi bye-law language favoured still creatives over film; video loops may be restricted until Town Planning confirms.</li>
        <li>Single-site concentration: one demolition order or slab refusal kills the only asset.</li>
        <li>Working capital: IGST at port, 3–6 months’ deposit, and tax before permission, on top of OEM payment terms.</li>
        <li>You do not control the building’s power quality or terrace leakage — contract for it or lose modules.</li>
      </ul>
    </div>
    <div class="swot-box o">
      <h3>Opportunities</h3>
      <ul>
        <li>Kakkanad / InfoPark / Edappally catchments have advertisers who already spend on outdoor and digital.</li>
        <li>Corporation’s own 50-board LED plan validates digital and can be a partner or a pricing umbrella — not only a rival — if you sit on private commercial buildings with clean files.</li>
        <li>October–November civil window is open now (southwest monsoon tail); foundations/anchors before next 1 June.</li>
        <li>Landlord JV (70/30) if cash is tight: you bring the screen, they bring the sightline.</li>
        <li>Bundle a later Lulu/Forum kiosk as “highway + mall” once the outdoor face is sold — do not lead with malls.</li>
        <li>Kozhikode Thondayad as site two after Kochi occupancy &gt; 70%; less contested than NH 66 Kochi.</li>
        <li>Volume OEM / CKD at USD 330 / sq.m with a hard FAT keeps payback inside ~18 months on building-mount cash.</li>
      </ul>
    </div>
    <div class="swot-box t">
      <h3>Threats</h3>
      <ul>
        <li>High Court and Corporation enforcement against unauthorised boards; private terrace is not a loophole without s. 272 leave.</li>
        <li>NHAI / MoRTH: no commercial hoarding in NH RoW; a facade that reads NH 66 traffic can still be treated as a hazard.</li>
        <li>Town Planning review of large digital boards (footpath, glare, motion) can tighten brightness and content rules after you have sold video.</li>
        <li>Structural / monsoon failure — public liability and criminal exposure; insurers will ask for the building certificate.</li>
        <li>Customs reclass to 8528 59 00 (20% BCD) or container exam in rain voiding IP warranty.</li>
        <li>Landlord rent reset at renewal; association politics in mixed-use buildings.</li>
        <li>Residential or domestic-meter buildings: back-billing and neighbour glare petitions.</li>
        <li>If you cannot pre-sell 50% of the loop, power + floor rent still run ~₹1.3 L/month on a dark board.</li>
      </ul>
    </div>
  </div>
</section>

<section class="section">
  <h1>7. Decision and 90-day sequence</h1>
  <div class="callout">
    <h3>Recommendation</h3>
    <p>Start with one road-facing 32 sq.m LED on a commercial Kochi building (Kakkanad / Edappally class), not a mall cluster and not two outdoor boards. Budget ₹38–45 lakh to be live. File permission before paying the OEM in full. Pre-sell 50% occupancy. Add Kozhikode or a mall kiosk only after this face is above ~70% sold.</p>
  </div>
  <table>
    <thead><tr><th>Week</th><th>Do</th><th>Do not</th></tr></thead>
    <tbody>
      <tr><td>1–2</td><td>Shortlist commercial buildings with a sightline; written owner NOC; advocate on title</td><td>Apartment terraces; domestic meters; plots touching NH RoW</td></tr>
      <tr><td>3–4</td><td>Structural engineer on the slab; hybrid licence drafted; IBPMS + s. 272 file opened</td><td>Order full FOB LED</td></tr>
      <tr><td>5–8</td><td>Inspectorate drawings; sub-meter; tax challan when demanded; factory FAT / booking</td><td>Highway-facing building without a PWD/NHAI view</td></tr>
      <tr><td>9–12</td><td>Permission in hand; cabinets ship; pre-sell 5–10 slots; install night window; 72 h burn-in</td><td>Go live dark; skip auto-dimming affidavit</td></tr>
    </tbody>
  </table>
  <p>If the only buildings on offer are shops glued to a service road or residential roofs, <strong>do not spend the ₹31 lakh</strong>. The sightline is the asset; the screen is a commodity.</p>
  <p class="disclaimer">Planning rates as of September 2026. Sources used in the parent blueprint: Kerala Municipality Act ss. 271–272; KMBR 2019; KSERC LT-VII(A) Gazette 05-Dec-2024; Kerala Electricity Duty Act 1963 (10%); IS 875 Part 3 Vb 39 m/s; IRC:46-1972; CBIC heading 8528. Confirm with Kochi / Kozhikode / Kannur Corporation Revenue, a Kerala-enrolled advocate, and CBIC before committing capital. Regenerated with <code>python3 scripts/build_cost_swot_pdf.py</code>.</p>
</section>

</body>
</html>
"""


def main() -> int:
    HTML(string=HTML_DOC, base_url=str(ROOT)).write_pdf(
        str(OUT_PDF),
        stylesheets=[CSS(string=CSS_TEXT)],
    )
    print(f"Wrote {OUT_PDF} ({OUT_PDF.stat().st_size / 1024:.0f} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
