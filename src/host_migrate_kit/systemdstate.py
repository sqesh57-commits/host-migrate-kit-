from __future__ import annotations

import subprocess
from typing import Any

DEFAULT_UNITS = [
    'ssh.service',
    'docker.service',
    'containerd.service',
    'ollama.service',
    'hiddify.service',
    'hcore.service',
]


def run(command: list[str]) -> str:
    try:
        result = subprocess.run(command, check=False, capture_output=True, text=True)
    except FileNotFoundError:
        return ''
    return result.stdout.strip()


def unit_state(unit: str) -> dict[str, Any]:
    active = subprocess.run(['systemctl', 'is-active', unit], capture_output=True, text=True)
    enabled = subprocess.run(['systemctl', 'is-enabled', unit], capture_output=True, text=True)
    return {
        'unit': unit,
        'active': active.returncode == 0,
        'active_status': active.stdout.strip() or active.stderr.strip(),
        'enabled': enabled.returncode == 0,
        'enabled_status': enabled.stdout.strip() or enabled.stderr.strip(),
    }


def collect_systemd_state(units: list[str] | None = None) -> list[dict[str, Any]]:
    return [unit_state(unit) for unit in (units or DEFAULT_UNITS)]
