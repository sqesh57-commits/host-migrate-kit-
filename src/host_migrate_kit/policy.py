from __future__ import annotations

from typing import Any

SAFE_CAPTURE_POLICY = {
    'systemd_units': {
        'what': 'unit files и drop-ins для curated списка сервисов',
        'class': 'config',
        'required_for_mvp': True,
    },
    'crontab': {
        'what': 'user crontab исходного хоста',
        'class': 'automation',
        'required_for_mvp': True,
    },
    'safe_etc_files': {
        'what': 'ограниченный curated набор файлов из /etc',
        'class': 'config',
        'required_for_mvp': True,
    },
    'safe_app_files': {
        'what': 'критичные app-level config files',
        'class': 'app-config',
        'required_for_mvp': True,
    },
}


def build_capture_policy() -> dict[str, Any]:
    return SAFE_CAPTURE_POLICY
