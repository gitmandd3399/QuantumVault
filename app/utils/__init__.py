"""
utils/security.py
─────────────────
Centralised security helpers for QuantumVault Academy.

Functions here are intentionally defensive-by-default:
  - All user-facing text is sanitised before rendering or storage.
  - No eval(), exec(), or pickle on user data — ever.
  - Rate-limit counters live in Streamlit session state (no server state needed
    for a single-user Streamlit app; swap to Redis for multi-user deployments).
"""

from __future__ import annotations

import hashlib
import html
import re
import time
from typing import Any

# Optional: install with  pip install bleach
try:
    import bleach  # type: ignore

    _BLEACH_AVAILABLE = True
except ImportError:
    _BLEACH_AVAILABLE = False


# ── Constants ─────────────────────────────────────────────────────────────────
MAX_INPUT_LENGTH = 512          # chars; reject anything longer
RATE_LIMIT_WINDOW = 60          # seconds
RATE_LIMIT_MAX_CALLS = 30       # per window per session


# ── Input sanitisation ────────────────────────────────────────────────────────

def sanitize_input(text: Any, max_length: int = MAX_INPUT_LENGTH) -> str:
    """
    Sanitise arbitrary user input.

    1. Coerce to str.
    2. Truncate to max_length.
    3. Strip all HTML tags (via bleach if available, else regex fallback).
    4. Escape HTML entities.
    5. Strip control characters.

    Returns a safe string safe to display or store.
    """
    if not isinstance(text, str):
        text = str(text)

    # Truncate
    text = text[:max_length]

    # Strip HTML tags
    if _BLEACH_AVAILABLE:
        text = bleach.clean(text, tags=[], attributes={}, strip=True)
    else:
        text = re.sub(r"<[^>]*>", "", text)

    # Escape remaining HTML entities
    text = html.escape(text)

    # Remove ASCII control characters (except tab/newline which are harmless)
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", text)

    return text.strip()


def validate_alphanumeric(text: str, allow_spaces: bool = False) -> bool:
    """Return True only if text contains letters, digits, and optionally spaces."""
    pattern = r"^[a-zA-Z0-9 ]+$" if allow_spaces else r"^[a-zA-Z0-9]+$"
    return bool(re.match(pattern, text))


# ── Rate limiting (session-scoped) ────────────────────────────────────────────

def check_rate_limit(key: str, session_state: dict) -> bool:
    """
    Simple in-session rate limiter.

    Args:
        key: Identifier for the action (e.g. "quiz_submit").
        session_state: Streamlit st.session_state dict.

    Returns:
        True  → request is allowed.
        False → rate limit exceeded; caller should show a warning.
    """
    rl_key = f"_rl_{key}"
    now = time.time()

    if rl_key not in session_state:
        session_state[rl_key] = {"count": 0, "window_start": now}

    bucket = session_state[rl_key]

    # Reset window if expired
    if now - bucket["window_start"] > RATE_LIMIT_WINDOW:
        bucket["count"] = 0
        bucket["window_start"] = now

    if bucket["count"] >= RATE_LIMIT_MAX_CALLS:
        return False

    bucket["count"] += 1
    return True


# ── Safe hashing helpers (for demo purposes in the app) ──────────────────────

def sha256_hex(data: str) -> str:
    """Return hex-encoded SHA-256 of the input string. Safe to call on user data."""
    return hashlib.sha256(sanitize_input(data).encode()).hexdigest()


def sha3_256_hex(data: str) -> str:
    """Return hex-encoded SHA3-256 — used in PQC schemes."""
    return hashlib.sha3_256(sanitize_input(data).encode()).hexdigest()


# ── Content Security helpers ──────────────────────────────────────────────────

def safe_filename(name: str) -> str:
    """
    Convert a user-supplied string into a filesystem-safe filename.
    Strips everything except alphanumerics, hyphens, underscores, dots.
    """
    name = sanitize_input(name, max_length=64)
    return re.sub(r"[^\w\-.]", "_", name)


# ── COPPA reminder ────────────────────────────────────────────────────────────

COPPA_NOTICE = (
    "QuantumVault Academy does not collect, store, or share personal information "
    "from users under 13 years of age, in compliance with COPPA. "
    "No account creation is required to use any learning module."
)
