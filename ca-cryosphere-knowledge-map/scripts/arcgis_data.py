# Records read from the ArcGIS web map "Cryosphere of Central Asia" (item 7fe9591b9929426da88eaa94fa4b470b), 2026-11-20.
# Site names are given as on the map. Coordinates are the layer geometries (WGS84).

METEO = [  # name, lat, lon, elev, period, location, operator
 ("Abramov",39.6485,71.5855,4091,"","", "GFZ/CAIAG (SDSS)"),
 ("Golubin",42.4816,74.4842,3305,"","", "GFZ/CAIAG (SDSS)"),
 ("Zulmart (No.139) - on rock",38.8829,73.0134,4591,"2019.03-2024.08","On rock","UniFR (SensAlpin)"),
 ("Zulmart (No.139) - on ice",38.8647,73.0033,4897,"2024.08-2024.12","On ice","UniFR (SensAlpin)"),
 ("Batysh Sook - on rock",41.7972,77.7490,4060,"2023.07-2025.08","On rock","UniFR (SensAlpin)"),
 ("Batysh Sook - on ice",41.7840,77.7516,4242,"2023.07-2025.08","On ice","UniFR (SensAlpin)"),
 ("Gregoriev",41.9791,77.9158,4600,"2018.02-2024.09","Firn on glacier","UniFR (SensAlpin)"),
 ("Uy-Bulak Pass",39.2030,73.4421,4264,"2024.04-2025.08","On gravel (cemented)","UniFR (SensAlpin)"),
 ("No.354 (Akshiirak)",41.8003,78.0848,3553,"2022.08-2025.08","On gravel (cemented)","UniFR (SensAlpin)"),
 ("No.457 (NHD)",37.4078,72.8217,4767,"2023.07-2025.08","On rock","UniFR (SensAlpin)"),
 ("Zholsaly-kezen Pass",43.0408,76.9433,3295,"2024.04-2025.06","On gravel (cemented)","UniFR (SensAlpin)"),
 ("Yakarcha (No.71)",38.9914,68.5779,3658,"2021.05-2025.08","On rock","UniFR (SensAlpin)"),
 ("Sangvor",38.7431,71.3587,3000,"2021.10-2024.09","","UniFR (SensAlpin)"),
 ("Barkrak",42.1167,71.0000,3660,"2022.08-2024.08","","UniFR (SensAlpin)"),
]
# One further meteo record on the map has no name and no coordinates.

RUNOFF = [  # name, start, end, lat, lon, remark
 ("Batysh Sook","2021-08-01","2025-08-15",41.7986,77.7496,"Position changed: 2021-2024 the station was at 41.80201, 77.75022."),
 ("No.354 (Akshiirak)","2022-08-17","2025-08-13",41.8112,78.1289,"Measurements also 23 Aug 2019 - 4 Sep 2021 at the same site."),
 ("Golubin","2024-08-07","2025-08-04",42.4779,74.4810,"Measurements also 25 Jul 2019 - 29 Sep 2021 at the same site."),
 ("Abramov (left)","2019-08-23","2024-07-23",39.6577,71.5695,"Two channels: orographic left- and right-hand pro-glacial streams."),
 ("Abramov (right)","2021-08-22","2024-07-22",39.6565,71.5707,"Two channels: orographic left- and right-hand pro-glacial streams."),
 ("Arabel-Suu","2023-07-12","2025-08-14",41.8794,78.0456,"Multiple glaciers at a river measurement location."),
 ("Zulmart (No.139) (high)","2023-08-10","2025-08-03",38.8803,73.0112,"High: flow behind outwash plain, difficult location."),
 ("Zulmart (No.139) (low)","2022-08-09","2025-08-03",38.8831,73.0137,"Low: includes small glacier on the orographic left."),
 ("No.457 (NHD)","2022-08-05","2025-08-07",37.4076,72.8201,""),
 ("Yakarcha (No.71) (high)","2023-09-24","2025-08-24",38.9875,68.5674,"High: close to the pro-glacial stream."),
 ("Yakarcha (No.71) (low)","2024-07-20","2025-08-24",38.9897,68.5774,"Low: several water sources draining through a lake."),
]

