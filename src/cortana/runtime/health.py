"""Runtime health snapshot."""
from dataclasses import dataclass
from datetime import datetime, timezone

from cortana.runtime.registry import ModuleRegistry


@dataclass(frozen=True, slots=True)
class HealthSnapshot:
    status: str
    timestamp: str
    modules: dict[str, str]


def get_health(registry: ModuleRegistry) -> HealthSnapshot:
    modules = registry.snapshot()
    failed = any(state == "failed" for state in modules.values())
    return HealthSnapshot(
        status="degraded" if failed else "ok",
        timestamp=datetime.now(timezone.utc).isoformat(),
        modules=modules,
    )
