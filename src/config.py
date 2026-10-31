from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    bot_token: str


def get_settings() -> Settings:
    token = os.getenv("BOT_TOKEN", "").strip()
    if not token or token == "put-your-token-here":
        raise RuntimeError("Set BOT_TOKEN in .env or environment variables")
    return Settings(bot_token=token)