PERMAFROST = [  # site, n profile ends+starts, mean lat, mean lon, survey dates, remark
 ("Abramov",20,39.649,71.579,"2021-08-20..24, 2022-07-26",""),
 ("Batysh Sook",18,41.767,77.773,"2021-08-02..04, 2022-08-20, 2023-07-12, 2023-07-23",""),
 ("Bulunkul",2,37.704,72.947,"2023-08-05",""),
 ("Golubin",16,42.483,74.491,"2021-07-18..20, 2022-08-07..11",""),
 ("Karakul",4,39.203,73.443,"2023-08-07",""),
 ("Kumtor",6,41.810,78.074,"2022-08-17..19",""),
 ("No.457 (NHD)",4,37.412,72.809,"2023-08-16..17",""),
 ("No.599 (Kjungey Ala-too)",2,42.792,76.842,"2021-07-26",""),
 ("Yakarcha (No.71)",4,38.991,68.586,"2022-08-22, 2022-08-27",""),
 ("Zulmart (No.139)",6,38.883,73.015,"2023-08-09..12",""),
 ("Akshiirak",1,41.800,78.085,"2022-08-19","start point only"),
 ("UyBulak Pass",1,39.203,73.442,"2023-07-04","start point only"),
 ("Zhosalykezen Pass",1,43.041,76.943,"2023-07-04","start point only"),
]

GLACIER_WGMS = [  # name, event, lat, lon
 ("Abramov","Surge (in 1978)",39.62,71.56),
 ("No.599 (Kjungey Ala-too)","",42.7925,76.8668),
 ("Golubin","",42.46,74.495),
 ("Gregoriev","",41.96,77.92),
 ("No.354 (Akshiirak)","Surge (in 1947)",41.7990,78.1506),
 ("No.457 (NHD)","Surge (n.d.)",37.3971,72.8274),
 ("Barkrak Sredniy East Branch","",42.1245,71.0066),
 ("Barkrak","",42.1210,70.9920),
 ("Barkrak Pravyy","",42.1380,71.0260),
 ("Batysh Sook","",41.79,77.75),
 ("Zulmart (No.139)","Surge (n.d.)",38.8628,73.0032),
 ("No. 676 (GGP)","",38.9472,68.2789),
 ("Yakarcha (No.71)","Surge (in 1973)",38.9811,68.5627),
]

SNOW = [  # name, lat, lon, elev, source
 ("Batysh Sook",41.7840,77.7516,4242,"UniFR (SensAlpin)"),
 ("Grigoriev",41.9791,77.9158,4600,"UniFR (SensAlpin)"),
 ("Sangvor",38.9167,71.0000,3000,"UniFR (SensAlpin)"),
 ("Zulmart on rock",38.8829,73.0134,4591,"UniFR (SensAlpin)"),
 ("Zulmart on ice",38.8647,73.0033,4897,"UniFR (SensAlpin)"),
 ("No.457 (NHD)",37.4078,72.8217,4767,"UniFR (SensAlpin)"),
 ("Yakarcha (No.71)",38.9914,68.5779,3658,"UniFR (SensAlpin)"),
 ("Golubin",42.4816,74.4842,3305,"SDSS"),
]

