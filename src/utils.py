"""
Утилиты для работы с ботом
"""
from typing import Optional
from datetime import datetime, timedelta


def format_datetime(dt: datetime, format_type: str = "full") -> str:
    """Форматирование даты и времени"""
    if format_type == "full":
        return dt.strftime("%d.%m.%Y %H:%M:%S")
    elif format_type == "date":
        return dt.strftime("%d.%m.%Y")
    elif format_type == "time":
        return dt.strftime("%H:%M:%S")
    elif format_type == "short":
        return dt.strftime("%d.%m.%Y %H:%M")
    return str(dt)


def format_timedelta(td: timedelta) -> str:
    """Форматирование временного интервала"""
    days = td.days
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    parts = []
    if days > 0:
        parts.append(f"{days}д")
    if hours > 0:
        parts.append(f"{hours}ч")
    if minutes > 0:
        parts.append(f"{minutes}м")
    if seconds > 0 or not parts:
        parts.append(f"{seconds}с")
    
    return " ".join(parts)


def escape_html(text: str) -> str:
    """Экранирование HTML символов"""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def format_bytes(bytes_count: int) -> str:
    """Форматирование размера в байтах"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_count < 1024.0:
            return f"{bytes_count:.2f} {unit}"
        bytes_count /= 1024.0
    return f"{bytes_count:.2f} PB"


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Обрезка текста с добавлением суффикса"""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def get_user_mention(
    user_id: int,
    username: Optional[str] = None,
    first_name: Optional[str] = None
) -> str:
    """Получение упоминания пользователя"""
    if username:
        return f"@{username}"
    elif first_name:
        return f'<a href="tg://user?id={user_id}">{escape_html(first_name)}</a>'
    else:
        return f"ID: {user_id}"


def validate_telegram_id(telegram_id: int) -> bool:
    """Валидация Telegram ID"""
    return isinstance(telegram_id, int) and telegram_id > 0


def validate_username(username: str) -> bool:
    """Валидация Telegram username"""
    if not username:
        return False
    # Username должен быть от 5 до 32 символов, содержать только буквы, цифры и подчеркивания
    return (
        5 <= len(username) <= 32 and
        username.replace('_', '').isalnum() and
        not username[0].isdigit()
    )


def parse_group_link(link: str) -> Optional[tuple[int, int]]:
    """Парсинг ссылки на группу/топик
    
    Возвращает (group_id, topic_id) или None
    """
    try:
        # Формат: https://t.me/c/1234567890/123
        if '/c/' in link:
            parts = link.split('/c/')[1].split('/')
            if len(parts) >= 2:
                group_id = -1000000000000 - int(parts[0])
                topic_id = int(parts[1])
                return (group_id, topic_id)
    except (ValueError, IndexError):
        pass
    return None


def is_admin(user_id: int, admin_ids: list[int]) -> bool:
    """Проверка, является ли пользователь администратором"""
    return user_id in admin_ids


def get_time_until(target_time: datetime) -> str:
    """Получение времени до указанной даты"""
    now = datetime.utcnow()
    if target_time <= now:
        return "Истекло"
    
    delta = target_time - now
    return format_timedelta(delta)


def get_time_since(past_time: datetime) -> str:
    """Получение времени с указанной даты"""
    now = datetime.utcnow()
    if past_time >= now:
        return "Только что"
    
    delta = now - past_time
    return format_timedelta(delta) + " назад"
