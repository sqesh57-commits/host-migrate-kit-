from __future__ import annotations

from datetime import UTC, datetime

from .collectors.host import collect_host_inventory
from .gapcheck import run_gap_check


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
        "checks": inventory["checks"],
        "gap_check": gap_check,
        "warnings": [gap["code"] for gap in gap_check["gaps"]],
    }
