import json, math, csv
from collections import Counter, defaultdict

path = '/home/hatch/workspace/user/files/Timeline_1_rvbm.json'
with open(path) as f:
    d = json.load(f)

segs = d['semanticSegments']
print('total segments:', len(segs))

act_types = Counter()
act_dist = defaultdict(float)
years = Counter()
trips = []
visits = Counter()
visit_locs = {}

for s in segs:
    st = s.get('startTime','')
    yr = st[:4] if st else '?'
    if 'activity' in s:
        t = s['activity']['topCandidate']['type']
        dm = s['activity'].get('distanceMeters', 0) or 0
        act_types[t] += 1
        act_dist[t] += dm
        years[(yr, t)] += dm
    elif 'visit' in s:
        tc = s['visit'].get('topCandidate') or {}
        pid = tc.get('placeId', '?')
        visits[pid] += 1
        loc = tc.get('placeLocation', {}).get('latLng')
        if loc and pid not in visit_locs:
            visit_locs[pid] = loc
    elif 'timelineMemory' in s:
        tm = s['timelineMemory'].get('trip')
        if tm:
            trips.append((s['startTime'], s['endTime'], tm.get('distanceFromOriginKms'), len(tm.get('destinations', []))))

print('\n--- activity counts ---')
for t, c in act_types.most_common():
    km = act_dist[t]/1000
    print(f'{t}: {c} segments, {km:,.0f} km')

print('\n--- top visit placeIds (need names) ---')
for pid, c in visits.most_common(20):
    print(pid, c, visit_locs.get(pid, ''))

print('\n--- trips ---')
print('trip count:', len(trips))
for t in trips[:10]:
    print(t)

# decimate path points across whole file for map: keep ~4000
pts = []
for s in segs:
    tp = s.get('timelinePath')
    if tp:
        for p in tp:
            pts.append((p['time'], p['point']))
print('\npath points:', len(pts))
step = max(1, len(pts)//4000)
sel = pts[::step]
with open('/home/hatch/workspace/timeline/path_points.csv','w',newline='') as f:
    w = csv.writer(f)
    w.writerow(['time','point'])
    for t, p in sel:
        w.writerow([t, p])
print('wrote', len(sel), 'sampled points')
