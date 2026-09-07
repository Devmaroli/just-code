#!/usr/bin/env python3
"""Build the Big Four-style strategy, SWOT and capital-formation PDF."""

from __future__ import annotations

from pathlib import Path

from weasyprint import CSS, HTML

ROOT = Path(__file__).resolve().parents[1]
OUT_PDF = ROOT / "docs" / "Kerala_DOOH_Strategy_and_Capital_Plan.pdf"

FONT_REG = "/usr/share/fonts/truetype/macos/Inter-Regular.ttf"
FONT_MED = "/usr/share/fonts/truetype/macos/Inter-Medium.ttf"
FONT_SEMI = "/usr/share/fonts/truetype/macos/Inter-SemiBold.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/macos/Inter-Bold.ttf"
FONT_ITA = "/usr/share/fonts/truetype/macos/Inter-Italic.ttf"

CSS_TEXT = f"""
@font-face {{ font-family: ReportSans; src: url("file://{FONT_REG}"); font-weight: 400; }}
@font-face {{ font-family: ReportSans; src: url("file://{FONT_MED}"); font-weight: 500; }}
@font-face {{ font-family: ReportSans; src: url("file://{FONT_SEMI}"); font-weight: 600; }}
@font-face {{ font-family: ReportSans; src: url("file://{FONT_BOLD}"); font-weight: 700; }}
@font-face {{ font-family: ReportSans; src: url("file://{FONT_ITA}"); font-style: italic; font-weight: 400; }}

:root {{
  --navy: #0B1F3A;
  --blue: #0E4D92;
  --mid: #1A6BB5;
  --sky: #4A9FE8;
  --ice: #E8F1FA;
  --paper: #F4F8FC;
  --ink: #122033;
  --muted: #5A6B7C;
  --line: #C5D5E8;
  --s: #0D7377;
  --w: #B58116;
  --o: #1A6BB5;
  --t: #B42318;
}}

* {{ box-sizing: border-box; }}
html, body {{
  margin: 0;
  padding: 0;
  color: var(--ink);
  font-family: ReportSans, Inter, sans-serif;
  font-size: 9.7pt;
  line-height: 1.42;
  background: #fff;
}}

@page {{
  size: A4;
  margin: 16mm 15mm 18mm 15mm;
  @top-left {{
    content: "Kerala DOOH  ·  Strategy, SWOT and capital formation";
    font-size: 7.6pt;
    color: #6B7C8D;
    font-family: ReportSans, sans-serif;
    letter-spacing: 0.04em;
  }}
  @top-right {{
    content: "Confidential  ·  Independent working paper";
    font-size: 7.6pt;
    color: #6B7C8D;
    font-family: ReportSans, sans-serif;
  }}
  @bottom-left {{
    content: "Not a Deloitte, PwC, EY or KPMG opinion  |  September 2026";
    font-size: 7.4pt;
    color: #6B7C8D;
    font-family: ReportSans, sans-serif;
  }}
  @bottom-right {{
    content: "Page " counter(page);
    font-size: 7.6pt;
    color: #6B7C8D;
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
  position: relative;
  min-height: 297mm;
  background: var(--navy);
  color: #F4F8FC;
  padding: 24mm 22mm 20mm 28mm;
  break-after: page;
  overflow: hidden;
}}
.cover::before {{
  content: "";
  position: absolute;
  left: 0; top: 0; bottom: 0;
  width: 9mm;
  background: var(--sky);
}}
.cover-kicker {{
  letter-spacing: 0.28em;
  text-transform: uppercase;
  font-size: 8pt;
  font-weight: 500;
  color: var(--sky);
  margin-bottom: 14mm;
}}
.cover h1 {{
  font-size: 26pt;
  font-weight: 700;
  line-height: 1.12;
  margin: 0 0 6mm 0;
  color: #fff;
  border: none;
  max-width: 160mm;
  padding: 0;
}}
.cover .sub {{
  font-size: 11.5pt;
  font-weight: 400;
  color: #B9D4F0;
  margin: 0 0 12mm 0;
  max-width: 158mm;
  line-height: 1.35;
}}
.cover-meta {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 5mm 12mm;
  border-top: 1px solid #1E3F66;
  padding-top: 7mm;
  font-size: 9.6pt;
  color: #E4EEF8;
}}
.cover-meta span {{
  display: block;
  color: var(--sky);
  font-size: 7.3pt;
  font-weight: 600;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  margin-bottom: 1.3mm;
}}
.cover-kpis {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4mm;
  margin: 12mm 0 0 0;
}}
.cover-kpis div {{
  border: 0.6pt solid #1E3F66;
  background: #0E2A4C;
  padding: 4.2mm 4.5mm;
}}
.cover-kpis span {{
  display: block;
  font-size: 7.2pt;
  font-weight: 600;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--sky);
}}
.cover-kpis strong {{
  display: block;
  font-size: 14pt;
  font-weight: 700;
  margin-top: 1.6mm;
  color: #fff;
}}
.cover-foot {{
  position: absolute;
  bottom: 16mm;
  left: 28mm;
  right: 22mm;
  font-size: 8pt;
  color: #9BB4CC;
  border-top: 1px solid #1E3F66;
  padding-top: 5mm;
}}

h1 {{
  color: var(--navy);
  font-size: 15.5pt;
  font-weight: 700;
  margin: 0 0 4.5mm 0;
  padding-bottom: 2.4mm;
  border-bottom: 2.2px solid var(--sky);
}}
h1 .num {{
  color: var(--mid);
  font-weight: 600;
  margin-right: 2.5mm;
  letter-spacing: 0.06em;
}}
h2 {{
  color: var(--blue);
  font-size: 11.3pt;
  font-weight: 600;
  margin: 6.5mm 0 2.6mm 0;
  padding-bottom: 1mm;
  border-bottom: 0.5pt solid var(--line);
  page-break-after: avoid;
}}
h3 {{
  color: var(--navy);
  font-size: 10pt;
  font-weight: 600;
  margin: 4mm 0 1.8mm 0;
  page-break-after: avoid;
}}
p {{ margin: 0 0 2.6mm 0; }}
ul, ol {{ margin: 0 0 3mm 0; padding-left: 5mm; }}
li {{ margin-bottom: 1.05mm; }}
.section {{ break-before: page; }}

table {{
  width: 100%;
  border-collapse: collapse;
  margin: 2mm 0 4.2mm 0;
  font-size: 8.3pt;
}}
table.wide {{ font-size: 7.6pt; }}
thead {{ display: table-header-group; }}
tr {{ page-break-inside: avoid; }}
th {{
  background: var(--navy);
  color: #F4F8FC;
  text-align: left;
  font-weight: 600;
  padding: 2mm 2.1mm;
}}
td {{
  padding: 1.65mm 2.1mm;
  border-bottom: 0.4pt solid var(--line);
  vertical-align: top;
}}
td.num, th.num {{ text-align: right; }}
tr:nth-child(even) td {{ background: var(--ice); }}
tr.total td {{
  background: var(--navy) !important;
  color: #F4F8FC;
  font-weight: 700;
}}

.note {{
  font-size: 8.1pt;
  color: var(--muted);
  margin: -0.5mm 0 3.8mm 0;
}}
.callout {{
  background: var(--navy);
  color: #F4F8FC;
  padding: 4.4mm 5.2mm;
  margin: 0 0 4.8mm 0;
}}
.callout h3 {{
  color: var(--sky);
  margin: 0 0 1.4mm 0;
  font-size: 8pt;
  font-weight: 600;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  border: none;
}}
.callout p {{ margin: 0; font-size: 9.6pt; color: #F4F8FC; }}
.callout.ice {{
  background: var(--ice);
  color: var(--ink);
  border-left: 2.4pt solid var(--mid);
}}
.callout.ice h3 {{ color: var(--blue); }}
.callout.ice p {{ color: var(--ink); }}

.toc {{
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 1.4mm 5mm;
  font-size: 10pt;
  margin: 2mm 0 5mm 0;
}}
.toc .n {{
  color: var(--mid);
  font-weight: 600;
  letter-spacing: 0.08em;
}}
.toc .t {{ color: var(--ink); }}

.steps {{
  display: grid;
  grid-template-columns: 1fr 1fr 1fr 1fr;
  gap: 3mm;
  margin: 2mm 0 4.5mm 0;
}}
.step {{
  background: var(--ice);
  border-top: 2.4pt solid var(--mid);
  padding: 3.2mm 3.4mm;
  font-size: 8.2pt;
  page-break-inside: avoid;
}}
.step strong {{
  display: block;
  color: var(--navy);
  font-size: 8pt;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  margin-bottom: 1.4mm;
}}

.swot {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 3.5mm;
  margin-top: 2mm;
}}
.swot-box {{
  border: 0.7pt solid var(--line);
  padding: 3.8mm 4.2mm;
  break-inside: avoid;
  background: #fff;
}}
.swot-box h3 {{
  margin: 0 0 2.2mm 0;
  font-size: 9.5pt;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  border: none;
}}
.swot-box.s h3 {{ color: var(--s); }}
.swot-box.w h3 {{ color: var(--w); }}
.swot-box.o h3 {{ color: var(--o); }}
.swot-box.t h3 {{ color: var(--t); }}
.swot-box ul {{ padding-left: 4mm; margin: 0; font-size: 8.2pt; }}
.swot-box li {{ margin-bottom: 1.45mm; }}

.disclaimer {{
  font-size: 7.7pt;
  color: var(--muted);
  border-top: 0.6pt solid var(--line);
  padding-top: 3mm;
  margin-top: 4mm;
}}
"""

