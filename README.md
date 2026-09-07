# Kerala DOOH Network Blueprint

Execution-ready business, compliance, hardware, and software plan for a six-node Digital Out-Of-Home network in **Kochi, Kozhikode, and Kannur**.

## Network (pilot)

| City | Outdoor unipole | Indoor dual-sided MUPI |
| --- | --- | --- |
| Kochi | 1 (Edappally / Kakkanad) | 2 (Lulu Mall, Forum Mall) |
| Kozhikode | 1 (Thondayad Bypass) | 1 (HiLite Mall) |
| Kannur | — | 1 (Secura Centre / Capitol Mall) |

**Total:** 2 dual-face outdoor LED unipoles + 4 indoor kiosks = 6 display nodes.

## Repository layout

| Path | Contents |
| --- | --- |
| [docs/KERALA_DOOH_BLUEPRINT.md](docs/KERALA_DOOH_BLUEPRINT.md) | Modules 1–6: compliance, sourcing, leases, finance, weather hardening, calculator usage |
| [docs/legal/SITE_LEASE_AND_MOU.md](docs/legal/SITE_LEASE_AND_MOU.md) | Kerala-specific site lease / mall MoU clause set |
| [docs/legal/STRUCTURAL_STABILITY_CERTIFICATE.md](docs/legal/STRUCTURAL_STABILITY_CERTIFICATE.md) | Structural engineer sign-off template (IS 875 / KMBR) |
| [docs/procurement/QC_AND_IMPORT_CHECKLIST.md](docs/procurement/QC_AND_IMPORT_CHECKLIST.md) | Factory QC, salt-spray, and ICTT Vallarpadam import workflow |
| [docs/Kerala_DOOH_Network_Blueprint.pdf](docs/Kerala_DOOH_Network_Blueprint.pdf) | Printable A4 report (cover + 6 modules + annexes) |
| [docs/Kerala_DOOH_Cost_Estimate_and_SWOT.pdf](docs/Kerala_DOOH_Cost_Estimate_and_SWOT.pdf) | Building vs unipole outdoor: cost split, rent, regulatory cash, SWOT |
| [dooh_kerala_calculator.py](dooh_kerala_calculator.py) | CAPEX / OPEX / revenue / payback calculator (Python stdlib) |

## Run the financial model

```bash
python3 dooh_kerala_calculator.py --scenario base
python3 dooh_kerala_calculator.py --scenario target
python3 dooh_kerala_calculator.py --occupancy 0.8 --lease-model hybrid --json
python3 -m unittest tests.test_dooh_kerala_calculator -v
```

## PDF report

A 26-page A4 working paper (cover, contents, six modules, three annexes) is generated at:

**[docs/Kerala_DOOH_Network_Blueprint.pdf](docs/Kerala_DOOH_Network_Blueprint.pdf)**

Regenerate after editing the markdown pack:

```bash
python3 -m pip install weasyprint markdown   # once
python3 scripts/build_pdf_report.py
python3 scripts/build_cost_swot_pdf.py
```

A shorter investor pack (building-mounted vs private-land unipole: cost split, rent, regulatory cash, SWOT) is at **[docs/Kerala_DOOH_Cost_Estimate_and_SWOT.pdf](docs/Kerala_DOOH_Cost_Estimate_and_SWOT.pdf)**.

## Model headlines (INR, dual-face outdoor, hybrid leases)

| Scenario | Economic CAPEX | Monthly EBITDA | Payback | Notes |
| --- | --- | --- | --- | --- |
| `base` | ₹1.95 Cr | ₹6.74 L | **29 months** | Premium FOB USD 650/sq.m, 75% occupancy |
| `target` | ₹1.54 Cr | ₹9.69 L | **15.9 months** | Volume OEM USD 330/sq.m, 90% occupancy, 6% commission |

The 12–16 month payback target is the `target` stack, not the flagship-import `base` case. Module 4 of the blueprint explains the levers.

## Disclaimer

Statutory rates (advertisement tax, KSEB tariff, customs BCD, stamp duty) change by gazette and council resolution. Confirm the live schedule with the concerned corporation, KSERC, CBIC, and a practising Kerala advocate before committing capital or signing leases.
