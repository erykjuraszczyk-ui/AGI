"""Command-line bootstrap for the Cortana foundation runtime."""
from __future__ import annotations

import asyncio
import logging

from cortana.runtime.health import get_health
from cortana.runtime.registry import ModuleRegistry


class FoundationModule:
    name = "foundation"

    async def start(self) -> None:
        logging.getLogger(__name__).info("Foundation module started")

    async def stop(self) -> None:
        logging.getLogger(__name__).info("Foundation module stopped")


async def run() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    registry = ModuleRegistry()
    registry.register(FoundationModule())
    await registry.start_all()
    snapshot = get_health(registry)
    logging.info("Cortana runtime health: %s; modules=%s", snapshot.status, snapshot.modules)
    await registry.stop_all()


def main() -> None:
    asyncio.run(run())


if __name__ == "__main__":
    main()
