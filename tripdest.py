import json, math
from collections import defaultdict

path = '/home/hatch/workspace/user/files/Timeline_1_rvbm.json'
with open(path) as f:
    d = json.load(f)
segs = d['semanticSegments']

def parse(s): return s

trips = []
for s in segs:
    if 'timelineMemory' in s:
        tm = s['timelineMemory'].get('trip')
        if tm and tm.get('distanceFromOriginKms', 0) > 1500:
            trips.append((s['startTime'], s['endTime'], tm['distanceFromOriginKms']))
trips.sort()

# collect path points per trip
for (st, en, dist) in trips:
    grid = defaultdict(int)
    total = 0
    for s in segs:
        tp = s.get('timelinePath')
        if not tp: continue
        if s['startTime'] >= st and s['endTime'] <= en:
            for p in tp:
                lat, lon = p['point'].replace('°','').split(', ')
                lat, lon = float(lat), float(lon)
                # 1-degree grid
                grid[(round(lat), round(lon))] += 1
                total += 1
    top = sorted(grid.items(), key=lambda x: -x[1])[:3]
    print(f"{st[:10]} -> {en[:10]} ({dist} km): {[(c, n) for c, n in top]}")
