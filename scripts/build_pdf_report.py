#!/usr/bin/env python3
"""Build the Kerala DOOH execution-blueprint PDF from the markdown pack."""

from __future__ import annotations

import html
import sys
from datetime import date
from pathlib import Path

import markdown
from weasyprint import CSS, HTML

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import dooh_kerala_calculator as calc  # noqa: E402

OUT_PDF = ROOT / "docs" / "Kerala_DOOH_Network_Blueprint.pdf"
OUT_HTML = ROOT / "docs" / "_pdf_build.html"

FONT_SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
FONT_SANS_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
FONT_SANS_ITALIC = "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"
FONT_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"


def md_to_html(text: str) -> str:
    return markdown.markdown(
        text,
        extensions=["tables", "fenced_code", "sane_lists", "nl2br", "smarty"],
    )


def inr_lakh(value: float) -> str:
    return f"₹{value / 100_000:,.2f} L"


def inr_cr(value: float) -> str:
    return f"₹{value / 10_000_000:,.2f} Cr"


def scenario_card(name: str) -> dict:
    preset = calc.scenario_presets(name)
    cfg = calc.CalculatorConfig(
        occupancy=preset["occupancy"],
        programmatic_fill=preset["programmatic_fill"],
        conservative_hs=preset["conservative_hs"],
        scenario=preset["scenario"],
        fob_usd_per_sqm=preset.get("fob_usd_per_sqm", calc.OUTDOOR_FOB_USD_PER_SQM),
        sales_commission=preset.get("sales_commission", calc.SALES_COMMISSION_RATE),
        amc_rate=preset.get("amc_rate", calc.AMC_RATE),
        outdoor_slots_per_face=preset.get("outdoor_slots_per_face", calc.OUTDOOR_SLOTS_PER_FACE),
    )
    return calc.compute(cfg)


def kpi_row(result) -> str:
    payback = f"{result.payback_months:.1f} mo" if result.payback_months else "n/a"
    return f"""
    <div class="kpi">
      <div class="kpi-label">{html.escape(result.scenario.upper())}</div>
      <div class="kpi-grid">
        <div><span>CAPEX</span><strong>{inr_cr(result.capex_total_inr)}</strong></div>
        <div><span>Revenue / mo</span><strong>{inr_lakh(result.revenue_gross_monthly_inr)}</strong></div>
        <div><span>EBITDA / mo</span><strong>{inr_lakh(result.ebitda_monthly_inr)}</strong></div>
        <div><span>Payback</span><strong>{payback}</strong></div>
        <div><span>Margin</span><strong>{result.net_operating_margin * 100:.1f}%</strong></div>
        <div><span>Annual ROI</span><strong>{(result.annual_roi or 0) * 100:.1f}%</strong></div>
      </div>
    </div>
    """


def load_section(path: Path, strip_h1: bool = True) -> str:
    text = path.read_text(encoding="utf-8")
    if strip_h1:
        lines = text.splitlines()
        if lines and lines[0].startswith("# "):
            text = "\n".join(lines[1:]).lstrip("\n")
    return md_to_html(text)


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
@font-face {{
  font-family: ReportMono;
  src: url("file://{FONT_MONO}");
}}

:root {{
  --ink: #1b2430;
  --muted: #4a5563;
  --rule: #c5a572;
  --band: #0f3d3e;
  --paper: #f7f3ea;
  --table-head: #0f3d3e;
}}

* {{ box-sizing: border-box; }}

html, body {{
  margin: 0;
  padding: 0;
  color: var(--ink);
  font-family: ReportSans, "Liberation Sans", sans-serif;
  font-size: 10.2pt;
  line-height: 1.45;
}}

