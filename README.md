# host-migrate-kit-

`host-migrate-kit-` — это переносимый набор инструментов для аудита Debian-oriented VPS, сбора критически важных конфигураций и данных, а также подготовки relocation bundle для быстрого восстановления на новом чистом сервере.

## Что это?

Это не snapshot-система и не полный образ диска.

Это проект, который помогает ответить на практический вопрос:

> Что именно нужно сохранить с текущего VPS, чтобы потом можно было быстро и предсказуемо развернуть всё на другом сервере?

Проект должен уметь:
- понять, что реально поднято на хосте
- выделить критически важные конфиги, сервисы и данные
- собрать это в переносимый набор артефактов
- помочь человеку восстановить всё на новом VPS с чистой Debian-oriented системой

## Для чего это нужно?

У типичного VPS есть несколько проблем:
- snapshot быстрый, но часто привязан к конкретному провайдеру
- raw-backup файлов не объясняет, как всё было связано между собой
- на сервере обычно смешаны:
  - systemd-сервисы
  - Docker-контейнеры
  - cron-задачи
  - сетевые правила
  - данные приложений
  - секреты
- при переезде на другой VPS нужно не просто сохранить файлы, а понять порядок восстановления

`host-migrate-kit-` нужен для того, чтобы переезд не превращался в археологию и ручное вспоминание, что где лежало и в каком порядке запускалось.

## Зачем делать отдельный проект?

Потому что задача уже выходит далеко за рамки обычного “сделай бэкап”.

Здесь нужен полноценный подход:
- аудит хоста
- inventory
- стратегия бэкапа
- relocation bundle
- manifest
- restore guide
- миграционные проверки

Если этого не оформить как отдельный проект, всё быстро расползётся по случайным скриптам, заметкам и одноразовым командам. В критический момент это обычно и ломается.

## Почему выбран именно такой подход?

### Почему не делаем ставку только на snapshot?

Потому что snapshot:
- удобен как аварийная страховка
- но часто плохо переносится между провайдерами
- не помогает, если новый VPS будет в другой стране или у другого хостера
- не всегда доступен для импорта как custom image

### Почему не ограничиваемся обычным архивом конфигов?

Потому что просто архив не отвечает на вопросы:
- какие сервисы реально были запущены
- какие unit-файлы были включены
- какие volumes были привязаны к контейнерам
- какие порты должны слушаться
- что восстанавливать в первую очередь

### Почему relocation bundle?

Relocation bundle — это компромисс между “полным образом диска” и “просто пачкой файлов”.

Он должен содержать:
- конфиги
- данные
- manifest
- checksums
- restore guide
- служебную информацию для ручного или полуавтоматического восстановления

Это делает сервер переносимым, а не просто архивируемым.

## Цель проекта

Сохранение критически важных данных и конфигурации для бэкапа и быстрого развертывания на другом VPS с чистой Debian-oriented системой.

## Область применения

На первом этапе проект ориентирован на:
- Debian 12+
- systemd-based Linux
- VPS с mixed-host нагрузкой

Под mixed-host понимается сервер, где могут одновременно жить:
- systemd-сервисы
- Docker / Docker Compose
- cron-задачи
- каталоги приложений в `/opt`, `/srv`, `/home/...`
- данные ботов, прокси, LLM-обвязки, automation-проектов

## Что входит в MVP?

- аудит хоста
- inventory
- relocation bundle
- backup strategy
- restore guide
- Docker volume support
- systemd export
- manifest generation
- migration checks

## Что означает каждый пункт MVP?

### Аудит хоста
Нужен, чтобы понять текущее состояние сервера: что запущено, что слушает порты, какие сервисы критичны, какие подсистемы вообще используются.

### Inventory
Нужен, чтобы превратить разрозненные данные в структурированную модель: сервисы, порты, таймеры, cron, volumes, пути данных, зависимости.

### Relocation bundle
Нужен, чтобы собрать всё действительно важное в один переносимый комплект артефактов.

### Backup strategy
Нужна, потому что один раз собрать bundle мало. Нужно понимать, как повторять процесс регулярно и безопасно.

### Restore guide
Нужен, чтобы восстановление не зависело от памяти владельца сервера или автора скриптов.

### Docker volume support
Нужен, потому что по мере роста проекта именно persistent data контейнеров почти всегда становится критичной.

### systemd export
Нужен, потому что на Debian-oriented VPS systemd — это один из главных источников истины о сервисах и порядке их запуска.

### Manifest generation
Нужен, чтобы результат был пригоден не только человеку, но и для автоматической проверки, diff, валидации и дальнейшей автоматизации.

### Migration checks
Нужны, чтобы заранее видеть дыры в переносимости, а не находить их уже после падения старого VPS.

## Ключевые принципы проекта

### Debian-first
Проект намеренно не пытается с первого дня поддерживать “любой Linux”.

Почему:
- это резко усложняет реализацию
- даёт много ложной универсальности
- мешает сделать хороший, надёжный MVP

