from __future__ import annotations

from typing import Any

REQUIRED_MANIFEST_KEYS = {
    'manifest_version',
    'generated_at',
    'host',
    'roles',
    'components',
    'runtime',
    'paths',
    'checks',
    'gap_check',
    'warnings',
}


def validate_manifest(manifest: dict[str, Any]) -> dict[str, Any]:
    missing = sorted(REQUIRED_MANIFEST_KEYS - set(manifest.keys()))
    issues = []
    if missing:
        issues.append({
            'severity': 'critical',
            'code': 'missing-required-keys',
            'message': f"В manifest отсутствуют обязательные ключи: {', '.join(missing)}",
        })

    host = manifest.get('host', {})
    if not host.get('hostname'):
        issues.append({
            'severity': 'warn',
            'code': 'missing-hostname',
            'message': 'В manifest не указан hostname.',
        })

    if not isinstance(manifest.get('roles', []), list):
        issues.append({
            'severity': 'warn',
            'code': 'roles-not-list',
            'message': 'Поле roles должно быть списком.',
        })

    return {
        'status': 'ok' if not issues else 'attention',
        'issue_count': len(issues),
        'issues': issues,
    }
