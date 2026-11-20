"""Clean the knowledge-map spreadsheet, merge ArcGIS-only sites, write data.json + corrections log."""
import json, math, os, re, sys
import pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import arcgis_data as A
# Usage: python3 build_data.py <master_spreadsheet.ods|.xlsx> [output data.json]
SHEET = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'in', 'km.ods')
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, 'data.json')

SRC_SHEET = 'Knowledge map spreadsheet (UPDATED sheet)'
SRC_ARC = 'ArcGIS map "Cryosphere of Central Asia"'

u = pd.read_excel(SHEET, engine='odf' if SHEET.endswith('.ods') else None, sheet_name='UPDATED', header=0)
u.columns = ['country','component','site','lat','lon','variable','mtype','method','equipment','freq',
             'status','start','stop','by','partners','note']
u['row'] = u.index + 2  # spreadsheet row number

log = []   # applied corrections
def L(kind, where, what, before='', after='', applied=True):
    log.append(dict(kind=kind, where=where, what=what, before=str(before), after=str(after), applied=applied))

def clean_str(v):
    if v is None or (isinstance(v, float) and math.isnan(v)): return ''
    s = str(v).replace('С', 'C').replace('с', 'c')  # Cyrillic С/с -> Latin
    return re.sub(r'\s+', ' ', s).strip()

# ---------- coordinates ----------
def num(v):
    if v is None or (isinstance(v, float) and math.isnan(v)): return None
    try: return float(v)
    except Exception:
        m = re.search(r'-?\d+(\.\d+)?', str(v)); return float(m.group()) if m else None

for i, r in u.iterrows():
    la, lo = num(r.lat), num(r.lon)
    if la is not None and la > 1000:
        L('Coordinate fixed', f'Row {r.row}: {clean_str(r.site)}', 'Latitude had a missing decimal point', r.lat, la/10000); la = la/10000
    if lo is not None and not isinstance(r.lon, (int, float)):
        L('Coordinate fixed', f'Row {r.row}: {clean_str(r.site)}', 'Longitude stored as text with a stray character', r.lon, lo)
    u.at[i, 'lat'], u.at[i, 'lon'] = la, lo

# ---------- organisations ----------
ORG_MAP = {'CRG': 'CRG', 'CARGC': 'CARGC', 'Kyrgyz Hydromet': 'Kyrgyz Hydromet', 'KazHydromet': 'KazHydromet',
           'UNIFR': 'UniFR', 'Uzhydromet': 'Uzhydromet', 'Tajhydromet': 'Tajhydromet'}
def orgs(v):
    out = []
    for p in re.split(r'[,;/]', clean_str(v)):
        p = p.strip()
        if p: out.append(ORG_MAP.get(p, p))
    return out
raw_by = set(u.by.dropna().astype(str))
for b in sorted(raw_by):
    if b != b.strip() or 'С' in b:
        L('Name harmonised', 'Measured by', 'Leading space or Cyrillic "С" removed so the organisation matches its other spellings', repr(b), ', '.join(orgs(b)))

# ---------- site names ----------
NAME_MAP = {
 'Batysh Suek': 'Batysh Sook', '#354': 'No.354 (Akshiirak)', '#599': 'No.599 (Kjungey Ala-Too)',
 '#676 (GGP)': 'No.676 (GGP)', '# 71 (Yakarcha)': 'Yakarcha (No.71)', '#457 (NHD)': 'No.457 (NHD)',
 'Uybulak Pass': 'Uy-Bulak Pass', 'Josalykezen Pass': 'Zholsaly-kezen Pass', 'Kon Chykur Bashisa': 'Kon-Chukurbashi',
 'Ishkashym': 'Ishkashim', 'Gregoriev': 'Grigoriev', 'Barkrak pravyy': 'Barkrak Pravyy', 'Barkrak Sredniy': 'Barkrak Sredniy',
}
ARC_NAME = {  # ArcGIS names -> canonical
 'Gregoriev': 'Grigoriev', 'No.599 (Kjungey Ala-too)': 'No.599 (Kjungey Ala-Too)', 'No. 676 (GGP)': 'No.676 (GGP)',
 'UyBulak Pass': 'Uy-Bulak Pass', 'Zhosalykezen Pass': 'Zholsaly-kezen Pass', 'Akshiirak': 'No.354 (Akshiirak)',
 'Barkrak Sredniy East Branch': 'Barkrak Sredniy', 'Zulmart (No.139)': 'Zulmart (No.139)',
}
def canon_arc(n):
    n = ARC_NAME.get(n, n)
    for suf in [' - on rock', ' - on ice', ' (high)', ' (low)', ' (left)', ' (right)', ' on rock', ' on ice']:
        if n.endswith(suf): n = n[: -len(suf)]
    return {'Zulmart': 'Zulmart (No.139)'}.get(n, ARC_NAME.get(n, n))

