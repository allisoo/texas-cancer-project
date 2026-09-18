"""Create the BEN-3 Galveston Bay Refinery benzene emissions CSV."""

import json
from io import StringIO
from pathlib import Path
from urllib.request import Request, urlopen

import pandas as pd


START_YEAR, END_YEAR = 2016, 2026
TRI_ID = "7759WBLNCH2415T"
FRS_ID = "110059763536"
BENZENE_ID = "0000071432"
LB_TO_KG = 0.45359237
VERIFIED_COORDINATES = (29.374444, -94.925000)
SOURCE_LABEL = "EPA TRI (Envirofacts DMap API; AIR FUG + AIR STACK)"

TRI_URL = (
    "https://data.epa.gov/dmapservice/tri.tri_reporting_form/"
    f"tri_facility_id/equals/{TRI_ID}/and/tri_chem_id/equals/{BENZENE_ID}/and/"
    f"reporting_year/greaterThanEqual/{START_YEAR}/and/"
    f"reporting_year/lessThanEqual/{END_YEAR}/and/active_status/equals/1/"
    "join/tri.tri_release_qty/doc_ctrl_num/equals/doc_ctrl_num/"
    "sort/reporting_year:asc/1:1000/json"
)
FRS_URL = (
    "https://ofmpub.epa.gov/frs_public2/frs_rest_services.get_facilities?"
    f"registry_id={FRS_ID}&program_output=yes&output=JSON"
)
TRI_EXPLORER_URL = (
    "https://enviro.epa.gov/triexplorer/facility_data?"
    f"tri=TRIQ1&tri_facility_id={TRI_ID}"
)
OUTPUT_FILE = Path(__file__).with_name("benzene_galveston_bay_2016_2026_v1.csv")


def download(url):
    """Download text from an EPA public-data URL."""
    request = Request(url, headers={"User-Agent": "BEN-3 data collection"})
    with urlopen(request, timeout=120) as response:
        return response.read().decode("utf-8-sig")


def get_coordinates():
    """Get the representative facility coordinates from EPA FRS."""
    try:
        facilities = json.loads(download(FRS_URL))["Results"]["FRSFacility"]
    except (OSError, json.JSONDecodeError) as error:
        print(f"FRS is unavailable; using verified coordinates ({error}).")
        return VERIFIED_COORDINATES

    if isinstance(facilities, dict):
        facilities = [facilities]

    facility = next(row for row in facilities if str(row["RegistryId"]) == FRS_ID)
    if "GALVESTON BAY REFINERY" not in facility["FacilityName"].upper():
        raise ValueError("The FRS facility name does not match Galveston Bay Refinery.")

    return float(facility["Latitude83"]), float(facility["Longitude83"])


def get_tri_air_releases():
    """Sum fugitive and stack benzene releases for each reporting year."""
    tri = pd.DataFrame(json.loads(download(TRI_URL)))
    if tri.empty:
        raise ValueError("EPA returned no TRI records for the requested facility and years.")

    required = {
        "reporting_year", "environmental_medium", "total_release", "release_na",
    }
    missing = required.difference(tri.columns)
    if missing:
        raise ValueError(f"EPA response is missing required fields: {sorted(missing)}")

    air = tri[tri["environmental_medium"].isin(["AIR FUG", "AIR STACK"])].copy()
    if air.empty:
        raise ValueError("EPA returned no fugitive or stack air-release records.")

    air["year"] = pd.to_numeric(air["reporting_year"])
    air["release_lb"] = pd.to_numeric(air["total_release"], errors="coerce")

    # EPA uses release_na=1 for a quantity that is not applicable; it contributes zero.
    not_applicable = air["release_na"].astype(str).eq("1")
    air.loc[not_applicable, "release_lb"] = air.loc[not_applicable, "release_lb"].fillna(0)
    if air["release_lb"].isna().any():
        raise ValueError("EPA returned an unexplained missing air-release quantity.")

    return air.groupby("year", as_index=False)["release_lb"].sum()


def check_against_tri_explorer(annual):
    """Confirm that the totals match EPA's separate TRI Explorer download."""
    text = download(TRI_EXPLORER_URL)
    csv_text = text[text.index('"Facility name"') :]
    explorer = pd.read_csv(StringIO(csv_text))

    explorer = explorer[
        explorer["TRI ID"].astype(str).eq(TRI_ID)
        & explorer["Chemical"].astype(str).str.casefold().eq("benzene")
        & explorer["Year"].between(START_YEAR, END_YEAR)
    ].copy()
    explorer["release_lb"] = pd.to_numeric(explorer["Total Air"])
    explorer = explorer.groupby("Year", as_index=False)["release_lb"].sum()
    explorer = explorer.rename(columns={"Year": "year"})

    comparison = annual.merge(explorer, on="year", suffixes=("_api", "_explorer"))
    if len(comparison) != len(annual) or not comparison["release_lb_api"].equals(
        comparison["release_lb_explorer"]
    ):
        raise ValueError("EPA Envirofacts and TRI Explorer totals do not match.")


def build_csv(annual, latitude, longitude):
    """Add requested fields, convert pounds to kilograms, and save the CSV."""
    output = pd.DataFrame({"year": range(START_YEAR, END_YEAR + 1)})
    output = output.merge(annual, on="year", how="left")
    output["emissions_kg"] = (output["release_lb"] * LB_TO_KG).round(6)

    output["facility_id"] = TRI_ID
    output["facility_name"] = "Galveston Bay Refinery"
    output["latitude"] = latitude
    output["longitude"] = longitude
    output["pollutant"] = "Benzene"
    output["source"] = SOURCE_LABEL

    columns = [
        "facility_id", "facility_name", "latitude", "longitude",
        "pollutant", "year", "emissions_kg", "source",
    ]
    output[columns].to_csv(OUTPUT_FILE, index=False, na_rep="", float_format="%.6f")


def main():
    latitude, longitude = get_coordinates()
    annual = get_tri_air_releases()
    check_against_tri_explorer(annual)
    build_csv(annual, latitude, longitude)
    print(f"Created {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
