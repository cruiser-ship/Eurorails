# Eurorails — Domain Context

## Purpose

A Python toolkit that digitizes the **Eurorails** board game map into a queryable hex-grid JSON graph. The pipeline converts a physical map photograph into `master_map.json`, a node graph encoding terrain types, city names, and water obstacle data on edges.

## Domain model

### Hex node

Fundamental unit. Each node maps to one hex cell on the physical board. Stored in `master_map.json` under key `r{row}_c{col}`.

Key fields: `type` (terrain), `city_name` (string or null), `neighbors` (map of node IDs → edge obstacle data).

**Terrain types:** `clear`, `mountain`, `alpine`, `small_city`, `medium_city`, `large_city`, `ferry`, `space_sea`.

`space_sea` nodes exist in the data but are skipped during rendering and pathfinding.

### City node

A hex node whose `type` is `small_city`, `medium_city`, or `large_city`. Has an associated `city_name` string. The city name editor (`city_adder.py`) assigns these names interactively.

### Water obstacle (river / lake edge)

An obstacle that lives on the **edge** between two adjacent nodes, stored bidirectionally in each node's `neighbors` map as `{river, river_name, lake, lake_name}`. Crossing a water obstacle during gameplay has a movement cost.

### Axial coordinates

Each node has `axial_q` (column) and `axial_r` (row) in an axial hex coordinate system. Odd rows are offset by −0.5 in q. Screen projection: `x = axial_q`, `y = −axial_r × (√3 / 2)`.

## Tool taxonomy

### Pipeline tools (`archives/`)

Build and transform map data. Run once (or re-run to edit). Not intended for ongoing use.

- `aligner2.py` — perspective-correct the map photo
- `type_plotting.py` — keyboard-driven terrain classification
- `river_plotter.py` — click-to-tag river/lake edges
- `master_map_maker.py` — merge rough draft + rivers → `master_map.json`

### Interactive editors (project root)

Read `master_map.json`, allow edits, write back.

- `city_adder.py` — assign city names to city nodes; keyboard-driven text entry
- `master_map_visualization.py` — read-only map viewer with click tooltips

## UI conventions

**Editing state display:** Shown as an axes-space overlay text element (`ax.text` with `transform=ax.transAxes`), anchored to the top-left corner of the map viewport. Must not affect figure layout or map axes geometry. Never use `fig.text()` for dynamic status — it lives in the figure margin and triggers `tight_layout` recalculations on redraw.

**Node selection:** Click within `DISTANCE_THRESHOLD = 0.4` map units of a node center. Selected city nodes enter edit mode; all other nodes show a tooltip annotation.

**Save / exit:** `q` saves pending changes and closes. `Esc` closes without saving (or cancels the current edit if in edit mode).
