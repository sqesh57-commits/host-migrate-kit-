from __future__ import annotations

import shutil
import subprocess
from typing import Any

REQUIRED_COMMANDS = ['python3', 'tar', 'git', 'ssh']
RECOMMENDED_COMMANDS = ['systemctl', 'ss', 'iptables-save', 'nft']
REQUIRED_PACKAGES_HINTS = ['python3-venv']


def command_exists(name: str) -> bool:
    return shutil.which(name) is not None


def systemctl_active(unit: str) -> bool:
    return subprocess.run(['systemctl', 'is-active', unit], capture_output=True).returncode == 0


def run_preflight() -> dict[str, Any]:
    required = {name: command_exists(name) for name in REQUIRED_COMMANDS}
    recommended = {name: command_exists(name) for name in RECOMMENDED_COMMANDS}

    issues = []
    for name, ok in required.items():
        if not ok:
            issues.append({
                'severity': 'critical',
                'code': f'missing-command-{name}',
                'message': f'Не найдена обязательная команда: {name}',
            })

    if not command_exists('python3'):
        issues.append({
            'severity': 'critical',
            'code': 'missing-python-runtime',
            'message': 'Отсутствует python3 runtime для запуска recovery tooling.',
        })

    if not command_exists('systemctl'):
        issues.append({
            'severity': 'warn',
            'code': 'missing-systemctl-runtime',
            'message': 'systemctl недоступен, systemd-совместимость среды ограничена.',
        })

    if not systemctl_active('ssh.service'):
        issues.append({
            'severity': 'warn',
            'code': 'ssh-not-active',
            'message': 'SSH не активен, удалённое сопровождение target VPS под вопросом.',
        })

    return {
        'status': 'ok' if not issues else 'attention',
        'required_commands': required,
        'recommended_commands': recommended,
        'package_hints': REQUIRED_PACKAGES_HINTS,
        'issue_count': len(issues),
        'issues': issues,
    }
