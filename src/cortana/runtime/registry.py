"""Module registry with explicit lifecycle states."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Protocol


class ModuleState(str, Enum):
    REGISTERED = "registered"
    STARTED = "started"
    STOPPED = "stopped"
    FAILED = "failed"


class RuntimeModule(Protocol):
    name: str

    async def start(self) -> None: ...
    async def stop(self) -> None: ...


@dataclass(slots=True)
class ModuleRecord:
    module: RuntimeModule
    state: ModuleState = ModuleState.REGISTERED
    error: str | None = None


class ModuleRegistry:
    def __init__(self) -> None:
        self._modules: dict[str, ModuleRecord] = {}

    def register(self, module: RuntimeModule) -> None:
        name = module.name.strip()
        if not name:
            raise ValueError("Module name cannot be empty")
        if name in self._modules:
            raise ValueError(f"Module already registered: {name}")
        self._modules[name] = ModuleRecord(module)

    async def start_all(self) -> None:
        for record in self._modules.values():
            try:
                await record.module.start()
                record.state = ModuleState.STARTED
                record.error = None
            except Exception as exc:
                record.state = ModuleState.FAILED
                record.error = f"{type(exc).__name__}: {exc}"
                await self.stop_all()
                raise

    async def stop_all(self) -> None:
        for record in reversed(tuple(self._modules.values())):
            if record.state == ModuleState.STARTED:
                try:
                    await record.module.stop()
                    record.state = ModuleState.STOPPED
                except Exception as exc:
                    record.state = ModuleState.FAILED
                    record.error = f"{type(exc).__name__}: {exc}"

    def snapshot(self) -> dict[str, str]:
        return {name: record.state.value for name, record in self._modules.items()}
