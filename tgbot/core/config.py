from decouple import config


DATABASE_URL = config("DATABASE_URL", cast=str)
TABLES_PREFIX = config("TABLES_PREFIX", cast=str)

TELEGRAM_BOT_API_TOKEN = config("TELEGRAM_BOT_API_TOKEN", cast=str)
TELEGRAM_BOT_ADMIN_IDS = config("TELEGRAM_BOT_ADMIN", cast=str).split(",")


class CeleryConfig:
    broker_url = "redis://localhost:6379/0"
    backend = "redis://localhost:6379/0"
    RESULT_BACKEND = "redis://localhost:6379/0"
    ACCEPT_CONTENT = ["application/json"]
    RESULT_SERIALIZER = "json"
    TASK_SERIALIZER = "json"
    TIMEZONE = "Asia/Almaty"


class CeleryConfigDocker:
    broker_url = "redis://redis:6379/0"
    backend = "redis://redis:6379/0"
    RESULT_BACKEND = "redis://redis:6379/0"
    ACCEPT_CONTENT = ["application/json"]
    RESULT_SERIALIZER = "json"
    TASK_SERIALIZER = "json"
    TIMEZONE = "Asia/Almaty"