u['site_c'] = u.site.map(clean_str)
for old, new in NAME_MAP.items():
    if (u.site_c == old).any():
        L('Name harmonised', f'Site "{old}"', 'Spelling aligned with the ArcGIS map / WGMS name so the records join', old, new)
u['site_c'] = u.site_c.map(lambda s: NAME_MAP.get(s, s))

# ---------- themes ----------
def theme(r):
    comp, var, meth = clean_str(r.component), clean_str(r.variable), clean_str(r.method)
    if 'runoff' in var.lower(): return 'Runoff'
    if comp == 'Permafrost' or meth in ('ERT&GST', 'ERT', 'GST', 'Borehole'): return 'Permafrost'
    if var == 'Temperature' and (meth == 'AWS' or meth == ''): return 'Meteorology'
    if comp == 'Glacier': return 'Glacier'
    return 'Snow'
u['theme'] = u.apply(theme, axis=1)
n_ert = ((u.component == 'Glacier') & u.method.isin(['ERT&GST', 'GST'])).sum()
L('Theme assigned', f'{n_ert} rows', 'Component "Glacier" with ERT/GST method shown in the Permafrost layer (ERT/GST are permafrost methods). Original component kept in the record.', 'Glacier', 'Permafrost layer')
L('Theme assigned', 'All rows', 'Runoff and air-temperature (AWS / weather-station) rows shown in their own Runoff and Meteorology layers, matching the five ArcGIS themes. Original component kept in the record.')

# ---------- years ----------
def year(v):
    m = re.search(r'(18|19|20)\d\d', clean_str(v)); return int(m.group()) if m else None

# ---------- country bounds ----------
BB = {'Kazakhstan': (40.5, 55.5, 46, 87.5), 'Kyrgyzstan': (39.1, 43.3, 69.2, 80.3),
      'Tajikistan': (36.6, 41.1, 67.3, 75.2), 'Uzbekistan': (37.1, 45.6, 55.9, 73.2)}

def km(a, b, c, d):
    p = math.pi/180; x = (d-b)*p*math.cos((a+c)/2*p); y = (c-a)*p; return 6371*math.hypot(x, y)

# ---------- ArcGIS reference positions (for cross-check + filling missing coordinates) ----------
arc_pos = {}
for n, la, lo, *_ in A.METEO: arc_pos.setdefault(canon_arc(n), (la, lo))
for n, ev, la, lo in A.GLACIER_WGMS: arc_pos[canon_arc(n)] = (la, lo)   # WGMS glacier position preferred
for n, c, la, lo, *_ in A.MAIN: arc_pos.setdefault(canon_arc(n), (la, lo))
for n, k, la, lo, *_ in A.PERMAFROST: arc_pos.setdefault(canon_arc(n), (la, lo))

sites, meas, flags = {}, [], {}
def site_key(country, name, la, lo):
    return f'{country}|{name}|{"" if la is None else round(la, 3)}|{"" if lo is None else round(lo, 3)}'
def flag(sk, text):
    flags.setdefault(sk, [])
    if text not in flags[sk]: flags[sk].append(text)