HTML_DOC = r"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="utf-8"/><title>Kerala DOOH — Strategy, SWOT and Capital Formation</title></head>
<body>

<section class="cover">
  <div class="cover-kicker">Confidential · Independent working paper · September 2026</div>
  <h1>Strategy, SWOT and capital formation</h1>
  <p class="sub">How a Big Four firm would run a consultation for a Kerala outdoor digital network — and the plan to switch on Site 1 when the promoter holds only ten percent of the cash.</p>
  <div class="cover-meta">
    <div><span>Client situation</span>First-time outdoor DOOH operator. Kochi first (Edappally / Kakkanad class sightline). Path A preferred: 32 sq.m building-mounted P3.91 LED.</div>
    <div><span>The constraint</span>Founder cash is ~10% of Site 1 live capital (~₹4.1 L of ₹41 L). This is a sequencing problem, not a “no business” problem.</div>
    <div><span>Engagement analogue</span>Six-week Strategy &amp; Capital module: diagnose, options, operating plan, SWOT, sources-and-uses, fundraising process.</div>
    <div><span>This paper is not</span>A Deloitte, PwC, EY or KPMG opinion, a quotation, or a securities offer. Confirm rates with Corporation, KSERC, CBIC and a Kerala advocate.</div>
  </div>
  <div class="cover-kpis">
    <div><span>Do not raise yet</span><strong>₹1.5–2.0 Cr</strong></div>
    <div><span>Raise after a file number</span><strong>₹37 L gap</strong></div>
    <div><span>Founder dry powder (10%)</span><strong>₹4.1 L</strong></div>
    <div><span>Recommended first asset</span><strong>Kochi 32 sq.m face</strong></div>
  </div>
  <div class="cover-foot">
    Prepared as an independent strategy memorandum in a Big Four engagement structure. A branded Big Four module of this scope would typically invoice more than Site 1 hardware — do not spend the 10% on a logo. Execute with a Kochi CA, a Kerala-enrolled advocate, and this pack.
  </div>
</section>

<section>
  <h1>Contents</h1>
  <div class="toc">
    <div class="n">01</div><div class="t">How a Big Four would run this consultation</div>
    <div class="n">02</div><div class="t">Executive briefing — the recommendation</div>
    <div class="n">03</div><div class="t">Situation diagnosis</div>
    <div class="n">04</div><div class="t">Market and the right to win</div>
    <div class="n">05</div><div class="t">Strategic options under a 10% cash constraint</div>
    <div class="n">06</div><div class="t">Recommended 36-month business plan</div>
    <div class="n">07</div><div class="t">Financial plan, uses of funds, unit economics</div>
    <div class="n">08</div><div class="t">SWOT — investor-facing</div>
    <div class="n">09</div><div class="t">Capital formation — closing the 90%</div>
    <div class="n">10</div><div class="t">Fundraising process, materials, who to call</div>
    <div class="n">11</div><div class="t">Governance, cap table, term-sheet headlines</div>
    <div class="n">12</div><div class="t">Conditions precedent and 90-day workplan</div>
  </div>
  <div class="callout">
    <h3>The one-line verdict</h3>
    <p>Do not raise for a six-node network. Spend the 10% to buy a Corporation file number and five brand letters of intent. Then raise about ₹37 lakh against a de-risked Kochi building-mounted face. Outdoor first; malls later; unipole only if no terrace has a sightline.</p>
  </div>
