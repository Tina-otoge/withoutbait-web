import os
import secrets
from pathlib import Path
import yaml


LOCAL_KEY = Path('./secret.key')
TOKENS_PATH = Path('./tokens.yml')

def get_secret_key():
    key = os.environ.get('SECRET_KEY')
    if key:
        return key
    if LOCAL_KEY.exists():
        return LOCAL_KEY.read_text()
    key = secrets.token_hex(32)
    LOCAL_KEY.write_text(key)
    return key


def get_tokens():
    if not TOKENS_PATH.exists():
        raise Exception('Missing tokens')
    with TOKENS_PATH.open() as f:
        data = yaml.safe_load(f)
    return data