for i, r in u.iterrows():
    country, name = clean_str(r.country), r.site_c
    la, lo = r.lat, r.lon
    la = None if la is None or (isinstance(la, float) and math.isnan(la)) else la
    lo = None if lo is None or (isinstance(lo, float) and math.isnan(lo)) else lo
    filled = False
    if la is None and name in arc_pos:
        la, lo = arc_pos[name]; filled = True
        L('Coordinate filled', f'Row {r.row}: {name}', 'No coordinates in the spreadsheet; position taken from the ArcGIS map (please confirm)', '', f'{la}, {lo}')
    sk = site_key(country, name, la, lo)
    if sk not in sites:
        sites[sk] = dict(id=len(sites), name=name, country=country, lat=la, lon=lo, sources=[SRC_SHEET])
    if filled: flag(sk, 'Coordinates taken from the ArcGIS map; not in the spreadsheet.')
    if la is None: flag(sk, 'No coordinates. Not shown on the map; listed in the table.')
    else:
        a, b, c, d = BB[country]
        if not (a <= la <= b and c <= lo <= d):
            flag(sk, f'Coordinates {la:.3f}, {lo:.3f} fall outside {country}. Check the position.')
        ref = {'East Zulmart (# 139)': 'Zulmart (No.139)'}.get(name, name)
        if ref in arc_pos and not filled:
            dist = km(la, lo, *arc_pos[ref])
            if dist > 5:
                flag(sk, f'Position differs by {dist:.0f} km from the ArcGIS/WGMS position ({arc_pos[ref][0]:.4f}, {arc_pos[ref][1]:.4f}){'' if ref == name else ' of ' + ref}. Check which is right.')
    status = clean_str(r.status)
    stop = year(r.stop)
    if status == 'Ongoing' and stop:
        flag(sk, f'"{clean_str(r.variable)}" is marked Ongoing but has a stop year ({stop}).')
    eq = clean_str(r.equipment)
    if re.fullmatch(r'since ?\d{4}', eq):
        flag(sk, f'Equipment column contains a date ("{eq}"); probably belongs in the start-year column.')
    m = dict(site=sites[sk]['id'], theme=r.theme, component=clean_str(r.component), variable=clean_str(r.variable),
             mtype=clean_str(r.mtype), method=clean_str(r.method), equipment=eq, freq=clean_str(r.freq),
             status=status or 'Unknown', start=clean_str(r.start), startYear=year(r.start), stop=stop,
             by=orgs(r.by), partners=orgs(r.partners), note=clean_str(r.note), source=SRC_SHEET, row=int(r.row))
    meas.append(m)

# ---------- merge ArcGIS-only records ----------
by_name = {}
for s in sites.values(): by_name.setdefault(s['name'], []).append(s)
sheet_themes = {}
for m in meas:
    sheet_themes.setdefault(next(s['name'] for s in sites.values() if s['id'] == m['site']), set()).add(m['theme'])
COUNTRY = {canon_arc(n): c for n, c, *_ in A.MAIN}
COUNTRY.update({'Arabel-Suu': 'Kyrgyzstan'})

SRC_ST = 'UniFr station list'
def arc_site(name, la, lo, country):
    return arc_site_src(name, la, lo, country, SRC_ARC)
def arc_site_src(name, la, lo, country, src):
    sk = site_key(country, name, la, lo)
    # reuse a sheet site of the same name within 3 km
    for s in by_name.get(name, []):
        if s['lat'] is not None and km(s['lat'], s['lon'], la, lo) < (0.02 if src == SRC_ST else 0.3):
            if src == SRC_ST and SRC_ST not in s['sources'] and (s['lat'], s['lon']) != (la, lo):
                L('Coordinate corrected', f'Site "{name}"', f'Position set to the UniFr station list (moved {km(s["lat"], s["lon"], la, lo)*1000:.0f} m)', f'{s["lat"]}, {s["lon"]}', f'{la}, {lo}')
                s['lat'], s['lon'] = la, lo
            if src not in s['sources']: s['sources'].append(src)
            return s
    if sk not in sites:
        sites[sk] = dict(id=len(sites), name=name, country=country, lat=la, lon=lo, sources=[src])
        by_name.setdefault(name, []).append(sites[sk])
    return sites[sk]

def add_arc(name, la, lo, th, variable, method, start, stop_year, status, by, note, label=None):
    cn = canon_arc(name)
    country = COUNTRY.get(cn, 'Kyrgyzstan' if la > 41 else 'Tajikistan')
    s = arc_site(cn, la, lo, country)
    meas.append(dict(site=s['id'], theme=th, component=th, variable=variable, mtype='Point measurements', method=method,
                     equipment='', freq='Continuous' if th in ('Meteorology', 'Runoff', 'Snow') else 'Campaign',
                     status=status, start=start, startYear=year(start), stop=stop_year, by=by, partners=[],
                     note=(f'{label}. ' if label and label != cn else '') + note, source=SRC_ARC, row=None))

def st_from_end(end):
    y = year(end)
    return ('Ongoing' if y and y >= 2025 else 'Unknown'), (None if y and y >= 2025 else y)

