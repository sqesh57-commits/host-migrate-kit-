from __future__ import annotations

from .manifest import build_manifest
from .preflight import run_preflight

ROLE_EXPECTATIONS = {
    'docker-host': ['docker'],
    'llm-host': ['python3'],
    'proxy-host': ['systemctl'],
    'automation-host': ['python3'],
}


def run_compat_check() -> dict:
    manifest = build_manifest()
    preflight = run_preflight()
    issues = []

    required = preflight['required_commands']
    recommended = preflight['recommended_commands']

    for role in manifest['roles']:
        expected = ROLE_EXPECTATIONS.get(role, [])
        for binary in expected:
            available = required.get(binary) if binary in required else recommended.get(binary)
            if not available:
                issues.append({
                    'severity': 'warn',
                    'code': f'missing-binary-for-role-{role}-{binary}',
                    'message': f'Для роли {role} не хватает ожидаемой команды {binary}.',
                })

    if manifest['checks'].get('docker_active') and not recommended.get('systemctl', False):
        issues.append({
            'severity': 'warn',
            'code': 'docker-without-systemctl',
            'message': 'Manifest указывает на docker-active, но на target хосте нет systemctl.',
        })

    if manifest['checks'].get('hiddify_active') and not recommended.get('iptables-save', False):
        issues.append({
            'severity': 'warn',
            'code': 'proxy-without-iptables-tooling',
            'message': 'Для proxy-host не найден iptables-save, сетевой restore может быть неполным.',
        })

    return {
        'status': 'ok' if not issues else 'attention',
        'issue_count': len(issues),
        'issues': issues,
        'roles': manifest['roles'],
    }
