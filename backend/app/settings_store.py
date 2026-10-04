import time

from .db import get_connection

CACHE_SECONDS = 5  # how long a value is reused before re-reading the database
_cache: dict = {}


class SettingsError(Exception):
    """Raised when settings cannot be read from the database."""


def _fetch(key: str):
    with get_connection() as conn:
        row = conn.execute(
            "SELECT value FROM app_settings WHERE key = %s", (key,)
        ).fetchone()
    if row is None:
        raise SettingsError(f"Setting '{key}' is missing in the database.")
    return row[0]


def get_setting(key: str):
    """Read a setting from PostgreSQL, with a short cache."""
    now = time.monotonic()
    hit = _cache.get(key)
    if hit and now - hit[0] < CACHE_SECONDS:
        return hit[1]

    try:
        value = _fetch(key)
    except SettingsError:
        raise
    except Exception:
        if hit:
            return hit[1]  # database briefly unavailable: use last known value
        raise SettingsError("The configuration database is unavailable.")

    _cache[key] = (now, value)
    return value


def get_model_config() -> dict:
    return get_setting("model_config")


def get_system_prompt() -> str:
    return get_setting("system_prompt")