# ---------- UniFr station lists (authoritative coordinates; replace overlapping ArcGIS records) ----------
_sd = os.path.dirname(os.path.abspath(SHEET))
STATION_DIR = next((d for d in [os.path.join(_sd, 'stations'), os.path.join(_sd, '..', 'stations'), os.path.join(HERE, 'stations'),
                                os.path.join(HERE, '..', 'data', 'stations')] if os.path.isdir(d)), '')
STATION_SITE = [  # (substring in station name, canonical site, country)
 ('No.457', 'No.457 (NHD)', 'Tajikistan'), ('Akshiirak borehole 2', 'Kumtor', 'Kyrgyzstan'), ('No.354', 'No.354 (Akshiirak)', 'Kyrgyzstan'),
 ('Akshiirak', 'No.354 (Akshiirak)', 'Kyrgyzstan'), ('Uy-Bulak', 'Uy-Bulak Pass', 'Tajikistan'), ('Zholsalykezen', 'Zholsaly-kezen Pass', 'Kazakhstan'),
 ('Batysh Sook', 'Batysh Sook', 'Kyrgyzstan'), ('Grigoriev', 'Grigoriev', 'Kyrgyzstan'), ('Yakartsha', 'Yakarcha (No.71)', 'Tajikistan'),
 ('Zulmart', 'Zulmart (No.139)', 'Tajikistan'), ('Nissai', 'Sangvor', 'Tajikistan'), ('Barkrak', 'Barkrak Sredniy', 'Uzbekistan'),
 ('Abramov', 'Abramov', 'Kyrgyzstan'), ('Golubin', 'Golubin', 'Kyrgyzstan'),
]
def station_site(name):
    for key, site, c in STATION_SITE:
        if key.lower() in name.lower(): return site, c
    return None, None
stations = []
for fn, kind in [('station_list_meteo.csv', 'meteo'), ('station_list_borehole.csv', 'borehole'), ('station_list_smartstake.csv', 'smartstake')]:
    fp = os.path.join(STATION_DIR, fn)
    if not os.path.exists(fp): continue
    for _, r in pd.read_csv(fp).iterrows():
        site, c = station_site(str(r['Name']))
        stations.append(dict(kind=kind, name=clean_str(r['Name']), vars=clean_str(r['Variables']), lat=num(r['Latitude']), lon=num(r['Longitude']),
                             elev=num(r['Elevation (m)']), start=clean_str(r['Start']), end=clean_str(r['End']), step=clean_str(r['Time step']),
                             site=site, country=c, file=fn))
HAVE_STATIONS = any(s['kind'] == 'meteo' for s in stations)

def add_station(st, th, variable, method):
    ey = year(st['end'])
    status = 'Ongoing' if ey and ey >= 2026 else 'Unknown'
    s = arc_site_src(st['site'], st['lat'], st['lon'], st['country'], SRC_ST)
    meas.append(dict(site=s['id'], theme=th, component=th, variable=variable, mtype='Point measurements', method=method, equipment='',
                     freq=f"Continuous ({st['step']})", status=status, start=st['start'], startYear=year(st['start']),
                     stop=None if status == 'Ongoing' else ey, by=['UniFR'], partners=[],
                     note=f"{st['name']}. {st['vars'][0].upper() + st['vars'][1:]}." + (f" Elevation {st['elev']:.0f} m." if st['elev'] else '') +
                          f" Data {st['start']} to {st['end']}.", source=SRC_ST + f" ({st['file']})", row=None))

n_st = 0; skipped = []
for st in stations:
    if st['lat'] is None or st['site'] is None:
        skipped.append(st['name']); continue
    v = st['vars'].lower()
    if st['kind'] == 'meteo':
        add_station(st, 'Meteorology', 'AWS: ' + st['vars'].split(';')[0], 'AWS'); n_st += 1
        if 'snow depth' in v: add_station(st, 'Snow', 'Snow depth (AWS)', 'AWS'); n_st += 1
    elif st['kind'] == 'borehole':
        if 'firn' in v or 'ice temperature' in v:
            add_station(st, 'Glacier', 'Firn/ice temperature', 'Thermistor chain')
        elif 'surface temperature' in v:
            add_station(st, 'Permafrost', 'Ground surface temperature', 'GST')
        else:
            add_station(st, 'Permafrost', 'Ground/soil temperature', 'Borehole')
        n_st += 1
    else:
        add_station(st, 'Glacier', 'Ice surface lowering (ablation)', 'Smart Stake'); n_st += 1
