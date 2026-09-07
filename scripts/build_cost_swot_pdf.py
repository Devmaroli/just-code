#!/usr/bin/env python3
"""Build the outdoor cost estimate + SWOT PDF (building-mounted vs unipole)."""

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
    content: "Kerala outdoor DOOH  ·  Building vs unipole";
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
  grid-template-columns: 1fr 1fr;
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
table.wide {{
  font-size: 7.7pt;
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
  <p class="sub">Building-mounted LED versus private-land unipole — cost estimate, rent, regulatory cash, and SWOT for a first Kochi site (Edappally / Kakkanad class sightline).</p>
  <div class="cover-meta">
    <div><span>Path A — building</span>Rent a commercial terrace or façade. Same 32 sq.m P3.91 screen. No pole, no piles, sub-meter on the building.</div>
    <div><span>Path B — unipole</span>12–15 m pole on private land outside NH RoW. Own foundation, own KSEB, own earth and lightning.</div>
    <div><span>Recommended first asset</span>One 8 m × 4 m (32 sq.m) road-facing P3.91 / P4 face, volume OEM, IP65, ≥ 5,500 nits — on a building if a sightline exists.</div>
    <div><span>Date</span>07 September 2026 · Kochi · Kozhikode · Kannur</div>
  </div>
  <div class="cover-kpis">
    <div><span>Path A — building, cash live</span><strong>₹38–45 lakh</strong></div>
    <div><span>Path B — unipole 1-face, cash live</span><strong>₹55–62 lakh</strong></div>
    <div><span>Path B — unipole dual, cash live</span><strong>₹75–90 lakh</strong></div>
    <div><span>Premium dual unipole (USD 650 FOB)</span><strong>~₹90–93 lakh</strong></div>
  </div>
  <div class="cover-foot">
    Advertisement tax, stamp duty, KSEB tariff and customs BCD must be confirmed against the live gazette and the Corporation schedule before capital is committed. This is not a legal opinion or a quotation from an OEM. Do not order FOB LED until owner / land NOC and a Corporation file number exist.
  </div>
</section>

<section>
  <h1>1. How the cost is split</h1>
  <div class="callout">
    <h3>Read this first</h3>
    <p>Two outdoor paths, one Kochi site. Mall kiosks are a different product and are not costed here. Do not start with two outdoor boards. If a commercial terrace or façade has a real road sightline, use Path A. Use Path B only if there is no such building, or you need both carriageways on one plot.</p>
  </div>
  <p>Same 32 sq.m P3.91 screen. Different civil, power and rent. Volume OEM (USD 330 / sq.m FOB), first site only — do not load a 6-node spare kit onto the first pole.</p>
  <table class="wide">
    <thead>
      <tr><th>Item</th><th>Path A — building 1-face</th><th>Path B — unipole 1-face</th><th>Path B — unipole dual</th></tr>
    </thead>
    <tbody>
      <tr><td>What it is</td><td>LED on rented terrace / façade</td><td>12–15 m pole, 1 screen, private land</td><td>Same pole, 2 screens, both carriageways</td></tr>
      <tr><td>LED area</td><td>32 sq.m</td><td>32 sq.m</td><td>64 sq.m</td></tr>
      <tr><td>Structure</td><td>Rooftop MS frame + strengthening ₹6.5 L</td><td>Pole + piles + soil + PE ₹17.8 L</td><td>Heavier pole + dual frames ₹20.5 L</td></tr>
      <tr><td>Power</td><td>Building LT-VII(A) sub-meter</td><td>Own KSEB 15 kW</td><td>Own KSEB 25 kW</td></tr>
      <tr class="total"><td>Hardware economic</td><td class="num">₹29 L</td><td class="num">₹46 L</td><td class="num">₹64 L</td></tr>
      <tr class="total"><td>Hardware cash (incl. IGST)</td><td class="num">₹31 L</td><td class="num">₹48 L</td><td class="num">₹68 L</td></tr>
      <tr><td>Year-0 admin / tax / engineers</td><td>₹5–8 L</td><td>₹6–10 L</td><td>₹6–10 L</td></tr>
      <tr><td>Space deposit (3–6 months)</td><td>₹1.5–6.0 L</td><td>₹2.4–4.8 L</td><td>₹2.4–4.8 L</td></tr>
      <tr class="total"><td>Cash to be live (plan)</td><td class="num">₹38–45 L</td><td class="num">₹55–62 L</td><td class="num">₹75–90 L</td></tr>
      <tr><td>Rent floor (hybrid 18%)</td><td>₹50,000 or 18% of ads</td><td>₹80,000 or 18% of ads</td><td>₹80,000 or 18% of ads</td></tr>
      <tr><td>Power / month (ex-rent)</td><td>₹50–60k (20% building markup)</td><td>~₹48,500 (own KSEB)</td><td>~₹96,000</td></tr>
      <tr><td>Typical permit path</td><td>3–5 months</td><td>4–6 months + monsoon civil window</td><td>4–6 months + monsoon civil window</td></tr>
      <tr><td>When to choose</td><td>Commercial terrace with road sightline</td><td>No building; one carriageway is enough</td><td>No building; need both carriageways</td></tr>
    </tbody>
  </table>
  <p class="note">Premium listed OEM (USD 650 / sq.m) on a dual unipole is the ~₹90–93 L hardware cash figure often quoted for a “land pole”. Volume OEM dual is ~₹68 L cash hardware — still about 2× a building-mounted single face. All ₹ at ₹84 / USD. IGST at Cochin Port is claimed as ITC.</p>
</section>

<section>
  <h1>2. Path A — building-mounted hardware</h1>
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
  <p class="note">Rounded to the nearest thousand. Hardware licence pack in this table is the OEM/file bundle; full lawyer + tax cash is in Section 5 so it is not double-counted in the ₹38–45 L live figure.</p>
</section>

<section>
  <h1>3. Path B — private-land unipole hardware</h1>
  <p>Same LED cabinets as Path A. The extra cash is civil and power: a 12–15 m IS 2062 pole, pile or raft foundation, two soil boreholes, own lightning protection, and a <em>new</em> KSEB LT-VII(A) service. Spares below are a <strong>first-site kit</strong> (₹1.8 L / face-equivalent), not the 6-node warehouse kit (₹4.2–6.3 L) in the network calculator.</p>
  <table>
    <thead>
      <tr>
        <th>Cost bucket</th>
        <th class="num">Unipole 8×4 m<br/>32 sq.m, 1 face</th>
        <th class="num">Unipole dual<br/>2 × 32 sq.m</th>
      </tr>
    </thead>
    <tbody>
      <tr><td><strong>A. Digital screen</strong> (LED FOB + freight + BCD/AIDC/SWS)</td><td class="num">₹11.6 L</td><td class="num">₹22.6 L</td></tr>
      <tr><td><strong>B. Pole, foundation, soil, PE</strong></td><td class="num">₹17.8 L</td><td class="num">₹20.5 L</td></tr>
      <tr><td><strong>C. Setup</strong> (earth, lightning, own KSEB, NovaStar, install, statutory pack, first-site spares, 8% buffer)</td><td class="num">₹16.1 L</td><td class="num">₹21.0 L</td></tr>
      <tr class="total"><td>Economic total</td><td class="num">₹46 L</td><td class="num">₹64 L</td></tr>
      <tr><td>IGST at port (GST credit)</td><td class="num">₹2.1 L</td><td class="num">₹4.1 L</td></tr>
      <tr class="total"><td>Cash to switch the screen on</td><td class="num">₹48 L</td><td class="num">₹68 L</td></tr>
    </tbody>
  </table>
  <p>Premium cabinets (~USD 650 / sq.m) on the <strong>dual</strong> unipole take hardware cash to about <strong>₹90–93 L</strong> — that is the “₹90 lakh land pole” figure. On a single-face volume OEM pole the premium path is ~₹60 L cash, not ₹90 L. Dual-face is the commercial default on a unipole because one structure covers both carriageways; it is usually wasted on a rooftop.</p>

  <h2>3.1 Single-face 32 sq.m ground unipole — line by line</h2>
  <table>
    <thead><tr><th>Split</th><th>Item</th><th class="num">₹</th></tr></thead>
    <tbody>
      <tr><td>Screen</td><td>LED cabinets FOB (32 sq.m × USD 330 × 84) — same as Path A</td><td class="num">8,87,000</td></tr>
      <tr><td>Screen</td><td>Sea freight + insurance to ICTT Vallarpadam</td><td class="num">1,50,000</td></tr>
      <tr><td>Screen</td><td>Customs BCD + AIDC + SWS</td><td class="num">1,25,000</td></tr>
      <tr><td>Structure</td><td>12–15 m MS unipole, pile/raft, 2 soil boreholes, coastal C5-M paint, PE</td><td class="num">17,80,000</td></tr>
      <tr><td>Setup</td><td>Electrical, earthing pits ≤ 2 Ω, Class II SPD, lightning IS/IEC 62305</td><td class="num">2,80,000</td></tr>
      <tr><td>Setup</td><td>New KSEB LT-VII(A) 3-phase 15 kW (deposit + service line + meter)</td><td class="num">2,20,000</td></tr>
      <tr><td>Setup</td><td>NovaStar TB60 + industrial player + dual-SIM 4G</td><td class="num">1,65,000</td></tr>
      <tr><td>Setup</td><td>K-SWIFT / municipal / PWD / NHAI first-year statutory pack</td><td class="num">2,50,000</td></tr>
      <tr><td>Setup</td><td>Crane, night lift, weld NDT, 72-hour burn-in</td><td class="num">1,80,000</td></tr>
      <tr><td>Setup</td><td>First-site spare modules + Mean Well PSU (not the 6-node kit)</td><td class="num">1,80,000</td></tr>
      <tr><td>Setup</td><td>Contingency 8%</td><td class="num">3,37,000</td></tr>
      <tr class="total"><td></td><td>Economic CAPEX</td><td class="num">45,55,000</td></tr>
      <tr><td></td><td>IGST cash at port (ITC)</td><td class="num">2,09,000</td></tr>
      <tr class="total"><td></td><td>Cash to switch on</td><td class="num">47,64,000</td></tr>
    </tbody>
  </table>
  <p class="note">Matches the calculator’s unipole civil and KSEB lines, with first-site spares instead of the network warehouse kit. Rounded to the nearest thousand.</p>

  <h2>3.2 Dual-face 32 sq.m ground unipole — what changes</h2>
  <table>
    <thead><tr><th>Item vs single-face</th><th class="num">₹</th></tr></thead>
    <tbody>
      <tr><td>Second 32 sq.m face (FOB + freight + duty)</td><td class="num">+11.0 L</td></tr>
      <tr><td>Heavier pole and dual frames (₹20.47 L vs ₹17.80 L)</td><td class="num">+2.7 L</td></tr>
      <tr><td>Electrical, KSEB 25 kW, controller, install, extra spares, extra 8%</td><td class="num">+4.9 L</td></tr>
      <tr class="total"><td>Economic total (volume OEM)</td><td class="num">64,08,000</td></tr>
      <tr><td>IGST at port</td><td class="num">4,06,000</td></tr>
      <tr class="total"><td>Cash to switch on (volume OEM)</td><td class="num">68,15,000</td></tr>
      <tr><td>Same dual pole, premium FOB USD 650 / sq.m — cash</td><td class="num">~92,45,000</td></tr>
    </tbody>
  </table>
  <p>Live cash on top of hardware: add ₹6–10 L year-0 admin (more PWD / NHAI / KMBR than a rooftop) and ₹2.4–4.8 L land deposit (3–6 months of the ₹80,000 Kochi floor). Plan <strong>₹55–62 L</strong> to go live on one face, <strong>₹75–90 L</strong> on dual (the top of that band covers premium cabinets or a highway file that runs long).</p>
</section>

<section>
  <h1>4. Renting cost (monthly)</h1>
  <p>This is the lease for the wall, terrace, or plot — not the screen. Sign a <strong>hybrid</strong>: minimum guarantee or 18% of that board’s Gross Advertising Revenue, whichever is higher. Register the licence if the term exceeds 11 months (Kerala Stamp Act + Registration Act).</p>

  <h2>4.1 Path A — commercial building (terrace / façade)</h2>
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
  <h3>Recommended first building contract (Kochi Class A)</h3>
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

  <h2>4.2 Path B — private land under a unipole</h2>
  <p>Land is dearer than a terrace because the owner is giving a dedicated plot, setbacks, and usually a new service line through their property. The calculator floor for Kochi outdoor land is <strong>₹80,000</strong> (not ₹50,000).</p>
  <table>
    <thead>
      <tr><th>Location quality</th><th class="num">Fixed rent / month</th><th>Revenue share alternative</th><th>Deposit</th></tr>
    </thead>
    <tbody>
      <tr><td><strong>Kochi outdoor land</strong> — Edappally / Kakkanad, outside NH RoW</td><td class="num">₹80,000–₹1,50,000</td><td>18% of board ads</td><td>3–6 months</td></tr>
      <tr><td><strong>Kozhikode outdoor land</strong> — Thondayad / city arterial</td><td class="num">₹45,000–₹80,000</td><td>18%</td><td>3–6 months</td></tr>
    </tbody>
  </table>
  <h3>Recommended first land contract (Kochi)</h3>
  <table>
    <thead><tr><th>Term</th><th>Detail</th></tr></thead>
    <tbody>
      <tr><td>Model</td><td>Hybrid: <strong>₹80,000 minimum or 18% of ads</strong>, whichever higher, plus GST</td></tr>
      <tr><td>Lock-in</td><td>18 months inside a 36-month licence; make-good of piles is expensive — write the exit</td></tr>
      <tr><td>Deposit</td><td>3 months of the minimum (₹2.40 L), interest-free, refundable on make-good</td></tr>
      <tr><td>Power</td><td>Own KSEB LT-VII(A) in your name; do not sit on the landowner’s domestic meter</td></tr>
      <tr><td>Worked rent, 1-face, 75% sold</td><td>Revenue ₹3.75 L × 18% = ₹67,500 → floor binds at <strong>₹80,000 / month</strong></td></tr>
      <tr><td>Worked rent, dual-face, 75% sold</td><td>Revenue ₹7.50 L × 18% = <strong>₹1,35,000 / month</strong></td></tr>
      <tr><td>Worked rent if unsold</td><td>Floor <strong>₹80,000 / month</strong> on both 1-face and dual</td></tr>
    </tbody>
  </table>

  <h2>4.3 Other monthly costs (not rent, still yours)</h2>
  <table>
    <thead>
      <tr><th>Item</th><th class="num">Building 1-face</th><th class="num">Unipole 1-face</th><th class="num">Unipole dual</th></tr>
    </thead>
    <tbody>
      <tr><td>Electricity, 18 h, auto-dim</td><td class="num">₹50–60k (20% markup)</td><td class="num">~₹48,500 (own KSEB)</td><td class="num">~₹96,000</td></tr>
      <tr><td>CMS + 4G</td><td class="num">₹3,500</td><td class="num">₹3,500</td><td class="num">₹3,500</td></tr>
      <tr><td>Local technician / AMC</td><td class="num">₹8,000–₹12,000</td><td class="num">₹8,000–₹12,000</td><td class="num">₹12,000–₹18,000</td></tr>
      <tr><td>Advertisement tax (planning)</td><td class="num">~₹13,000 Class A</td><td class="num">~₹13,000 Class A</td><td class="num">~₹26,000 Class A</td></tr>
      <tr class="total"><td>Total besides rent</td><td class="num">₹75,000–₹90,000</td><td class="num">₹73,000–₹78,000</td><td class="num">₹1.35–1.45 L</td></tr>
    </tbody>
  </table>
  <p>All-in monthly (rent + power + tax + upkeep), Kochi Class A, one face: building <strong>₹1.2–2.0 L</strong>; unipole <strong>₹1.5–2.3 L</strong> (higher floor, slightly cheaper power). Dual unipole at 75% sold: rent ₹1.35 L + ~₹1.4 L other ≈ <strong>₹2.7–2.8 L</strong> against ₹7.50 L gross.</p>
</section>

<section>
  <h1>5. Administrative and regulatory cash</h1>
  <p>Neither path skips ss. 271–272 of the Kerala Municipality Act. Path A skips piles and a roadside pole. Path B is treated as a new outdoor display “building”: soil, KMBR as a new structure, own KSEB service, and tighter setbacks.</p>

  <h2>5.1 One-time filings and professionals</h2>
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
      <tr class="total"><td>All-in year-0 regulatory cash</td><td class="num">₹5–8 L building · ₹6–10 L unipole</td><td>Critical path 8–12 weeks (no NH) or 4–6 months (highway / new pole)</td></tr>
    </tbody>
  </table>
  <p class="note">Tax formula used: area (sq.m) × zone rate × digital factor 2.0. Class A planning rate ₹2,500 static → ₹5,000 digital. Class B → ₹3,000 digital (₹96,000 / year on 32 sq.m). Confirm the live council schedule; the Act does not freeze a statewide rupee rate.</p>

  <h2>5.2 Gates that still apply on a rented building</h2>
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
  <p><strong>Do not order full FOB cabinets until there is a written owner / land NOC and a Corporation file number.</strong> Import can beat permission by six weeks; warehouse then costs more than the fee.</p>

  <h2>5.3 Extra gates on a unipole (Path B only)</h2>
  <table>
    <thead><tr><th>Gate</th><th>Why it is extra vs a building</th><th>If skipped</th></tr></thead>
    <tbody>
      <tr><td>Soil investigation (2 boreholes)</td><td>Piles / raft on laterite and fill; cost sits inside the ₹17.8 L structure line</td><td>Under-designed foundation; monsoon tilt</td></tr>
      <tr><td>KMBR as a new “building” / outdoor display</td><td>A pole is not an addition to an existing occupancy; IBPMS treats it as a new structure</td><td>Unauthorised construction, easier demolition</td></tr>
      <tr><td>Own KSEB LT-VII(A) service</td><td>Cannot hide 15–25 kW on a hut or domestic meter; new service line + security deposit</td><td>Back-billing, disconnection</td></tr>
      <tr><td>IRC / Kerala setbacks</td><td>IRC:46 10 m from carriageway; Kerala files often want ~50 m from road / footpath</td><td>PWD / NHAI hazard notice</td></tr>
      <tr><td>NH RoW exclusion</td><td>No commercial hoarding inside National Highway right of way — private title is not enough if the pole sits in RoW</td><td>Removal; you eat the pole</td></tr>
      <tr><td>Monsoon civil window</td><td>Do not open foundations after 1 June; a half-built unipole is a High Court case</td><td>Flooded pits, slipped calendar, rusted steel</td></tr>
      <tr><td>AAI NOCAS</td><td>12–15 m tip is more likely to enter CIAL surfaces than a façade flush with the roof</td><td>Height cut after steel is up</td></tr>
    </tbody>
  </table>
  <p>Year-0 admin is why the unipole band is ₹6–10 L rather than ₹5–8 L: extra soil PE, KMBR as a new building, PWD / NHAI, and KSEB new-connection chasing. Critical path is typically <strong>4–6 months</strong>.</p>
</section>

<section>
  <h1>6. Cash to be live and monthly P&amp;L</h1>
  <h2>6.1 Money required before the first paid loop</h2>
  <table class="wide">
    <thead>
      <tr>
        <th></th>
        <th class="num">Building 18 sq.m</th>
        <th class="num">Building 32 sq.m</th>
        <th class="num">Unipole 1-face</th>
        <th class="num">Unipole dual</th>
      </tr>
    </thead>
    <tbody>
      <tr><td>Screen + structure + electrics (cash, incl. IGST)</td><td class="num">₹21 L</td><td class="num">₹31 L</td><td class="num">₹48 L</td><td class="num">₹68 L</td></tr>
      <tr><td>Admin, lawyers, engineers, filings, year-1 tax</td><td class="num">₹5–8 L</td><td class="num">₹5–8 L</td><td class="num">₹6–10 L</td><td class="num">₹6–10 L</td></tr>
      <tr><td>Space deposit (3–6 months)</td><td class="num">₹1.2–3.6 L</td><td class="num">₹1.5–6.0 L</td><td class="num">₹2.4–4.8 L</td><td class="num">₹2.4–4.8 L</td></tr>
      <tr class="total"><td>Cash to be live</td><td class="num">₹27–33 L</td><td class="num">₹38–45 L</td><td class="num">₹55–62 L</td><td class="num">₹75–90 L</td></tr>
    </tbody>
  </table>
  <p class="note">Dual unipole top of band includes premium FOB (USD 650) or a long highway file. Volume OEM dual is closer to ₹77–83 L if admin stays inside ₹10 L.</p>

  <h2>6.2 Kochi Class A — building 32 sq.m, 10 slots × ₹50,000</h2>
  <table>
    <thead><tr><th></th><th class="num">50% sold</th><th class="num">75% sold</th><th class="num">90% sold</th></tr></thead>
    <tbody>
      <tr><td>Gross advertising revenue</td><td class="num">₹2.50 L</td><td class="num">₹3.75 L</td><td class="num">₹4.50 L</td></tr>
      <tr><td>Hybrid rent (max of ₹50,000 and 18%)</td><td class="num">₹50,000</td><td class="num">₹67,500</td><td class="num">₹81,000</td></tr>
      <tr><td>Power + tax + CMS + AMC (mid)</td><td class="num">₹82,000</td><td class="num">₹82,000</td><td class="num">₹82,000</td></tr>
      <tr class="total"><td>Left before sales commission and promoter salary</td><td class="num">₹1.18 L</td><td class="num">₹2.26 L</td><td class="num">₹2.87 L</td></tr>
    </tbody>
  </table>
  <p>At 75% sold, simple payback on ₹41 L live cash (mid-range) is about <strong>18 months</strong> before commission.</p>

  <h2>6.3 Same loop on a unipole</h2>
  <table>
    <thead>
      <tr>
        <th></th>
        <th class="num">1-face 50%</th>
        <th class="num">1-face 75%</th>
        <th class="num">1-face 90%</th>
        <th class="num">Dual 75%</th>
        <th class="num">Dual 90%</th>
      </tr>
    </thead>
    <tbody>
      <tr><td>Gross advertising revenue</td><td class="num">₹2.50 L</td><td class="num">₹3.75 L</td><td class="num">₹4.50 L</td><td class="num">₹7.50 L</td><td class="num">₹9.00 L</td></tr>
      <tr><td>Hybrid rent (max of ₹80,000 and 18%)</td><td class="num">₹80,000</td><td class="num">₹80,000</td><td class="num">₹81,000</td><td class="num">₹1.35 L</td><td class="num">₹1.62 L</td></tr>
      <tr><td>Power + tax + CMS + AMC (mid)</td><td class="num">₹75,000</td><td class="num">₹75,000</td><td class="num">₹75,000</td><td class="num">₹1.41 L</td><td class="num">₹1.41 L</td></tr>
      <tr class="total"><td>Left before commission and promoter salary</td><td class="num">₹0.95 L</td><td class="num">₹2.20 L</td><td class="num">₹2.94 L</td><td class="num">₹4.74 L</td><td class="num">₹5.97 L</td></tr>
    </tbody>
  </table>
  <p>A single-face unipole at 75% sold leaves about the same monthly cash as the building (~₹2.2 L vs ₹2.26 L) because cheaper own-KSEB power offsets the higher ₹80,000 land floor. The penalty is capital: ~₹58 L live vs ~₹41 L, so payback stretches to about <strong>26 months</strong> before commission. Dual-face is why people build poles: at 75% sold the leftover is ~₹4.74 L/month; payback on ~₹80 L live cash is about <strong>17 months</strong> — close to the building, with twice the inventory — if both carriageways are actually sold.</p>
  <p>Pre-sell at least half the loop before the crane. Programmatic (Hivestack / Lemma) is for unsold time, not the plan. Two Lulu/Forum kiosks at ₹8,500/slot still do not cover a small ops team. One Kochi outdoor face does, if the sightline is real.</p>
</section>

<section class="section">
  <h1>7. SWOT — outdoor digital advertising (Kerala)</h1>
  <p>Scoped to a first Kochi outdoor LED, either <strong>building-mounted</strong> or a <strong>private-land unipole outside NH RoW</strong> — not mall MUPI, not a flex hoarding, not a pole inside highway land.</p>
  <div class="swot">
    <div class="swot-box s">
      <h3>Strengths</h3>
      <ul>
        <li>Unit economics dwarf indoor: one 32 sq.m Kochi face at 75% sold leaves ~₹2.2–2.3 L/month after rent and power; a mall kiosk at ₹8,500 leaves ~₹0.3–0.4 L.</li>
        <li>Building mount cuts first-site hardware from ~₹48 L (volume unipole 1-face) or ~₹90 L (premium dual pole) to ~₹31 L.</li>
        <li>Unipole height and dual-face cover both carriageways from one plot; own KSEB avoids a 20% building power markup.</li>
        <li>National and regional brands already buy outdoor; jewellery, auto, education, healthcare and QSR are live categories in Kochi.</li>
        <li>Illegal flex removal and Corporation-designated LED create scarcity of <em>legal</em> digital inventory.</li>
        <li>Programmatic SSPs (Hivestack, Lemma) can fill remainder-of-loop without a second sales team.</li>
        <li>Hybrid rent shares downside with the building owner or landowner.</li>
      </ul>
    </div>
    <div class="swot-box w">
      <h3>Weaknesses</h3>
      <ul>
        <li>Permission is political and slow (30–90 days; 4–6 months if highway-facing or a new pole). Hardware can arrive before the file moves.</li>
        <li>KSEB is the second-largest site cost after rent (~₹48–60k / face / month).</li>
        <li>Unipole doubles (or triples) first-site capital vs a terrace; piles cannot be moved if the sightline was misread.</li>
        <li>Coastal monsoon: salt, 3,000 mm rain, 39 m/s design wind; cheap iron frames and acrylic conformal coat will fail. Do not open unipole foundations after 1 June.</li>
        <li>Older Kochi bye-law language favoured still creatives over film; video loops may be restricted until Town Planning confirms.</li>
        <li>Single-site concentration: one demolition order, slab refusal, or setback miss kills the only asset.</li>
        <li>Working capital: IGST at port, 3–6 months’ deposit, and tax before permission, on top of OEM payment terms.</li>
        <li>Building path: you do not control power quality or terrace leakage. Unipole path: you own every pit, every rusted bolt, and the make-good of piles.</li>
      </ul>
    </div>
    <div class="swot-box o">
      <h3>Opportunities</h3>
      <ul>
        <li>Kakkanad / InfoPark / Edappally catchments have advertisers who already spend on outdoor and digital.</li>
        <li>Corporation’s own 50-board LED plan validates digital and can be a partner or a pricing umbrella — not only a rival — if you sit on private commercial land or buildings with clean files.</li>
        <li>October–November civil window is open now (southwest monsoon tail); anchors or foundations before next 1 June.</li>
        <li>Landlord / landowner JV (70/30) if cash is tight: you bring the screen, they bring the sightline.</li>
        <li>Bundle a later Lulu/Forum kiosk as “highway + mall” once the outdoor face is sold — do not lead with malls.</li>
        <li>Kozhikode Thondayad as site two after Kochi occupancy &gt; 70%; less contested than NH 66 Kochi.</li>
        <li>Volume OEM / CKD at USD 330 / sq.m with a hard FAT keeps building-mount payback inside ~18 months; dual unipole can match that if both faces sell.</li>
      </ul>
    </div>
    <div class="swot-box t">
      <h3>Threats</h3>
      <ul>
        <li>High Court and Corporation enforcement against unauthorised boards; private terrace or private plot is not a loophole without s. 272 leave.</li>
        <li>NHAI / MoRTH: no commercial hoarding in NH RoW; a façade or pole that reads NH 66 traffic can still be treated as a hazard. Kerala files often want ~50 m from the road, not only IRC’s 10 m.</li>
        <li>Town Planning review of large digital boards (footpath, glare, motion) can tighten brightness and content rules after you have sold video.</li>
        <li>Structural / monsoon failure — public liability and criminal exposure; insurers will ask for the building certificate or the soil + PE pack.</li>
        <li>Customs reclass to 8528 59 00 (20% BCD) or container exam in rain voiding IP warranty.</li>
        <li>Landlord or landowner rent reset at renewal; association politics in mixed-use buildings; neighbour glare petitions on unipoles.</li>
        <li>Residential or domestic-meter sites: back-billing and disconnection.</li>
        <li>If you cannot pre-sell 50% of the loop, floor rent + power still run ~₹1.3 L/month (building) or ~₹1.55 L/month (unipole) on a dark board.</li>
      </ul>
    </div>
  </div>
</section>

<section class="section">
  <h1>8. Decision and 90-day sequence</h1>
  <div class="callout">
    <h3>Recommendation</h3>
    <p>Prefer Path A: one road-facing 32 sq.m LED on a commercial Kochi building (Kakkanad / Edappally class) if a terrace or façade has a real sightline. Budget ₹38–45 lakh to be live. Use Path B (unipole) only if no such building exists, or you need both carriageways — then budget ₹55–62 lakh for one face or ₹75–90 lakh for dual. Still one Kochi site, not two poles, and not a mall cluster. File permission before paying the OEM in full. Pre-sell 50% occupancy. Add Kozhikode or a mall kiosk only after this face is above ~70% sold.</p>
  </div>
  <table>
    <thead><tr><th>Week</th><th>Path A — building</th><th>Path B — unipole extra</th><th>Do not</th></tr></thead>
    <tbody>
      <tr><td>1–2</td><td>Shortlist commercial buildings; written owner NOC; advocate on title</td><td>Private land outside NH RoW; IRC / ~50 m setback sketch; soil quote</td><td>Apartment terraces; domestic meters; plots in NH RoW</td></tr>
      <tr><td>3–4</td><td>Structural engineer on the slab; hybrid licence; IBPMS + s. 272 file</td><td>Two boreholes; KMBR as a new structure; land hybrid at ₹80k or 18%</td><td>Order full FOB LED</td></tr>
      <tr><td>5–8</td><td>Inspectorate drawings; sub-meter; tax challan; factory FAT / booking</td><td>New KSEB 15/25 kW file; PWD/NHAI pack; AAI NOCAS if the tip is high</td><td>Open foundations after 1 June; highway file with no PWD view</td></tr>
      <tr><td>9–12</td><td>Permission in hand; cabinets ship; pre-sell 5–10 slots; night install; 72 h burn-in</td><td>Cast piles only after permission; crane + weld NDT; earth &lt; 2 Ω</td><td>Go live dark; skip auto-dimming affidavit</td></tr>
    </tbody>
  </table>
  <p>If the only buildings on offer are shops glued to a service road or residential roofs, <strong>do not spend the ₹31 lakh</strong> on a terrace. If the only land on offer sits inside NH RoW or fails setback, <strong>do not spend the ₹48–68 lakh</strong> on a pole. The sightline is the asset; the screen is a commodity.</p>
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