Выбор в пользу Debian-oriented систем сделан потому, что именно под них сейчас есть реальная задача и реальные данные.

### Portability first
Главная цель — переносимость между VPS, а не идеальный бэкап внутри одного провайдера.

### Read-only by default
Сбор информации должен быть безопасным. По умолчанию проект должен читать и фиксировать состояние, а не менять его.

### Machine-readable + human-readable
Результат должен быть полезен и человеку, и автоматике.

То есть нужны:
- JSON manifest / inventory
- Markdown restore guide / summary

### Явные артефакты вместо магии
Лучше иметь:
- manifest
- checksums
- список включённых путей
- warnings

чем “умный чёрный ящик”, который что-то там собрал, но никто не понимает что именно.

## Как этим пользоваться

Ниже описан текущий практический способ использования MVP.

### 1. Подготовка окружения

На Debian-oriented хосте рекомендуется запускать проект через отдельное Python-окружение.

Пример:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -e .
```

Если на хосте ещё нет `python3-venv`, это нужно установить отдельно.

Если нужно сделать только быстрый read-only запуск на бедном хосте без `venv`, допустим аварийный режим:

```bash
PYTHONPATH=src python3 -m host_migrate_kit.command audit
```

Но это именно запасной режим, а не основной.

### 2. Базовый аудит

Краткая сводка по хосту:

```bash
hmk audit
```

JSON-вариант:

```bash
hmk audit --json
```

### 3. Сбор inventory

Собрать структурированный inventory:

```bash
hmk inventory --pretty
```

Сохранить в файл:

```bash
hmk inventory --pretty --output inventory.json
```

### 4. Сбор manifest

Построить manifest:

```bash
hmk manifest --pretty
```

Сохранить в файл:

```bash
hmk manifest --pretty --output manifest.json
```

### 5. Проверки перед bundle phase

Проверка структуры manifest:

```bash
hmk validate-manifest --pretty
```

Проверка явных пробелов:

```bash
hmk gap-check --pretty
```

Проверка runtime-готовности хоста:

```bash
hmk preflight --pretty
```

Проверка совместимости ролей и target runtime:

```bash
hmk compat-check --pretty
```

### 6. Построение dry-run relocation bundle

Создать dry-run bundle layout:

```bash
hmk bundle-plan --pretty
```

Указать свой каталог для артефактов:

```bash
hmk bundle-plan --output-dir ./dist --pretty
```

После этого появится bundle directory с базовыми артефактами:
- `manifest/manifest.json`
- `manifest/checksums.json`
- `reports/bundle-plan.json`
- `reports/summary.md`
- `reports/restore-guide.md`
- `staging/staging-index.json`

### 7. Что уже попадает в staging

Сейчас controlled staging умеет собирать:
- curated systemd unit files
- systemd drop-ins
- systemd active/enabled state
- user crontab
- safe `/etc` files
- safe app files

### 8. Построение dry-run restore/apply плана

После сборки bundle можно построить план восстановления:

```bash
hmk apply-plan ./dist/<bundle-id> --pretty
```

Сейчас это dry-run шаги, которые помогают понять порядок восстановления, но не меняют систему автоматически.

### 9. Проверка полноты bundle

Проверить, что обязательные MVP-артефакты bundle на месте:

```bash
hmk verify-bundle ./dist/<bundle-id> --pretty
```

### 10. Текущий рекомендуемый порядок работы

Если использовать проект по назначению уже сейчас, я бы шёл так:

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

### 11. Что важно понимать прямо сейчас

Текущий MVP:
- уже полезен для аудита, inventory и dry-run relocation flow
- уже умеет собирать ранний relocation bundle
- уже умеет строить restore/apply план
- но пока ещё не является fully automatic restore system

То есть сейчас это:
- инструмент подготовки к миграции
- инструмент проверки переносимости
- инструмент сборки relocation artifacts

Но не “одна кнопка полностью восстановить любой VPS”.

## Предполагаемая структура проекта

- `src/host_migrate_kit/`
  - core CLI и orchestration
  - collectors для systemd, Docker, network, cron, app paths
  - manifest generation
  - bundle assembly
  - restore validation
- `docs/`
  - архитектурные решения
  - техническая спецификация
  - roadmap
  - модель восстановления
- `examples/`
  - примеры конфигурации
  - include/exclude lists
- `tests/`
  - unit tests и integration-lite тесты

## Какие артефакты должен уметь создавать проект?

Ожидаемые результаты работы:
- структурированный inventory JSON
- manifest JSON
- человекочитаемый audit summary
- staged relocation bundle directory или archive
- checksums
- restore checklist / restore guide

## Что сознательно не входит в MVP?

- full disk imaging
- bare-metal cloning
- привязка к конкретному провайдеру
- автоматический restore без проверки человеком
- попытка сразу поддерживать все Linux-дистрибутивы

## Ближайшие документы

- `TZ.md` — подробное техническое задание
- `ROADMAP.md` — этапы реализации
