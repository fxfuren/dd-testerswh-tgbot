from typing import Optional

from aiogram import Bot
from aiogram.enums import ParseMode
from loguru import logger

from config import settings
from keyboards import Emoji, get_back_to_menu_keyboard
from utils import escape_html


async def send_notification_to_user(
    bot: Bot,
    telegram_id: int,
    message: str,
    parse_mode: ParseMode = ParseMode.HTML,
) -> bool:
    """Отправка уведомления пользователю в ЛС"""
    try:
        await bot.send_message(
            chat_id=telegram_id,
            text=message,
            parse_mode=parse_mode,
            reply_markup=get_back_to_menu_keyboard(),
        )
        logger.info(f"Notification sent to user {telegram_id}")
        return True
    except Exception as e:
        logger.error(
            f"Failed to send notification to user {telegram_id}: {str(e)}"
        )
        return False


async def send_notification_to_group(
    bot: Bot, message: str, parse_mode: ParseMode = ParseMode.HTML
) -> bool:
    """Отправка уведомления в группу в топик"""
    try:
        await bot.send_message(
            chat_id=settings.GROUP_ID,
            message_thread_id=settings.TOPIC_ID,
            text=message,
            parse_mode=parse_mode,
        )
        logger.info("Notification sent to group topic")
        return True
    except Exception as e:
        logger.error(f"Failed to send notification to group: {str(e)}")
        return False


async def notify_access_granted(
    bot: Bot,
    telegram_id: int,
    username: Optional[str] = None,
    panel_username: str = "",
):
    """Уведомление о предоставлении доступа"""
    user_mention = f"@{escape_html(username)}" if username else f"ID: {telegram_id}"

    # Уведомление пользователю
    user_message = (
        f'<b><tg-emoji emoji-id="{Emoji.CHECK}">✅</tg-emoji> Доступ предоставлен!</b>\n\n'
        f'<tg-emoji emoji-id="{Emoji.PROFILE}">👤</tg-emoji> <b>Ваш id:</b> <code>{panel_username}</code>\n\n'
        f'<tg-emoji emoji-id="{Emoji.INFO}">ℹ️</tg-emoji> Теперь вы можете использовать VPN сервис.\n'
        f"Для получения конфигурации обратитесь к администратору."
    )
    await send_notification_to_user(bot, telegram_id, user_message)

    # Уведомление в группу
    group_message = (
        f'<b><tg-emoji emoji-id="{Emoji.PERSON_CHECK}">👤</tg-emoji> Новый пользователь</b>\n\n'
        f'<tg-emoji emoji-id="{Emoji.PROFILE}">👤</tg-emoji> <b>Пользователь:</b> {user_mention}\n'
        f'<tg-emoji emoji-id="{Emoji.TAG}">🏷</tg-emoji> <b>Ваш id:</b> <code>{panel_username}</code>\n'
        f'<tg-emoji emoji-id="{Emoji.CHECK}">✅</tg-emoji> <b>Статус:</b> Доступ предоставлен'
    )
    await send_notification_to_group(bot, group_message)


async def notify_access_revoked(
    bot: Bot,
    telegram_id: int,
    username: Optional[str] = None,
    reason: str = "Исключение из группы",
):
    """Уведомление об отзыве доступа"""
    user_mention = f"@{escape_html(username)}" if username else f"ID: {telegram_id}"

    # Уведомление пользователю
    user_message = (
        f'<b><tg-emoji emoji-id="{Emoji.CROSS}">❌</tg-emoji> Доступ отозван</b>\n\n'
        f'<tg-emoji emoji-id="{Emoji.INFO}">ℹ️</tg-emoji> <b>Причина:</b> {reason}\n\n'
        f"Ваша подписка была деактивирована.\n"
        f"Для восстановления доступа обратитесь к администратору."
    )
    await send_notification_to_user(bot, telegram_id, user_message)

    # Уведомление в группу
    group_message = (
        f'<b><tg-emoji emoji-id="{Emoji.PERSON_CROSS}">👤</tg-emoji> Доступ отозван</b>\n\n'
        f'<tg-emoji emoji-id="{Emoji.PROFILE}">👤</tg-emoji> <b>Пользователь:</b> {user_mention}\n'
        f'<tg-emoji emoji-id="{Emoji.INFO}">ℹ️</tg-emoji> <b>Причина:</b> {reason}\n'
        f'<tg-emoji emoji-id="{Emoji.CROSS}">❌</tg-emoji> <b>Статус:</b> Подписка деактивирована'
    )
    await send_notification_to_group(bot, group_message)


