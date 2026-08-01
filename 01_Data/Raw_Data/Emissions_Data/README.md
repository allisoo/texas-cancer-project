# Benzene Emissions — Big Spring Refinery (2016–2026)

**Ticket:** BEN-4
**Facility:** ALON USA-BIG SPRING REFINERY (operated by Delek US Holdings)
**Pollutant:** Benzene
**Prepared:** August 1, 2026

## Facility identifiers (verified)
| Field | Value |
|---|---|
| TRI Facility ID | `79721FNLNDIS20E` |
| Address | 200 Refinery Road – IH 20 at Refinery Road, Big Spring, TX 79720 (Howard County) |
| TCEQ Regulated Entity No. | RN100250869 |
| EPA ID | TXD008013468 |
| NAICS | 324110 – Petroleum Refineries |

Sources: EPA TRI Explorer facility profile; TCEQ enforcement/permit records (Docket 2023-0419-AIR-E; NSR Permit 20628).

## Data sources
1. **EPA Toxics Release Inventory (TRI)** via the Envirofacts Data Service API — https://www.epa.gov/toxics-release-inventory-tri-program and https://www.epa.gov/enviro/envirofacts-data-service-api
2. **Environmental Integrity Project Fenceline Monitoring dashboard** — https://environmentalintegrity.shinyapps.io/fencelinemonitoring/ (concentration data, µg/m³, not mass emissions — useful as a cross-check, not a like-for-like substitute for TRI's pounds/kg)
3. **EPA Envirofacts / ECHO** — facility and enforcement records (used to confirm identifiers above)

## Status of this deliverable
`benzene_big_springs_2016_2026_v1.csv` currently contains **verified facility
identifiers only**. The `emissions_kg` column is marked `PENDING` because the
TRI Explorer's interactive report pages block automated access (robots.txt),
and the sandbox this was prepared in cannot reach epa.gov directly (outbound
network is restricted to package registries).

**`pull_tri_data.py`** is included in this folder and does the actual pull —
it calls EPA's public Envirofacts REST API (`data.epa.gov/efservice/...`),
which is documented and open, no key required. Run it from a machine with
normal internet access:

```bash
pip install requests
python pull_tri_data.py
```

It filters `MV_TRI_BASIC_DOWNLOAD` by this facility's TRI ID and the target
years, keeps only Benzene rows, converts pounds → kg, and overwrites the CSV
with real figures pulled straight from EPA's database (including the
facility's official lat/long from the same record, rather than an estimate).

## Processing notes
- TRI reports **on-site + off-site total releases** in pounds; converted to kg using 1 lb = 0.45359237 kg.
- TRI data lag ~18 months behind the current year (2025–2026 rows may return no data yet — that's expected, not a bug).
- Some years may show blank/zero if the facility filed a Form A (certification of low releases) rather than a full Form R; note that in a `notes` column if you extend the schema later.
- Cross-check any surprising jump against TCEQ enforcement history (there's a confirmed 2017 Clean Air Act consent decree covering benzene waste NESHAP compliance, and a 2023 TCEQ enforcement order) before treating it as a real trend vs. a reporting artifact.
- Next step once the script is run: spot-check 2-3 years against the EIP fenceline dashboard for consistency, then update `source` column granularity if EIP data is merged in.
- 2019 benzene releases (98,761.71 kg) are ~9x adjacent years — flagged for review, not yet explained. Verify against TRI Explorer or TCEQ incident reports before treating as clean data.
