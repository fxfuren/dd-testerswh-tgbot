from aiogram import F, Router
from aiogram.enums import ChatType, ParseMode
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message
from loguru import logger

from api_client import api_client
from config import settings
from keyboards import (
    Emoji,
    get_back_to_menu_keyboard,
    get_main_menu_keyboard,
)

router = Router()

# Кэш для хранения ID последних сообщений пользователей
user_messages = {}


async def edit_or_send_message(
    message: Message,
    text: str,
    reply_markup=None,
    parse_mode: ParseMode = ParseMode.HTML,
):
    """Редактирование существующего сообщения или отправка нового"""
    user_id = message.from_user.id

    if user_id in user_messages:
        try:
            await message.bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=user_messages[user_id],
                text=text,
                reply_markup=reply_markup,
                parse_mode=parse_mode,
            )
            return
        except Exception:
            pass

    # Отправляем новое сообщение
    sent_message = await message.answer(
        text=text, reply_markup=reply_markup, parse_mode=parse_mode
    )
    user_messages[user_id] = sent_message.message_id


async def edit_callback_message(
    callback: CallbackQuery,
    text: str,
    reply_markup=None,
    parse_mode: ParseMode = ParseMode.HTML,
):
    """Редактирование сообщения из callback"""
    try:
        await callback.message.edit_text(
            text=text, reply_markup=reply_markup, parse_mode=parse_mode
        )
    except Exception as e:
        logger.warning(f"Failed to edit message: {str(e)}")
        await callback.message.answer(
            text=text, reply_markup=reply_markup, parse_mode=parse_mode
        )


@router.message(CommandStart())
async def cmd_start(message: Message):
    """Обработка команды /start"""

    if message.chat.type != ChatType.PRIVATE:
        return

    user = message.from_user

    # Очищаем кэш сообщений для этого пользователя, чтобы отправить новое сообщение
    if user.id in user_messages:
        del user_messages[user.id]

    welcome_text = (
        f'<b><tg-emoji emoji-id="{Emoji.PARTY}">🎉</tg-emoji> Добро пожаловать, {user.first_name}!</b>\n\n'
        f'<tg-emoji emoji-id="{Emoji.BOT}">🤖</tg-emoji> Я бот для управления доступом к тестовой подписке.\n\n'
        f'<tg-emoji emoji-id="{Emoji.INFO}">ℹ️</tg-emoji> Для получения доступа:\n'
        f"1. Запросите ссылку для входа в группу у администратора\n"
        f"2. Вступите в группу по предоставленной ссылке\n"
        f"3. Запросите доступ через меню\n\n"
        f"Выберите действие:"
    )

    await edit_or_send_message(
        message, welcome_text, reply_markup=get_main_menu_keyboard()
    )


@router.callback_query(F.data == "main_menu")
async def callback_main_menu(callback: CallbackQuery):
    """Главное меню"""
    await callback.answer()

    text = (
        f'<b><tg-emoji emoji-id="{Emoji.HOME}">🏘</tg-emoji> Главное меню</b>\n\n'
        f'<tg-emoji emoji-id="{Emoji.INFO}">ℹ️</tg-emoji> Выберите действие:'
    )

    await edit_callback_message(
        callback, text, reply_markup=get_main_menu_keyboard()
    )




