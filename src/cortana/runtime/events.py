"""Typed asynchronous in-process event bus."""
from __future__ import annotations

import asyncio
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Awaitable, Callable
from uuid import uuid4


@dataclass(frozen=True, slots=True)
class Event:
    name: str
    payload: dict[str, Any]
    event_id: str
    occurred_at: datetime

    @classmethod
    def create(cls, name: str, payload: dict[str, Any]) -> "Event":
        if not name.strip():
            raise ValueError("Event name cannot be empty")
        return cls(name, payload, str(uuid4()), datetime.now(timezone.utc))


Handler = Callable[[Event], Awaitable[None]]


class EventBus:
    """In-process event dispatcher; handler failures are returned to the publisher."""

    def __init__(self) -> None:
        self._handlers: dict[str, list[Handler]] = defaultdict(list)
        self._lock = asyncio.Lock()

    async def subscribe(self, event_name: str, handler: Handler) -> None:
        if not event_name.strip():
            raise ValueError("Event name cannot be empty")
        async with self._lock:
            if handler not in self._handlers[event_name]:
                self._handlers[event_name].append(handler)

    async def publish(self, event: Event) -> None:
        async with self._lock:
            handlers = tuple(self._handlers.get(event.name, ()))
        if handlers:
            await asyncio.gather(*(handler(event) for handler in handlers))