async def notify_user_banned(
    bot: Bot, telegram_id: int, username: Optional[str] = None
):
    """Уведомление о бане пользователя"""
    user_mention = f"@{escape_html(username)}" if username else f"ID: {telegram_id}"

    # Уведомление пользователю
    user_message = (
        f'<b><tg-emoji emoji-id="{Emoji.LOCK_CLOSED}">🔒</tg-emoji> Вы были заблокированы</b>\n\n'
        f'<tg-emoji emoji-id="{Emoji.INFO}">ℹ️</tg-emoji> Ваш доступ к тестовой подписке был заблокирован.\n'
        f"Для получения дополнительной информации обратитесь к администратору."
    )
    await send_notification_to_user(bot, telegram_id, user_message)

    # Уведомление в группу
    group_message = (
        f'<b><tg-emoji emoji-id="{Emoji.LOCK_CLOSED}">🔒</tg-emoji> Пользователь заблокирован</b>\n\n'
        f'<tg-emoji emoji-id="{Emoji.PROFILE}">👤</tg-emoji> <b>Пользователь:</b> {user_mention}\n'
        f'<tg-emoji emoji-id="{Emoji.CROSS}">❌</tg-emoji> <b>Статус:</b> Заблокирован и удален из группы'
    )
    await send_notification_to_group(bot, group_message)


async def notify_user_kicked(
    bot: Bot, telegram_id: int, username: Optional[str] = None
):
    """Уведомление об исключении пользователя"""
    user_mention = f"@{escape_html(username)}" if username else f"ID: {telegram_id}"

    # Уведомление пользователю
    user_message = (
        f'<b><tg-emoji emoji-id="{Emoji.CROSS}">❌</tg-emoji> Вы были исключены из группы</b>\n\n'
        f'<tg-emoji emoji-id="{Emoji.INFO}">ℹ️</tg-emoji> Ваш доступ к тестовой подписке был отозван."\n'
    )
    await send_notification_to_user(bot, telegram_id, user_message)

    # Уведомление в группу
    group_message = (
        f'<b><tg-emoji emoji-id="{Emoji.PERSON_CROSS}">👤</tg-emoji> Пользователь исключен</b>\n\n'
        f'<tg-emoji emoji-id="{Emoji.PROFILE}">👤</tg-emoji> <b>Пользователь:</b> {user_mention}\n'
        f'<tg-emoji emoji-id="{Emoji.CROSS}">❌</tg-emoji> <b>Статус:</b> Исключен, подписка отозвана'
    )
    await send_notification_to_group(bot, group_message)


async def notify_admins(
    bot: Bot, message: str, parse_mode: ParseMode = ParseMode.HTML
):
    """Отправка уведомления всем администраторам"""
    for admin_id in settings.admin_ids_list:
        try:
            await bot.send_message(
                chat_id=admin_id, text=message, parse_mode=parse_mode
            )
            logger.info(f"Admin notification sent to {admin_id}")
        except Exception as e:
            logger.error(
                f"Failed to send admin notification to {admin_id}: {str(e)}"
            )


async def broadcast_message(
    bot: Bot,
    user_ids: list[int],
    message: str,
    parse_mode: ParseMode = ParseMode.HTML,
) -> tuple[int, int]:
    """Рассылка сообщения пользователям"""
    success_count = 0
    fail_count = 0

    for user_id in user_ids:
        try:
            await bot.send_message(
                chat_id=user_id,
                text=message,
                parse_mode=parse_mode,
                reply_markup=get_back_to_menu_keyboard(),
            )
            success_count += 1
            logger.info(f"Broadcast message sent to {user_id}")
        except Exception as e:
            fail_count += 1
            logger.error(f"Failed to send broadcast to {user_id}: {str(e)}")

    return success_count, fail_count
