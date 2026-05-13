# ROADMAP: host-migrate-kit-

Этот документ описывает этапы развития проекта, их смысл и причины выбора именно такой последовательности.

Главная идея roadmap: не пытаться сразу построить “универсальную миграционную платформу”, а идти слоями, где каждый следующий этап опирается на предыдущий.

## Почему roadmap разбит на фазы?

Потому что задача многослойная:
- сначала нужно понять, что вообще есть на сервере
- потом это нужно формализовать
- потом научиться это собирать
- потом описать восстановление
- потом проверять переносимость и полноту

Если перепрыгнуть через ранние фазы, дальше проект быстро упрётся в хаос:
- bundle будет собираться без чёткого понимания состава
- restore guide будет писаться на догадках
- migration checks станут проверять неясную модель

## Phase 0. Основание проекта

### Что это?
Этап, на котором проект получает имя, границы, цель, минимальную архитектуру и основные документы.

### Для чего это нужно?
Чтобы не начинать писать код в пустоту, без договорённости о том, что вообще считается результатом.

### Зачем это нужно?
Без этого проект быстро превращается в набор разрозненных утилит и заметок без общей модели.

### Почему такой выбор?
Потому что для инфраструктурных инструментов архитектурная ясность на старте особенно важна: позднее исправление модели хранения артефактов и форматов отчётов обычно обходится дорого.

### Deliverables
- README
- ТЗ
- roadmap
- базовое решение по структуре репозитория

## Phase 1. Аудит хоста и inventory

### Что это?
Первый прикладной этап: инструмент начинает читать хост и собирать факты о нём.

### Для чего это нужно?
Чтобы зафиксировать реальное состояние сервера, а не опираться на предположения.

### Зачем это нужно?
Нельзя корректно строить migration bundle, если заранее не понятно:
- какие сервисы реально важны
- какие процессы слушают порты
- что включено в systemd
- какие cron/timer механизмы задействованы
- есть ли Docker и persistent volumes

### Почему такой выбор?
Потому что inventory — это фундамент для всех последующих этапов. Всё остальное должно строиться на структурированных фактах.

### Scope
- OS / kernel metadata
- listening ports
- running/enabled systemd services
- timers and cron jobs
- Docker / containerd presence
- disk usage
- selected network/firewall state
- important top-level paths

### Deliverables
- `hmk-audit`
- `hmk-inventory`
- draft JSON schema для inventory
- human-readable summary

### Success criteria
Инструмент без изменения состояния хоста умеет собрать полезный и понятный inventory с Debian VPS.

## Phase 2. Модель manifest

### Что это?
Этап, где проект получает каноническое описание состояния миграции в machine-readable виде.

### Для чего это нужно?
Чтобы все остальные части проекта работали с одной и той же моделью данных.

### Зачем это нужно?
Если нет manifest-модели, то:
- bundle трудно валидировать
- сложно понимать, что именно попало в сборку
- diff между двумя состояниями становится неявным
- restore automation в будущем будет строиться на песке

### Почему такой выбор?
Manifest — это источник истины для bundle, restore и migration checks. Поэтому его лучше проектировать рано, а не “потом как-нибудь”.

### Scope
- host metadata
- services
- ports
- cron/timers
- Docker workloads
- selected data paths
- warnings and unresolved items
- checksums and collection metadata

### Deliverables
- схема manifest
- генератор manifest
- валидация структуры

### Success criteria
Повторные запуски дают предсказуемый, структурированный manifest, пригодный для сборки bundle и планирования восстановления.

## Phase 3. Сборка relocation bundle

### Что это?
Этап, где проект начинает не только описывать сервер, но и собирать его переносимые артефакты.

### Для чего это нужно?
Чтобы из inventory и manifest получился практический результат, который можно увезти на другой VPS.

### Зачем это нужно?
Потому что хороший отчёт о сервере ещё не равен возможности восстановить сервер.

### Почему такой выбор?
После аудита и manifest уже достаточно информации, чтобы начать собирать bundle осмысленно, а не вслепую.

### Scope
- configs из `/etc`, user configs и app-specific paths
- systemd unit export
- cron export
- selected data paths
- Docker metadata foundations
- checksums
- staged bundle layout

### Deliverables
- `hmk-bundle`
- структура bundle directory
- `checksums.txt`
- include/exclude support

### Success criteria
Проект умеет собрать inspectable relocation bundle, который можно архивировать, переносить и проверять.