</section>

<section class="section">
  <h1><span class="num">01</span>How a Big Four would run this consultation</h1>
  <p>A Deloitte, PwC, EY or KPMG Strategy team would not start with a logo on an LED. They would treat this as a <strong>capital-constrained market-entry</strong> problem: one geography (Kochi), one asset class (road-facing digital), one binding constraint (founder cash = 10% of first-site live capital). The work is a six-week module with four workstreams and a steering decision at the end.</p>

  <div class="steps">
    <div class="step"><strong>Week 1–2 · Discover</strong>Promoter interviews. Confirm the ₹4.1 L is unencumbered. Walk three Kochi buildings and one land plot. Title scan. Map Corporation / PWD / KSEB gates. No OEM order.</div>
    <div class="step"><strong>Week 3–4 · Diagnose</strong>Demand (who already buys Kochi outdoor). Supply (legal digital scarcity). Options: mall-only, two poles, building, unipole, landlord JV. Kill the ones that fail the 10% test.</div>
    <div class="step"><strong>Week 5 · Design</strong>Operating model, 36-month plan, sources-and-uses, SWOT, cap table, investor narrative. Data-room index. Conditions precedent to Round 1.</div>
    <div class="step"><strong>Week 6 · Decide</strong>Investment-committee style memo. 90-day plan. Introductions list (not a fundraise run by the firm unless a separate retainer is signed).</div>
  </div>

  <table>
    <thead><tr><th>Workstream</th><th>What they would test</th><th>Pass / fail for this promoter</th></tr></thead>
    <tbody>
      <tr><td>Commercial</td><td>Can one Kochi face at ₹50,000/slot clear rent and power at 50% sold?</td><td>Pass at 50% on a building (₹1.18 L leftover). Fail if malls-first.</td></tr>
      <tr><td>Regulatory</td><td>Is there a lawful site that is not NH RoW, not a domestic meter, not an apartment terrace?</td><td>Unknown until a building is named. This is the Round 0 job.</td></tr>
      <tr><td>Financial</td><td>What is the true “required capital”? Six nodes, or Site 1?</td><td>Site 1 live cash is ₹38–45 L (building) or ₹55–90 L (unipole). Six-node ₹1.5–2.0 Cr is a later conversation.</td></tr>
      <tr><td>Capital</td><td>Who funds the 90%, in what instrument, after what proof?</td><td>Not VC. Angel / NRI / advertiser-investor + customer prepay + optional equipment debt, after a file number.</td></tr>
    </tbody>
  </table>

  <div class="callout ice">
    <h3>Fee honesty — why you should not hire the logo</h3>
    <p>A branded Big Four strategy module of this scope in India often invoices ₹40–80 lakh. That is more than the recommended first board. Spending the 10% on a consulting brand would consume the only cash that can buy permission. This memorandum is the work product of that module. Execute it with a Kochi chartered accountant, a Kerala-enrolled advocate, a structural PE, and the cost pack already in this repository.</p>
  </div>

  <h2>What they would refuse to put in the pitch</h2>
  <ul>
    <li>A six-city map before one Corporation file exists.</li>
    <li>A 12-month payback that assumes 90% occupancy and USD 330 FOB with no FAT.</li>
    <li>Mall kiosks as the “cheap start” (two Kochi malls do not cover a small ops team).</li>
    <li>A land unipole inside NH RoW, or any raise that pays an OEM before s. 272 is on a file.</li>
  </ul>
</section>

<section class="section">
  <h1><span class="num">02</span>Executive briefing — the recommendation</h1>
  <div class="callout">
    <h3>Recommendation to the promoter</h3>
    <p>Lock Path A: one road-facing 32 sq.m P3.91 LED on a commercial Kochi building. Deploy the ₹4.1 lakh as Round 0 (entity, title, structural, IBPMS / s. 272, sales LOIs). Raise Round 1 of ~₹37 lakh only after a written owner NOC and a Corporation file number. Do not import cabinets, do not pour piles, do not sign a ₹1.5 lakh fixed rent on a dark screen.</p>
  </div>
  <table>
    <thead><tr><th>Decision</th><th>Big Four answer</th><th>Why</th></tr></thead>
    <tbody>
      <tr><td>First city</td><td>Kochi</td><td>Slot rate ₹50,000 vs Kozhikode ₹30,000. Brands already spend here.</td></tr>
      <tr><td>First asset</td><td>Building-mounted 32 sq.m, 1 face</td><td>Live cash ₹38–45 L vs unipole ₹55–90 L. Dual-face is a pole logic, not a rooftop logic.</td></tr>
      <tr><td>Malls</td><td>Year 2 bundle, not Year 0</td><td>Indoor contribution does not cover ops. Outdoor does, if the sightline is real.</td></tr>
      <tr><td>Unipole</td><td>Only if no terrace has a sightline</td><td>Same leftover ~₹2.2 L/month on one face; ~₹17 L extra capital; 4–6 month civil window.</td></tr>
      <tr><td>How much to raise now</td><td>Nothing until a file number, then ~₹37 L</td><td>Investors fund de-risked steel, not a slide.</td></tr>
      <tr><td>Instrument mix</td><td>CCPS + customer prepay + optional NBFC</td><td>Asset-heavy, not a SaaS seed. Keep founder control above 65%.</td></tr>
      <tr><td>Valuation posture</td><td>₹60–90 L post-money after file + 5 LOIs</td><td>Pre-revenue OOH. Do not sell 40% for ₹10 L to a flex contractor.</td></tr>
    </tbody>
  </table>
  <p>If the only buildings on offer are shops on a service road, residential roofs, or plots inside NH RoW, <strong>stop</strong>. The 10% is then still intact. The sightline is the asset; the screen is a commodity.</p>
</section>

