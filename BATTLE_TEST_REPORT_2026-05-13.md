# BATTLE TEST REPORT — 2026-05-13

## Цель

Проверить `host-migrate-kit-` не на слишком чистом тестовом VPS, а на усложнённом стенде, который больше похож на живой mixed-host.

## Что было добавлено на тестовый VPS

На стенд были добавлены дополнительные сущности для stress/realism testing:

### Пользователи
- `hmkdemo`
- `hmkuser2`
- `hmksys` (system account)

### Systemd services
- `demo-alpha.service`
- `demo-beta.service`
- `demo-gamma.service`
- `demo-disabled.service`
- `demo-masked.service`

### Drop-ins / overrides
- `demo-alpha.service.d/override.conf`
- `demo-gamma.service.d/override.conf`

### App-like paths
- `/opt/hmk-demo-app/config/app.conf`
- `/opt/hmk-demo-app/data/state.txt`
- `/srv/hmk-web/config/site.env`
- `/usr/local/hmk-worker/conf/worker.env`
- `/opt/hmk-web-link` (symlink)
- `/opt/hmk-broken/bad-link` (broken symlink)

### Automation
- дополнительный cron entry
- `hmk-demo.timer`

## Что прогонялось

На усложнённом стенде были прогнаны:
- `inventory`
- `manifest`
- `preflight`
- `compat-check`
- `bundle-plan`

## Что toolkit увидел

Итоговый боевой прогон показал:
- `running_services: 15`
- `enabled_services: 17`
- `timers: 9`
- `local_users: 4`
- `cron_entries: 1`
- `roles: ['proxy-host', 'automation-host']`
- `preflight: ok`
- `compat: ok`

## Что это означает

### 1. Аналитический контур реагирует на усложнение среды
Toolkit начал видеть:
- рост числа сервисов
- рост числа пользователей
- наличие timers
- наличие cron
- более сложную роль хоста

Это хороший признак: аналитика не осталась “слепой” после усложнения тестового стенда.

### 2. Role detection уже не совсем примитивна
После добавления automation-сущностей хост стал определяться как:
- `proxy-host`
- `automation-host`

Это полезный сигнал, потому что роли реально отражают наблюдаемое состояние, а не жёстко пришиты к одному кейсу.

### 3. Preflight и compat не ломаются на шумном хосте
Даже после добавления новых сервисов и путей:
- `preflight = ok`
- `compat = ok`

Это означает, что проверки не завязаны только на стерильный сценарий.

## Что пока видно как ограничение

### 1. App detection ещё узкая
Manifest сейчас показывает только curated app paths:
- `/home/sqesh/.openclaw`
- `/home/sqesh/.openclaw/workspace`
- `/opt/hiddify`

То есть новые demo paths в `/srv`, `/usr/local`, `/opt/hmk-demo-app` пока не стали first-class частью app-model.

### 2. Broken symlink scenario пока не выделяется отдельно
Битый симлинк был добавлен в тестовую среду, но текущая модель отчёта не делает на этом явного акцента.

### 3. Cron coverage всё ещё ограничена
На предыдущем прогоне был сигнал, что cron может не всегда отражаться так, как ожидается. После усложнения стенда `cron_entries` уже стал `1`, что лучше, но этот слой всё ещё требует внимания.

## До / после

### До усложнения стенда
- `running_services: 14`
- `local_users: 3`
- `cron_entries: 0`
- `roles: ['proxy-host']`

### После усложнения стенда
- `running_services: 15`
- `local_users: 4`
- `cron_entries: 1`
- `roles: ['proxy-host', 'automation-host']`

## Практический вывод

`host-migrate-kit-` уже полезен как аналитический и подготовительный relocation tool даже на более “боевом” VPS.

Он уже умеет:
- видеть усложнение host state
- строить полезные structured outputs
- не ломаться на умеренном уровне шума
- подтверждать readiness/compatibility на усложнённой среде

## Что стоит делать дальше

### Ближайшие улучшения аналитического слоя
1. Расширить app-path model
2. Явно учитывать symlink / broken symlink cases
3. Усилить cron/systemd timer coverage
4. Добавить более явные warnings по нестандартным артефактам

## Итоговая оценка

Боевой тест на усложнённом стенде можно считать успешным.

Аналитический слой проекта уже проходит не только “чистый MVP demo”, но и более реалистичный mixed-host сценарий.
