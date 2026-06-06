from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any

app = FastAPI(title="Aegis Theme & Style Analyzer")

class StyleRequest(BaseModel):
    room_count: int
    corridor_length: float
    floor_label: str

@app.post("/generate-theme")
async def generate_theme(req: StyleRequest):
    # Generates custom styles and themes depending on drawing geometry profile
    is_high_density = req.room_count > 15
    is_lobby = "lobby" in req.floor_label.lower() or "ground" in req.floor_label.lower()
    
    if is_lobby:
        theme = {
            "name": "Sleek Glassmorphic Lobby",
            "primary": "#10b981", # Emerald Accent
            "glowColor": "rgba(16, 185, 129, 0.25)",
            "backdropFilter": "contrast(1.1) brightness(1.05)",
            "wallStroke": "#34d399",
            "wallWidth": 3.0,
            "gridColor": "rgba(16, 185, 129, 0.03)",
            "roomOpacity": 0.15,
            "texture": "glass"
        }
    elif is_high_density:
        theme = {
            "name": "Industrial Grid Complex",
            "primary": "#f59e0b", # Amber Accent
            "glowColor": "rgba(245, 158, 11, 0.25)",
            "backdropFilter": "brightness(0.9)",
            "wallStroke": "#fbbf24",
            "wallWidth": 2.5,
            "gridColor": "rgba(245, 158, 11, 0.02)",
            "roomOpacity": 0.08,
            "texture": "concrete"
        }
    else:
        theme = {
            "name": "Neon Evacuation Standard",
            "primary": "#6366f1", # Indigo Accent
            "glowColor": "rgba(99, 102, 241, 0.2)",
            "backdropFilter": "none",
            "wallStroke": "#818cf8",
            "wallWidth": 2.0,
            "gridColor": "rgba(255, 255, 255, 0.02)",
            "roomOpacity": 0.12,
            "texture": "blueprint"
        }

    return {
        "success": True,
        "theme": theme
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
