from __future__ import annotations

from pathlib import Path
from typing import Any


def build_apply_plan(bundle_root: str) -> dict[str, Any]:
    root = Path(bundle_root)
    steps = []

    systemd_dir = root / 'staging' / 'systemd'
    cron_file = root / 'staging' / 'cron' / 'user-crontab.txt'
    etc_dir = root / 'staging' / 'etc'

    if systemd_dir.exists():
        units = sorted([p.name for p in systemd_dir.iterdir() if p.is_file()])
        steps.append({
            'step': 'restore-systemd-units',
            'status': 'planned',
            'details': units,
        })
        steps.append({
            'step': 'systemd-daemon-reload',
            'status': 'planned',
            'details': ['systemctl daemon-reload'],
        })

    if cron_file.exists():
        steps.append({
            'step': 'review-crontab',
            'status': 'planned',
            'details': [str(cron_file)],
        })

    if etc_dir.exists():
        files = sorted([p.name for p in etc_dir.iterdir() if p.is_file()])
        steps.append({
            'step': 'review-safe-etc-files',
            'status': 'planned',
            'details': files,
        })

    steps.append({
        'step': 'post-restore-preflight',
        'status': 'planned',
        'details': ['hmk preflight', 'hmk gap-check', 'hmk compat-check'],
    })

    return {
        'bundle_root': str(root),
        'step_count': len(steps),
        'steps': steps,
    }
