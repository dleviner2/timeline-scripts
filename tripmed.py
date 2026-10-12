import json, statistics
from collections import defaultdict

path = '/home/hatch/workspace/user/files/Timeline_1_rvbm.json'
with open(path) as f:
    d = json.load(f)
segs = d['semanticSegments']

trips = []
for s in segs:
    if 'timelineMemory' in s:
        tm = s['timelineMemory'].get('trip')
        if tm and tm.get('distanceFromOriginKms', 0) > 1500:
            trips.append((s['startTime'], s['endTime'], tm['distanceFromOriginKms']))
trips.sort()

# far from home (>300 km) points medians
hx, hy = 34.73, -86.59
for (st, en, dist) in trips:
    lats, lons = [], []
    for s in segs:
        tp = s.get('timelinePath')
        if not tp: continue
        if s['startTime'] >= st and s['endTime'] <= en:
            for p in tp:
                la, lo = [float(x) for x in p['point'].replace('°','').split(', ')]
                if abs(la-hx)+abs(lo-hy) > 3:  # away from home
                    lats.append(la); lons.append(lo)
    if lats:
        print(f"{st[:10]} -> {en[:10]} ({dist} km): median=({statistics.median(lats):.3f}, {statistics.median(lons):.3f}) n={len(lats)}")
