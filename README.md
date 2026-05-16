# Remnawave Telegram VPN Bot

Telegram бот для автоматического управления доступом к VPN через Remnawave панель.

## Возможности

- 🔐 Автоматическое создание пользователей в Remnawave панели
- 🔗 Автоматическая выдача ссылки подписки
- 👥 Мониторинг членства в Telegram группе
- 🚫 Автоматический отзыв доступа при выходе/бане
- 📢 Уведомления в группу и личные сообщения
- 🎨 Премиум эмодзи Telegram
- ⚡ Без базы данных - вся информация в Remnawave панели

## Быстрый старт

### Локальный запуск

```bash
# 1. Установить зависимости
pip install -r requirements.txt

# 2. Настроить .env файл
cp .env.example .env
nano .env

# 3. Запустить бота
python -m src.main
```

### Docker

```bash
# 1. Настроить .env файл
nano .env

# 2. Запустить
docker-compose up -d

# 3. Проверить логи
docker-compose logs -f bot
```

## Структура проекта

```
dd-testerswh-tgbot/
├── src/                    # Исходный код
│   ├── handlers/          # Обработчики событий
│   │   ├── user_handlers.py    # Команды пользователей
│   │   └── group_handlers.py   # События группы
│   ├── tests/             # Unit тесты
│   ├── main.py            # Точка входа
│   ├── config.py          # Конфигурация
│   ├── api_client.py      # API клиент Remnawave
│   ├── keyboards.py       # Клавиатуры и эмодзи
│   ├── notifications.py   # Система уведомлений
│   ├── middlewares.py     # Middleware
│   ├── filters.py         # Фильтры
│   ├── states.py          # FSM состояния
│   ├── utils.py           # Утилиты
│   └── constants.py       # Константы
├── logs/                  # Логи (создается автоматически)
├── .env                   # Конфигурация (создать вручную)
├── docker-compose.yml     # Docker Compose
├── Dockerfile             # Docker образ
├── requirements.txt       # Python зависимости
└── requirements-dev.txt   # Dev зависимости
```

## Настройка

### 1. Создайте .env файл

```env
# Telegram Bot
BOT_TOKEN=your_bot_token_here
ADMIN_IDS=123456789,987654321

# Group Settings
GROUP_ID=-1001234567890
TOPIC_ID=1

# Remnawave Panel API
PANEL_URL=https://panel.example.com
PANEL_SECRET_KEY=your_secret_key
PANEL_API_TOKEN=your_api_token

# User Settings
USER_TAG=ADMIN
EXTERNAL_SQUAD=WL-ADMIN-squad
INTERNAL_SQUAD=ADMIN-WHITE-LIST
HWID_LIMIT=1

# Logging
LOG_LEVEL=INFO
```

### 2. Получите токен бота

1. Напишите [@BotFather](https://t.me/BotFather)
2. Создайте нового бота: `/newbot`
3. Скопируйте токен в `BOT_TOKEN`

### 3. Настройте бота в BotFather

1. Отключите приватность: `/setprivacy` → `Disable`
2. Добавьте команды: `/setcommands`
```
start - Запуск бота
```

### 4. Добавьте бота в группу

- Добавьте бота как администратора
- Дайте права: удаление сообщений, бан пользователей, приглашение пользователей

### 5. Получите GROUP_ID

1. Добавьте бота в группу
2. Напишите что-нибудь в группе
3. Откройте: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
4. Найдите `"chat":{"id":-1001234567890}` - это ваш GROUP_ID

## Как работает

1. **Пользователь вступает в группу** → Бот отправляет приветственное сообщение
2. **Пользователь нажимает "Получить доступ"** → Бот проверяет членство в группе
3. **Бот создает пользователя** → В панели Remnawave с именем `USER_wl-{telegram_id}`
4. **Бот отправляет ссылку подписки** → Пользователь получает ссылку для VPN клиента
5. **Пользователь покидает группу** → Бот отзывает подписку
6. **Пользователь забанен** → Бот удаляет пользователя из панели

## Архитектура

Бот работает **без собственной базы данных**. Вся информация о пользователях хранится в Remnawave панели:
- При запросе доступа бот создает пользователя в панели через API
- При проверке статуса бот запрашивает данные из панели по username `USER_wl-{telegram_id}`
- При выходе из группы бот отзывает доступ через API панели
- При бане бот удаляет пользователя из панели

Это упрощает архитектуру и исключает необходимость синхронизации данных.

## Технологии

- Python 3.13
- aiogram 3.15.0 (Telegram Bot framework)
- aiohttp 3.10.10 (HTTP клиент)
- pydantic-settings 2.6.1 (Конфигурация)
- loguru 0.7.3 (Логирование)
- Docker & Docker Compose
- Без базы данных

## Управление

```bash
# Просмотр логов
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
