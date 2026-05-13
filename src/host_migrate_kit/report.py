from __future__ import annotations

from .manifest import build_manifest


def build_human_report() -> str:
    manifest = build_manifest()
    lines = [
        '# host-migrate-kit report',
        '',
        f"Хост: {manifest['host']['hostname']}",
        f"ОС: {manifest['host']['os_release'].get('PRETTY_NAME', 'unknown')}",
        f"Kernel: {manifest['host']['kernel']}",
        '',
        '## Роли хоста',
    ]
    for role in manifest['roles']:
        lines.append(f'- {role}')
    if not manifest['roles']:
        lines.append('- роли не определены')

    lines += [
        '',
        '## Ключевые компоненты',
        f"- Running services: {manifest['components']['services']['running_count']}",
        f"- Enabled services: {manifest['components']['services']['enabled_count']}",
        f"- Listening ports: {manifest['components']['network']['listening_count']}",
        f"- Cron entries: {manifest['components']['automation']['cron_count']}",
        f"- Timers: {manifest['components']['automation']['timer_count']}",
        f"- Filesystems: {manifest['components']['storage']['filesystem_count']}",
        f"- Manual apt packages: {manifest['components']['packages']['manual_apt_count']}",
        '',
        '## Пути под relocation bundle',
    ]
    for item in manifest['paths']:
        lines.append(
            f"- {item['path']}: exists={item['exists']}, kind={item.get('kind', 'unknown')}, mode={item.get('mode', '-')}, uid={item.get('owner_uid', '-')}, gid={item.get('group_gid', '-')}"
        )

    lines += [
        '',
        '## Capture policy',
    ]
    for name, item in manifest['capture_policy'].items():
        lines.append(
            f"- {name}: class={item['class']}, required_for_mvp={item['required_for_mvp']}, what={item['what']}"
        )

    lines += [
        '',
        '## Gap check',
        f"- Status: {manifest['gap_check']['status']}",
        f"- Gap count: {manifest['gap_check']['gap_count']}",
    ]

    if manifest['gap_check']['gaps']:
        for gap in manifest['gap_check']['gaps']:
            lines.append(f"- [{gap['severity']}] {gap['code']}: {gap['message']}")
    else:
        lines.append('- Явных пробелов не найдено')

    return '\n'.join(lines) + '\n'
