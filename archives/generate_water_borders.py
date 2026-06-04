import json
import math

def generate_borders():
    # Load your current active topological graph
    with open('map_rough_draft.json', 'r') as f:
        data = json.load(f)

    graph_nodes = data['graph_data']

    # Mathematical Constants matching lattice architecture
    R = 1 / math.sqrt(3)
    SQRT3_OVER_2 = math.sqrt(3) / 2

    # Vector block representing the 6 flat-topped hex faces
    DIRECTIONS = [
        ((1,  0),  5, 0),  # Right
        ((0,  1),  4, 5),  # Down-Right
        ((-1, 1),  3, 4),  # Down-Left
        ((-1, 0),  2, 3),  # Left
        ((0, -1),  1, 2),  # Up-Left
        ((1, -1),  0, 1),  # Up-Right
    ]

    def hex_vertex(x, y, k):
        angle = k * math.pi / 3 + math.pi / 6
        return (x + R * math.cos(angle), y + R * math.sin(angle))

    def neighbor_key(r, c, dq, dr):
        n_r = r + dr
        if dr == 0:
            n_c = c + dq
        elif r % 2 == 0:
            if (dq, dr) == (0, 1):   n_c = c + 1
            if (dq, dr) == (-1, 1):  n_c = c
            if (dq, dr) == (0, -1):  n_c = c
            if (dq, dr) == (1, -1):  n_c = c + 1
        else:
            if (dq, dr) == (0, 1):   n_c = c
            if (dq, dr) == (-1, 1):  n_c = c - 1
            if (dq, dr) == (0, -1):  n_c = c - 1
            if (dq, dr) == (1, -1):  n_c = c
        return f"r{n_r}_c{n_c}"

    border_segments = []

    for node_id, node in graph_nodes.items():
        node_type = node.get('type')
        if node_type == 'space_sea' or not node_type:
            continue

        q = node['axial_q']
        c = node['col']
        r = node['axial_r']

        # Convert axial points to grid Cartesian spaces
        x = q
        y = -r * SQRT3_OVER_2

        for (dq, dr), vi, vj in DIRECTIONS:
            key = neighbor_key(r, c, dq, dr)
            # If neighbor does not exist, it represents an open sea boundary edge line segment
            if key not in graph_nodes:
                p1 = hex_vertex(x, y, vi)
                p2 = hex_vertex(x, y, vj)
                
                # Save individual structural lines as coordinate pair entries
                segment_data = {
                    "from_node": node_id,
                    "direction": [dq, dr],
                    "coordinates": [
                        [p1[0], p1[1]],
                        [p2[0], p2[1]]
                    ]
                }
                border_segments.append(segment_data)

    # Compile structured JSON schema layer layout out
    output_data = {
        "meta": {
            "description": "Calculated water coastlines and ocean boundaries for Eurorails map",
            "total_segments": len(border_segments)
        },
        "water_borders": border_segments
    }

    with open('map_borders.json', 'w') as out_f:
        json.dump(output_data, out_f, indent=4)

    print(f"Successfully calculated and extracted {len(border_segments)} coastline vectors into 'map_borders.json'!")

if __name__ == "__main__":
    generate_borders()