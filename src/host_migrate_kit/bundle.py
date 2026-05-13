from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path

from .manifest import build_manifest
from .report import build_human_report
from .restore import build_restore_guide
from .staging import collect_crontab, collect_safe_etc_files, collect_systemd_units, write_staging_index

DEFAULT_DIRS = [
    "/etc",
    "/home",
    "/opt",
]

DEFAULT_UNITS = [
    "ssh.service",
    "docker.service",
    "containerd.service",
    "ollama.service",
    "hiddify.service",
    "hcore.service",
]


def build_bundle_layout(output_dir: Path) -> dict:
    manifest = build_manifest()
    bundle_id = datetime.now(UTC).strftime("bundle-%Y%m%dT%H%M%SZ")
    root = output_dir / bundle_id
    (root / "manifest").mkdir(parents=True, exist_ok=True)
    (root / "configs").mkdir(parents=True, exist_ok=True)
    (root / "data").mkdir(parents=True, exist_ok=True)
    (root / "reports").mkdir(parents=True, exist_ok=True)

    manifest_path = root / "manifest" / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    included = []
    for item in DEFAULT_DIRS:
        path = Path(item)
        included.append(
            {
                "path": item,
                "exists": path.exists(),
                "kind": classify_path(path),
            }
        )

    report = {
        "bundle_id": bundle_id,
        "generated_at": datetime.now(UTC).isoformat(),
        "included_paths": included,
    }
    report_path = root / "reports" / "bundle-plan.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    human_report_path = root / "reports" / "summary.md"
    human_report_path.write_text(build_human_report(), encoding="utf-8")

    staging_dir = root / 'staging'
    systemd_info = collect_systemd_units(staging_dir / 'systemd', DEFAULT_UNITS)
    crontab_info = collect_crontab(staging_dir / 'cron')
    etc_info = collect_safe_etc_files(staging_dir / 'etc')
    restore_guide_path = root / 'reports' / 'restore-guide.md'
    restore_guide_path.write_text(build_restore_guide(), encoding='utf-8')
    staging_index_path = write_staging_index(
        staging_dir,
        {
            'systemd_units': systemd_info,
            'crontab': crontab_info,
            'safe_etc_files': etc_info,
        },
    )

    checksums = {
        "manifest/manifest.json": sha256_file(manifest_path),
        "reports/bundle-plan.json": sha256_file(report_path),
        "reports/summary.md": sha256_file(human_report_path),
        "reports/restore-guide.md": sha256_file(restore_guide_path),
        "staging/staging-index.json": sha256_file(staging_index_path),
    }
    checksum_path = root / "manifest" / "checksums.json"
    checksum_path.write_text(json.dumps(checksums, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    return {
        "bundle_id": bundle_id,
        "root": str(root),
        "manifest_path": str(manifest_path),
        "report_path": str(report_path),
        "checksum_path": str(checksum_path),
        "human_report_path": str(human_report_path),
        "staging_index_path": str(staging_index_path),
        "restore_guide_path": str(restore_guide_path),
        "included_paths": included,
    }


def classify_path(path: Path) -> str:
    if not path.exists():
        return "missing"
    if path.is_dir():
        return "directory"
    if path.is_file():
        return "file"
    return "other"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        while chunk := fh.read(65536):
            digest.update(chunk)
    return digest.hexdigest()
