from __future__ import annotations

from pathlib import Path
from typing import Any

APP_PATHS = [
    Path('/home/sqesh/.openclaw'),
    Path('/home/sqesh/.openclaw/workspace'),
    Path('/opt/hiddify'),
]


def collect_app_paths() -> list[dict[str, Any]]:
    items = []
    for path in APP_PATHS:
        items.append(
            {
                'path': str(path),
                'exists': path.exists(),
                'kind': 'directory' if path.is_dir() else 'file' if path.is_file() else 'missing',
            }
        )
    return items
