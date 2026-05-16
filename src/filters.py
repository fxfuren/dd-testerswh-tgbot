"""
Фильтры для бота
"""
from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery
from src.config import settings
from typing import Union


class IsAdminFilter(Filter):
    """Фильтр для проверки, является ли пользователь администратором"""
    
    async def __call__(self, event: Union[Message, CallbackQuery]) -> bool:
        user_id = event.from_user.id
        return user_id in settings.admin_ids_list


class IsPrivateChatFilter(Filter):
    """Фильтр для проверки, что сообщение в личном чате"""
    
    async def __call__(self, message: Message) -> bool:
        return message.chat.type == "private"


class IsGroupChatFilter(Filter):
    """Фильтр для проверки, что сообщение в группе"""
    
    async def __call__(self, message: Message) -> bool:
        return message.chat.type in ["group", "supergroup"]


class IsTargetGroupFilter(Filter):
    """Фильтр для проверки, что событие в целевой группе"""
    
    async def __call__(self, event: Union[Message, CallbackQuery]) -> bool:
        if isinstance(event, Message):
            return event.chat.id == settings.GROUP_ID
        return False
