from __future__ import annotations

import shutil
import subprocess
from typing import Any


def run(command: list[str]) -> str:
    try:
        result = subprocess.run(command, check=False, capture_output=True, text=True)
    except FileNotFoundError:
        return ""
    return result.stdout.strip()


def parse_timers() -> list[dict[str, str]]:
    output = run(["systemctl", "list-timers", "--all", "--no-pager", "--no-legend"])
    timers: list[dict[str, str]] = []
    for line in output.splitlines():
        parts = line.split()
        if len(parts) < 6:
            continue
        timers.append(
            {
                "next": " ".join(parts[0:5]),
                "left": parts[5],
                "unit": parts[-2] if len(parts) >= 2 else "",
                "activates": parts[-1] if len(parts) >= 1 else "",
            }
        )
    return timers


def parse_df() -> list[dict[str, Any]]:
    output = run(["df", "-h"])
    rows = []
    lines = output.splitlines()
    if len(lines) <= 1:
        return rows
    for line in lines[1:]:
        parts = line.split()
        if len(parts) < 6:
            continue
        rows.append(
            {
                "filesystem": parts[0],
                "size": parts[1],
                "used": parts[2],
                "available": parts[3],
                "use_percent": parts[4],
                "mountpoint": parts[5],
            }
        )
    return rows


def parse_apt_manual() -> list[str]:
    return [line.strip() for line in run(["apt-mark", "showmanual"]).splitlines() if line.strip()]


def detect_binaries() -> dict[str, bool]:
    names = ["python3", "systemctl", "ss", "docker", "ollama", "iptables-save", "nft"]
    return {name: shutil.which(name) is not None for name in names}