@page {{
  size: A4;
  margin: 18mm 16mm 20mm 16mm;
  @top-left {{
    content: "Kerala DOOH Network  ·  Kochi · Kozhikode · Kannur";
    font-family: ReportSans, sans-serif;
    font-size: 8pt;
    color: #5c6570;
    letter-spacing: 0.04em;
  }}
  @top-right {{
    content: "Confidential working paper";
    font-family: ReportSans, sans-serif;
    font-size: 8pt;
    color: #5c6570;
  }}
  @bottom-left {{
    content: "Execution blueprint  |  September 2026";
    font-family: ReportSans, sans-serif;
    font-size: 8pt;
    color: #5c6570;
  }}
  @bottom-right {{
    content: "Page " counter(page);
    font-family: ReportSans, sans-serif;
    font-size: 8pt;
    color: #5c6570;
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
  page: first;
  min-height: 297mm;
  background: var(--band);
  color: #f7f3ea;
  padding: 28mm 22mm 22mm 22mm;
  break-after: page;
}}
.cover-kicker {{
  letter-spacing: 0.28em;
  text-transform: uppercase;
  font-size: 9pt;
  color: var(--rule);
  margin-bottom: 18mm;
}}
.cover h1 {{
  font-size: 28pt;
  line-height: 1.12;
  margin: 0 0 8mm 0;
  font-weight: 700;
  max-width: 150mm;
  color: #f7f3ea;
  border-bottom: none;
  padding-bottom: 0;
}}
.cover .sub {{
  font-size: 13pt;
  color: #d7c4a3;
  margin: 0 0 16mm 0;
  max-width: 150mm;
}}
.cover-meta {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 6mm 12mm;
  max-width: 160mm;
  font-size: 10pt;
  border-top: 1px solid #2c6a6b;
  padding-top: 8mm;
}}
.cover-meta span {{
  display: block;
  color: var(--rule);
  font-size: 8pt;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  margin-bottom: 1.5mm;
}}
.cover-foot {{
  position: absolute;
  bottom: 18mm;
  left: 22mm;
  right: 22mm;
  font-size: 8.5pt;
  color: #c9d6d6;
  border-top: 1px solid #2c6a6b;
  padding-top: 6mm;
}}

h1, h2, h3, h4 {{
  color: var(--band);
  page-break-after: avoid;
  line-height: 1.25;
}}
h1 {{
  font-size: 18pt;
  margin: 0 0 6mm 0;
  padding-bottom: 3mm;
  border-bottom: 2px solid var(--rule);
}}
h2 {{
  font-size: 13.5pt;
  margin: 9mm 0 3.5mm 0;
  padding-bottom: 1.5mm;
  border-bottom: 0.6pt solid #d8c7a8;
}}
h3 {{
  font-size: 11.5pt;
  margin: 6mm 0 2.5mm 0;
}}
h4 {{
  font-size: 10.5pt;
  margin: 4mm 0 2mm 0;
}}
p {{ margin: 0 0 3mm 0; }}
ul, ol {{ margin: 0 0 3.5mm 1.5mm; padding-left: 5mm; }}
li {{ margin-bottom: 1.2mm; }}
strong {{ color: #122226; }}
a {{ color: #0f3d3e; text-decoration: none; }}
blockquote {{
  margin: 3mm 0 4mm 0;
  padding: 2.5mm 4mm;
  border-left: 3px solid var(--rule);
  background: #f3eee3;
  color: var(--muted);
}}

table {{
  width: 100%;
  border-collapse: collapse;
  margin: 2mm 0 5mm 0;
  font-size: 8.7pt;
  page-break-inside: auto;
}}
thead {{ display: table-header-group; }}
tr {{ page-break-inside: avoid; }}
th {{
  background: var(--table-head);
  color: #f7f3ea;
  text-align: left;
  padding: 2.2mm 2.4mm;
  font-weight: 700;
}}
td {{
  padding: 1.8mm 2.4mm;
  border-bottom: 0.4pt solid #d7ddd8;
  vertical-align: top;
}}
tr:nth-child(even) td {{ background: #f4f1e8; }}

pre, code {{
  font-family: ReportMono, monospace;
}}
code {{
  font-size: 8.6pt;
  background: #eef2ef;
  padding: 0 1mm;
}}
pre {{
  background: #122226;
  color: #e8efe8;
  font-size: 8pt;
  line-height: 1.4;
  padding: 4mm;
  margin: 2mm 0 5mm 0;
  white-space: pre-wrap;
  word-break: break-word;
}}
pre code {{
  background: transparent;
  color: inherit;
  padding: 0;
}}

.section {{
  break-before: page;
}}
.section.keep {{
  break-before: auto;
}}
.toc {{
  break-after: page;
}}
.toc ol {{
  list-style: none;
  padding: 0;
  margin: 0;
}}
.toc li {{
  display: flex;
  justify-content: space-between;
  border-bottom: 0.4pt dotted #c9c1b2;
  padding: 2.4mm 0;
  font-size: 11pt;
}}
.toc .num {{
  color: var(--rule);
  font-weight: 700;
  margin-right: 4mm;
}}
.callout {{
  background: #0f3d3e;
  color: #f7f3ea;
  padding: 5mm 6mm;
  margin: 0 0 7mm 0;
}}
.callout h3 {{
  color: var(--rule);
  margin: 0 0 2mm 0;
  font-size: 10pt;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}}
.callout p {{ margin: 0; font-size: 10pt; }}
.kpi {{
  border: 0.6pt solid #d8c7a8;
  padding: 4mm 5mm;
  margin: 0 0 5mm 0;
  break-inside: avoid;
}}
.kpi-label {{
  font-size: 8.5pt;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--band);
  font-weight: 700;
  margin-bottom: 3mm;
}}
.kpi-grid {{
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 3mm;
}}
.kpi-grid span {{
  display: block;
  font-size: 7.5pt;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--muted);
}}
.kpi-grid strong {{
  font-size: 12pt;
}}
.disclaimer {{
  font-size: 8.5pt;
  color: var(--muted);
  border-top: 0.6pt solid #d8c7a8;
  padding-top: 3mm;
  margin-top: 6mm;
}}
"""


def build_html() -> str:
    today = date(2026, 9, 7).strftime("%d %B %Y")
    base = scenario_card("base")
    target = scenario_card("target")
    conservative = scenario_card("conservative")

    exec_md = f"""
This report is the execution pack for a **six-node Digital Out-Of-Home (DOOH) pilot** across Kerala’s three strongest north-and-central media markets. The network is two dual-face outdoor LED unipoles (Edappally / Kakkanad and Thondayad Bypass) plus four indoor dual-sided 55-inch MUPI kiosks (Lulu Mall, Forum Mall, HiLite Mall, Secura Centre / Capitol Mall).

**Hardware envelope.** Outdoor: P3.91 or P4 SMD LED, die-cast aluminium, IP65/IP66, ≥ 5,500 nits auto-dimming, silicone conformal coat, coastal C5-M paint. Indoor: dual 55-inch 2,500–3,000 nit commercial 4K behind 8 mm toughened glass. Players: NovaStar Taurus TB60 / TB30 with PiSignage or VNNOX, offline cache, and Hivestack / Lemma programmatic tags.

**The P&L hinge.** The stated slot card (Kochi outdoor ₹50,000 / Kozhikode outdoor ₹30,000 / mall ₹8,500 per slot per month) **does not repay a flagship China import in 12–16 months**. Dual-face outdoor inventory, hybrid leases (minimum guarantee vs 18% of site gross), and a volume OEM FOB are what land payback inside the target band.

| Scenario | Occupancy | LED FOB | Economic CAPEX | EBITDA / month | Payback |
| --- | ---: | ---: | ---: | ---: | ---: |
| Base (premium import) | 75% | USD 650 / sq.m | {inr_cr(base.capex_total_inr)} | {inr_lakh(base.ebitda_monthly_inr)} | {base.payback_months:.1f} months |
| Target (volume CKD) | 90% | USD 330 / sq.m | {inr_cr(target.capex_total_inr)} | {inr_lakh(target.ebitda_monthly_inr)} | {target.payback_months:.1f} months |
| Conservative HS 85285900 | 60% | USD 650 / sq.m | {inr_cr(conservative.capex_total_inr)} | {inr_lakh(conservative.ebitda_monthly_inr)} | {conservative.payback_months or 0:.1f} months |

Live numbers are produced by `dooh_kerala_calculator.py`. Statutory rupee rates (advertisement tax, stamp duty, KSERC slabs, BCD) must be confirmed with the corporation, KSERC, CBIC and a Kerala-enrolled advocate before capital is committed.
"""

    exec_html = f"""
<section class="section keep">
  <h1>0. Executive summary</h1>
  <div class="callout">
    <h3>Decision snapshot</h3>
    <p>Build dual-face outdoor unipoles on private land outside NH 66 RoW. Lease mall kiosks on a hybrid floor-plus-18% model. Import or CKD only after factory salt-spray and 72-hour burn-in. Cast outdoor foundations before 1 June. Use the target hardware/sales stack if a 12–16 month payback is a board constraint.</p>
  </div>
  {kpi_row(base)}
  {kpi_row(target)}
  {md_to_html(exec_md)}
</section>
"""
    blueprint = (ROOT / "docs" / "KERALA_DOOH_BLUEPRINT.md").read_text(encoding="utf-8")
    parts = blueprint.split("\n## MODULE ")
    intro = parts[0]
    intro_body = "\n".join(intro.splitlines()[1:])
    module_html = [f"""
<section class="section keep">
  <h1>Network topology and design envelope</h1>
  {md_to_html(intro_body)}
</section>
"""]
    titles = {
        "1": "Module 1 — Administrative, regulatory and compliance roadmap",
        "2": "Module 2 — Hardware sourcing and procurement",
        "3": "Module 3 — Site leasing and mall pitch",
        "4": "Module 4 — Financial model and ROI",
        "5": "Module 5 — Technical deployment and weather hardening",
        "6": "Module 6 — Automated execution script and mobilisation",
    }
    for chunk in parts[1:]:
        num = chunk[0]
        rest = chunk[1:]  # starts with " — Title\n"
        # remove the original MODULE title line
        rest = rest.split("\n", 1)[1] if "\n" in rest else rest
        heading = titles.get(num, f"Module {num}")
        module_html.append(
            f'<section class="section"><h1>{html.escape(heading)}</h1>{md_to_html(rest)}</section>'
        )

    annex_a = load_section(ROOT / "docs" / "legal" / "SITE_LEASE_AND_MOU.md")
    annex_b = load_section(ROOT / "docs" / "legal" / "STRUCTURAL_STABILITY_CERTIFICATE.md")
    annex_c = load_section(ROOT / "docs" / "procurement" / "QC_AND_IMPORT_CHECKLIST.md")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <title>Kerala DOOH Network — End-to-End Execution Blueprint</title>
</head>
<body>
  <section class="cover">
    <div class="cover-kicker">Confidential  ·  Working paper  ·  Not a legal opinion</div>
    <h1>Kerala Digital Out-Of-Home Network</h1>
    <p class="sub">End-to-end execution blueprint for a six-node pilot across Kochi, Kozhikode and Kannur — compliance, sourcing, leases, finance, coastal hardening and automation.</p>
    <div class="cover-meta">
      <div><span>Geography</span>Kochi · Kozhikode · Kannur</div>
      <div><span>Nodes</span>2 dual-face outdoor unipoles + 4 indoor MUPI kiosks</div>
      <div><span>Outdoor spec</span>P3.91 / P4 · IP65/66 · ≥ 5,500 nits · C5-M</div>
      <div><span>Indoor spec</span>Dual 55-inch 2,500–3,000 nit · 8 mm glass</div>
      <div><span>Target payback</span>{target.payback_months:.1f} months on the volume OEM stack</div>
      <div><span>Document date</span>{today}</div>
    </div>
    <div class="cover-foot">
      Prepared as an operations and investment working paper. Advertisement tax, customs classification, stamp duty and KSEB tariff must be confirmed against the live gazette before money moves. Courts: Ernakulam / Kozhikode / Kannur.
    </div>
  </section>

  <section class="toc">
    <h1>Contents</h1>
    <ol>
      <li><span><span class="num">00</span> Executive summary</span></li>
      <li><span><span class="num">01</span> Network topology and design envelope</span></li>
      <li><span><span class="num">02</span> Administrative, regulatory and compliance roadmap</span></li>
      <li><span><span class="num">03</span> Hardware sourcing and procurement</span></li>
      <li><span><span class="num">04</span> Site leasing and mall pitch</span></li>
      <li><span><span class="num">05</span> Financial model and ROI</span></li>
      <li><span><span class="num">06</span> Technical deployment and weather hardening</span></li>
      <li><span><span class="num">07</span> Calculator, formulas and 90-day mobilisation</span></li>
      <li><span><span class="num">A</span> Site lease / mall MoU clause set</span></li>
      <li><span><span class="num">B</span> Structural stability certificate template</span></li>
      <li><span><span class="num">C</span> Factory QC and ICTT Vallarpadam import checklist</span></li>
    </ol>
  </section>

  {exec_html}
  {''.join(module_html)}

  <section class="section">
    <h1>Annex A — Site lease agreement / mall MoU clause set</h1>
    {annex_a}
  </section>
  <section class="section">
    <h1>Annex B — Structural stability certificate (IS 875 / KMBR)</h1>
    {annex_b}
  </section>
  <section class="section">
    <h1>Annex C — Factory QC and Cochin Port import checklist</h1>
    {annex_c}
    <p class="disclaimer">End of report. Regenerated with <code>python3 scripts/build_pdf_report.py</code>. Figures in Module 4 and the executive summary are live outputs of <code>dooh_kerala_calculator.py</code>.</p>
  </section>
</body>
</html>
"""


def main() -> int:
    html_doc = build_html()
    OUT_HTML.write_text(html_doc, encoding="utf-8")
    HTML(filename=str(OUT_HTML), base_url=str(ROOT)).write_pdf(
        str(OUT_PDF),
        stylesheets=[CSS(string=CSS_TEXT)],
    )
    OUT_HTML.unlink(missing_ok=True)
    size_kb = OUT_PDF.stat().st_size / 1024
    print(f"Wrote {OUT_PDF} ({size_kb:.0f} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
