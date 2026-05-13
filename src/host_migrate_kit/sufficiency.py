from __future__ import annotations

from .manifest import build_manifest


def run_sufficiency_check() -> dict:
    manifest = build_manifest()
    checks = []
    blocking_issues = []

    has_map = bool(manifest.get('service_to_data_map'))
    checks.append({'name': 'service_map', 'status': 'ok' if has_map else 'fail'})
    if not has_map:
        blocking_issues.append('service_to_data_map is empty')

    has_must_backup = bool(manifest.get('data_classification', {}).get('must-backup'))
    checks.append({'name': 'must_backup_class', 'status': 'ok' if has_must_backup else 'fail'})
    if not has_must_backup:
        blocking_issues.append('must-backup class is empty')

    has_capture_policy = bool(manifest.get('capture_policy'))
    checks.append({'name': 'capture_policy', 'status': 'ok' if has_capture_policy else 'fail'})
    if not has_capture_policy:
        blocking_issues.append('capture_policy is empty')

    has_paths = bool(manifest.get('paths'))
    checks.append({'name': 'path_metadata', 'status': 'ok' if has_paths else 'warn'})

    has_apps = bool(manifest.get('apps'))
    checks.append({'name': 'app_paths', 'status': 'ok' if has_apps else 'warn'})

    if blocking_issues:
        status = 'FAIL'
        summary = 'Backup недостаточен: не хватает обязательных слоёв модели.'
        next_action = 'Добить service/data map и обязательную классификацию backup-слоя.'
    else:
        status = 'PASS'
        summary = 'Базовый backup-readiness слой присутствует.'
        next_action = 'Расширять data coverage и усиливать restore sufficiency.'

    return {
        'status': status,
        'summary': summary,
        'checks': checks,
        'blocking_issues': blocking_issues,
        'next_action': next_action,
    }
