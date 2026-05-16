"""
Middleware для бота
"""
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User
from loguru import logger
from datetime import datetime


class LoggingMiddleware(BaseMiddleware):
    """Middleware для логирования всех событий"""
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        user: User = data.get("event_from_user")
        
        if user:
            logger.info(
                f"Event from user {user.id} (@{user.username}): {event.__class__.__name__}"
            )
        
        start_time = datetime.utcnow()
        
        try:
            result = await handler(event, data)
            return result
        except Exception as e:
            logger.error(f"Error in handler: {str(e)}", exc_info=True)
            raise
        finally:
            duration = (datetime.utcnow() - start_time).total_seconds()
            logger.debug(f"Handler execution time: {duration:.3f}s")


class ThrottlingMiddleware(BaseMiddleware):
    """Middleware для защиты от спама"""
    
    def __init__(self, rate_limit: float = 1.0):
        self.rate_limit = rate_limit
        self.user_timestamps: Dict[int, datetime] = {}
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        user: User = data.get("event_from_user")
        
        if not user:
            return await handler(event, data)
        
        now = datetime.utcnow()
        last_time = self.user_timestamps.get(user.id)
        
        if last_time:
            time_passed = (now - last_time).total_seconds()
            if time_passed < self.rate_limit:
                logger.warning(f"Throttling user {user.id}: too many requests")
                return None
        
        self.user_timestamps[user.id] = now
        return await handler(event, data)