<section class="section">
  <h1><span class="num">03</span>Situation diagnosis</h1>
  <h2>What is true</h2>
  <table>
    <thead><tr><th>Fact</th><th>Implication for a 10% cash promoter</th></tr></thead>
    <tbody>
      <tr><td>Kerala Municipality Act ss. 271–272 applies on private buildings and private land</td><td>Permission is a product you can buy with the 10%. Steel is not.</td></tr>
      <tr><td>A building-mounted 32 sq.m face costs ~₹31 L hardware, ₹38–45 L to be live</td><td>Required capital for “a business” is ~₹41 L, not ₹2 Cr. 10% = ₹4.1 L.</td></tr>
      <tr><td>A volume dual unipole is ~₹68 L hardware, ₹75–90 L live; premium dual ~₹90–93 L</td><td>A pole consumes two to three times the raise. Do not default to it.</td></tr>
      <tr><td>At 75% sold, 10 × ₹50,000, leftover after rent and power is ~₹2.2–2.3 L / month</td><td>One legal Kochi face can pay a promoter. Two mall kiosks cannot.</td></tr>
      <tr><td>Hybrid rent (floor or 18%) beats a high fixed lease on a dark board</td><td>Share downside with the landlord. Floor ₹50k building / ₹80k land.</td></tr>
      <tr><td>Illegal flex is being removed; Corporation is itself planning designated LED</td><td>Legal digital inventory is scarce. A clean file is a moat. A dirty file is a High Court case.</td></tr>
    </tbody>
  </table>
  <h2>What is not yet true (and must not be pretended)</h2>
  <ul>
    <li>No named building, no owner NOC, no Corporation file number, no structural certificate on a specific slab.</li>
    <li>No audited books, no GST trail of advertising revenue, no proof-of-play history.</li>
    <li>No FAT-passed OEM relationship. FOB USD 330 is a target, not a purchase order.</li>
    <li>Founder has not yet pre-sold a single slot. Until LOIs exist, occupancy is a hope.</li>
  </ul>
  <p>A Big Four IC memo would stamp this <strong>Stage 0 — permission and demand</strong>. Capital markets work (Round 1) starts when Stage 0 has artefacts, not when the pitch deck is pretty.</p>
</section>

<section class="section">
  <h1><span class="num">04</span>Market and the right to win</h1>
  <p>Do not quote a national OOH TAM. Investors in this raise are buying <strong>one Kochi sightline</strong>. The relevant market is advertisers who already buy outdoor or digital in Ernakulam: jewellery, auto, healthcare, education, QSR, real estate, political (capped and seasonal), and regional BFSI.</p>
  <table>
    <thead><tr><th>Layer</th><th>Definition</th><th>Planning view</th></tr></thead>
    <tbody>
      <tr><td>Demand</td><td>Monthly loop of 10 slots × ₹50,000 on a Class A Kochi face</td><td>₹5.00 L gross if full; ₹3.75 L at 75%; ₹2.50 L at 50%.</td></tr>
      <tr><td>Who pays</td><td>Local and national brands with Kochi retail or Gulf-return catchments</td><td>Five named LOIs are worth more than a TAM slide. Target jewellery + auto + hospital + education + one national.</td></tr>
      <tr><td>Supply</td><td>Legal digital faces on private commercial buildings / plots outside NH RoW</td><td>Scarce. Flex is being cleaned. Corporation LED is a rival and a pricing umbrella.</td></tr>
      <tr><td>Right to win</td><td>Clean s. 272 file + proof-of-play + hybrid landlord + volume OEM FAT</td><td>Not “we know media.” Everyone in Kochi knows media. Few will sit in Town Planning for 90 days.</td></tr>
      <tr><td>Programmatic</td><td>Hivestack / Lemma on unsold time</td><td>Floor filler at ~55% of direct CPM. Not the plan. Do not raise on it.</td></tr>
    </tbody>
  </table>
  <p>Competitive set to name in the data room: existing Kochi OOH operators (mostly flex / vinyl), mall media owners, and the Corporation’s designated LED programme. Position as <strong>the legal private digital face</strong>, not as “the Kochi Times OOH.”</p>
</section>

<section class="section">
  <h1><span class="num">05</span>Strategic options under a 10% cash constraint</h1>
  <p>Every option is scored against three tests: (1) can the 10% buy the de-risking, (2) is Round 1 under ₹50 L, (3) does monthly leftover cover a promoter at 50% sold.</p>
  <table class="wide">
    <thead>
      <tr><th>Option</th><th>Live cash</th><th>10% test</th><th>50% leftover</th><th>Verdict</th></tr>
    </thead>
    <tbody>
      <tr><td>A. Building 32 sq.m, 1 face (recommended)</td><td>₹38–45 L</td><td>₹4.1 L buys permission + LOIs</td><td>~₹1.18 L</td><td><strong>Do this</strong></td></tr>
      <tr><td>B. Building compact 18 sq.m</td><td>₹27–33 L</td><td>Easier raise</td><td>Weaker rate card</td><td>Only if the wall is small</td></tr>
      <tr><td>C. Unipole 1-face</td><td>₹55–62 L</td><td>Round 1 jumps to ~₹53 L</td><td>~₹0.95 L</td><td>If no terrace</td></tr>
      <tr><td>D. Unipole dual</td><td>₹75–90 L</td><td>Too large for first close</td><td>Fat if both faces sell</td><td>Site 2 logic, not Site 1 with 10% cash</td></tr>
      <tr><td>E. Two Kochi mall kiosks only</td><td>Low hardware, high rent</td><td>Looks cheap</td><td>Negative vs ops</td><td><strong>Kill</strong></td></tr>
      <tr><td>F. Full 6-node network now</td><td>₹1.54–1.95 Cr</td><td>10% = ₹15–20 L, still not enough</td><td>Model only</td><td><strong>Kill as a raise</strong></td></tr>
      <tr><td>G. Landlord JV on Path A</td><td>Cash live drops by deposit + rent holiday</td><td>Best 10% fit</td><td>Same ops, 12–25% given up</td><td><strong>Prefer if landlord is real</strong></td></tr>
    </tbody>
  </table>
  <p>If the promoter actually holds 10% of the <em>six-node</em> cheque (₹15–20 L) rather than 10% of Site 1, say so in Round 0. That is enough to fund permission <em>and</em> the landlord deposit, and it shrinks Round 1. It is still not a reason to order two poles.</p>
</section>