# "Main Information" layer: site descriptions as on the map (region label as on the map).
MAIN = [  # name, country, lat, lon, region_on_map, morphometry, instrumentation
 ("Zholsaly-kezen Pass","Kazakhstan",43.0333,76.95,"Northern Tien Shan","3295 m a.s.l.","RST: 1 (Barandun et al., accepted)"),
 ("Abramov","Kyrgyzstan",39.6167,71.55,"Pamir-Alay","3650–5000 m a.s.l., 21 km² (2024), north-facing","GFZ station (CAWa project; Schöne et al., 2013); RST: 8"),
 ("Batysh Sook","Kyrgyzstan",41.7833,77.75,"Central Tian Shan, Akshiirak Range","3950–4450 m a.s.l., 1.08 km² (2016), northern slope of the Zhetim-Bel ridge; volume 0.033 km³ ± 6.5% (2010)","RST: 3"),
 ("Gregoriev","Kyrgyzstan",41.9667,77.9167,"Central Tien Shan, Kyrgyz Ala-Too Range","4100–4600 m a.s.l. (flat glacier plateau), ~8 km², south slope of the Terskey Ala-Too","RST: 0"),
 ("Golubin","Kyrgyzstan",42.4667,74.4833,"Northern Tian Shan, Kyrgyz Ala-Too Range","3300–4400 m a.s.l., 5.42 km² (2018), northern slope of the Kyrgyz Alatau; volume 0.348 km³; 'length: 235 m in 2022'","GFZ station (CAWa project; Schöne et al., 2013); RST: 3"),
 ("No.354 (Akshiirak)","Kyrgyzstan",41.7833,78.1667,"Central Tian Shan, Akshiirak Range","3750–4680 m a.s.l., 6.4 km² (2016), tongue oriented NW; volume 0.272 ± 0.022 km³","RST: 0"),
 ("No.599 (Kjungey Ala-too)","Kyrgyzstan",42.7833,76.8667,"Northern Tien Shan, Kungey Ala-Too Range","3780 m a.s.l.",""),
 ("Kumtor","Kyrgyzstan",41.8167,78.0667,"Central Tien Shan, Akshiirak Range","3660 m a.s.l.","RST: 3 (Mathys et al., 2025)"),
 ("No. 676 (GGP)","Tajikistan",38.9333,68.2833,"Pamir-Alay","",""),
 ("Sangvor","Tajikistan",38.9167,71.0,"Western Pamir","2518–5305 m a.s.l., 37.4 km² (basin area)","RST: 0"),
 ("Uy-Bulak Pass","Tajikistan",39.2,73.45,"Western Pamir","","RST: 3"),
 ("Yakarcha (No.71)","Tajikistan",38.9833,68.5667,"Pamir-Alay","~3300 m a.s.l. (mean altitude)",""),
 ("Kon-Chukurbashi","Tajikistan",39.25,73.55,"Western Pamir","",""),
 ("Zulmart (No.139)","Tajikistan",38.8667,73.0,"Western Pamir","4625–5497 m a.s.l., 3.64 km², SW-facing","RST: 2"),
 ("Ishkashim","Tajikistan",37.5667,73.0833,"Western Pamir","",""),
 ("No.457 (NHD)","Tajikistan",37.4,72.8333,"Western Pamir","4580 m a.s.l.","RST: 1"),
 ("Karakul","Tajikistan",39.2,73.45,"Western Pamir","4210 m a.s.l.","RST: 1 (Mathys et al., 2025)"),
 ("Bulunkul","Tajikistan",37.7,72.95,"Western Pamir","3720 m a.s.l.","RST: 1 (Mathys et al., 2025)"),
 ("Barkrak","Uzbekistan",42.1167,71.0,"Western Tian Shan, Zeravshan Range","3500–4100 m a.s.l., 2.18 km² (2016); volume 0.087 km³","RST: 0"),
 ("Barkrak Pravyy","Uzbekistan",42.138,71.026,"Western Tian Shan, Zeravshan Range","",""),
 ("Barkrak Sredniy East Branch","Uzbekistan",42.1245,71.0066,"Western Tian Shan, Zeravshan Range","",""),
]

# Region corrections proposed for the platform (shown with the original label in the corrections log).
REGION_FIX = {
 "Karakul": ("Eastern Pamir", "Karakul lies in the Eastern Pamir, not the Western Pamir."),
 "Uy-Bulak Pass": ("Eastern Pamir", "Uy-Bulak Pass lies in the Eastern Pamir, not the Western Pamir."),
 "Bulunkul": ("Eastern Pamir", "Bulunkul lies in the Eastern Pamir, not the Western Pamir."),
 "Kon-Chukurbashi": ("Eastern Pamir", "Kon-Chukurbashi lies in the Eastern Pamir, not the Western Pamir."),
 "Zulmart (No.139)": ("Eastern Pamir (Zulmart / Muzkol area)", "Zulmart lies in the Central/Eastern Pamir, not the Western Pamir."),
 "Gregoriev": ("Inner Tien Shan, Terskey Ala-Too Range", "Map labelled it Kyrgyz Ala-Too; its own description says south slope of the Terskey Ala-Too."),
 "Barkrak": ("Western Tien Shan (Pskem basin)", "Barkrak is in the Western Tien Shan, Pskem basin, not the Zeravshan Range (Pamir-Alay). Please verify range name."),
 "Barkrak Pravyy": ("Western Tien Shan (Pskem basin)", "As for Barkrak. Please verify."),
 "Barkrak Sredniy East Branch": ("Western Tien Shan (Pskem basin)", "As for Barkrak. Please verify."),
}
REGION_VERIFY = {"Sangvor": "Labelled Western Pamir on the map; please verify (Rasht / Peter the First range area?)."}
