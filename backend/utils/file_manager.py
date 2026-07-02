from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def absolute_path(relative_path: str) -> Path:
    """
    Convert relative path stored in metadata
    into absolute filesystem path.
    """

    return PROJECT_ROOT / relative_path