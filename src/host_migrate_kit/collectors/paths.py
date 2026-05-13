from __future__ import annotations

import os
import stat
from pathlib import Path
from typing import Any

DEFAULT_PATHS = [
    '/etc',
    '/home',
    '/opt',
]


def collect_path_metadata(paths: list[str] | None = None) -> list[dict[str, Any]]:
    items = []
    for raw in paths or DEFAULT_PATHS:
        path = Path(raw)
        item: dict[str, Any] = {
            'path': raw,
            'exists': path.exists(),
        }
        if not path.exists():
            item['kind'] = 'missing'
            items.append(item)
            continue
        st = path.stat()
        item.update(
            {
                'kind': classify_mode(st.st_mode),
                'owner_uid': st.st_uid,
                'group_gid': st.st_gid,
                'mode': oct(stat.S_IMODE(st.st_mode)),
            }
        )
        items.append(item)
    return items


def classify_mode(mode: int) -> str:
    if stat.S_ISDIR(mode):
        return 'directory'
    if stat.S_ISREG(mode):
        return 'file'
    if stat.S_ISLNK(mode):
        return 'symlink'
    return 'other'
