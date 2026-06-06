import os
import sys
import httpx
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse

# Add current directory to python path to resolve submodules
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from vision_worker.sheet_intel import app as vision_app
from vision_worker.style_generator import app as style_app
from topology_engine.graph_builder import app as topology_app

app = FastAPI(title="Aegis Intelligence Gateway")

# Mount other sub-apps locally
app.mount("/vision", vision_app)
app.mount("/style", style_app)
app.mount("/topology", topology_app)

CAD_SERVICE_URL = os.environ.get(
    "CAD_SERVICE_URL", 
    "http://98.89.152.3:5000"
)

# Async HTTP Client for proxying
http_client = httpx.AsyncClient(base_url=CAD_SERVICE_URL, timeout=60.0)

@app.api_route("/cad/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH"])
async def proxy_cad(request: Request, path: str):
    """Proxy requests for the CAD worker to the hosted CAD microservice."""
    # Build target URL
    url = httpx.URL(path=path, query=request.url.query.encode("utf-8"))
    
    # Forward headers, omitting host to prevent SSL / routing issues
    headers = {k: v for k, v in request.headers.items() if k.lower() != "host"}
    
    req = http_client.build_request(
        method=request.method,
        url=url,
        headers=headers,
        content=request.stream(),
    )
    
    resp = await http_client.send(req, stream=True)
    
    return StreamingResponse(
        resp.iter_raw(),
        status_code=resp.status_code,
        headers=dict(resp.headers),
    )

@app.get("/")
def read_root():
    return {
        "service": "Aegis Intelligence Gateway",
        "status": "online",
        "endpoints": {
            "cad": "/cad (proxied to hosted CAD service)",
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

