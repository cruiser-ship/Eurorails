import json
import shutil

# --- Configure inputs here ---
ROW = 39
LEFT_COL = 0
RIGHT_COL = 65
SHIFT = -1  # positive = right, negative = left
# ----------------------------

INPUT_FILE = "map_rough_draft.json"
BACKUP_FILE = "map_rough_draft_backup.json"

START_X = 126
DELTA_X = 35


def pixel_x_for(row, col):
    x = START_X + col * DELTA_X
    if row % 2 == 1:
        x -= DELTA_X // 2
    return x


def axial_q_for(row, col):
    return col if row % 2 == 0 else col - 0.5


def shift_section(row, left_col, right_col, shift):
    if shift == 0:
        print("Shift is 0 — nothing to do.")
        return

    with open(INPUT_FILE, "r") as f:
        data = json.load(f)
    graph = data["graph_data"]

    # Collect selected nodes
    selected = {
        key: node
        for key, node in graph.items()
        if node["row"] == row and left_col <= node["col"] <= right_col
    }

    if not selected:
        print(f"No nodes found in row {row} between cols {left_col} and {right_col}.")
        return

    selected_cols = {node["col"] for node in selected.values()}
    target_cols = {c + shift for c in selected_cols}

    # All cols occupied in this row that are NOT part of the selection
    occupied_cols = {
        node["col"]
        for node in graph.values()
        if node["row"] == row and node["col"] not in selected_cols
    }

    conflicts = target_cols & occupied_cols
    if conflicts:
        print(f"Shift blocked — target cols already occupied: {sorted(conflicts)}")
        return

    # Backup before modifying
    shutil.copy2(INPUT_FILE, BACKUP_FILE)
    print(f"Backed up to {BACKUP_FILE}")

    # Process in safe order to avoid key collisions when shifting within same row
    nodes_to_shift = sorted(
        selected.items(),
        key=lambda kv: kv[1]["col"],
        reverse=(shift > 0),
    )

    for key, node in nodes_to_shift:
        del graph[key]
        new_col = node["col"] + shift
        new_key = f"r{row}_c{new_col}"
        graph[new_key] = {
            "row": row,
            "col": new_col,
            "axial_q": axial_q_for(row, new_col),
            "axial_r": row,
            "type": node["type"],
            "pixel_x": pixel_x_for(row, new_col),
            "pixel_y": node["pixel_y"],
        }

    with open(INPUT_FILE, "w") as f:
        json.dump(data, f, indent=4)

    direction = "right" if shift > 0 else "left"
    print(
        f"Shifted {len(selected)} node(s) in row {row} "
        f"(cols {left_col}–{right_col}) {direction} by {abs(shift)}."
    )


if __name__ == "__main__":
    shift_section(ROW, LEFT_COL, RIGHT_COL, SHIFT)
