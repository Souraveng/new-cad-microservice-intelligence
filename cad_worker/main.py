import os
import math
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any

app = FastAPI(title="Aegis CAD Worker")

# Pure Python DBSCAN clustering implementation to avoid scikit-learn dependency issues
def dbscan_points(points: List[tuple], eps: float, min_samples: int) -> List[int]:
    labels = [-1] * len(points)
    cluster_id = 0
    
    def get_neighbors(p_idx):
        neighbors = []
        p = points[p_idx]
        for i, q in enumerate(points):
            if math.hypot(p[0] - q[0], p[1] - q[1]) < eps:
                neighbors.append(i)
        return neighbors

    for i in range(len(points)):
        if labels[i] != -1:
            continue
        neighbors = get_neighbors(i)
        if len(neighbors) < min_samples:
            labels[i] = -1 # Noise
            continue
        
        labels[i] = cluster_id
        seed_set = [n for n in neighbors if n != i]
        for s in seed_set:
            if labels[s] == -1: # Noise becomes border point
                labels[s] = cluster_id
            if labels[s] != -1:
                continue
            labels[s] = cluster_id
            s_neighbors = get_neighbors(s)
            if len(s_neighbors) >= min_samples:
                for sn in s_neighbors:
                    if sn not in seed_set:
                        seed_set.append(sn)
        cluster_id += 1
    return labels

@app.post("/segment")
async def segment_drawing(
    file: UploadFile = File(...),
    floor_id: str = Form(...)
):
    # Mocking ezdxf / ODA processing of CAD vector entities
    filename = file.filename
    # Let's read file and parse some mock lines or lines extracted from request
    content = await file.read()
    
    # Simple mock geometry parser returning layout elements
    # In a real environment, this parses DXF/DWG using ezdxf.
    return {
        "success": True,
        "filename": filename,
        "layers": ["WALLS", "DOORS", "ROOMS", "STAIRS", "ELEVATORS"],
        "linesGeom": [
            {"layer": "WALLS", "x1": 10.0, "y1": 10.0, "x2": 90.0, "y2": 10.0},
            {"layer": "WALLS", "x1": 90.0, "y1": 10.0, "x2": 90.0, "y2": 90.0},
            {"layer": "WALLS", "x1": 90.0, "y1": 90.0, "x2": 10.0, "y2": 90.0},
            {"layer": "WALLS", "x1": 10.0, "y1": 90.0, "x2": 10.0, "y2": 10.0},
        ],
        "texts": [
            {"layer": "ROOMS", "x": 20.0, "y": 20.0, "text": f"Room 101 ({floor_id})"},
            {"layer": "STAIRS", "x": 50.0, "y": 50.0, "text": "EXIT STAIRS"},
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5001)
