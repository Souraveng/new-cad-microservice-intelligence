import os
import sys

# Add current directory to python path to resolve submodules
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from fastapi import FastAPI
from cad_worker.main import app as cad_app
from vision_worker.sheet_intel import app as vision_app
from vision_worker.style_generator import app as style_app
from topology_engine.graph_builder import app as topology_app

app = FastAPI(title="Aegis Intelligence Gateway")

# Mount sub-apps
app.mount("/cad", cad_app)
app.mount("/vision", vision_app)
app.mount("/style", style_app)
app.mount("/topology", topology_app)

@app.get("/")
def read_root():
    return {
        "service": "Aegis Intelligence Gateway",
        "status": "online",
        "endpoints": {
            "cad": "/cad",
            "vision": "/vision",
            "style": "/style",
            "topology": "/topology"
        }
    }

if __name__ == "__main__":
    import uvicorn
    # Default to Cloud Run's $PORT environment variable
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
