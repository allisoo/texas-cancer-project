# BEN-1: Benzene Emissions Data — Pasadena Refinery

## Facility
- Facility: Pasadena Refining System Inc
- Address: 111 Red Bluff Rd, Pasadena, TX 77506 (Harris County)
- TRI Facility ID: 77506CRWNC111RE
- NAICS: 324110 (Petroleum Refineries)

## Data source
EPA TRI Basic Data Files
(https://www.epa.gov/toxics-release-inventory-tri-program/tri-basic-data-files-calendar-years-1987-present),
Texas state files, years 2016–2024. Records isolated by TRI Facility ID and filtered to
Benzene. On-site air release totals converted from pounds to kilograms
(kg = lbs x 0.453592).

## Download date
2026-08-08

## Why only one source was used
The task listed three sources to check. TRI Basic Data Files map directly onto the
requested format — facility-level, annual, mass-based emissions in kg — so they were the
right and sufficient source for this deliverable:

- **EPA Envirofacts API** returns the same underlying TRI records as the Basic Data
  Files — pulling from it would just duplicate the same numbers through a different
  access method, so it wasn't needed here.
- **EIP Fenceline Monitoring** tracks a different metric entirely: air *concentration*
  at the facility's property line (ug/m3), available only from 2018 onward, rather than
  annual mass released. It doesn't map onto the `emissions_kg` column this deliverable
  calls for. It's better suited to the exposure-modeling stage of the project (Stage 3)
  — worth flagging as a separate follow-up task if the team wants concentration-level
  data too, but out of scope here.

## Processing notes
- Coordinate system: WGS84 (lat/long as reported in the TRI Basic Data Files)
- 2025–2026 data not yet available due to TRI's standard reporting lag (a given year's
  data is typically released the following year)
- On-site air release figure used: fugitive + stack air release, summed where reported
  as separate columns
- No duplicate facility records found across the years checked

## QA checklist
- [x] Coordinates verified (-90/90, -180/180)
- [x] CRS specified (WGS84)
- [x] Units documented (kg, converted from lbs, factor 0.453592)
- [x] Missing values documented (2025–2026 not yet released)
- [x] Duplicates removed
- [x] Required columns present
- [x] Filenames standardized
- [x] Metadata included (source, date, notes)
