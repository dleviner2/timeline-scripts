import json, csv

path = '/home/hatch/workspace/user/files/Timeline_1_rvbm.json'
with open(path) as f:
    d = json.load(f)
segs = d['semanticSegments']

pts = []
for s in segs:
    tp = s.get('timelinePath')
    if tp:
        for p in tp:
            pts.append((p['time'], p['point']))
pts.sort()
step = max(1, len(pts)//15000)
sel = pts[::step]

out = '/home/hatch/workspace/timeline/travel-samples.csv'
with open(out, 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['timestamp', 'latitude', 'longitude', 'year'])
    for t, p in sel:
        la, lo = p.replace('°','').split(', ')
        w.writerow([t, float(la), float(lo), t[:4]])
print('wrote', len(sel), 'rows to', out)