@router.callback_query(F.data == "get_access")
async def callback_get_access(callback: CallbackQuery):
    """Запрос доступа к тестовой подписке"""
    await callback.answer()

    user = callback.from_user

    # Проверяем членство в группе
    try:
        member = await callback.bot.get_chat_member(settings.GROUP_ID, user.id)

        if member.status in ["left", "kicked"]:
            text = (
                f'<b><tg-emoji emoji-id="{Emoji.CROSS}">❌</tg-emoji> Доступ запрещен</b>\n\n'
                f'<tg-emoji emoji-id="{Emoji.INFO}">ℹ️</tg-emoji> Для получения доступа запросите ссылку у администратора.\n\n'
                f"После вступления вернитесь и запросите доступ снова."
            )

            await edit_callback_message(
                callback, text, reply_markup=get_back_to_menu_keyboard()
            )
            return
    except Exception as e:
        logger.error(f"Error checking group membership: {str(e)}")
        text = (
            f'<b><tg-emoji emoji-id="{Emoji.CROSS}">❌</tg-emoji> Ошибка проверки</b>\n\n'
            f"Не удалось проверить членство в группе. Попробуйте позже."
        )
        await edit_callback_message(
            callback, text, reply_markup=get_back_to_menu_keyboard()
        )
        return

    # Проверяем, есть ли уже пользователь в панели с именем USER_wl-{telegram_id}
    panel_username = f"USER_wl-{user.id}"
    panel_user = await api_client.get_user_by_username(panel_username)

    if panel_user:
        is_active = panel_user.get("isActive", False)
        username = panel_user.get("username", "")
        subscription_url = panel_user.get("subscriptionUrl", "")

        if is_active:
            text = (
                f'<b><tg-emoji emoji-id="{Emoji.CHECK}">✅</tg-emoji> У вас уже есть доступ</b>\n\n'
                f'<tg-emoji emoji-id="{Emoji.TAG}">🏷</tg-emoji> <b>Ваш id:</b> <code>{username}</code>\n\n'
            )
            if subscription_url:
                text += f'<tg-emoji emoji-id="{Emoji.LINK}">🔗</tg-emoji> <b>Ссылка подписки:</b>\n<code>{subscription_url}</code>\n\n'
        else:
            # Реактивируем пользователя
            uuid = panel_user.get("uuid")
            if uuid:
                result = await api_client.enable_user(uuid)
                # Получаем обновленные данные пользователя
                panel_user = await api_client.get_user_by_username(
                    panel_username
                )
                if panel_user:
                    subscription_url = panel_user.get("subscriptionUrl", "")

            text = (
                f'<b><tg-emoji emoji-id="{Emoji.CHECK}">✅</tg-emoji> Доступ восстановлен!</b>\n\n'
                f'<tg-emoji emoji-id="{Emoji.TAG}">🏷</tg-emoji> <b>Ваш id:</b> <code>{username}</code>\n\n'
            )
            if subscription_url:
                text += f'<tg-emoji emoji-id="{Emoji.LINK}">🔗</tg-emoji> <b>Ссылка подписки:</b>\n<code>{subscription_url}</code>\n\n'
            text += "Ваш доступ к тестовой подписке был восстановлен."
    else:
        # Создаем нового пользователя
        text = (
            f'<b><tg-emoji emoji-id="{Emoji.LOADING}">🔄</tg-emoji> Создание аккаунта...</b>\n\n'
            f"Пожалуйста, подождите..."
        )
        await edit_callback_message(callback, text)

        # Создаем пользователя в панели
        panel_result = await api_client.create_user(user.id, user.username)

        if panel_result:
            # API возвращает данные в формате {'response': {...}}
            user_data = panel_result.get("response", panel_result)
            subscription_url = user_data.get("subscriptionUrl", "")

            # Отправляем уведомление в группу (без уведомления пользователю, так как оно уже будет отправлено ниже)
            user_mention = (
                f"@{user.username}" if user.username else f"ID: {user.id}"
            )
            group_message = (
                f'<b><tg-emoji emoji-id="{Emoji.PERSON_CHECK}">👤</tg-emoji> Новый пользователь</b>\n\n'
                f'<tg-emoji emoji-id="{Emoji.PROFILE}">👤</tg-emoji> <b>Пользователь:</b> {user_mention}\n'
                f'<tg-emoji emoji-id="{Emoji.TAG}">🏷</tg-emoji> <b>Ваш id:</b> <code>{panel_username}</code>\n'
                f'<tg-emoji emoji-id="{Emoji.CHECK}">✅</tg-emoji> <b>Статус:</b> Доступ предоставлен'
            )
            try:
                await callback.bot.send_message(
                    chat_id=settings.GROUP_ID,
                    message_thread_id=settings.TOPIC_ID,
                    text=group_message,
                    parse_mode=ParseMode.HTML,
                )
            except Exception as e:
                logger.error(f"Failed to send notification to group: {str(e)}")

            text = (
                f'<b><tg-emoji emoji-id="{Emoji.CHECK}">✅</tg-emoji> Доступ предоставлен!</b>\n\n'
                f'<tg-emoji emoji-id="{Emoji.TAG}">🏷</tg-emoji> <b>Ваш id:</b> <code>{panel_username}</code>\n\n'
            )
            if subscription_url:
                text += f'<tg-emoji emoji-id="{Emoji.LINK}">🔗</tg-emoji> <b>Ссылка подписки:</b>\n<code>{subscription_url}</code>\n\n'
            text += f'<tg-emoji emoji-id="{Emoji.INFO}">ℹ️</tg-emoji> Скопируйте ссылку подписки и добавьте её в Happ.\n'
        else:
            text = (
                f'<b><tg-emoji emoji-id="{Emoji.CROSS}">❌</tg-emoji> Ошибка создания аккаунта</b>\n\n'
                f"Не удалось создать аккаунт. Попробуйте позже или обратитесь к администратору."
            )

    await edit_callback_message(
        callback, text, reply_markup=get_back_to_menu_keyboard()
    )


@router.callback_query(F.data == "help")
async def callback_help(callback: CallbackQuery):
    """Помощь"""
    await callback.answer()

    text = (
        f'<b><tg-emoji emoji-id="{Emoji.INFO}">ℹ️</tg-emoji> Помощь</b>\n\n'
        f"<b>Как получить доступ:</b>\n"
        f"1. Вступите в нашу группу\n"
        f'2. Нажмите "Получить доступ" в главном меню\n'
        f"3. Получите логин для панели\n"
        f"4. Обратитесь к администратору за конфигурацией\n\n"
        f"<b>Важно:</b>\n"
        f"• Если вы покинете группу, доступ будет отозван\n"
        f"• При бане в группе аккаунт будет удален\n"
        f"• Для восстановления доступа вступите в группу заново\n\n"
        f'<tg-emoji emoji-id="{Emoji.MEGAPHONE}">📣</tg-emoji> По всем вопросам обращайтесь к администраторам группы.'
    )

    await edit_callback_message(
        callback, text, reply_markup=get_back_to_menu_keyboard()
    )
