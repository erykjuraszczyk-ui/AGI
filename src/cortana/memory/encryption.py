"""Authenticated encryption helper. Key lifecycle is intentionally external."""
from __future__ import annotations

import os


class EncryptionUnavailable(RuntimeError):
    pass


def encrypt(plaintext: bytes, key: bytes) -> bytes:
    """Encrypt bytes with AES-256-GCM; output is nonce || ciphertext+tag."""
    if len(key) != 32:
        raise ValueError("AES-256-GCM requires a 32-byte key")
    try:
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    except ImportError as exc:
        raise EncryptionUnavailable("Install the 'crypto' extra to use encryption") from exc
    nonce = os.urandom(12)
    return nonce + AESGCM(key).encrypt(nonce, plaintext, None)


def decrypt(envelope: bytes, key: bytes) -> bytes:
    if len(key) != 32:
        raise ValueError("AES-256-GCM requires a 32-byte key")
    if len(envelope) < 28:
        raise ValueError("Encrypted envelope is too short")
    try:
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    except ImportError as exc:
        raise EncryptionUnavailable("Install the 'crypto' extra to use encryption") from exc
    return AESGCM(key).decrypt(envelope[:12], envelope[12:], None)
