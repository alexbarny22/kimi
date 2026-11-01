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

## Автообновление при правках

На компе, где должен крутиться бот:

```bash
git clone https://github.com/alexbarny22/kimi.git
cd kimi
cp .env.example .env  # вставьте BOT_TOKEN
```

Запуск с автоподтягиванием из `main`:

- Windows: двойным кликом `start_autoupdate.bat` или в терминале `start_autoupdate.bat`
- macOS/Linux: `bash start_autoupdate.sh`

`supervisor.py` каждые 30 секунд проверяет `origin/main`; если появился новый коммит — останавливает бота, делает `git pull --ff-only`, при необходимости ставит зависимости и запускает бота снова. Интервал можно поменять через `UPDATE_INTERVAL`, ветку через `BOT_BRANCH`.

## Структура

- `supervisor.py` — автообновление и перезапуск;
- `src/bot.py` — точка входа;
- `src/config.py` — загрузка настроек из окружения;
- `src/handlers/` — обработчики команд и сообщений;
- `.env.example` — пример переменных окружения, реальные секреты сюда не коммитить;
- `docs/deploy-example.md` — пример будущего серверного автодеплоя.
