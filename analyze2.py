import json
from collections import defaultdict

path = '/home/hatch/workspace/user/files/Timeline_1_rvbm.json'
with open(path) as f:
    d = json.load(f)
segs = d['semanticSegments']

year_act = defaultdict(lambda: defaultdict(float))
trips = []
for s in segs:
    st = s.get('startTime','')
    yr = int(st[:4]) if st[:4].isdigit() else 0
    if 'activity' in s:
        t = s['activity']['topCandidate']['type']
        dm = s['activity'].get('distanceMeters', 0) or 0
        year_act[yr][t] += dm/1000
    elif 'timelineMemory' in s:
        tm = s['timelineMemory'].get('trip')
        if tm:
            trips.append((st[:10], s['endTime'][:10], tm.get('distanceFromOriginKms'), len(tm.get('destinations',[]))))

years = sorted(year_act)
print('YEAR | drive km | fly km | cycle km | walk km | run km')
for y in years:
    a = year_act[y]
    print(f"{y} | {a['IN_PASSENGER_VEHICLE']:,.0f} | {a['FLYING']:,.0f} | {a['CYCLING']:,.0f} | {a['WALKING']:,.0f} | {a['RUNNING']:,.0f}")

print('\n--- far trips (>1500 km from home) ---')
for t in trips:
    if t[2] and t[2] > 1500:
        print(t)

print('\n--- 2025-2026 trips ---')
for t in trips:
    if t[0][:4] in ('2025','2026'):
        print(t)
