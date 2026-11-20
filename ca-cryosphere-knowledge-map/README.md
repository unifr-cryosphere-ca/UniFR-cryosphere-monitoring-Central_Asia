# Cryosphere Monitoring in Central Asia – Knowledge Map

An interactive inventory of in situ cryosphere monitoring in Kazakhstan, Kyrgyzstan, Tajikistan and Uzbekistan: where glaciers, snow, permafrost, glacial runoff and mountain meteorology are observed, by whom, with which methods, and since when.

**Live map:** https://unifr-cryosphere-ca.github.io/UniFR-cryosphere-monitoring-Central_Asia/

**Repository:** https://github.com/unifr-cryosphere-ca/UniFR-cryosphere-monitoring-Central_Asia

Maintained by the University of Fribourg, Department of Geosciences, within the UNDP–UNESCO–GEF project on strengthening the resilience of Central Asian countries through regional cooperation on the cryosphere. It replaces and corrects the earlier ArcGIS Online map “Cryosphere of Central Asia”.

## What is in this repository

| Path | Content |
|---|---|
| `index.html` | The web map (map with five layers, filters, site pop-ups, table, data-issues log). |
| `data/source/knowledge_map_master.xlsx` | **Master spreadsheet.** Sheet `UPDATED`: one row per measurement. Sheets `Sources_*`: sources per country (contact details removed). |
| `data/stations/*.csv` | UniFr station lists (AWS, boreholes, firn/ice temperature, ground-surface-temperature loggers, SmartStakes). Their coordinates override the old ArcGIS positions. |
| `scripts/build_data.py` | Cleans the spreadsheet, harmonises names, merges the station lists and remaining ArcGIS records, flags problems, writes `data/data.json`. |
| `scripts/arcgis_data.py` | Records and site descriptions carried over from the old ArcGIS map (runoff stations, ERT profiles, GFZ/SDSS stations), and the region corrections. |
| `scripts/export_arcgis.py` | Writes ArcGIS-ready CSV files to `exports/`. |
| `data/data.json` | Built data used by the map. **Do not edit by hand**; it is rebuilt automatically. |
| `exports/` | CSV files for ArcGIS or other GIS software, the full record table and the corrections log. |
| `docs/` | Update guide. |
| `CHANGELOG.md` | Manual change log: who changed what, and why. |

## How to update the map

You only edit the **spreadsheet** or a **station list**. Everything else happens automatically.

1. Download `data/source/knowledge_map_master.xlsx` (or the station list), edit it, keep the sheet name `UPDATED` and the column order.
2. In the repository on GitHub, open the same folder, click **Add file → Upload files**, upload the edited file with the **same file name**, write a short description of the change, and click **Commit changes**.
3. The workflow *Build data and publish the map* runs (tab **Actions**, about 1–2 minutes). It rebuilds `data/data.json` and the exports and publishes the map.
4. Open the live map and check the change and the **Data issues** tab.
5. Add a line to `CHANGELOG.md`.

If the workflow fails (red cross in **Actions**), open it to read the error; usually a column was moved or renamed. The previous version of the map stays online until the next successful run.

Spreadsheet rules (coordinates in decimal degrees WGS84, controlled values for component and status, organisation abbreviations) are in the update guide in `docs/`.

### Running the build on your own computer (optional)

```bash
pip install -r requirements.txt          # Python 3.12 or newer
python scripts/build_data.py data/source/knowledge_map_master.xlsx data/data.json
python scripts/export_arcgis.py data/data.json exports
python -m http.server                     # then open http://localhost:8000
```

## Access and ownership

The repository belongs to a GitHub **organisation**, not to a person. Keep at least two owners at all times (*organisation → People*). Add new maintainers as members with write access to this repository. Nobody needs to share a password.

## Publishing on GitHub Pages (first time only)

*Settings → Pages → Build and deployment → Source: **GitHub Actions***. Then run the workflow once from the **Actions** tab (*Run workflow*).

## Citation and archiving

Connect the repository to [Zenodo](https://zenodo.org) (log in with GitHub, enable the repository) and create a **Release** on GitHub. Zenodo then archives each release with a DOI. See `CITATION.cff`.

## Licence

Code: MIT (see `LICENSE`). Data (spreadsheet, station lists, `data/`, `exports/`): **to be confirmed by the project partners**; proposed CC BY 4.0.

## Sources

National hydrometeorological services and research institutes of Kazakhstan, Kyrgyzstan, Tajikistan and Uzbekistan (interviews compiled in the master spreadsheet); World Glacier Monitoring Service, Fluctuations of Glaciers database; University of Fribourg station lists; ArcGIS Online map “Cryosphere of Central Asia” (E. Grimaître, University of Fribourg). Background maps © OpenStreetMap contributors, OpenTopoMap (CC-BY-SA), CARTO.
