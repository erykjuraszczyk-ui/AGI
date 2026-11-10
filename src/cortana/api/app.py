"""Optional localhost health API with managed runtime lifecycle."""
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI

from cortana.runtime.application import CortanaApplication


_runtime = CortanaApplication()


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    await _runtime.start()
    try:
        yield
    finally:
        await _runtime.stop()


app = FastAPI(
    title="Cortana Foundation API",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/health")
async def health() -> dict[str, object]:
    snapshot = _runtime.health()
    return {
        "status": snapshot.status,
        "runtime_state": snapshot.runtime_state,
        "timestamp": snapshot.timestamp,
        "modules": snapshot.modules,
    }


@app.get("/version")
async def version() -> dict[str, str]:
    return {"name": "Cortana Foundation Engine", "version": "0.1.0"}
