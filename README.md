# host-migrate-kit-

Portable toolkit for auditing a Debian-oriented VPS, collecting critical configuration and data, and preparing a relocation bundle for fast recovery on a clean host.

## Goal

Preserve critical data and configuration for backup and fast redeployment on another VPS with a clean Debian-oriented system.

## Why this exists

Typical VPS backups solve only part of the problem:
- snapshots are fast but often not portable across providers
- raw file backups miss service topology and restore order
- mixed hosts with systemd services, Docker workloads, cron jobs, and custom app state need more than a tarball

`host-migrate-kit-` is meant to provide a practical middle path:
- inspect what is really running
- capture critical state in a structured way
- generate a relocation bundle with machine-readable manifest and human-readable restore notes
- help validate migration readiness before and after a move

## Scope

Debian-oriented systems first:
- Debian 12+
- Ubuntu and similar systemd-based derivatives later, where compatible

Primary workload types:
- systemd-managed services
- Docker and Docker Compose workloads
- cron jobs and timers
- host-level application state
- network and firewall state
- custom directories such as `/opt/...`, app data, and user-owned config

## MVP

- host audit
- inventory
- relocation bundle
- backup strategy
- restore guide
- Docker volume support
- systemd export
- manifest generation
- migration checks

## Design principles

- Debian-first, not universal-Linux-first
- portability over provider-specific snapshots
- machine-readable outputs plus human-readable reports
- minimal assumptions about the target VPS
- explicit manifests and checksums
- safe-by-default, read-only collection unless explicitly asked otherwise
- mixed-host support, not Docker-only and not systemd-only

## Planned architecture

- `src/host_migrate_kit/`
  - core CLI and orchestration
  - collectors for systemd, Docker, network, cron, app paths
  - manifest generation
  - bundle assembly
  - restore validation
- `docs/`
  - architecture decisions
  - technical specification
  - roadmap
  - restore model
- `examples/`
  - sample config and include/exclude lists
- `tests/`
  - unit tests for manifests, path resolution, bundle layout, and collectors

## Expected outputs

Typical run artifacts should include:
- structured inventory JSON
- bundle manifest JSON
- human-readable audit summary
- relocation archive or staged bundle directory
- checksums
- restore checklist

## Non-goals for MVP

- full bare-metal image cloning
- hypervisor-specific image import/export automation
- cross-distro universal compatibility
- automatic production restore without review

## Initial target use case

A mixed Debian VPS running:
- OpenClaw
- Hiddify / hcore-like services
- Ollama
- cron-based automation
- future Dockerized bots and helper services

## Next documents

- `TZ.md` for technical requirements
- `ROADMAP.md` for phased implementation plan
