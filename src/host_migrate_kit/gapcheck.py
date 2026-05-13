from __future__ import annotations

from .collectors.host import collect_host_inventory


def run_gap_check() -> dict:
    inventory = collect_host_inventory()
    gaps: list[dict[str, str]] = []

    if not inventory['runtime']['binaries'].get('python3', False):
        gaps.append({
            'severity': 'critical',
            'code': 'missing-python3',
            'message': 'На хосте не найден python3, инструмент не сможет штатно работать.',
        })

    if not inventory['runtime']['binaries'].get('systemctl', False):
        gaps.append({
            'severity': 'warn',
            'code': 'missing-systemctl',
            'message': 'systemctl отсутствует, systemd inventory будет неполным.',
        })

    if not inventory['runtime']['ssh']['active']:
        gaps.append({
            'severity': 'warn',
            'code': 'ssh-inactive',
            'message': 'SSH не активен, удалённое администрирование может быть неготово к миграции.',
        })

    if not inventory['automation']['crontab'] and not inventory['automation']['timers']:
        gaps.append({
            'severity': 'info',
            'code': 'no-automation-detected',
            'message': 'Не найдены cron jobs и timers, automation-слой может отсутствовать или ещё не покрыт.',
        })

    if not inventory['services']['running']:
        gaps.append({
            'severity': 'warn',
            'code': 'no-running-services',
            'message': 'Не найдено запущенных сервисов, это необычно для VPS под миграцию.',
        })

    if not inventory['storage']['filesystems']:
        gaps.append({
            'severity': 'warn',
            'code': 'no-filesystem-data',
            'message': 'Не удалось собрать данные о файловых системах.',
        })

    if inventory['checks'].get('docker_active') and not inventory['runtime']['binaries'].get('docker', False):
        gaps.append({
            'severity': 'warn',
            'code': 'docker-service-without-cli',
            'message': 'Docker service активен, но docker CLI не найден в PATH.',
        })

    return {
        'status': 'ok' if not [g for g in gaps if g['severity'] in {'critical', 'warn'}] else 'attention',
        'gap_count': len(gaps),
        'gaps': gaps,
    }
