"""Command-line entry point for the Cortana foundation runtime."""
from __future__ import annotations

import asyncio
import logging

from cortana.runtime.application import CortanaApplication


class FoundationModule:
    """Minimal lifecycle module proving runtime startup and shutdown."""

    name = "foundation"

    async def start(self) -> None:
        logging.getLogger(__name__).info("Foundation module started")

    async def stop(self) -> None:
        logging.getLogger(__name__).info("Foundation module stopped")


async def run(stop_event: asyncio.Event | None = None) -> None:
    """Run until the supplied event is set or the process is interrupted."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    application = CortanaApplication()
    application.register_module(FoundationModule())
    await application.start()
    snapshot = application.health()
    logging.info(
        "Cortana runtime state=%s health=%s modules=%s",
        application.state.value,
        snapshot.status,
        snapshot.modules,
    )
    try:
        await (stop_event or asyncio.Event()).wait()
    finally:
        await application.stop()


def main() -> None:
    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        logging.getLogger(__name__).info("Cortana runtime interrupted by operator")


if __name__ == "__main__":
    main()
