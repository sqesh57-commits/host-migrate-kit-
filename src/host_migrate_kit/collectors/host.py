from __future__ import annotations

import platform
import socket
import subprocess
from pathlib import Path

from .runtime import parse_failed_units, parse_logged_users, parse_passwd_users, parse_ssh_status
from .system import detect_binaries, parse_apt_manual, parse_df, parse_timers


def run(command: list[str]) -> str:
    try:
        result = subprocess.run(command, check=False, capture_output=True, text=True)
    except FileNotFoundError:
        return ""
    return result.stdout.strip()


def read_os_release() -> dict[str, str]:
    data: dict[str, str] = {}
    path = Path("/etc/os-release")
    if not path.exists():
        return data
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line or "=" not in line:
            continue
        key, value = line.split("=", 1)
        data[key] = value.strip().strip('"')
    return data


def parse_ss_listening() -> list[dict[str, str]]:
    output = run(["ss", "-ltnup"])
    lines = output.splitlines()
    if len(lines) <= 1:
        return []
    items: list[dict[str, str]] = []
    for line in lines[1:]:
        parts = line.split()
        if len(parts) < 5:
            continue
        items.append(
            {
                "netid": parts[0],
                "state": parts[1],
                "local_address": parts[4],
                "process": " ".join(parts[6:]) if len(parts) > 6 else "",
            }
        )
    return items


def parse_systemd_services(state: str) -> list[str]:
    output = run(
        [
            "systemctl",
            "list-unit-files" if state == "enabled" else "list-units",
            "--type=service",
            "--state=" + state,
            "--no-pager",
            "--no-legend",
        ]
    )
    services = []
    for line in output.splitlines():
        if not line.strip():
            continue
        services.append(line.split()[0])
    return services


def parse_running_services() -> list[str]:
    output = run(["systemctl", "list-units", "--type=service", "--state=running", "--no-pager", "--no-legend"])
    services = []
    for line in output.splitlines():
        if not line.strip():
            continue
        services.append(line.split()[0])
    return services


def parse_crontab() -> list[str]:
    output = run(["crontab", "-l"])
    entries = []
    for line in output.splitlines():
        striped = line.strip()
        if not striped or striped.startswith("#"):
            continue
        entries.append(striped)
    return entries


def service_is_active(name: str) -> bool:
    result = subprocess.run(["systemctl", "is-active", name], capture_output=True, text=True)
    return result.returncode == 0


def detect_roles(running_services: list[str]) -> list[str]:
    roles = []
    joined = " ".join(running_services)
    if "docker.service" in joined or "containerd.service" in joined:
        roles.append("docker-host")
    if "ollama.service" in joined:
        roles.append("llm-host")
    if "hiddify.service" in joined or "hcore.service" in joined:
        roles.append("proxy-host")
    if parse_crontab():
        roles.append("automation-host")
    return roles


def collect_host_summary() -> dict:
    os_release = read_os_release()
    running_services = parse_running_services()
    enabled_services = parse_systemd_services("enabled")
    listening = parse_ss_listening()
    cron_entries = parse_crontab()

    return {
        "hostname": socket.gethostname(),
        "os_pretty_name": os_release.get("PRETTY_NAME", "unknown"),
        "kernel": platform.release(),
        "uptime": run(["uptime", "-p"]) or run(["uptime"]),
        "listening_port_count": len(listening),
        "running_service_count": len(running_services),
        "enabled_service_count": len(enabled_services),
        "cron_entry_count": len(cron_entries),
        "docker_active": service_is_active("docker.service"),
        "ollama_active": service_is_active("ollama.service"),
        "detected_roles": detect_roles(running_services),
    }


def collect_host_inventory() -> dict:
    os_release = read_os_release()
    running_services = parse_running_services()
    enabled_services = parse_systemd_services("enabled")
    listening = parse_ss_listening()
    cron_entries = parse_crontab()

    return {
        "schema_version": 1,
        "host": {
            "hostname": socket.gethostname(),
            "kernel": platform.release(),
            "os_release": os_release,
        },
        "services": {
            "running": running_services,
            "enabled": enabled_services,
        },
        "network": {
            "listening": listening,
        },
        "automation": {
            "crontab": cron_entries,
            "timers": parse_timers(),
        },
        "storage": {
            "filesystems": parse_df(),
        },
        "packages": {
            "manual_apt": parse_apt_manual(),
        },
        "runtime": {
            "binaries": detect_binaries(),
            "logged_users": parse_logged_users(),
            "local_users": parse_passwd_users(),
            "failed_units": parse_failed_units(),
            "ssh": parse_ssh_status(),
        },
        "roles": detect_roles(running_services),
        "checks": {
            "docker_active": service_is_active("docker.service"),
            "ollama_active": service_is_active("ollama.service"),
            "hiddify_active": service_is_active("hiddify.service"),
        },
    }
