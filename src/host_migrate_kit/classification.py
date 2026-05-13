from __future__ import annotations

from typing import Any


def build_data_classification() -> dict[str, Any]:
    return {
        'must-backup': [
            '/etc/systemd/system',
            '/home/sqesh/.openclaw',
            '/opt/hiddify',
            'user crontab',
            'ssh host keys and access secrets',
            'stateful app data',
        ],
        'restore-required': [
            '/home/sqesh/.openclaw/workspace',
            'safe /etc files',
            'systemd drop-ins',
            'safe app files',
        ],
        'rebuildable': [
            'manual apt package list',
            'inventory JSON',
            'manifest JSON',
        ],
        'ignore': [
            'temporary files',
            'cache-like artifacts',
            'ad-hoc noise files',
        ],
    }
