"""Export data.json as ArcGIS Online-ready CSV files (one point layer per theme, all records, corrections log).
Usage: python3 export_arcgis.py [data.json] [output folder]
Import each *_sites.csv in ArcGIS Online with Add > Add layer from file; location fields: latitude / longitude."""
import csv, json, os, re, sys

SRC = sys.argv[1] if len(sys.argv) > 1 else 'data.json'
OUT = sys.argv[2] if len(sys.argv) > 2 else 'arcgis_export'
LINK = os.environ.get('PLATFORM_URL', 'https://claude.ai/artifact/RHU1Pj98fZKPQsgPA8L41y')  # set by the GitHub workflow
os.makedirs(OUT, exist_ok=True)
d = json.load(open(SRC)); S = d['sites']; M = d['meas']

def cut(s, n=250):  # keep text fields short enough for ArcGIS string fields
    s = re.sub(r'\s+', ' ', str(s)).strip(); return s if len(s) <= n else s[:n - 1] + '…'
def srcshort(src):
    return 'ArcGIS map' if src.startswith('ArcGIS') else ('UniFr station list' if src.startswith('UniFr station') else 'Knowledge map spreadsheet')
def coordsrc(s):
    srcs = set(srcshort(m['source']) for m in s['ms'])
    if any(f.startswith('Coordinates taken from the ArcGIS') for f in s['flags']): return 'ArcGIS map (not yet verified)'
    if 'UniFr station list' in srcs: return 'UniFr station list'
    if srcs == {'ArcGIS map'}: return 'ArcGIS map (not yet verified)'
    return 'Knowledge map spreadsheet'
uniq = lambda xs: '; '.join(dict.fromkeys(x for x in xs if x))
for s in S: s['ms'] = []
for m in M: S[m['site']]['ms'].append(m)

for layer in ['Glacier', 'Snow', 'Permafrost', 'Runoff', 'Meteorology']:
    rows = []
    for s in S:
        ms = [m for m in s['ms'] if m['theme'] == layer]
        if not ms or s['lat'] is None: continue
        sy = [m['startYear'] for m in ms if m['startYear']]; st = [m['stop'] for m in ms if m['stop']]
        info = s.get('info') or {}
        rows.append(dict(
            Name=s['name'], Country=s['country'], Layer=layer, latitude=f"{s['lat']:.5f}", longitude=f"{s['lon']:.5f}",
            Variables=cut(uniq(m['variable'] for m in ms)), Methods=cut(uniq(m['method'] for m in ms)),
            Frequency=cut(uniq(m['freq'] for m in ms)), Status=cut(uniq(m['status'] for m in ms)),
            StartYear=min(sy) if sy else '', StopYear=max(st) if st and not any(m['status'] == 'Ongoing' for m in ms) else '',
            MeasuredBy=cut(uniq(o for m in ms for o in m['by'])), Partners=cut(uniq(o for m in ms for o in m['partners'])),
            Region=cut(info.get('region', '')), NRecords=len(ms), Source=cut(uniq(srcshort(m['source']) for m in ms)),
            CoordSource=coordsrc(s), DataIssue=cut(' | '.join(s['flags'])),
            Details=cut(' | '.join(f"{m['variable']} ({m['method'] or 'method n/a'}, {m['status']}{', ' + m['start'] if m['start'] else ''})" for m in ms)),
            PlatformLink=LINK))
    with open(f'{OUT}/CA_Cryosphere_{layer}_sites.csv', 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    print(f'CA_Cryosphere_{layer}_sites.csv', len(rows))

flds = ['Name', 'Country', 'Layer', 'latitude', 'longitude', 'Component', 'Variable', 'MeasurementType', 'Method', 'Equipment',
        'Frequency', 'Status', 'Start', 'StartYear', 'StopYear', 'MeasuredBy', 'Partners', 'Note', 'Source', 'SourceRow', 'DataIssue']
with open(f'{OUT}/CA_Cryosphere_all_records.csv', 'w', newline='', encoding='utf-8-sig') as f:
    w = csv.DictWriter(f, fieldnames=flds); w.writeheader()
    for m in M:
        s = S[m['site']]
        w.writerow(dict(Name=s['name'], Country=s['country'], Layer=m['theme'],
            latitude='' if s['lat'] is None else f"{s['lat']:.5f}", longitude='' if s['lon'] is None else f"{s['lon']:.5f}",
            Component=m['component'], Variable=m['variable'], MeasurementType=m['mtype'], Method=m['method'], Equipment=m['equipment'],
            Frequency=m['freq'], Status=m['status'], Start=m['start'], StartYear=m['startYear'] or '', StopYear=m['stop'] or '',
            MeasuredBy='; '.join(m['by']), Partners='; '.join(m['partners']), Note=cut(m['note']), Source=srcshort(m['source']),
            SourceRow=m['row'] or '', DataIssue=cut(' | '.join(s['flags']))))
print('CA_Cryosphere_all_records.csv', len(M))

with open(f'{OUT}/CA_Cryosphere_corrections_log.csv', 'w', newline='', encoding='utf-8-sig') as f:
    w = csv.writer(f); w.writerow(['Type', 'Where', 'What', 'Before', 'After', 'Status'])
    for l in d['log']: w.writerow([l['kind'], l['where'], l['what'], l['before'], l['after'], 'applied' if l['applied'] else 'to review'])
print('CA_Cryosphere_corrections_log.csv', len(d['log']))
