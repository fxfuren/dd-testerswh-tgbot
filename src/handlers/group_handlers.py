from aiogram import Router, F
from aiogram.types import ChatMemberUpdated
from aiogram.filters import ChatMemberUpdatedFilter, KICKED, MEMBER, ADMINISTRATOR, CREATOR, RESTRICTED, LEFT
from loguru import logger
from config import settings
from api_client import api_client
from notifications import notify_access_revoked, notify_user_banned, notify_user_kicked

router = Router()


@router.chat_member(
    ChatMemberUpdatedFilter(
        member_status_changed=(KICKED | LEFT | RESTRICTED)
    )
)
async def on_user_left_or_banned(event: ChatMemberUpdated):
    """Обработка выхода, исключения или бана пользователя из группы"""
    
    # Проверяем, что событие произошло в нашей группе
    if event.chat.id != settings.GROUP_ID:
        return
    
    user = event.new_chat_member.user
    old_status = event.old_chat_member.status
    new_status = event.new_chat_member.status
    
    logger.info(
        f"User status changed in group: {user.id} (@{user.username}) "
        f"from {old_status} to {new_status}"
    )
    
    # Проверяем, был ли пользователь участником группы
    if old_status not in ["member", "administrator", "creator", "restricted"]:
        logger.info(f"User {user.id} old_status={old_status} not in allowed statuses, skipping")
        return
    
    logger.info(f"Processing user {user.id} status change, searching in panel...")
    
    # Получаем пользователя из панели по username USER_wl-{telegram_id}
    panel_username = f"USER_wl-{user.id}"
    panel_user = await api_client.get_user_by_username(panel_username)
    
    if not panel_user:
        logger.info(f"User {user.id} (username: {panel_username}) not found in panel, skipping")
        return
    
    logger.info(f"User {user.id} found in panel with UUID: {panel_user.get('uuid')}")
    
    uuid = panel_user.get('uuid')
    
    if not uuid:
        logger.warning(f"User {user.id} has no UUID in panel")
        return
    
    # Определяем причину и действие
    if new_status == "kicked":
        reason = "Бан в группе"
        logger.warning(f"User {user.id} was BANNED from group, revoking and deleting...")
        
        # Отзываем подписку и удаляем пользователя из панели
        await api_client.revoke_user_subscription(uuid)
        await api_client.delete_user(uuid)
        
        # Отправляем уведомления
        await notify_user_banned(
            event.bot,
            user.id,
            user.username
        )
        
    elif new_status in ["left", "restricted"]:
        reason = "Исключение из группы" if new_status == "left" else "Ограничение прав"
        logger.warning(f"User {user.id} LEFT or was KICKED from group, revoking subscription...")
        
        # Отзываем подписку
        await api_client.revoke_user_subscription(uuid)
        
        # Отправляем уведомления
        await notify_user_kicked(
            event.bot,
            user.id,
            user.username
        )


@router.chat_member(
    ChatMemberUpdatedFilter(
        member_status_changed=(MEMBER | ADMINISTRATOR | CREATOR)
    )
)
async def on_user_joined(event: ChatMemberUpdated):
    """Обработка вступления пользователя в группу"""
    
    # Проверяем, что событие произошло в нашей группе
    if event.chat.id != settings.GROUP_ID:
        return
    
    user = event.new_chat_member.user
    old_status = event.old_chat_member.status
    new_status = event.new_chat_member.status
    
    logger.info(
        f"User joined group: {user.id} (@{user.username}) "
        f"from {old_status} to {new_status}"
    )
    
    # Проверяем, что пользователь действительно присоединился
    if old_status in ["member", "administrator", "creator"]:
        return
    
    # Проверяем, есть ли пользователь в панели по username USER_wl-{telegram_id}
    panel_username = f"USER_wl-{user.id}"
    panel_user = await api_client.get_user_by_username(panel_username)
    
    if panel_user:
        is_active = panel_user.get('isActive', False)
        uuid = panel_user.get('uuid')
        
        # Если пользователь уже есть, но неактивен - активируем
        if not is_active and uuid:
            logger.info(f"Reactivating user {user.id}")
            await api_client.enable_user(uuid)
            
            # Отправляем уведомление
            try:
                await event.bot.send_message(
                    chat_id=user.id,
                    text=(
                        '<b><tg-emoji emoji-id="5870633910337015697">✅</tg-emoji> Доступ восстановлен!</b>\n\n'
                        'Вы снова вступили в группу, ваш доступ к VPN восстановлен.'
                    ),
                    parse_mode="HTML"
                )
            except Exception as e:
                logger.error(f"Failed to send reactivation message to {user.id}: {str(e)}")
        else:
            logger.info(f"User {user.id} already active")
    else:
        # Новый пользователь - отправляем приветствие
        logger.info(f"New user {user.id} joined group")
        
        try:
            await event.bot.send_message(
                chat_id=user.id,
                text=(
                    '<b><tg-emoji emoji-id="6041731551845159060">🎉</tg-emoji> Добро пожаловать!</b>\n\n'
                    'Вы вступили в группу. Для получения доступа к VPN напишите мне команду /start'
                ),
                parse_mode="HTML"
            )
        except Exception as e:
            logger.error(f"Failed to send welcome message to {user.id}: {str(e)}")
