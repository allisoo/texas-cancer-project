# Benzene air releases — Galveston Bay Refinery (2016–2026)

**Task:** BEN-3  
**Facility:** Galveston Bay Refinery  
**Pollutant:** Benzene  
**Refreshed:** September 17, 2026

This folder contains the requested annual CSV and a Python script that rebuilds it from public EPA data.

## Files

- `benzene_galveston_bay_2016_2026_v1.csv` — cleaned annual benzene air-release data.
- `collect_benzene_galveston_bay.py` — downloads, checks, converts, and writes the CSV.

## Facility identifiers

| Field | Value |
|---|---|
| Public facility name | Galveston Bay Refinery |
| TRI facility ID | `7759WBLNCH2415T` |
| TRI reporting name | BLANCHARD REFINING CO LLC |
| EPA FRS Registry ID | `110059763536` |
| Address | 2401 Fifth Avenue South, Texas City, Texas |
| Representative coordinates (NAD83) | `29.374444`, `-94.925000` |

EPA's Facility Registry Service record connects the facility identity, coordinates, and TRI program record. Marathon Petroleum uses the public name **Galveston Bay Refinery** for the same address. The former Texas City refinery's separate TRI ID, `77590MRTHNFOOTO`, is not combined with this facility because it was a distinct TRI facility in the earlier years.

The script requests the coordinates from FRS each time it runs. If that service is temporarily unavailable, it uses the verified coordinates shown above and prints a warning; a returned facility-name mismatch still stops the script.

## Data sources

1. **EPA TRI Envirofacts DMap API** — the primary source for annual benzene release quantities.
2. **EPA TRI Explorer facility download** — an independent EPA cross-check of the annual air totals.
3. **EPA Facility Registry Service (FRS)** — facility identity and representative coordinates.
4. **Environmental Integrity Project fenceline dashboard** — facility context and benzene concentration monitoring; not used as a mass-emissions substitute.

Source links:

- EPA TRI program: https://www.epa.gov/toxics-release-inventory-tri-program
- EPA Envirofacts data services: https://www.epa.gov/enviro/envirofacts-data-service-api
- EPA FRS record: https://ofmpub.epa.gov/frs_public2/frs_rest_services.get_facilities?registry_id=110059763536&program_output=yes&output=JSON
- EPA TRI facility profile: https://enviro.epa.gov/triexplorer/release_fac_profile?TRI=7759WBLNCH2415T&TRILIB=TRIQ1&YEAR=2024
- Marathon Petroleum facility page: https://www.marathonpetroleum.com/Operations/Refining/Galveston-Bay-Refinery/
- EIP fenceline dashboard: https://environmentalintegrity.shinyapps.io/fencelinemonitoring/

## Processing method

The script requests active TRI forms for facility ID `7759WBLNCH2415T`, benzene chemical ID `0000071432` (CAS 71-43-2), and reporting years 2016–2026. It then:

1. Keeps only `AIR FUG` and `AIR STACK` release rows.
2. Sums those air releases by reporting year.
3. Checks the annual pound totals against EPA TRI Explorer.
4. Converts pounds to kilograms using `1 lb = 0.45359237 kg`.
5. Writes one row for every requested year, leaving unavailable years blank.

A missing release quantity is treated as zero only when EPA marks that row `release_na=1` (not applicable). Any unexplained missing quantity stops the script. Output values are rounded to six decimal places.

The primary query is stored in the script. The CSV uses the shorter source label `EPA TRI (Envirofacts DMap API; AIR FUG + AIR STACK)` so the file remains readable.

## EIP monitoring note

EIP identifies the monitoring network as **Marathon Galveston Bay Texas City**. Fenceline monitoring reports benzene concentration in micrograms per cubic meter. The requested `emissions_kg` column is annual released mass. Concentration cannot be converted to kilograms without additional airflow and dispersion information, so EIP data are used for identity and context only and are not merged into the TRI mass totals.

## Year availability

The live EPA query returned benzene air-release values for 2016–2024 when refreshed on September 17, 2026. It returned no active facility benzene record for reporting years 2025 or 2026, so those `emissions_kg` cells are blank rather than zero.

- Reporting-year 2025 forms were due July 1, 2026, but this facility's benzene record was not present in the queried EPA service on the refresh date.
- Reporting-year 2026 forms are due July 1, 2027.

EPA may revise historical submissions. Rerunning the script can therefore produce revised historical values or populate a newly published year.

## Reproduction

Requires Python 3 and pandas. From this folder, run:

```text
python collect_benzene_galveston_bay.py
```
