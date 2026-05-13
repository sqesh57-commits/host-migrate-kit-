from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

SYSTEMD_DIRS = [
    Path('/etc/systemd/system'),
    Path('/lib/systemd/system'),
]

SAFE_ETC_FILES = [
    Path('/etc/os-release'),
    Path('/etc/hostname'),
    Path('/etc/hosts'),
    Path('/etc/resolv.conf'),
]


def collect_systemd_units(target_dir: Path, unit_names: list[str]) -> list[dict[str, Any]]:
    target_dir.mkdir(parents=True, exist_ok=True)
    copied = []
    for unit in unit_names:
        source = find_systemd_unit(unit)
        item = {
            'unit': unit,
            'found': source is not None,
            'dropins': [],
        }
        if source is None:
            copied.append(item)
            continue
        dest = target_dir / unit
        shutil.copy2(source, dest)
        item['source'] = str(source)
        item['dest'] = str(dest)
        item['dropins'] = collect_systemd_dropins(target_dir, unit)
        copied.append(item)
    return copied


def find_systemd_unit(name: str) -> Path | None:
    for base in SYSTEMD_DIRS:
        candidate = base / name
        if candidate.exists():
            return candidate
    return None


def collect_systemd_dropins(target_dir: Path, unit_name: str) -> list[dict[str, str]]:
    copied = []
    for base in SYSTEMD_DIRS:
        dropin_dir = base / f'{unit_name}.d'
        if not dropin_dir.exists() or not dropin_dir.is_dir():
            continue
        dest_dir = target_dir / f'{unit_name}.d'
        dest_dir.mkdir(parents=True, exist_ok=True)
        for item in sorted(dropin_dir.iterdir()):
            if not item.is_file():
                continue
            dest = dest_dir / item.name
            shutil.copy2(item, dest)
            copied.append({
                'source': str(item),
                'dest': str(dest),
            })
    return copied


def collect_crontab(target_dir: Path) -> dict[str, Any]:
    import subprocess

    target_dir.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
    dest = target_dir / 'user-crontab.txt'
    if result.returncode != 0:
        dest.write_text('', encoding='utf-8')
        return {
            'found': False,
            'dest': str(dest),
        }
    dest.write_text(result.stdout, encoding='utf-8')
    return {
        'found': True,
        'dest': str(dest),
    }


def collect_safe_etc_files(target_dir: Path) -> list[dict[str, Any]]:
    target_dir.mkdir(parents=True, exist_ok=True)
    copied = []
    for source in SAFE_ETC_FILES:
        item = {
            'path': str(source),
            'found': source.exists(),
        }
        if source.exists():
            dest = target_dir / source.name
            shutil.copy2(source, dest)
            item['dest'] = str(dest)
        copied.append(item)
    return copied


def write_staging_index(target_dir: Path, payload: dict[str, Any]) -> Path:
    path = target_dir / 'staging-index.json'
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return path
