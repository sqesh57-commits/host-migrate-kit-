# NEXT STEPS: host-migrate-kit-

## Цель ближайшего цикла

Завершить первый осмысленный MVP через короткую stabilizing-фазу, агентный review и финальный full-flow test на тестовом VPS.

## Ближайший план

### Шаг 1. Stabilization
- cleanup структуры модулей
- улучшение CLI error handling
- более надёжная работа с путями bundle root
- убрать хрупкие места в тестовых shell-проверках

### Шаг 2. Focused bundle hardening
- проверить, какие ещё safe app files стоит включить
- при необходимости расширить curated staging
- улучшить apply-plan в части restore ordering

### Шаг 3. Агентный review
Подключить агентов на:
- архитектурный review текущего MVP
- review restore/apply direction
- review рисков и недостающих слоёв перед фиксацией MVP

### Шаг 4. Refactor after review
- внести небольшие исправления по замечаниям
- не расширять резко scope
- доработать только то, что реально усиливает MVP

### Шаг 5. Final full-flow test
Прогнать на тестовом VPS полный доступный контур:
- audit
- inventory
- manifest
- validate-manifest
- gap-check
- preflight
- compat-check
- bundle-plan
- apply-plan

### Шаг 6. MVP completion point
Если после review и повторного full-flow прогона всё стабильно:
- зафиксировать это как первый завершённый MVP point
- подготовить список follow-up задач для post-MVP цикла

## Важное ограничение

На ближайшем цикле не расширять scope слишком сильно.

Цель сейчас не “добавить всё возможное”, а:
- стабилизировать уже созданный контур
- подтвердить его на стенде
- закончить первый реальный MVP