## Phase 4. Документация восстановления

### Что это?
Этап, где проект начинает объяснять, как применять собранный bundle на новом сервере.

### Для чего это нужно?
Чтобы восстановление не зависело от памяти владельца и не превращалось в ручную импровизацию.

### Зачем это нужно?
Даже хороший bundle бесполезен, если нет понятного порядка:
- что ставить первым
- что разворачивать вторым
- какие секреты нужны
- как проверять успешность

### Почему такой выбор?
Restore guide логично строить после того, как уже понятны inventory и структура bundle.

### Scope
- generated restore checklist
- host preparation steps
- restore ordering
- post-restore validation hints
- notes about secrets, ports, and dependencies

### Deliverables
- `restore-guide.md`
- шаблоны restore notes

### Success criteria
Человек может восстановить стек на чистом Debian VPS, имея bundle и generated guide.

## Phase 5. Поддержка Docker volumes

### Что это?
Этап углубления в Docker persistence.

### Для чего это нужно?
Чтобы проект был действительно полезен, когда на сервере начнут накапливаться контейнеры и данные в volumes.

### Зачем это нужно?
В Docker-инфраструктуре именно persistent data чаще всего и является самым ценным и самым легко теряемым слоем.

### Почему этот этап не раньше?
Потому что сначала нужно иметь общую модель inventory, manifest и bundle, а уже потом углубляться в частный, но очень важный слой Docker persistence.

### Scope
- enumerate volumes
- map volumes to containers/projects
- export volume metadata
- optionally archive volumes
- warnings for live databases and consistency risks

### Deliverables
- Docker volume collector
- archive strategy for named volumes and bind mounts
- consistency notes

### Success criteria
Docker workloads и их persistent data становятся полноценной частью relocation bundle.

## Phase 6. Migration checks

### Что это?
Этап валидации и снижения рисков.

### Для чего это нужно?
Чтобы находить проблемы до переезда, а не после него.

### Зачем это нужно?
Переезд ломается не только из-за отсутствия файлов, но и из-за невидимых несовместимостей:
- забытые зависимости
- неполный bundle
- отсутствующие порты
- неготовый target VPS

### Почему этот этап после bundle и restore guide?
Потому что проверять нужно уже относительно сформированной модели и ожидаемого процесса восстановления.

### Scope
- source host readiness checks
- bundle completeness checks
- target VPS readiness checks
- post-restore smoke checks

### Deliverables
- `hmk-restore-check`
- warning/error severity model
- readiness report

### Success criteria
Оператор получает actionable feedback до и после миграции.

## Phase 7. Интеграция backup strategy

### Что это?
Этап превращения разовой миграционной утилиты в инструмент регулярной готовности к переезду.

### Для чего это нужно?
Чтобы relocation bundle не собирался только “когда уже горит”, а существовал как поддерживаемый процесс.

### Зачем это нужно?
Потому что лучший migration plan — тот, который уже заранее обкатан и регулярно обновляется.

### Почему это финальная фаза MVP-цикла?
Потому что сначала должен появиться рабочий способ audit → inventory → bundle → restore, и только потом имеет смысл формализовать регулярные бэкапы и retention.

### Scope
- local archive strategy
- optional encrypted offsite backup backend
- retention strategy
- scheduled runs
- run artifacts and logs

### Deliverables
- backup strategy doc
- config examples
- optional scheduled-run templates

### Success criteria
Проект помогает не только эвакуироваться один раз, но и поддерживать постоянную миграционную готовность.

## Отложенные идеи

Это важно, но не обязательно для первого рабочего релиза:
- слой совместимости для Ubuntu
- provider-specific restore notes
- remote source-to-target migration mode
- optional restic backend integration
- richer diff between audit runs
- secret redaction helpers
- database-aware collectors and dumps

## Почему именно такой порядок реализации?

Рекомендуемый порядок:
1. Phase 0
2. Phase 1
3. Phase 2
4. Phase 3
5. Phase 4
6. Phase 6
7. Phase 5
8. Phase 7

### Обоснование
- сначала нужно увидеть хост
- потом описать его моделью
- потом собрать bundle
- потом понять восстановление
- потом проверить готовность миграции
- потом углубиться в Docker persistence
- потом автоматизировать регулярный backup lifecycle

Это снижает риск того, что проект слишком рано уйдёт в сложность без рабочего результата.
