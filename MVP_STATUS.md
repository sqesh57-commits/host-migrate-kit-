# MVP STATUS: host-migrate-kit-

## Текущее состояние

Проект дошёл до раннего рабочего MVP-контура.

Сейчас уже реализованы и прогнаны вживую ключевые базовые команды:
- `hmk audit`
- `hmk inventory`
- `hmk manifest`
- `hmk validate-manifest`
- `hmk gap-check`
- `hmk preflight`
- `hmk compat-check`
- `hmk bundle-plan`
- `hmk apply-plan`

## Что уже умеет проект

### 1. Аудит и inventory
Проект умеет:
- собирать host summary
- строить inventory JSON
- фиксировать сервисы, порты, cron, timers, filesystems, пакеты, runtime binaries
- определять базовые роли хоста

### 2. Manifest и validation
Проект умеет:
- строить machine-readable manifest
- валидировать структуру manifest
- включать в manifest gap-check и warnings
- фиксировать app paths и path metadata

### 3. Migration readiness
Проект умеет:
- выполнять `gap-check`
- выполнять `preflight`
- выполнять `compat-check`

Это уже даёт первый уровень оценки готовности хоста и target VPS к миграции.

### 4. Bundle planning
Проект умеет строить dry-run bundle layout с:
- `manifest.json`
- `checksums`
- `bundle-plan.json`
- `summary.md`
- `restore-guide.md`
- staging index

### 5. Controlled staging
Проект уже умеет собирать:
- systemd unit files
- systemd drop-ins
- systemd active/enabled state
- user crontab
- safe `/etc` files
- safe app files

### 6. Restore flow
Проект уже умеет строить dry-run `apply-plan`, который учитывает:
- restore systemd units
- daemon reload
- review enable targets
- review start targets
- review cron
- review safe files
- post-restore checks

## Что уже протестировано

### Локально
Проверены все основные команды в локальной среде.

### На тестовом VPS
Прогнан базовый и расширенный контур на стенде.

Подтверждены рабочие сценарии:
- `audit`
- `inventory`
- `manifest`
- `validate-manifest`
- `gap-check`
- `preflight`
- `compat-check`
- `bundle-plan`
- `apply-plan`

## Текущие сильные стороны

- проект уже полезен практически, а не только концептуально
- есть machine-readable и human-readable артефакты
- есть первые проверки совместимости
- есть controlled staging вместо слепого копирования всего подряд
- есть ранний restore-flow

## Что ещё не закрыто до более зрелого MVP

### 1. Stabilization / cleanup
Нужно:
- выровнять структуру модулей
- подчистить helper layers
- улучшить обработку ошибок
- сделать CLI устойчивее

### 2. Bundle completeness
Нужно:
- расширить curated app-specific staging
- аккуратно углубить systemd context
- улучшить staging index и artifact bookkeeping

### 3. Restore realism
Нужно:
- сделать apply-plan богаче
- добавить post-restore verification слой
- чётче разделить automated vs manual restore steps

### 4. Final MVP pass
Нужно:
- провести sanity/review проход агентами
- сделать небольшой рефакторинг по результатам
- затем ещё раз прогнать полный контур на тестовом VPS

## Текущий честный статус

`host-migrate-kit-` уже находится на стадии **раннего рабочего MVP-кандидата**, но ещё не на стадии “завершённый MVP без оговорок”.

Самая правильная следующая цель:
- быстро пройти stabilization + focused review + final full-flow test
- и после этого зафиксировать первый осмысленный MVP completion point
