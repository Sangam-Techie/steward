"""Security utilities for token creation and hashing.

Provides helpers for issuing signed device tokens and computing
deterministic hashes of tokens for storage or lookup.
"""

import datetime
import hashlib

import jwt

from .config import settings


def create_device_token(device_id: str, platform: str) -> str:
    """Create a signed JWT for a device that expires after 365 days."""
    payload = {
        "device_id": device_id,
        "platform": platform,
        "exp": datetime.datetime.now(datetime.timezone.utc)
        + datetime.timedelta(days=365),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm="HS256")


def hash_token(token: str) -> str:
    """Return the SHA-256 hex digest of the given token."""
    return hashlib.sha256(token.encode("utf-8")).hexdigest()
