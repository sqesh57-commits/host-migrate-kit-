from __future__ import annotations

import argparse
import json
from pathlib import Path

from .collectors.host import collect_host_inventory, collect_host_summary
from .bundle import build_bundle_layout
from .gapcheck import run_gap_check
from .compat import run_compat_check
from .manifest import build_manifest
from .preflight import run_preflight
from .schema import validate_manifest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="hmk",
        description="host-migrate-kit: аудит и inventory для Debian-oriented VPS",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    audit = sub.add_parser("audit", help="Собрать краткий аудит хоста")
    audit.add_argument("--json", action="store_true", help="Вывести JSON вместо текста")

    inventory = sub.add_parser("inventory", help="Собрать структурированный inventory")
    inventory.add_argument(
        "--output",
        type=Path,
        help="Путь для сохранения inventory JSON",
    )
    inventory.add_argument("--pretty", action="store_true", help="Форматировать JSON с отступами")

    manifest = sub.add_parser("manifest", help="Собрать краткий manifest хоста")
    manifest.add_argument(
        "--output",
        type=Path,
        help="Путь для сохранения manifest JSON",
    )
    manifest.add_argument("--pretty", action="store_true", help="Форматировать JSON с отступами")

    bundle = sub.add_parser("bundle-plan", help="Собрать dry-run layout будущего relocation bundle")
    bundle.add_argument(
        "--output-dir",
        type=Path,
        default=Path("./dist"),
        help="Каталог для генерации dry-run bundle layout",
    )
    bundle.add_argument("--pretty", action="store_true", help="Форматировать JSON с отступами")

    gap = sub.add_parser("gap-check", help="Проверить явные пробелы перед bundle/migration этапом")
    gap.add_argument("--pretty", action="store_true", help="Форматировать JSON с отступами")

    validate = sub.add_parser("validate-manifest", help="Проверить структуру текущего manifest")
    validate.add_argument("--pretty", action="store_true", help="Форматировать JSON с отступами")

    preflight = sub.add_parser("preflight", help="Проверить runtime-совместимость хоста для восстановления")
    preflight.add_argument("--pretty", action="store_true", help="Форматировать JSON с отступами")

    compat = sub.add_parser("compat-check", help="Сверить target runtime с ролями и ожиданиями manifest")
    compat.add_argument("--pretty", action="store_true", help="Форматировать JSON с отступами")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "audit":
        summary = collect_host_summary()
        if args.json:
            print(json.dumps(summary, ensure_ascii=False, indent=2))
        else:
            print(render_summary(summary))
        return 0

    if args.command == "inventory":
        inventory = collect_host_inventory()
        text = json.dumps(inventory, ensure_ascii=False, indent=2 if args.pretty else None)
        if args.output:
            args.output.write_text(text + "\n", encoding="utf-8")
        else:
            print(text)
        return 0

    if args.command == "manifest":
        manifest = build_manifest()
        text = json.dumps(manifest, ensure_ascii=False, indent=2 if args.pretty else None)
        if args.output:
            args.output.write_text(text + "\n", encoding="utf-8")
        else:
            print(text)
        return 0

    if args.command == "bundle-plan":
        bundle = build_bundle_layout(args.output_dir)
        text = json.dumps(bundle, ensure_ascii=False, indent=2 if args.pretty else None)
        print(text)
        return 0

    if args.command == "gap-check":
        gap = run_gap_check()
        text = json.dumps(gap, ensure_ascii=False, indent=2 if args.pretty else None)
        print(text)
        return 0

    if args.command == "validate-manifest":
        validation = validate_manifest(build_manifest())
        text = json.dumps(validation, ensure_ascii=False, indent=2 if args.pretty else None)
        print(text)
        return 0

    if args.command == "preflight":
        report = run_preflight()
        text = json.dumps(report, ensure_ascii=False, indent=2 if args.pretty else None)
        print(text)
        return 0

    if args.command == "compat-check":
        report = run_compat_check()
        text = json.dumps(report, ensure_ascii=False, indent=2 if args.pretty else None)
        print(text)
        return 0

    parser.error("Неизвестная команда")
    return 2


def render_summary(summary: dict) -> str:
    lines = [
        "host-migrate-kit audit",
        f"Host: {summary['hostname']}",
        f"OS: {summary['os_pretty_name']}",
        f"Kernel: {summary['kernel']}",
        f"Uptime: {summary['uptime']}",
        f"Listening ports: {summary['listening_port_count']}",
        f"Running services: {summary['running_service_count']}",
        f"Enabled services: {summary['enabled_service_count']}",
        f"Cron entries: {summary['cron_entry_count']}",
        f"Docker active: {'yes' if summary['docker_active'] else 'no'}",
        f"Ollama active: {'yes' if summary['ollama_active'] else 'no'}",
    ]
    if summary.get("detected_roles"):
        lines.append("Detected roles: " + ", ".join(summary["detected_roles"]))
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())