<section class="section">
  <h1><span class="num">06</span>Recommended 36-month business plan</h1>
  <p>One legal Kochi face, then cash and proof, then a second outdoor. Malls are a bundle sold to the same brands, not a separate start-up.</p>
  <table>
    <thead>
      <tr><th></th><th>Months 0–4 · Round 0</th><th>Months 5–12 · Site 1</th><th>Year 2</th><th>Year 3</th></tr>
    </thead>
    <tbody>
      <tr><td>What is live</td><td>File + 5 LOIs. No LED.</td><td>1 × 32 sq.m Kochi building face</td><td>Same face at 75–85% sold</td><td>Optional Kozhikode outdoor or second Kochi face</td></tr>
      <tr><td>Occupancy target</td><td>LOIs for 50% of loop</td><td>50% at go-live → 75% by month 10</td><td>80%</td><td>80%+ on node 1; 60% on node 2</td></tr>
      <tr><td>Gross / month (planning)</td><td>—</td><td>₹2.5–3.75 L</td><td>₹3.75–4.5 L</td><td>Node 1 + Kozhikode ~₹2.25 L at 75%</td></tr>
      <tr><td>Leftover / month before salary</td><td>−₹0.3 L burn</td><td>₹1.2–2.3 L</td><td>₹2.3–2.9 L</td><td>Two outdoor leftover, still no mall drag</td></tr>
      <tr><td>Capital event</td><td>Founder ₹4.1 L</td><td>Round 1 ~₹37 L</td><td>None if occupancy holds</td><td>Optional Round 2 ₹40–60 L for node 2</td></tr>
      <tr><td>Team</td><td>Promoter + advocate + PE</td><td>Promoter sells; 1 local tech on AMC</td><td>+ part-time traffic / creative</td><td>Do not hire a “network CEO”</td></tr>
      <tr><td>Software</td><td>Rate card + one-pager</td><td>NovaStar + PiSignage/VNNOX; auto-dim</td><td>Hivestack/Lemma on unsold only</td><td>Proof-of-play pack for Round 2</td></tr>
    </tbody>
  </table>
  <h2>Operating model (Site 1)</h2>
  <ul>
    <li><strong>Entity:</strong> private limited, Kerala GSTIN, current account with AD code (IEC only if importing).</li>
    <li><strong>Site:</strong> leave-and-licence, hybrid ₹50,000 or 18%, 36 months, 18-month lock-in, 3-month deposit (or waived in JV).</li>
    <li><strong>Hardware:</strong> volume OEM USD 330/sq.m, FAT (IP65, 5,500 nits, salt spray, 72-hour burn-in) before BL. NovaStar TB60.</li>
    <li><strong>Sales:</strong> founder-led, 10-second slots in a 100-second loop, 10 slots. Pre-sell 5 before crane. No agency in year 1 unless they bring an IO.</li>
    <li><strong>Do not:</strong> apartment terrace, domestic meter, NH RoW, ₹1.5 L fixed rent, FOB order before file number, two outdoor boards in year 1.</li>
  </ul>
</section>

<section class="section">
  <h1><span class="num">07</span>Financial plan, uses of funds, unit economics</h1>
  <p>Planning case: Path A, 32 sq.m, volume OEM, USD/INR 84, Kochi Class A, 10 × ₹50,000, hybrid rent. Mid-range live cash <strong>₹41 L</strong>. Founder 10% = <strong>₹4.1 L</strong>. Gap = <strong>₹36.9 L</strong>.</p>

  <h2>7.1 Uses — Round 0 (founder 10%)</h2>
  <table>
    <thead><tr><th>Use</th><th class="num">₹</th><th>Why this, not steel</th></tr></thead>
    <tbody>
      <tr><td>Company, GSTIN, current account, CA</td><td class="num">30,000</td><td>You cannot raise into a proprietorship with a cousin’s PAN.</td></tr>
      <tr><td>Advocate: title + hybrid licence draft + stamp plan</td><td class="num">60,000</td><td>No NOC, no deal.</td></tr>
      <tr><td>Structural PE on a named building + frame design</td><td class="num">1,00,000</td><td>Investors will ask; insurers will ask.</td></tr>
      <tr><td>IBPMS / KMBR drawings + s. 272 file opening</td><td class="num">70,000</td><td>This is the product Round 1 buys against.</td></tr>
      <tr><td>Inspectorate sketch + KSEB sub-meter paperwork</td><td class="num">30,000</td><td>Start the queue; do not pay full connection yet.</td></tr>
      <tr><td>Sales kit, site photography, 8 weeks promoter float</td><td class="num">80,000</td><td>Five LOIs are the other half of de-risking.</td></tr>
      <tr><td>Contingency / travel / Corporation miscellaneous</td><td class="num">40,000</td><td>Files move on chai and presence.</td></tr>
      <tr class="total"><td>Round 0 total (the 10%)</td><td class="num">4,10,000</td><td>Must leave a Corporation file number + 5 LOIs</td></tr>
    </tbody>
  </table>
  <p class="note">If a named building is not in hand by week 3, stop spending. Do not “keep the consultant busy.”</p>

  <h2>7.2 Uses — Round 1 (the 90%, after file number)</h2>
  <table>
    <thead><tr><th>Use</th><th class="num">₹ L</th><th>Note</th></tr></thead>
    <tbody>
      <tr><td>Screen + structure + electrics (cash, incl. IGST)</td><td class="num">31.1</td><td>Volume OEM. ITC on IGST ~₹2.1 L.</td></tr>
      <tr><td>Remaining year-0 tax, insurance, Inspectorate, sub-meter</td><td class="num">4.0</td><td>Round 0 already spent ~₹1.5–2 L of the ₹5–8 L admin band.</td></tr>
      <tr><td>Landlord deposit (or waived in JV)</td><td class="num">1.5</td><td>3 months of ₹50,000 floor. 6 months if owner insists.</td></tr>
      <tr><td>Working capital — 1 month power + CMS</td><td class="num">0.8</td><td>Do not go live with a dark meter.</td></tr>
      <tr class="total"><td>Round 1 uses</td><td class="num">~37.4</td><td>Closes ~₹41 L live cash with Round 0 already spent</td></tr>
    </tbody>
  </table>

  <h2>7.3 Site 1 monthly P&amp;L (building, Kochi Class A)</h2>
  <table>
    <thead><tr><th></th><th class="num">50% sold</th><th class="num">75% sold</th><th class="num">90% sold</th></tr></thead>
    <tbody>
      <tr><td>Gross advertising revenue</td><td class="num">₹2.50 L</td><td class="num">₹3.75 L</td><td class="num">₹4.50 L</td></tr>
      <tr><td>Hybrid rent</td><td class="num">₹50,000</td><td class="num">₹67,500</td><td class="num">₹81,000</td></tr>
      <tr><td>Power + tax + CMS + AMC</td><td class="num">₹82,000</td><td class="num">₹82,000</td><td class="num">₹82,000</td></tr>
      <tr class="total"><td>Leftover before commission and salary</td><td class="num">₹1.18 L</td><td class="num">₹2.26 L</td><td class="num">₹2.87 L</td></tr>
    </tbody>
  </table>
  <p>Founder sells in year 1 (no 10% agency). Simple payback on ₹41 L at 75% sold is about <strong>18 months</strong>. At 50% it is about <strong>35 months</strong> — still a business, not a mall trap. Pre-sell half the loop so you never live the 0% case (floor rent + power still ~₹1.3 L/month dark).</p>
  <p>Unipole 1-face leftover at 75% is similar (~₹2.20 L) but payback stretches to ~26 months on ~₹58 L live. Dual unipole leftover ~₹4.74 L at 75% — attractive only if Round 1 can actually close at ₹75–90 L. With 10% cash, it usually cannot.</p>

  <h2>7.4 If the 10% is of the six-node cheque, not of Site 1</h2>
  <p>Some promoters mean “I have 10% of ₹1.5–2.0 Cr” (₹15–20 L), not 10% of ₹41 L. That is a different conversation, and still not a six-node raise.</p>
  <table>
    <thead><tr><th>Founder cash</th><th>What it funds</th><th>What it still does not fund</th></tr></thead>
    <tbody>
      <tr><td>₹4.1 L (10% of Site 1)</td><td>Round 0 only: file, PE, LOIs</td><td>Deposit, LED, tax challan in full</td></tr>
      <tr><td>₹15–20 L (10% of 6-node)</td><td>Round 0 + landlord deposit + year-1 tax + a thicker working-capital buffer</td><td>The screen. Round 1 shrinks to ~₹25–28 L equity, which is an easier close</td></tr>
      <tr><td>₹41 L (100% of Site 1)</td><td>You do not raise. You switch on Path A yourself</td><td>Still do not order a second pole</td></tr>
    </tbody>
  </table>
  <div class="callout ice">
    <h3>Tell the investor which 10% you mean</h3>
    <p>Write the number in rupees on page one of the data room: “Founder cash in the company as of [date]: ₹____.” Ambiguity here is how otherwise serious meetings die in the first five minutes.</p>
  </div>
