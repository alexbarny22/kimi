from __future__ import annotations

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

router = Router(name="start")


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer("Бот запущен. Отправь любое сообщение — я его повторю.")


@router.message()
async def echo(message: Message) -> None:
    if message.text:
        await message.answer(message.text)
