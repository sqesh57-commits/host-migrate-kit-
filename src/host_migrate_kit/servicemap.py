from __future__ import annotations

from typing import Any


def build_service_to_data_map() -> list[dict[str, Any]]:
    return [
        {
            'service_id': 'openclaw',
            'service_name': 'openclaw',
            'service_type': 'systemd',
            'runtime_unit': 'openclaw-gateway.service',
            'role': 'automation-host',
            'config_paths': ['/home/sqesh/.openclaw', '/home/sqesh/.openclaw/openclaw.json'],
            'data_paths': ['/home/sqesh/.openclaw/workspace'],
            'secret_refs': ['/home/sqesh/.openclaw/.env'],
            'ports': ['127.0.0.1:18789'],
            'depends_on': [],
            'restore_order': 30,
            'backup_class': 'must-backup',
            'notes': ['Требует Python runtime и валидный config/env слой.'],
        },
        {
            'service_id': 'hiddify',
            'service_name': 'hiddify',
            'service_type': 'systemd',
            'runtime_unit': 'hiddify.service',
            'role': 'proxy-host',
            'config_paths': ['/etc/systemd/system/hiddify.service'],
            'data_paths': ['/opt/hiddify'],
            'secret_refs': [],
            'ports': [],
            'depends_on': ['network-online.target'],
            'restore_order': 20,
            'backup_class': 'must-backup',
            'notes': ['Связан с network/systemd состоянием и proxy-layer артефактами.'],
        },
        {
            'service_id': 'ssh',
            'service_name': 'ssh',
            'service_type': 'systemd',
            'runtime_unit': 'ssh.service',
            'role': 'access',
            'config_paths': ['/etc/hosts', '/etc/systemd/system/ssh.service'],
            'data_paths': [],
            'secret_refs': ['ssh host keys and access secrets'],
            'ports': ['0.0.0.0:22'],
            'depends_on': [],
            'restore_order': 10,
            'backup_class': 'must-backup',
            'notes': ['Критично для восстановления удалённого доступа на новом VPS.'],
        },
    ]
