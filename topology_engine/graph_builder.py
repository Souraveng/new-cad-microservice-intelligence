from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Any

app = FastAPI(title="Aegis Topology Engine")

class GraphRequest(BaseModel):
    walls: List[Dict[str, float]]
    doors: List[Dict[str, Any]]
    rooms: List[Dict[str, Any]]
    stairs: List[Dict[str, Any]]
    exits: List[Dict[str, Any]]
    elevators: List[Dict[str, Any]]
    floor_id: str

@app.post("/build-graph")
async def build_graph(req: GraphRequest):
    # Deterministic evacuation graph construction logic
    # In a real environment, this processes medial-axis skeletons.
    nodes = []
    edges = []
    warnings = []
    blocking_issues = []
    
    # 1. Connect exits
    if not req.exits:
        blocking_issues.append("No exit anchors detected on the floor layout. Evacuation routing cannot be built.")
    else:
        for idx, exit_pt in enumerate(req.exits):
            node_id = f"{req.floor_id}_exit_{idx}"
            nodes.append({
                "id": node_id,
                "x": exit_pt.get("x", 50.0),
                "y": exit_pt.get("y", 15.0),
                "type": "exit",
                "label": exit_pt.get("label", "Exit")
            })
            
    # 2. Connect rooms
    for idx, room in enumerate(req.rooms):
        node_id = f"{req.floor_id}_room_{idx}"
        nodes.append({
            "id": node_id,
            "x": room.get("x", 30.0),
            "y": room.get("y", 30.0),
            "type": "room",
            "label": room.get("label", f"Room {idx}")
        })
        # Mock connecting room node to nearest exit/corridor node
        if nodes and len(nodes) > 1:
            edges.append({
                "id": f"edge_room_{idx}",
                "from": node_id,
                "to": nodes[0]["id"],
                "kind": "corridor"
            })
            
    # 3. Connect stairs
    for idx, stair in enumerate(req.stairs):
        node_id = f"{req.floor_id}_stair_{idx}"
        nodes.append({
            "id": node_id,
            "x": stair.get("x", 80.0),
            "y": stair.get("y", 80.0),
            "type": "stair",
            "label": stair.get("label", "Exit Stair")
        })
        if nodes and len(nodes) > 1:
            edges.append({
                "id": f"edge_stair_{idx}",
                "from": node_id,
                "to": nodes[0]["id"],
                "kind": "stairs"
            })

    # Warnings checks
    if not req.stairs:
        warnings.append("No stairwells detected on this floor plan region.")
        
    return {
        "success": True,
        "nodes": nodes,
        "edges": edges,
        "validationReport": {
            "blockingIssues": blocking_issues,
            "warnings": warnings,
            "confidenceScore": 0.88
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5002)
