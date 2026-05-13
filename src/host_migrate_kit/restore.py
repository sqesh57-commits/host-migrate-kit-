from __future__ import annotations

from .manifest import build_manifest


def build_restore_guide() -> str:
    manifest = build_manifest()
    lines = [
        '# Черновой restore guide',
        '',
        '## 1. Подготовка нового VPS',
        '- Установить Debian-oriented систему.',
        '- Обновить пакеты и установить базовые утилиты: python3, python3-venv, tar, git, openssh-server.',
        '- Подготовить SSH-доступ и пользователя для администрирования.',
        '',
        '## 2. Подготовка runtime',
        '- Создать рабочий каталог проекта восстановления.',
        '- Поднять отдельное Python virtual environment.',
        '- Развернуть host-migrate-kit и проверить runtime prerequisites.',
        '',
        '## 3. Восстановление системного слоя',
        '- Проверить и восстановить нужные systemd unit-файлы из staging/systemd.',
        '- Перечитать systemd daemon и включить только нужные сервисы.',
        '- Сверить enablement и зависимости вручную.',
        '',
        '## 4. Восстановление automation слоя',
        '- Проверить содержимое staging/cron/user-crontab.txt.',
        '- Восстановить cron-задачи только после проверки путей и зависимостей.',
        '',
        '## 5. Восстановление конфигов и данных',
        '- Разобрать manifest и summary, проверить включённые пути relocation bundle.',
        '- Восстанавливать конфиги и данные поэтапно, начиная с критичных сервисов.',
        '',
        '## 6. Проверка после восстановления',
        f"- Сверить роли хоста: {', '.join(manifest['roles']) if manifest['roles'] else 'не определены'}.",
        '- Проверить listening ports, running services и automation.',
        '- Запустить gap-check после восстановления.',
        '',
        '## 7. Текущий статус guide',
        '- Это черновой guide первого этапа.',
        '- Он будет расширяться по мере появления реального relocation bundle и более точного manifest.',
    ]
    return '\n'.join(lines) + '\n'
