import pytest

from cortana.runtime.application import CortanaApplication, RuntimeState
from cortana.runtime.events import Event


class ProbeModule:
    name = "probe"

    def __init__(self, fail_start: bool = False):
        self.fail_start = fail_start
        self.started = False
        self.stopped = False

    async def start(self):
        if self.fail_start:
            raise RuntimeError("startup failure")
        self.started = True

    async def stop(self):
        self.stopped = True


@pytest.mark.asyncio
async def test_application_lifecycle_and_runtime_events():
    application = CortanaApplication()
    module = ProbeModule()
    received: list[str] = []

    async def capture(event: Event):
        received.append(event.name)

    await application.event_bus.subscribe("runtime.started", capture)
    await application.event_bus.subscribe("runtime.stopped", capture)
    application.register_module(module)

    await application.start()
    assert application.state is RuntimeState.RUNNING
    assert application.health().status == "ok"
    assert module.started is True

    await application.stop()
    assert application.state is RuntimeState.STOPPED
    assert module.stopped is True
    assert received == ["runtime.started", "runtime.stopped"]


@pytest.mark.asyncio
async def test_application_rejects_registration_after_start():
    application = CortanaApplication()
    await application.start()
    with pytest.raises(RuntimeError):
        application.register_module(ProbeModule())
    await application.stop()


@pytest.mark.asyncio
async def test_application_rolls_back_modules_when_startup_fails():
    application = CortanaApplication()
    first = ProbeModule()
    failing = ProbeModule(fail_start=True)
    failing.name = "failing"
    application.register_module(first)
    application.register_module(failing)

    with pytest.raises(RuntimeError, match="startup failure"):
        await application.start()

    assert application.state is RuntimeState.FAILED
    assert first.started is True
    assert first.stopped is True


@pytest.mark.asyncio
async def test_application_stop_before_start_is_safe():
    application = CortanaApplication()
    await application.stop()
    assert application.state is RuntimeState.STOPPED
    assert application.health().status == "stopped"
