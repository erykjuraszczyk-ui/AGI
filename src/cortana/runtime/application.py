"""Application-level lifecycle orchestration for Cortana Runtime."""
from __future__ import annotations

import asyncio
from enum import Enum

from cortana.runtime.events import Event, EventBus
from cortana.runtime.health import HealthSnapshot, get_health
from cortana.runtime.registry import ModuleRegistry, RuntimeModule


class RuntimeState(str, Enum):
    NEW = "new"
    STARTING = "starting"
    RUNNING = "running"
    STOPPING = "stopping"
    STOPPED = "stopped"
    FAILED = "failed"


class CortanaApplication:
    """Coordinates module lifecycle, runtime events, and health reporting.

    This class deliberately does not execute operating-system commands, activate
    devices, or contact model providers. Those capabilities belong behind
    separately authorized adapters.
    """

    def __init__(
        self,
        registry: ModuleRegistry | None = None,
        event_bus: EventBus | None = None,
    ) -> None:
        self.registry = registry or ModuleRegistry()
        self.event_bus = event_bus or EventBus()
        self._state = RuntimeState.NEW
        self._lifecycle_lock = asyncio.Lock()

    @property
    def state(self) -> RuntimeState:
        return self._state

    def register_module(self, module: RuntimeModule) -> None:
        if self._state is not RuntimeState.NEW:
            raise RuntimeError("Modules can only be registered before runtime startup")
        self.registry.register(module)

    async def start(self) -> None:
        async with self._lifecycle_lock:
            if self._state is not RuntimeState.NEW:
                raise RuntimeError(f"Cannot start runtime from state: {self._state.value}")
            self._state = RuntimeState.STARTING
            try:
                await self.registry.start_all()
                self._state = RuntimeState.RUNNING
                await self.event_bus.publish(
                    Event.create("runtime.started", {"state": self._state.value})
                )
            except Exception:
                self._state = RuntimeState.FAILED
                await self.registry.stop_all()
                raise

    async def stop(self) -> None:
        async with self._lifecycle_lock:
            if self._state is RuntimeState.STOPPED:
                return
            if self._state is RuntimeState.NEW:
                self._state = RuntimeState.STOPPED
                return
            self._state = RuntimeState.STOPPING
            await self.registry.stop_all()
            self._state = RuntimeState.STOPPED
            await self.event_bus.publish(
                Event.create("runtime.stopped", {"state": self._state.value})
            )

    def health(self) -> HealthSnapshot:
        return get_health(self.registry, runtime_state=self._state.value)
