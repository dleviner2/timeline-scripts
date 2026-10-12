import json

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
print('total raw path points:', len(pts))

TARGET = 15000
step = max(1, len(pts)//TARGET)
sel = pts[::step]
print('sampled:', len(sel))

# compact JS array: [lat,lon,year]
out = []
for t, p in sel:
    la, lo = p.replace('°','').split(', ')
    out.append(f"[{float(la):.4f},{float(lo):.4f},{t[:4]}]")
with open('/home/hatch/workspace/timeline/heat_data.js', 'w') as f:
    f.write(','.join(out))
print('data bytes:', len(','.join(out)))
