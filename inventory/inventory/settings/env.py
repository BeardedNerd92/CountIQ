import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def env_bool(name: str, default: str = "0") -> bool:
    return os.environ.get(name, default) == "1"

def db_conn(DB_ENGINE:str) -> dict:
    DATABASES={}
    if DB_ENGINE == "django.db.backends.sqlite3":
        DATABASES = {
            "default": {
                "ENGINE": DB_ENGINE,
                "NAME": os.environ.get("DB_NAME", "db.sqlite3"),
            }
        }
    else:
        DATABASES = {
            "default": {
                "ENGINE": DB_ENGINE,
                "NAME": os.environ.get("DB_NAME", ""),
                "USER": os.environ.get("DB_USER", ""),
                "PASSWORD": os.environ.get("DB_PASSWORD", ""),
                "HOST": os.environ.get("DB_HOST", ""),
                "PORT": os.environ.get("DB_PORT", ""),
            }
        }
    return DATABASES