from dataclasses import dataclass

from .core.config import (
    DATABASE_URL,
    TELEGRAM_BOT_ADMIN_IDS,
    TELEGRAM_BOT_API_TOKEN,
)


@dataclass
class DbConfig:
    url: str


@dataclass
class TgBot:
    token: str
    admin_ids: list
    use_redis: bool


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig


def cast_bool(value: str) -> bool:
    if not value:
        return False
    return value.lower() in ("true", "t", "1", "yes")


def load_config():
    return Config(
        tg_bot=TgBot(
            token=TELEGRAM_BOT_API_TOKEN,
            admin_ids=list(map(int, TELEGRAM_BOT_ADMIN_IDS)),
            use_redis=False,
        ),
        db=DbConfig(url=DATABASE_URL),
    )
