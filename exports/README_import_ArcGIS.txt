Central Asia Cryosphere Monitoring - ArcGIS Online import files
Built 2026-11-20 from the knowledge-map spreadsheet + UniFr station lists + ArcGIS runoff/ERT records.

POINT LAYERS (one row per site/station point, one file per layer):
  CA_Cryosphere_Glacier_sites.csv
  CA_Cryosphere_Snow_sites.csv
  CA_Cryosphere_Permafrost_sites.csv
  CA_Cryosphere_Runoff_sites.csv
  CA_Cryosphere_Meteorology_sites.csv
Import: ArcGIS Online map > Add > Add layer from file > choose the CSV.
Location: "Latitude and Longitude"; latitude field = latitude, longitude field = longitude (WGS84 decimal degrees).
Encoding: UTF-8. Headers have no spaces or special characters.
Key field for joins with Main Information: Name.
Column CoordSource says where each position comes from. "ArcGIS map (not yet verified)" =
runoff stations and ERT profiles still waiting for the corrected ArcGIS coordinate list.
Text fields are cut at 250 characters (marked with …); full details are in the all-records file.

FULL TABLE:
  CA_Cryosphere_all_records.csv  - one row per measurement (780 rows), same fields as the web platform.
  Rows without latitude/longitude (52 sites) have no coordinates yet.

CORRECTIONS:
  CA_Cryosphere_corrections_log.csv - every correction applied ("applied") and open problem ("to review").
  Apply the "Coordinate corrected" and "Region corrected" rows to the Main Information layer too.

Pop-up suggestion: title {Name}; show Country, Layer, Variables, Methods, Status, StartYear, StopYear,
MeasuredBy, Partners, Region, DataIssue, and PlatformLink as a link ("Full inventory").
