import pytest

from cortana.runtime.events import Event, EventBus
from cortana.runtime.registry import ModuleRegistry, ModuleState


class DummyModule:
    name = "dummy"

    def __init__(self):
        self.started = False
        self.stopped = False

    async def start(self):
        self.started = True

    async def stop(self):
        self.stopped = True


@pytest.mark.asyncio
async def test_registry_lifecycle():
    registry = ModuleRegistry()
    module = DummyModule()
    registry.register(module)
    await registry.start_all()
    assert registry.snapshot()["dummy"] == ModuleState.STARTED.value
    await registry.stop_all()
    assert module.started and module.stopped
    assert registry.snapshot()["dummy"] == ModuleState.STOPPED.value


@pytest.mark.asyncio
async def test_event_bus_dispatches_event():
    bus = EventBus()
    received = []

    async def handler(event):
        received.append(event.payload["value"])

    await bus.subscribe("sample", handler)
    await bus.publish(Event.create("sample", {"value": 42}))
    assert received == [42]
