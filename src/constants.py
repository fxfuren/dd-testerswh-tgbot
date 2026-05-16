"""
Константы для бота
"""

# Версия бота
BOT_VERSION = "1.0.0"

# Максимальные значения
MAX_USERNAME_LENGTH = 32
MAX_MESSAGE_LENGTH = 4096
MAX_CAPTION_LENGTH = 1024
MAX_BROADCAST_USERS = 1000

# Таймауты (в секундах)
API_TIMEOUT = 30
DATABASE_TIMEOUT = 10
NOTIFICATION_TIMEOUT = 5

# Интервалы (в секундах)
RETRY_INTERVAL = 5
CLEANUP_INTERVAL = 3600  # 1 час

# Лимиты
MAX_RETRIES = 3
MAX_LOGS_PER_USER = 100
MAX_USERS_PER_PAGE = 20

# Статусы пользователей
USER_STATUS_ACTIVE = "active"
USER_STATUS_INACTIVE = "inactive"
USER_STATUS_BANNED = "banned"

# Действия в логах
ACTION_GRANTED = "granted"
ACTION_REVOKED = "revoked"
ACTION_BANNED = "banned"
ACTION_KICKED = "kicked"
ACTION_REACTIVATED = "reactivated"

# Типы уведомлений
NOTIFICATION_TYPE_ACCESS_GRANTED = "access_granted"
NOTIFICATION_TYPE_ACCESS_REVOKED = "access_revoked"
NOTIFICATION_TYPE_USER_BANNED = "user_banned"
NOTIFICATION_TYPE_USER_KICKED = "user_kicked"

# Сообщения об ошибках
ERROR_USER_NOT_FOUND = "Пользователь не найден"
ERROR_ACCESS_DENIED = "Доступ запрещен"
ERROR_NOT_IN_GROUP = "Вы не состоите в группе"
ERROR_ALREADY_HAS_ACCESS = "У вас уже есть доступ"
ERROR_API_ERROR = "Ошибка API панели"
ERROR_DATABASE_ERROR = "Ошибка базы данных"
ERROR_UNKNOWN = "Неизвестная ошибка"

# Сообщения об успехе
SUCCESS_ACCESS_GRANTED = "Доступ предоставлен"
SUCCESS_ACCESS_REVOKED = "Доступ отозван"
SUCCESS_USER_CREATED = "Пользователь создан"
SUCCESS_USER_UPDATED = "Пользователь обновлен"
SUCCESS_USER_DELETED = "Пользователь удален"

# Callback data префиксы
CB_MAIN_MENU = "main_menu"
CB_PROFILE = "profile"
CB_GET_ACCESS = "get_access"
CB_HELP = "help"
CB_ADMIN = "admin"
CB_ADMIN_STATS = "admin_stats"
CB_ADMIN_USERS = "admin_users"
CB_ADMIN_BROADCAST = "admin_broadcast"
CB_CANCEL = "cancel"
CB_CONFIRM = "confirm"
CB_BACK = "back"

# Форматы дат
DATE_FORMAT_FULL = "%d.%m.%Y %H:%M:%S"
DATE_FORMAT_SHORT = "%d.%m.%Y %H:%M"
DATE_FORMAT_DATE = "%d.%m.%Y"
DATE_FORMAT_TIME = "%H:%M:%S"

# Префиксы для логирования
LOG_PREFIX_API = "[API]"
LOG_PREFIX_DB = "[DB]"
LOG_PREFIX_BOT = "[BOT]"
LOG_PREFIX_GROUP = "[GROUP]"
LOG_PREFIX_USER = "[USER]"
LOG_PREFIX_ADMIN = "[ADMIN]"

# Эмодзи для статусов (fallback если премиум недоступны)
EMOJI_SUCCESS = "✅"
EMOJI_ERROR = "❌"
EMOJI_WARNING = "⚠️"
EMOJI_INFO = "ℹ️"
EMOJI_LOADING = "⏳"
EMOJI_LOCK = "🔒"
EMOJI_UNLOCK = "🔓"
EMOJI_USER = "👤"
EMOJI_USERS = "👥"
EMOJI_SETTINGS = "⚙️"
EMOJI_STATS = "📊"
EMOJI_NOTIFICATION = "🔔"
