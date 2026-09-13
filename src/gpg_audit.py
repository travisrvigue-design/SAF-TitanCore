"""
GPG audit logger wrapper.
- Serializes events to JSON
- Attempts to GPG-sign using system gpg if available (stubbed in CI)
- Appends signed records to ./logs/audit.log
"""
import json
import subprocess
import os
from datetime import datetime

LOG_PATH = os.environ.get('SAF_AUDIT_LOG', './logs/audit.log')
AUTHORIZED_KEYS = os.environ.get('SAF_AUTH_KEYS', './docs/security/authorized_keys.txt')

class GPGAuditLog:
    def __init__(self, log_path: str = None):
        self.log_path = log_path or LOG_PATH
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)

    def _sign(self, payload: str) -> str:
        # Attempt to sign using gpg; in CI or offline this will return an empty signature and print a warning
        try:
            p = subprocess.run(['gpg', '--batch', '--yes', '--armor', '--sign'], input=payload.encode('utf-8'), stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            return p.stdout.decode('utf-8')
        except Exception as e:
            print('GPG signing failed or not available in environment:', e)
            return ''

    def log_event(self, event_type: str, payload: dict):
        record = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'agent': payload.get('agent', 'unknown'),
            'event_type': event_type,
            'payload': payload,
            'signature': None
        }
        serialized = json.dumps(record, sort_keys=True)
        signature = self._sign(serialized)
        record['signature'] = signature
        with open(self.log_path, 'a') as f:
            f.write(json.dumps(record) + '\n')
        return record
