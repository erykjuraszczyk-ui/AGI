"""Default-deny authorization primitives."""
from dataclasses import dataclass
from enum import Enum


class Decision(str, Enum):
    ALLOW = "allow"
    DENY = "deny"


@dataclass(frozen=True, slots=True)
class AuthorizationRequest:
    action: str
    resource: str
    explicitly_approved: bool = False


@dataclass(frozen=True, slots=True)
class AuthorizationDecision:
    decision: Decision
    reason: str


class DefaultDenyPolicy:
    def authorize(self, request: AuthorizationRequest) -> AuthorizationDecision:
        if request.explicitly_approved and request.action.strip() and request.resource.strip():
            return AuthorizationDecision(Decision.ALLOW, "Explicit approval supplied")
        return AuthorizationDecision(Decision.DENY, "Default-deny: explicit approval required")
