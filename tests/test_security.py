import pytest

from cortana.governance.policy import AuthorizationRequest, Decision, DefaultDenyPolicy
from cortana.memory.encryption import decrypt, encrypt


def test_default_deny_policy():
    policy = DefaultDenyPolicy()
    denied = policy.authorize(AuthorizationRequest("run", "process"))
    allowed = policy.authorize(AuthorizationRequest("run", "process", True))
    assert denied.decision is Decision.DENY
    assert allowed.decision is Decision.ALLOW


def test_aes_gcm_round_trip_and_tamper_detection():
    pytest.importorskip("cryptography")
    key = b"k" * 32
    envelope = encrypt(b"private-memory", key)
    assert decrypt(envelope, key) == b"private-memory"
    damaged = envelope[:-1] + bytes([envelope[-1] ^ 1])
    with pytest.raises(Exception):
        decrypt(damaged, key)
