from __future__ import annotations

from datetime import UTC, datetime

from .apps import collect_app_paths
from .classification import build_data_classification
from .collectors.host import collect_host_inventory
from .collectors.paths import collect_path_metadata
from .gapcheck import run_gap_check
from .policy import build_capture_policy
from .servicemap import build_service_to_data_map


def build_manifest() -> dict:
    inventory = collect_host_inventory()
    gap_check = run_gap_check()
    return {
        "manifest_version": 1,
        "generated_at": datetime.now(UTC).isoformat(),
        "host": inventory["host"],
        "roles": inventory["roles"],
        "components": {
            "services": {
                "running_count": len(inventory["services"]["running"]),
                "enabled_count": len(inventory["services"]["enabled"]),
            },
            "network": {
                "listening_count": len(inventory["network"]["listening"]),
            },
            "automation": {
                "cron_count": len(inventory["automation"]["crontab"]),
                "timer_count": len(inventory["automation"]["timers"]),
            },
            "storage": {
                "filesystem_count": len(inventory["storage"]["filesystems"]),
            },
            "packages": {
                "manual_apt_count": len(inventory["packages"]["manual_apt"]),
            },
        },
        "runtime": inventory["runtime"],
        "paths": collect_path_metadata(),
        "apps": collect_app_paths(),
        "capture_policy": build_capture_policy(),
        "data_classification": build_data_classification(),
        "service_to_data_map": build_service_to_data_map(),
        "checks": inventory["checks"],
        "gap_check": gap_check,
        "warnings": [gap["code"] for gap in gap_check["gaps"]],
    }
