def get_value(d: dict, key: str) -> str:
    """Return stripped value for key, or empty string if not found."""
    value = d.get(key)
    return value.strip()
