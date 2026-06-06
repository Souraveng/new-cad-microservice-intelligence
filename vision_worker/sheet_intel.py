import os
from fastapi import FastAPI, UploadFile, File, Form
from typing import List, Dict, Any

app = FastAPI(title="Aegis Vision Worker")

@app.post("/classify")
async def classify_regions(
    file: UploadFile = File(...)
):
    # Returns detected sub-regions (e.g. floor plans, elevations, legends)
    # Mocking PaliGemma model inference output
    return {
        "success": True,
        "regions": [
            {
                "regionId": "region_1",
                "bounds": {"minX": 0, "maxX": 100, "minY": 0, "maxY": 100},
                "type": "floor_plan",
                "typeConfidence": 0.95,
                "floorPlanScore": 0.92,
                "suggestedFloorLabel": "Floor 1",
                "previewUrl": "/api/static/crop_1.png"
            },
            {
                "regionId": "region_2",
                "bounds": {"minX": 110, "maxX": 150, "minY": 0, "maxY": 100},
                "type": "elevation",
                "typeConfidence": 0.88,
                "floorPlanScore": 0.12,
                "suggestedFloorLabel": None,
                "previewUrl": "/api/static/crop_2.png"
            }
        ]
    }

@app.post("/extract-elements")
async def extract_elements(
    file: UploadFile = File(...),
    region_id: str = Form(...)
):
    # Mocking PaliGemma wall, door, room, stair, exit detection
    return {
        "success": True,
        "regionId": region_id,
        "elements": {
            "walls": [
                {"x1": 15.0, "y1": 15.0, "x2": 85.0, "y2": 15.0},
                {"x1": 85.0, "y1": 15.0, "x2": 85.0, "y2": 85.0},
                {"x1": 85.0, "y1": 85.0, "x2": 15.0, "y2": 85.0},
                {"x1": 15.0, "y1": 85.0, "x2": 15.0, "y2": 15.0}
            ],
            "doors": [
                {"x": 50.0, "y": 15.0, "label": "Main Entry"}
            ],
            "rooms": [
                {"points": [{"x": 20, "y": 20}, {"x": 40, "y": 20}, {"x": 40, "y": 40}, {"x": 20, "y": 40}], "label": "101"}
            ],
            "stairs": [
                {"x": 80.0, "y": 80.0, "label": "Exit Stair A"}
            ],
            "exits": [
                {"x": 50.0, "y": 15.0, "label": "FINAL EXIT"}
            ],
            "elevators": []
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
