# Remnawave Telegram VPN Bot

Telegram бот для управления VPN доступом через Remnawave панель. Автоматически создает пользователей при вступлении в группу и отзывает доступ при выходе.

## Возможности

- Автоматическое создание пользователей в Remnawave панели
- Выдача ссылки подписки для VPN клиента
- Мониторинг членства в Telegram группе
- Отзыв доступа при выходе или бане
- Уведомления в группу и личные сообщения
- Работает без собственной базы данных

## Запуск

### Docker

```bash
# Настроить .env файл
nano .env

# Запустить
docker-compose up -d

# Логи
docker-compose logs -f bot
```

### Локально

```bash
pip install -r requirements.txt
python -m src.main
```

## Структура

```
src/
├── handlers/
│   ├── user_handlers.py    # Команды пользователей
│   └── group_handlers.py   # События группы
├── tests/                  # Unit тесты
├── main.py                 # Точка входа
├── config.py               # Конфигурация
├── api_client.py           # API клиент Remnawave
├── keyboards.py            # Клавиатуры
├── notifications.py        # Уведомления
├── middlewares.py          # Middleware
├── filters.py              # Фильтры
├── states.py               # FSM состояния
├── utils.py                # Утилиты
└── constants.py            # Константы
```

## Конфигурация

Создайте `.env` файл:

```env
# Telegram
BOT_TOKEN=your_bot_token_here
ADMIN_IDS=123456789,987654321
GROUP_ID=-1001234567890
TOPIC_ID=1

# Remnawave API
PANEL_URL=https://panel.example.com
PANEL_SECRET_KEY=your_secret_key
PANEL_API_TOKEN=your_api_token

# Настройки пользователей
USER_TAG=ADMIN
EXTERNAL_SQUAD=uuid-of-external-squad
INTERNAL_SQUAD=uuid-of-internal-squad
HWID_LIMIT=1
TRAFFIC_LIMIT_GB=15

# Логирование
LOG_LEVEL=INFO
```

**Важно:** `EXTERNAL_SQUAD` и `INTERNAL_SQUAD` должны быть UUID squad'ов из панели Remnawave, а не их названия.

### Получение токена бота

1. Напишите [@BotFather](https://t.me/BotFather)
2. `/newbot` → создайте бота
3. Скопируйте токен в `BOT_TOKEN`
4. `/setprivacy` → `Disable`
5. `/setcommands` → добавьте: `start - Запуск бота`

### Настройка группы

1. Добавьте бота в группу как администратора
2. Дайте права: удаление сообщений, бан пользователей, приглашение
3. Получите GROUP_ID: `https://api.telegram.org/bot<TOKEN>/getUpdates`

## Как работает

1. Пользователь вступает в группу → приветственное сообщение с кнопкой
2. Нажимает "Получить доступ" → бот проверяет членство
3. Бот создает пользователя в Remnawave: `USER_wl-{telegram_id}`
4. Отправляет ссылку подписки в личные сообщения
5. При выходе из группы → отзыв подписки
6. При бане → удаление из панели

Вся информация хранится в Remnawave панели. Бот использует API для создания, проверки и удаления пользователей по username паттерну `USER_wl-{telegram_id}`.

## Технологии

- Python 3.13
- aiogram 3.15.0
- aiohttp 3.10.10
- pydantic-settings 2.6.1
- loguru 0.7.3
- Docker

## Управление

```bash
# Логи
docker-compose logs -f bot

# Перезапуск
docker-compose restart bot

# Остановка
docker-compose down

# Обновление
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## Лицензия

MIT
