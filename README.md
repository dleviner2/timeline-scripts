# Timeline analysis scripts

Works on a Google Maps Timeline (Semantic History) JSON export.

- `analyze.py` - overall stats: segment counts, distances by activity type, top visited place IDs, trip count, and writes a 4,000-point sample CSV
- `analyze2.py` - per-year driving/flying/cycling/walking/running distances, far trips (>1500 km from home), 2025-2026 trips
- `tripdest.py` - clusters raw path points per far trip on a 1-degree grid
- `tripmed.py` - median coordinates (away from home) per far trip
- `heatmap.py` - samples ~15k path points to `heat_data.js` for the Leaflet map
- `build_html.py` - builds `travel-heatmap.html` (Leaflet + leaflet.heat, OpenStreetMap tiles)
- `export_csv.py` - writes `travel-samples.csv` (timestamp, latitude, longitude, year)

Set the `path` variable in each script to point at your own timeline JSON export.
