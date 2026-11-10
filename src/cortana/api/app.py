"""Optional localhost health API."""
from fastapi import FastAPI

from cortana.runtime.health import get_health
from cortana.runtime.registry import ModuleRegistry

app = FastAPI(title="Cortana Foundation API", version="0.1.0")
_registry = ModuleRegistry()


@app.get("/health")
async def health() -> dict[str, object]:
    snapshot = get_health(_registry)
    return {"status": snapshot.status, "timestamp": snapshot.timestamp, "modules": snapshot.modules}


@app.get("/version")
async def version() -> dict[str, str]:
    return {"name": "Cortana Foundation Engine", "version": "0.1.0"}
