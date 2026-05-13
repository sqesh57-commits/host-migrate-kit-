from __future__ import annotations

from pathlib import Path
from typing import Any

EXPECTED_REPORTS = [
    'manifest/manifest.json',
    'manifest/checksums.json',
    'reports/bundle-plan.json',
    'reports/summary.md',
    'reports/restore-guide.md',
    'staging/staging-index.json',
]


def run_bundle_verify(bundle_root: str) -> dict[str, Any]:
    root = Path(bundle_root)
    missing = []
    for rel in EXPECTED_REPORTS:
        if not (root / rel).exists():
            missing.append(rel)

    status = 'ok' if not missing else 'attention'
    return {
        'status': status,
        'missing_count': len(missing),
        'missing': missing,
    }
