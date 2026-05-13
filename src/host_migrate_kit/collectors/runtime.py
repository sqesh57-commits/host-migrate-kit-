from __future__ import annotations

import pwd
import subprocess
from typing import Any


def run(command: list[str]) -> str:
    try:
        result = subprocess.run(command, check=False, capture_output=True, text=True)
    except FileNotFoundError:
        return ""
    return result.stdout.strip()


def parse_failed_units() -> list[str]:
    output = run(["systemctl", "--failed", "--no-pager", "--no-legend"])
    items = []
    for line in output.splitlines():
        if not line.strip():
            continue
        items.append(line.split()[0])
    return items


def parse_logged_users() -> list[dict[str, str]]:
    output = run(["who"])
    users = []
    for line in output.splitlines():
        parts = line.split()
        if len(parts) < 5:
            continue
        users.append(
            {
                "user": parts[0],
                "tty": parts[1],
                "date": parts[2],
                "time": parts[3],
                "from": parts[4].strip('()'),
            }
        )
    return users


def parse_passwd_users(min_uid: int = 1000) -> list[dict[str, Any]]:
    users = []
    for entry in pwd.getpwall():
        if entry.pw_uid < min_uid:
            continue
        users.append(
            {
                "name": entry.pw_name,
                "uid": entry.pw_uid,
                "gid": entry.pw_gid,
                "home": entry.pw_dir,
                "shell": entry.pw_shell,
            }
        )
    return users


def parse_ssh_status() -> dict[str, Any]:
    return {
        "active": subprocess.run(["systemctl", "is-active", "ssh.service"], capture_output=True).returncode == 0,
        "enabled": subprocess.run(["systemctl", "is-enabled", "ssh.service"], capture_output=True).returncode == 0,
        "config_present": True,
    }