if stations:
    L('Records merged', 'UniFr station lists', f'{n_st} records from the UniFr station lists (meteo, borehole, SmartStake) added with their coordinates, periods and time steps.' +
      (f' Not placed (no coordinates): {", ".join(skipped)}.' if skipped else ''))
# compare ArcGIS meteo positions with the station list and log corrections
if HAVE_STATIONS:
    for n, la, lo, el, per, loc, op in A.METEO:
        if 'UniFR' not in op: continue
        cands = [st for st in stations if st['kind'] == 'meteo' and st['site'] == {'Barkrak': 'Barkrak Sredniy'}.get(canon_arc(n), canon_arc(n)) and st['lat'] is not None]
        if not cands: continue
        best = min(cands, key=lambda st: km(la, lo, st['lat'], st['lon']))
        d = km(la, lo, best['lat'], best['lon'])
        if per and best['start'][:7].replace('-', '.') != per.split('-')[0]:
            L('ArcGIS issue', f'ArcGIS meteo "{n}"', f'Period on the map ({per}) differs from the UniFr station list ({best["start"]} to {best["end"]}). Station list used.', applied=False)
        if d > 0.3 or (best['elev'] and abs(best['elev'] - el) > 20):
            L('Coordinate corrected', f'ArcGIS meteo "{n}"', f'Replaced by the UniFr station list ("{best["name"]}"): position moved {d:.1f} km' +
              (f', elevation {el} → {best["elev"]:.0f} m' if best['elev'] and abs(best['elev'] - el) > 20 else ''), f'{la}, {lo}', f'{best["lat"]}, {best["lon"]}')
    for n, la, lo, el, src in A.SNOW:
        if 'UniFR' not in src: continue
        cands = [st for st in stations if st['kind'] == 'meteo' and st['site'] == canon_arc(n)]
        if cands:
            best = min(cands, key=lambda st: km(la, lo, st['lat'], st['lon']))
            d = km(la, lo, best['lat'], best['lon'])
            if d > 0.3:
                L('Coordinate corrected', f'ArcGIS snow "{n}"', f'Replaced by the UniFr station list ("{best["name"]}"): position moved {d:.0f} km', f'{la}, {lo}', f'{best["lat"]}, {best["lon"]}')
    L('Records replaced', 'ArcGIS meteo and snow layers', 'UniFr AWS and snow-height records from the ArcGIS map replaced by the UniFr station lists (correct coordinates, periods, variables). GFZ/SDSS stations Abramov and Golubin kept from the ArcGIS map.')

added = 0
for n, la, lo, el, per, loc, op in A.METEO:
    if HAVE_STATIONS and 'UniFR' in op: continue
    a, b = (per.split('-') + [''])[:2] if per else ('', '')
    stt, stp = st_from_end(b) if b else ('Ongoing', None)
    by = ['UniFR'] if 'UniFR' in op else ['GFZ', 'CAIAG']
    add_arc(n, la, lo, 'Meteorology', 'Air temperature, humidity, wind, radiation' + (', precipitation' if 'SDSS' in op else ''),
            'AWS', a, stp, stt, by, f'Elevation {el} m.' + (f' {loc}.' if loc else '') + f' Period {per}.' * bool(per) + f' Operator: {op}.', label=n); added += 1
for n, a, b, la, lo, rm in A.RUNOFF:
    stt, stp = st_from_end(b)
    add_arc(n, la, lo, 'Runoff', 'Glacial runoff', 'Pressure sensor', a, stp, stt, ['UniFR'], f'{a} to {b}. {rm}', label=n); added += 1
for n, k, la, lo, dates, rm in A.PERMAFROST:
    add_arc(n, la, lo, 'Permafrost', 'ERT tomography profiles', 'ERT', dates[:4], None, 'Unknown', ['UniFR'],
            f'{k} profile end-points on the map. Surveys: {dates}.' + (' Only the start point is on the map; end point missing.' if rm else '')); added += 1
for n, la, lo, el, src in A.SNOW:
    if HAVE_STATIONS and 'UniFR' in src: continue
    add_arc(n, la, lo, 'Snow', 'Snow height', 'AWS', '', None, 'Ongoing', ['UniFR'] if 'UniFR' in src else ['GFZ', 'CAIAG'],
            f'Elevation {el} m. Source: {src}.', label=n); added += 1
