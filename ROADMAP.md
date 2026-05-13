# ROADMAP: host-migrate-kit-

## Phase 0. Project foundation

Goal:
- create repository skeleton
- document purpose, constraints, and MVP
- lock the Debian-first architecture direction

Deliverables:
- README
- ТЗ
- roadmap
- initial package/layout decision

## Phase 1. Host audit and inventory

Goal:
- gather reliable read-only host facts

Scope:
- OS / kernel metadata
- listening ports
- running and enabled systemd services
- timers and cron jobs
- Docker / containerd presence
- disk usage
- selected network/firewall state
- important top-level paths

Deliverables:
- `hmk-audit`
- `hmk-inventory`
- JSON inventory schema draft
- human-readable audit summary

Success criteria:
- tool can inspect a Debian VPS and produce useful structured output without modifying host state

## Phase 2. Manifest model

Goal:
- define the canonical machine-readable representation of migration state

Scope:
- host metadata
- services
- ports
- cron/timers
- Docker workloads
- selected data paths
- warnings and unresolved items
- checksums and collection metadata

Deliverables:
- manifest schema draft
- manifest generator
- validation logic

Success criteria:
- repeated runs produce predictable manifest structure suitable for bundle assembly and restore planning

## Phase 3. Relocation bundle assembly

Goal:
- collect critical configuration and selected data into a portable bundle

Scope:
- configs from `/etc`, user configs, and app-specific paths
- systemd unit export
- cron export
- selected data paths
- Docker-related metadata and volume support foundations
- checksums
- staged bundle layout

Deliverables:
- `hmk-bundle`
- bundle directory layout
- `checksums.txt`
- include/exclude config support

Success criteria:
- tool can produce a structured relocation bundle that is inspectable and archivable

## Phase 4. Restore documentation

Goal:
- help a human restore the stack on a clean Debian VPS

Scope:
- generated restore checklist
- host preparation steps
- restore ordering
- post-restore validation hints
- caveats for secrets, ports, and service dependencies

Deliverables:
- generated `restore-guide.md`
- templates for restore notes

Success criteria:
- a human can restore the audited stack on a clean Debian host using the generated bundle plus guide

## Phase 5. Docker volume support

Goal:
- make future Docker-heavy migrations practical

Scope:
- enumerate volumes
- map volumes to containers/projects
- export volume metadata
- optionally archive volumes into the bundle
- document consistency limitations for live databases

Deliverables:
- Docker volume collector
- archive strategy for named volumes and bind mounts
- warnings for stateful databases

Success criteria:
- Docker workloads and their persistent data become first-class citizens in the relocation bundle

## Phase 6. Migration checks

Goal:
- reduce migration surprises

Scope:
- source host readiness checks
- bundle completeness checks
- target VPS readiness checks
- post-restore smoke checks

Deliverables:
- `hmk-restore-check`
- warning/error severity model
- migration readiness report

Success criteria:
- operator gets actionable feedback before and after migration

## Phase 7. Backup strategy integration

Goal:
- define a repeatable backup workflow instead of one-off bundle creation

Scope:
- local archive strategy
- optional encrypted offsite backup backend
- retention strategy
- scheduled runs
- run artifacts and logs

Deliverables:
- backup strategy doc
- config examples
- optional scheduled-run templates

Success criteria:
- project supports both emergency relocation and routine backup hygiene

## Deferred / future ideas

- Ubuntu compatibility layer
- provider-specific restore notes
- remote source-to-target migration mode
- optional restic backend integration
- richer diffing between audit runs
- secret redaction helpers
- database-aware collectors and dumps

## Recommended implementation order

1. Phase 0
2. Phase 1
3. Phase 2
4. Phase 3
5. Phase 4
6. Phase 6
7. Phase 5
8. Phase 7

Rationale:
- first understand the host
- then model it
- then collect it
- then document restore
- then add richer migration safety and Docker depth
