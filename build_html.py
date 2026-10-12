data = open('/home/hatch/workspace/timeline/heat_data.js').read()

html = '''<!DOCTYPE html>
<html data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
<style>
  * { box-sizing: border-box; }
  body { margin: 0; font-family: -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
  #wrap { display: flex; flex-direction: column; height: 560px; background: var(--hatch-widget-bg, #fff); color: var(--hatch-widget-text, #111); }
  #bar { display: flex; align-items: center; gap: 8px; padding: 8px 12px; border-bottom: 1px solid var(--hatch-widget-border, #e2e2e2); flex-wrap: wrap; }
  #bar .title { font-weight: 600; font-size: 14px; margin-right: auto; }
  .chip { border: 1px solid var(--hatch-widget-border, #d5d5d5); background: var(--hatch-widget-surface, #f6f6f6); color: var(--hatch-widget-text, #111); border-radius: 999px; padding: 5px 12px; font-size: 12px; cursor: pointer; }
  .chip.active { background: var(--hatch-widget-accent, #2f7cf6); color: var(--hatch-widget-on-accent, #fff); border-color: transparent; }
  #map { flex: 1; min-height: 0; }
  #legend { position: absolute; bottom: 22px; right: 10px; z-index: 500; background: var(--hatch-widget-surface, rgba(255,255,255,.92)); border: 1px solid var(--hatch-widget-border, #ddd); border-radius: 8px; padding: 6px 10px; font-size: 11px; color: var(--hatch-widget-muted, #555); }
  #legend .grad { height: 8px; width: 120px; border-radius: 4px; background: linear-gradient(to right, #2c7bb6, #abd9e9, #ffffbf, #fdae61, #d7191c); margin: 4px 0 2px; }
  #meta { padding: 6px 12px; font-size: 11px; color: var(--hatch-widget-muted, #666); border-top: 1px solid var(--hatch-widget-border, #e2e2e2); }
  #mapwrap { position: relative; flex: 1; min-height: 0; display: flex; flex-direction: column; }
</style>
</head>
<body>
<div id="wrap">
  <div id="bar">
    <span class="title">Travel heatmap</span>
    <button class="chip" data-f="all">All years</button>
    <button class="chip" data-f="a">2011&ndash;2015</button>
    <button class="chip" data-f="b">2016&ndash;2020</button>
    <button class="chip" data-f="c">2021&ndash;2026</button>
  </div>
  <div id="mapwrap">
    <div id="map"></div>
    <div id="legend"><div>Time spent</div><div class="grad"></div><div>less &rarr; more</div></div>
  </div>
  <div id="meta"></div>
</div>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script src="https://unpkg.com/leaflet.heat@0.2.0/dist/leaflet-heat.js"></script>
<script>
var PTS = [DATA];
var state = window.hatchWidget ? window.hatchWidget.getState({filter: "all"}) : {filter: "all"};

var map = L.map("map", { worldCopyJump: true }).setView([36.5, -90], 4);
L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", { maxZoom: 18, attribution: "&copy; OpenStreetMap" }).addTo(map);

function inRange(p) {
  var y = p[2], f = state.filter;
  if (f === "all") return true;
  if (f === "a") return y >= 2011 && y <= 2015;
  if (f === "b") return y >= 2016 && y <= 2020;
  return y >= 2021;
}

var heat = null;
function render() {
  var sel = PTS.filter(inRange);
  var latlngs = sel.map(function(p){ return [p[0], p[1]]; });
  if (heat) { map.removeLayer(heat); }
  heat = L.heatLayer(latlngs, { radius: 22, blur: 16, maxZoom: 14, minOpacity: 0.35,
    gradient: {0.0:"#2c7bb6", 0.25:"#abd9e9", 0.5:"#ffffbf", 0.75:"#fdae61", 1.0:"#d7191c"} });
  heat.addTo(map);
  document.querySelectorAll(".chip").forEach(function(c){ c.classList.toggle("active", c.dataset.f === state.filter); });
  var yrs = sel.map(function(p){return p[2];});
  var lo = Math.min.apply(null, yrs), hi = Math.max.apply(null, yrs);
  document.getElementById("meta").textContent = sel.length.toLocaleString() + " location samples" + (lo && hi && lo !== hi ? " (" + lo + " - " + hi + ")" : "");
}
document.querySelectorAll(".chip").forEach(function(c){
  c.addEventListener("click", function(){
    state = { filter: c.dataset.f };
    if (window.hatchWidget) window.hatchWidget.setState(state);
    render();
  });
});
if (window.hatchWidget) {
  window.addEventListener("hatch-widget-state", function(e){ state = e.detail.state; render(); });
}
render();
</script>
</body>
</html>'''
html = html.replace('DATA', data)
open('/home/hatch/workspace/timeline/travel-heatmap.html', 'w').write(html)
print('bytes:', len(html))