</section>

<section class="section">
  <h1><span class="num">08</span>SWOT — investor-facing</h1>
  <p>This is the SWOT a Big Four would put in the IC memo: capital and permission first, not LED pitch-size. Operational SWOT of Path A vs Path B sits in the companion cost pack.</p>
  <div class="swot">
    <div class="swot-box s">
      <h3>Strengths</h3>
      <ul>
        <li>Unit economics of one legal Kochi outdoor face dwarf indoor: ~₹2.3 L leftover at 75% vs ~₹0.3 L on a mall kiosk.</li>
        <li>Building mount keeps Site 1 inside a ₹40 L raise — fundable by one angel + prepay, not a VC process.</li>
        <li>Permission, once held, is slow for copiers; Corporation LED scarcity is a tailwind for legal private inventory.</li>
        <li>Hybrid rent and founder-as-salesperson keep the cash-out low in year 1.</li>
        <li>Visible asset: investors can stand on the footpath and see what they funded. Rare in “tech” pitches.</li>
        <li>Round 0 uses the 10% on artefacts investors actually diligence (file number, PE cert, LOIs).</li>
      </ul>
    </div>
    <div class="swot-box w">
      <h3>Weaknesses</h3>
      <ul>
        <li>Ten percent cash. No books. First-time promoter. Every Round 1 cheque is a personal-trust cheque.</li>
        <li>Permission is political (30–90 days; 4–6 months if highway-facing). Calendar can eat the civil window.</li>
        <li>Single-site concentration: one demolition order or slab refusal kills the only asset.</li>
        <li>Power is the second-largest site cost. Auto-dimming is a P&amp;L control, not a nice-to-have.</li>
        <li>FOB USD 330 is not secured; customs reclass to 20% BCD adds ~₹1 L+ on one face.</li>
        <li>No in-house fabrication or media-network brand. You are an operator, not Times OOH.</li>
      </ul>
    </div>
    <div class="swot-box o">
      <h3>Opportunities</h3>
      <ul>
        <li>Landlord JV: terrace + deposit waived for 12–25% of the SPV — the cleanest way to shrink the 90%.</li>
        <li>Advertiser-investor: a jewellery / hospital / auto group takes two slots and ₹10–18 L of CCPS.</li>
        <li>Kerala NRI / Gulf family capital, on FEMA-clean terms, is a real channel — not a VC deck.</li>
        <li>Customer 3-month prepay (₹5–7.5 L) is non-dilutive working capital once the file exists.</li>
        <li>Equipment hypothecation after import can take ₹8–12 L of peak cash off the equity ask.</li>
        <li>Site 2 (Kozhikode) can be a follow-on after proof-of-play, not part of this raise.</li>
      </ul>
    </div>
    <div class="swot-box t">
      <h3>Threats</h3>
      <ul>
        <li>Selling 40% for ₹10 L to a “media partner” who only knows flex. That is a failed raise, not a close.</li>
        <li>Raising ₹2 Cr on a six-node slide with no file. Sophisticated money will walk; unsophisticated money will own you.</li>
        <li>Ordering FOB before s. 272: warehouse rent then exceeds the fee; monsoon can void IP warranty at ICTT.</li>
        <li>NHAI / High Court climate: private terrace is not a loophole. Highway-facing still needs PWD/NHAI.</li>
        <li>Landlord rent reset, association politics, domestic-meter temptation, neighbour glare petitions.</li>
        <li>Hiring a Big Four implementation team or a “CMO” before the crane. The 10% dies of overhead.</li>
      </ul>
    </div>
  </div>
</section>

