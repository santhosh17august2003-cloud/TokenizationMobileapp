from __future__ import annotations

from datetime import datetime, timedelta, timezone
import hashlib
import hmac
import os
import secrets

import jwt


class AuthenticationError(Exception):
    """Raised when authentication or token creation fails."""


JWT_ALGORITHM = "HS256"
TOKEN_LIFETIME_MINUTES = 60


def _secret_key() -> str:
    secret = os.getenv("JWT_SECRET_KEY")
    if not secret:
        raise AuthenticationError("JWT_SECRET_KEY is not configured.")
    return secret


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 120_000)
    return f"{salt.hex()}:{digest.hex()}"


def verify_password(password: str, stored_hash: str) -> bool:
    try:
        salt_hex, digest_hex = stored_hash.split(":", 1)
        expected = bytes.fromhex(digest_hex)
        actual = hashlib.pbkdf2_hmac(
            "sha256", password.encode(), bytes.fromhex(salt_hex), 120_000
        )
        return hmac.compare_digest(actual, expected)
    except (ValueError, TypeError):
        return False


def create_access_token(user_id: int, email: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user_id),
        "email": email,
        "iat": now,
        "exp": now + timedelta(minutes=TOKEN_LIFETIME_MINUTES),
    }
    return jwt.encode(payload, _secret_key(), algorithm=JWT_ALGORITHM)


def verify_access_token(token: str) -> dict:
    try:
        return jwt.decode(token, _secret_key(), algorithms=[JWT_ALGORITHM])
    except jwt.PyJWTError as exc:
        raise AuthenticationError("Your session has expired. Please log in again.") from exc