L('Records merged', 'ArcGIS map', f'{added} records from the ArcGIS layers (runoff, ERT profiles' + ('' if HAVE_STATIONS else ', AWS, snow height') + ', GFZ/SDSS stations) added with source "ArcGIS map".', '', '')

# ---------- site descriptions from the Main Information layer ----------
desc = {}
for n, c, la, lo, reg, morph, inst in A.MAIN:
    cn = canon_arc(n)
    region, note = reg, ''
    if n in A.REGION_FIX:
        region, why = A.REGION_FIX[n]
        L('Region corrected', n, why, reg, region)
    if n in A.REGION_VERIFY:
        note = A.REGION_VERIFY[n]
    desc[cn] = dict(region=region, morph=morph, inst=inst.replace('accepted', 'accepted') , verify=note)
for n, ev, la, lo in A.GLACIER_WGMS:
    if ev: desc.setdefault(canon_arc(n), {})['event'] = ev + ' (WGMS FoG, 2025-02; please verify)'
for s in sites.values():
    if s['name'] in desc:
        s['info'] = desc[s['name']]
        if desc[s['name']].get('verify'): flag(site_key(s['country'], s['name'], s['lat'], s['lon']), desc[s['name']]['verify'])

# ArcGIS-internal issues worth listing
for kind, where, what in [
    ('ArcGIS issue', 'Meteo layer', 'One record has no name and no coordinates; not carried over.'),
    ('ArcGIS issue', 'Glacier layer', 'Stray record "GLACIOLOGICAL DATA" with no coordinates; not carried over.'),
    ('ArcGIS issue', 'Permafrost layers', '44 profile start points but 41 end points (Akshiirak, Uy-Bulak Pass, Zholsaly-kezen have no end point). Dates mix two formats (20.08.21 and 2021-08-20).'),
    ('ArcGIS issue', 'Sangvor', 'Two different positions on the map: 38.7431, 71.3587 (meteo) and 38.9167, 71.0000 (snow, main info), about 35 km apart. The spreadsheet has a third: 38.52, 71.05. The UniFr station list confirms 38.74311, 71.35874 (Nissai/Sangvor AWS, 3909 m).'),
    ('ArcGIS issue', 'Several sites', 'Main-information coordinates rounded to whole arc-minutes (e.g. 42.1167, 71.0000), 1–2 km off. Layer geometries used instead where available.'),
    ('ArcGIS issue', 'Golubin runoff', 'Start date 2024-08-07, but the remark says measurements also ran 2019–2021.'),
    ('ArcGIS issue', 'Golubin description', '"length: 235 m in 2022" is probably the front retreat, not the glacier length (~5 km).'),
    ('ArcGIS issue', 'Citations', '"Barandun et al., Accepted a" should be replaced by the published reference.'),
    ('ArcGIS issue', 'Names', 'Inconsistent spellings: Gregoriev/Grigoriev, Uy-Bulak/UyBulak, Zholsaly-kezen/Zhosalykezen, Kjungey/Kungey Ala-Too. Harmonised here.'),
]:
    L(kind, where, what, applied=False)

# ---------- write ----------
for sk, fl in flags.items():
    if sk in sites: sites[sk]['flags'] = fl
site_list = sorted(sites.values(), key=lambda s: s['id'])
for s in site_list:
    s.setdefault('flags', [])
    if s['lat'] is not None: s['lat'], s['lon'] = round(float(s['lat']), 5), round(float(s['lon']), 5)
import datetime
out = dict(sites=site_list, meas=meas, log=log, built=datetime.date.today().isoformat())
json.dump(out, open(OUT, 'w'), ensure_ascii=False, separators=(',', ':'))

# summary
import collections
print('sites', len(site_list), 'mapped', sum(s['lat'] is not None for s in site_list), 'meas', len(meas))
print('flagged sites', sum(bool(s['flags']) for s in site_list))
print(collections.Counter(m['theme'] for m in meas))
print(collections.Counter(o for m in meas for o in m['by']).most_common())
print(collections.Counter(m['status'] for m in meas))
print('log', len(log))
for s in site_list:
    if s['flags'] and any('differs' in f or 'outside' in f for f in s['flags']): print(' ', s['name'], s['flags'])