<section class="section">
  <h1><span class="num">09</span>Capital formation — closing the 90%</h1>
  <div class="callout">
    <h3>The pitch line (use this, not a TAM)</h3>
    <p>We are not raising to buy a network. We are raising to switch on one legal Kochi face that already has a Corporation file and five brand LOIs. The 10% founder cash bought the permission. Your money buys the screen.</p>
  </div>
  <p>Round 1 is a <strong>barbell</strong>: some non-dilutive cash (prepay, optional debt, landlord in-kind) plus one equity cheque. Do not run a 40-investor seed. Do not talk to SaaS VCs.</p>

  <h2>9.1 Sources to close ~₹37 L (planning close)</h2>
  <table>
    <thead>
      <tr><th>Source</th><th>Instrument</th><th class="num">₹ L</th><th>Dilution</th><th>Condition to draw</th></tr>
    </thead>
    <tbody>
      <tr><td>Founder (already in)</td><td>Equity — Round 0</td><td class="num">4.1</td><td>Founder residual</td><td>Spent on file + LOIs</td></tr>
      <tr><td>Landlord</td><td>Deposit waived + 3-month holiday, or 12–20% equity</td><td class="num">1.5–3.0 saved</td><td>0–20%</td><td>Clean title, hybrid licence</td></tr>
      <tr><td>Anchor brands</td><td>3-month prepay on 5 slots, GST invoice, escrow</td><td class="num">7.5</td><td>0%</td><td>File number + sightline photos</td></tr>
      <tr><td>Angel / NRI / advertiser-investor</td><td>CCPS, 18–24 month conversion</td><td class="num">18.0</td><td>16–22%</td><td>Data room; personal guarantee on any debt</td></tr>
      <tr><td>NBFC / equipment (optional)</td><td>Hypothecation of LED post-import</td><td class="num">8–10</td><td>0% (debt)</td><td>GSTIN, banked account, often PG of founder</td></tr>
      <tr class="total"><td>Planning close</td><td>Equity + prepay + in-kind (± debt)</td><td class="num">~41 live</td><td>Founder ≥ 65%</td><td>No FOB until money is in escrow</td></tr>
    </tbody>
  </table>
  <p class="note">If NBFC says no (likely without two years of books), increase the CCPS cheque to ~₹25–28 L or deepen the landlord JV. Do not fill the hole with a moneylender against the family house if the sightline is not signed.</p>

  <h2>9.2 Two acceptable structures</h2>
  <table>
    <thead><tr><th></th><th>Structure 1 — Angel heavy</th><th>Structure 2 — Landlord JV (preferred if owner is real)</th></tr></thead>
    <tbody>
      <tr><td>Founder</td><td>78% ordinary</td><td>68% ordinary</td></tr>
      <tr><td>Angel / NRI</td><td>22% CCPS for ₹18–22 L</td><td>15% CCPS for ₹15–18 L</td></tr>
      <tr><td>Landlord</td><td>0% (cash rent + deposit)</td><td>17% for terrace + deposit waived + holiday</td></tr>
      <tr><td>Customers</td><td>₹7.5 L advance, not equity</td><td>₹7.5 L advance, not equity</td></tr>
      <tr><td>Debt</td><td>₹8–10 L if available</td><td>Avoid if JV already shrinks cash</td></tr>
      <tr><td>Post-money (indicative)</td><td>₹80–1,00 L</td><td>₹80–1,00 L including in-kind at conservative value</td></tr>
    </tbody>
  </table>
  <p>Indicative math: ₹18 L for 20% implies ₹90 L post-money. That is enough for a first-time promoter with a file and LOIs, and not so high that Round 2 is boxed in. Anyone offering ₹10 L for 40% is buying the company, not funding a screen.</p>

  <h2>9.3 Who actually writes cheques in this market</h2>
  <ul>
    <li><strong>Advertiser-investors</strong> — jewellery, hospitals, auto dealers, education groups who already buy Kochi outdoor. Best fit: 2 slots + CCPS.</li>
    <li><strong>NRI / Gulf family</strong> — Kerala’s real informal VC. Use FEMA-clean CCPS, Indian company, authorised dealer bank. Not hawala, not cash in a bag.</li>
    <li><strong>One Kochi or Bangalore angel</strong> who has operated OOH, print, or mall media. Not a SaaS fund. Not a “startup community.”</li>
    <li><strong>Not:</strong> seed VCs, listed NBFCs without books (unless LAP on other property — generally refuse), crypto, partnership with a flex contractor who wants 50% and the crane contract.</li>
  </ul>

  <h2>9.4 What the 10% must never fund</h2>
  <ul>
    <li>FOB cabinets, a unipole fabrication advance, or a mall licence deposit.</li>
    <li>A Big Four, a branding agency, or a full-time CMO.</li>
    <li>Personal lifestyle. Round 0 is a file and five meetings a week in Ernakulam.</li>
  </ul>
</section>

<section class="section">
  <h1><span class="num">10</span>Fundraising process, materials, who to call</h1>
  <p>A Big Four would not “run a roadshow” on this ticket unless separately retained. They would build a <strong>12-week close process</strong> the promoter executes. Start the process only when Round 0 artefacts exist. Talking before that trains investors to say no.</p>

  <h2>10.1 Twelve-week close (after file number)</h2>
  <table>
    <thead><tr><th>Week</th><th>Promoter does</th><th>Investor sees</th></tr></thead>
    <tbody>
      <tr><td>1–2</td><td>Data room live. 15-name list. Warm intros only (CA, advocate, brands).</td><td>This memo + cost pack + file scan + LOIs.</td></tr>
      <tr><td>3–5</td><td>8–10 first meetings. Site walk. One term sheet target, not five.</td><td>Slab, sightline at peak hour, hybrid licence draft.</td></tr>
      <tr><td>6–8</td><td>Exclusive with one lead (21-day exclusivity). Lawyer on SHA/SSA.</td><td>Cap table, use of funds, FAT protocol, escrow instruction.</td></tr>
      <tr><td>9–12</td><td>Money in escrow. Then OEM booking. Then crane.</td><td>No steel ordered on a promise.</td></tr>
    </tbody>
  </table>

  <h2>10.2 Data room index (keep it thin)</h2>
  <ol>
    <li>This strategy memorandum + the cost/SWOT PDF + the execution blueprint PDF.</li>
    <li>Certificate of incorporation, PAN, GSTIN, shareholding (founder 100% pre-round).</li>
    <li>Owner NOC, title note from advocate, hybrid licence draft.</li>
    <li>Corporation file number / acknowledgement; tax challan if already paid.</li>
    <li>Structural PE certificate (IS 875, 39 m/s) on <em>that</em> building.</li>
    <li>Five LOIs: advertiser, period, slot count, price, prepay willingness.</li>
    <li>OEM FAT protocol and two quote comparisons (volume vs premium).</li>
    <li>18-month cash waterfall (this section 7 and 9).</li>
    <li>Draft CCPS term sheet (section 11).</li>
  </ol>
  <p>That is nine folders. Not a brand film. Not a 40-slide TAM.</p>

  <h2>10.3 Meeting script (12 minutes)</h2>
  <ol>
    <li>The asset: one legal Kochi face, this building, this sightline (photo).</li>
    <li>The constraint we already solved: permission and 50% demand (file + LOIs).</li>
    <li>The cheque: ₹18 L CCPS for ~20%, uses on one page, founder stays operator.</li>
    <li>The return path: 18-month payback at 75%; follow-on only after proof-of-play.</li>
    <li>The kill criteria: no NH RoW, no FOB before escrow, no second node in this round.</li>
  </ol>
