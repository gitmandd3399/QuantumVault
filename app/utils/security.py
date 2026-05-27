"""
utils/security.py — re-exported from utils/__init__.py for convenience.
Import from either location:
    from utils.security import sanitize_input
    from utils import sanitize_input
"""
from utils import (  # noqa: F401  (re-export)
    sanitize_input,
    validate_alphanumeric,
    check_rate_limit,
    sha256_hex,
    sha3_256_hex,
    safe_filename,
    COPPA_NOTICE,
)

# ── Level Thresholds ──────────────────────────────────────────────────────────

LEVELS = {
    0:   "🔰 Recruit",
    50:  "🕵️ Cadet",
    150: "🔐 Agent",
    300: "⚡ Specialist",
    500: "🛡️ Cipher Corps",
    750: "🌐 Quantum Guardian",
}

def get_level(xp: int) -> str:
    """Return the rank name for a given XP total."""
    current_level = "🔰 Recruit"
    for threshold, rank in LEVELS.items():
        if xp >= threshold:
            current_level = rank
    return current_level


def get_next_level_xp(xp: int) -> int:
    """Return how many XP needed to reach the next level."""
    thresholds = sorted(LEVELS.keys())
    for threshold in thresholds:
        if xp < threshold:
            return threshold
    return thresholds[-1]


def get_level_progress(xp: int) -> float:
    """Return progress to next level as a 0.0 to 1.0 float for progress bars."""
    thresholds = sorted(LEVELS.keys())
    for i, threshold in enumerate(thresholds):
        if xp < threshold:
            prev = thresholds[i - 1] if i > 0 else 0
            progress = (xp - prev) / (threshold - prev)
            return round(min(max(progress, 0.0), 1.0), 2)
    return 0.0