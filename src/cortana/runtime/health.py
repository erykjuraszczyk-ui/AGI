"""Runtime health snapshot."""
from dataclasses import dataclass
from datetime import datetime, timezone

from cortana.runtime.registry import ModuleRegistry


@dataclass(frozen=True, slots=True)
class HealthSnapshot:
    status: str
    timestamp: str
    modules: dict[str, str]
    runtime_state: str = "unknown"


def get_health(
    registry: ModuleRegistry,
    runtime_state: str | None = None,
) -> HealthSnapshot:
    modules = registry.snapshot()
    failed = any(state == "failed" for state in modules.values())
    state = runtime_state or "unknown"
    if failed:
        status = "degraded"
    elif state in {"new", "starting", "stopping", "stopped", "failed"}:
        status = state
    else:
        status = "ok"
    return HealthSnapshot(
        status=status,
        timestamp=datetime.now(timezone.utc).isoformat(),
        modules=modules,
        runtime_state=state,
    )