</section>

<section class="section">
  <h1><span class="num">11</span>Governance, cap table, term-sheet headlines</h1>
  <p>Keep the company boring and clean. Investors in a ₹18 L cheque still walk if the SHA looks like a VC growth round — or if there is no SHA at all.</p>
  <table>
    <thead><tr><th>Item</th><th>Headline for Round 1</th></tr></thead>
    <tbody>
      <tr><td>Vehicle</td><td>One private limited company. No LLP, no “we’ll incorporate later.” Optional site SPV only if landlord insists — still 100% owned by the HoldCo except landlord’s agreed %.</td></tr>
      <tr><td>Instrument</td><td>CCPS, compulsorily converting in 18–24 months or at Round 2, 1:1 into equity, 8% non-cumulative coupon accruing.</td></tr>
      <tr><td>Amount / %</td><td>₹15–22 L for 16–22%. Founder not below 65% fully diluted after landlord (if any).</td></tr>
      <tr><td>Valuation</td><td>₹70–90 L post-money. Information rights, not a board veto on operations. Board: founder + 1 investor observer.</td></tr>
      <tr><td>Use of proceeds</td><td>LED + structure + remaining statutory + deposit + 1 month WC. No related-party drain, no other city.</td></tr>
      <tr><td>Reserved matters</td><td>New debt &gt; ₹10 L, second site, related-party contracts, founder salary &gt; ₹50k/month in year 1, sale of the face.</td></tr>
      <tr><td>Founder vest</td><td>4-year reverse vest with 1-year cliff on a portion (25%) so a disappearing promoter does not strand the LED.</td></tr>
      <tr><td>Information</td><td>Monthly occupancy, proof-of-play, bank balance. Quarterly unaudited. Year-1 audit.</td></tr>
      <tr><td>Exit</td><td>No promise of IPO. Path is cash yield + optional sale of the site company to a network after 3 years of clean files.</td></tr>
    </tbody>
  </table>
  <div class="callout ice">
    <h3>Personal guarantee</h3>
    <p>NBFCs will ask for a personal guarantee. Angels sometimes will. Give it on equipment debt if the LED is hypothecated and insured. Do not give an unlimited PG on landlord make-good of someone else’s building. Cap any PG at the debt principal.</p>
  </div>
</section>

<section class="section">
  <h1><span class="num">12</span>Conditions precedent and 90-day workplan</h1>
  <div class="callout">
    <h3>Do not open Round 1 until all of these exist</h3>
    <p>Written owner NOC; advocate title note; structural PE on that slab; IBPMS / s. 272 file number; five brand LOIs covering ≥ 50% of the loop; hybrid licence in draft; GSTIN live. Until then, the only money that moves is the ₹4.1 L Round 0 wallet.</p>
  </div>
  <table>
    <thead><tr><th>Week</th><th>Do</th><th>Spend from the 10%</th><th>Do not</th></tr></thead>
    <tbody>
      <tr><td>1–2</td><td>Incorporate / GST if needed. Shortlist 5 commercial buildings. Advocate on the best two titles. Confirm the ₹4.1 L is in the company account.</td><td>~₹0.6 L</td><td>Apartment terraces; domestic meters; NH RoW plots; OEM calls that “need 50% advance.”</td></tr>
      <tr><td>3–4</td><td>Written NOC. PE on the chosen slab. Hybrid licence drafted. IBPMS + s. 272 opened. One-pager + rate card to 20 brands.</td><td>~₹1.7 L</td><td>Order FOB. Pay a “liaison” cash to skip the file. Sign ₹1.5 L fixed rent.</td></tr>
      <tr><td>5–8</td><td>Chase the file in person. Inspectorate sketch. Collect 5 LOIs. Build the nine-folder data room. 15-name investor list, no outbound spam.</td><td>~₹1.2 L</td><td>Hire staff. Start a unipole soil bid “just in case” unless Path A is dead.</td></tr>
      <tr><td>9–12</td><td>File still moving: keep selling. File in hand: 12-week Round 1 process (section 10). Escrow. Then FAT/OEM.</td><td>Remainder</td><td>Crane. Dual-face. Kozhikode. Mall MoUs. Big Four implementation.</td></tr>
    </tbody>
  </table>
  <h2>Kill switches (write these on the inside cover of the bank passbook)</h2>
  <ul>
    <li>No named commercial building with a real sightline by week 4 → stop. Keep the rest of the 10%.</li>
    <li>No file number by week 16 → do not raise; do not import; revisit Path B only if setbacks and title are clean.</li>
    <li>No 50% LOIs by crane minus 30 days → delay install; do not go live dark.</li>
    <li>Any term sheet &gt; 30% dilution for &lt; ₹15 L → walk.</li>
  </ul>
  <p>If Path A is impossible and Path B (unipole) is the only lawful sightline, restart this memo with live cash ₹55–62 L (1-face) or ₹75–90 L (dual). The 10% then funds soil + KMBR as a new structure + KSEB new-connection queue — still not the pole. The fundraising logic does not change: <strong>permission and demand first, steel second.</strong></p>
  <p class="disclaimer">Independent working paper, September 2026. This is not a legal opinion, a valuation, a securities offer, or a report of Deloitte, PwC, EY, KPMG or any affiliate. Planning rates (advertisement tax, KSEB LT-VII(A), customs BCD, stamp duty) change by gazette and council resolution. Confirm with Kochi / Kozhikode / Kannur Corporation Revenue, KSERC, CBIC, an authorised dealer bank (for any NRI cheque), and a practising Kerala advocate before committing capital. Companion files: <code>docs/Kerala_DOOH_Cost_Estimate_and_SWOT.pdf</code>, <code>docs/Kerala_DOOH_Network_Blueprint.pdf</code>, <code>dooh_kerala_calculator.py</code>. Regenerated with <code>python3 scripts/build_strategy_capital_pdf.py</code>.</p>
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
