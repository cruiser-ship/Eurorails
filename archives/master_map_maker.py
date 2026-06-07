import json

# Explicit axial directions provided for the map layout
DIRECTIONS = [
    {"dq": 1, "dr": 0}, {"dq": -1, "dr": 0},
    {"dq": 0.5, "dr": 1}, {"dq": -0.5, "dr": 1},
    {"dq": 0.5, "dr": -1}, {"dq": -0.5, "dr": -1}
]

def create_master_map_axial(map_draft_path, rivers_path, output_path):
    with open(map_draft_path, 'r') as f:
        map_draft = json.load(f)
        
    with open(rivers_path, 'r') as f:
        rivers_data = json.load(f)

    master_map = {}
    axial_to_id = {}  # Registry to translate (q, r) floats back to "r#_c#" keys

    # Step 1: Initialize all nodes and map their precise spatial vector positions
    for node_id, data in map_draft.items():
        q = data.get("axial_q")
        r = data.get("axial_r")
        
        # Link this absolute coordinate combination directly back to its string key identifier
        axial_to_id[(q, r)] = node_id
        
        master_map[node_id] = {
            "id": node_id,
            "row": data.get("row"),
            "col": data.get("col"),
            "axial_q": q,
            "axial_r": r,
            "type": data.get("type", "clear"),
            "city_name": None,  
            "neighbors": {}
        }

    # Step 2: Traverse connections via spatial vectors and translate back to r#_c# keys
    for node_id, node_data in master_map.items():
        q = node_data["axial_q"]
        r = node_data["axial_r"]
        
        for vec in DIRECTIONS:
            neighbor_q = q + vec["dq"]
            neighbor_r = r + vec["dr"]
            
            # Safely verify if a tile exists at those coordinates via our positional index map
            target_key = (neighbor_q, neighbor_r)
            if target_key in axial_to_id:
                neighbor_id = axial_to_id[target_key]
                
                node_data["neighbors"][neighbor_id] = {
                    "river": False,
                    "river_name": None,
                    "lake": False,
                    "lake_name": None
                }

        # Step 3: Overlay explicit river/lake boundary details from rivers.json
        if node_id in rivers_data:
            for obstacle in rivers_data[node_id]:
                neighbor_id = obstacle.get("neighbor")
                
                if neighbor_id in node_data["neighbors"]:
                    obs_type = obstacle.get("type")
                    obs_name = obstacle.get("name")
                    
                    if obs_type == "river":
                        node_data["neighbors"][neighbor_id]["river"] = True
                        node_data["neighbors"][neighbor_id]["river_name"] = obs_name
                    elif obs_type == "lake":
                        node_data["neighbors"][neighbor_id]["lake"] = True
                        node_data["neighbors"][neighbor_id]["lake_name"] = obs_name

    with open(output_path, 'w') as f:
        json.dump(master_map, f, indent=4)
    print(f"Success! Master map safely generated: {output_path}")

if __name__ == "__main__":
    create_master_map_axial("map_rough_draft.json", "rivers.json", "master_map.json")