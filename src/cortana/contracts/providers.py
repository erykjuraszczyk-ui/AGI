"""Provider-neutral contracts for local/cloud models and perception."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Protocol


class ProviderKind(str, Enum):
    LOCAL = "local"
    CLOUD = "cloud"


@dataclass(frozen=True, slots=True)
class ModelRequest:
    prompt: str
    contains_sensitive_data: bool = False
    cloud_authorized: bool = False


@dataclass(frozen=True, slots=True)
class ModelResponse:
    text: str
    provider: ProviderKind
    model_id: str


class ModelProvider(Protocol):
    kind: ProviderKind

    async def generate(self, request: ModelRequest) -> ModelResponse: ...


class PerceptionModality(str, Enum):
    IMAGE = "image"
    CAMERA_FRAME = "camera_frame"
    AUDIO = "audio"
    SPEECH_TRANSCRIPT = "speech_transcript"


@dataclass(frozen=True, slots=True)
class Observation:
    modality: PerceptionModality
    source: str
    observed_at: str
    content_reference: str | None
    confidence: float | None = None
    consent_granted: bool = False

    def __post_init__(self) -> None:
        if self.confidence is not None and not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")
