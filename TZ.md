# ТЗ: host-migrate-kit-

## 1. Назначение

`host-migrate-kit-` предназначен для аудита Debian-oriented VPS, фиксации критически важного состояния хоста и подготовки relocation bundle для быстрого развертывания на другом VPS с чистой системой.

## 2. Основная цель

Сохранение критически важных данных и конфигурации для бэкапа и быстрого развертывания на другом VPS на чистой Debian-oriented системе.

## 3. Контекст задачи

Целевой сервер может содержать смешанную инфраструктуру:
- systemd-сервисы
- Docker / Docker Compose
- cron-задачи
- кастомные каталоги с данными и конфигами
- сетевые правила
- пользовательские секреты и runtime state

При этом:
- текущий VPS может быть внезапно недоступен
- новый VPS может быть у другого провайдера
- может не быть возможности загрузить собственный образ диска
- в будущем инфраструктура может вырасти за счет контейнеров и ботов

## 4. Требования MVP

### 4.1 Аудит хоста
Инструмент должен уметь в read-only режиме собирать:
- версию ОС и ядра
- список активных и enabled systemd unit-файлов
- список listening ports
- cron и systemd timers
- наличие и состояние Docker / containerd / Podman
- ключевые сетевые данные
- использование диска
- важные сервисы и их источник состояния

### 4.2 Inventory
Инструмент должен формировать inventory артефакт со структурированными данными о:
- сервисах
- портах
- пакетах
- таймерах
- cron-задачах
- Docker workloads и volumes
- путях данных
- системных зависимостях

### 4.3 Relocation bundle
Инструмент должен собирать relocation bundle, включающий:
- конфиги
- системные unit-файлы
- cron-артефакты
- Docker metadata
- выбранные каталоги данных
- manifest
- checksums
- restore guide

### 4.4 Backup strategy
Инструмент должен поддерживать понятную стратегию бэкапа для:
- конфигов
- данных
- Docker volumes
- ручных include/exclude путей

### 4.5 Restore guide
Инструмент должен генерировать человекочитаемый restore guide для нового Debian VPS.

### 4.6 Docker volume support
Инструмент должен уметь:
- перечислять volumes
- сопоставлять их с контейнерами и compose-проектами
- включать volume data в relocation bundle

### 4.7 systemd export
Инструмент должен экспортировать:
- service units
- drop-ins
- enablement context
- зависимости, если это возможно без опасного вмешательства

### 4.8 Manifest generation
Инструмент должен генерировать machine-readable manifest с минимумом:
- host metadata
- collected components
- included paths
- bundle contents
- timestamps
- checksums
- warnings / missing pieces

### 4.9 Migration checks
Инструмент должен уметь выполнять проверки:
- готовности исходного сервера к миграции
- полноты собранного bundle
- минимальной готовности нового VPS к восстановлению

## 5. Целевая платформа

Основная платформа MVP:
- Debian 12+
- systemd-based systems

Поддержка Ubuntu и близких дистрибутивов допускается позже как совместимый слой, но не является обязательной целью MVP.

## 6. Технологический стек

Предлагаемый стек:
- Python 3.11+
- stdlib-first подход
- `argparse` для CLI на старте
- `logging` stdlib для логирования
- JSON как основной machine-readable формат
- Markdown для human-readable отчётов
- shell helper scripts только там, где это действительно удобно

## 7. Архитектурные принципы

- Debian-first
- portability first
- read-only by default
- modular collectors
- explicit manifests
- reproducible outputs
- human + machine readability
- no hard dependency on provider snapshots

## 8. Не-цели MVP

В MVP не требуется:
- full disk imaging
- загрузка cloud image в провайдеров
- полная кросс-дистрибутивность
- автоматический безусловный restore в production
- полноценная оркестрация удалённого переезда между двумя VPS

## 9. Ожидаемые артефакты

### 9.1 Audit output
- краткий human-readable summary
- структурированный JSON report

### 9.2 Inventory output
- inventory JSON
- warnings list

### 9.3 Bundle output
- bundle directory или tar.gz archive
- manifest.json
- checksums.txt
- restore-guide.md

## 10. Критерии успеха MVP

MVP считается успешным, если он позволяет:
1. понять, что реально поднято на Debian VPS
2. собрать критически важные конфиги и данные
3. получить relocation bundle с manifest и restore guide
4. восстановить сервисы вручную по generated guide на чистом Debian VPS без зависимости от provider snapshot
