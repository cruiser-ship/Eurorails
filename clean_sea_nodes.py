import json
import os
import sys

# ── CONFIGURE HERE ────────────────────────────────────────────────────────────
INPUT_FILE = "map_rough_draft.json"
# ─────────────────────────────────────────────────────────────────────────────


def load_json(path):
    with open(path, "r") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)


def backup(input_path):
    stem, ext = os.path.splitext(input_path)
    backup_path = f"{stem}_backup{ext}"
    save_json(backup_path, load_json(input_path))
    return backup_path


input_path = sys.argv[1] if len(sys.argv) > 1 else INPUT_FILE

if not os.path.exists(input_path):
    print(f"Error: File '{input_path}' not found.", file=sys.stderr)
    sys.exit(1)

backup_path = backup(input_path)
print(f"Backup saved to: {backup_path}")

data = load_json(input_path)
graph = data["graph_data"]

before = len(graph)
purged_keys = [k for k, v in graph.items() if v.get("type") == "space_sea"]
for k in purged_keys:
    del graph[k]

save_json(input_path, data)

remaining = len(graph)
print(f"Nodes before:     {before}")
print(f"space_sea purged: {len(purged_keys)}")
print(f"Nodes remaining:  {remaining}")
