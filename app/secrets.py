import os
import secrets
from pathlib import Path


LOCAL_KEY = Path('./secret.key')

def get_secret_key():
    key = os.environ.get('SECRET_KEY')
    if key:
        return key
    if LOCAL_KEY.exists():
        return LOCAL_KEY.read_text()
    key = secrets.token_hex(32)
    LOCAL_KEY.write_text(key)
    return key
