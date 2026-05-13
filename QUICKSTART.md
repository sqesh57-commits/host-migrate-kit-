# QUICKSTART: host-migrate-kit-

Короткий старт для первого практического использования.

## 1. Подготовка

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -e .
```

Если `python3-venv` ещё не установлен, сначала добавьте его в систему.

Аварийный read-only режим без `venv`:

```bash
PYTHONPATH=src python3 -m host_migrate_kit.command audit
```

## 2. Базовый цикл

### Аудит

```bash
hmk audit
```

### Inventory

```bash
hmk inventory --pretty --output inventory.json
```

### Manifest

```bash
hmk manifest --pretty --output manifest.json
```

### Проверки

```bash
hmk validate-manifest --pretty
hmk gap-check --pretty
hmk preflight --pretty
hmk compat-check --pretty
```

## 3. Dry-run relocation bundle

```bash
hmk bundle-plan --output-dir ./dist --pretty
```

После этого появится каталог `./dist/<bundle-id>/`.

## 4. Dry-run restore flow

```bash
hmk apply-plan ./dist/<bundle-id> --pretty
hmk verify-bundle ./dist/<bundle-id> --pretty
```

## 5. Минимально рекомендуемый порядок

```bash
hmk audit
hmk inventory --pretty --output inventory.json
hmk manifest --pretty --output manifest.json
hmk validate-manifest --pretty
hmk gap-check --pretty
hmk preflight --pretty
hmk compat-check --pretty
hmk bundle-plan --output-dir ./dist --pretty
hmk apply-plan ./dist/<bundle-id> --pretty
hmk verify-bundle ./dist/<bundle-id> --pretty
```

## 6. Что делает MVP уже сейчас

MVP уже умеет:
- собирать host state
- строить inventory и manifest
- проверять базовую readiness/compatibility
- строить dry-run relocation bundle
- собирать controlled staging
- строить dry-run apply plan
- проверять полноту bundle

## 7. Что MVP пока не делает

MVP пока не является fully automatic restore system.

То есть это уже:
- инструмент подготовки к миграции
- инструмент relocation planning
- инструмент сборки bundle и dry-run restore flow

Но пока не “однокнопочный полный restore без ручного контроля”.
