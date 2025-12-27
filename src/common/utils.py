import re
from pathlib import Path


def bool_to_str(value, default=False):
    if value is None:
        return "true" if default else "false"
    return "true" if bool(value) else "false"


def ensure_time_unit(value: str, default_unit: str = "s") -> str:
    value = str(value)
    return value if re.search(r"[A-Za-z]", value) else value + default_unit


def like_path(s: str) -> bool:
    try:
        Path(s)
        return True
    except Exception:
        return False
