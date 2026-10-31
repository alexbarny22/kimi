# kimi

Стартовый каркас Telegram-бота на Python + aiogram 3.

## Быстрый старт

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# вставьте токен в .env
python -m src.bot
```

## Структура

- `src/bot.py` — точка входа;
- `src/config.py` — загрузка настроек из окружения;
- `src/handlers/` — обработчики команд и сообщений;
- `.env.example` — пример переменных окружения, реальные секреты сюда не коммитить;
- `docs/deploy-example.md` — пример будущего автодеплоя.

## Обновление бота из GitHub

Рабочая схема: правки идут через ветку и PR в `main`. После merge можно настроить автодеплой через GitHub Actions/webhook/cron — для этого понадобятся данные сервера, где запущен бот.
