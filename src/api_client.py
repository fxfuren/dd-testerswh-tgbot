import aiohttp
import asyncio
import ssl
from typing import Optional, Dict, Any
from loguru import logger
from src.config import settings


class RemnawaveAPI:
    """Клиент для работы с Remnawave Panel API"""
    
    def __init__(self):
        self.base_url = settings.PANEL_URL.rstrip('/')
        self.secret_key = settings.PANEL_SECRET_KEY
        self.api_token = settings.PANEL_API_TOKEN
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Получение или создание HTTP сессии"""
        if self.session is None or self.session.closed:
            # Создаем SSL контекст, который не проверяет сертификаты
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            
            # Добавляем заголовки браузера
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            }
            
            connector = aiohttp.TCPConnector(ssl=ssl_context, force_close=False, limit=100, limit_per_host=30)
            self.session = aiohttp.ClientSession(
                connector=connector,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=60, connect=30, sock_read=30)
            )
            
            # Устанавливаем cookie через специальный URL
            auth_url = f"{self.base_url}/auth/login?{self.secret_key}"
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    async with self.session.get(auth_url, allow_redirects=True) as response:
                        logger.info(f"Authentication request status: {response.status}")
                        if response.status == 200:
                            response_text = await response.text()
                            logger.debug(f"Authentication response length: {len(response_text)}")
                            logger.info("Authentication successful, cookie set")
                            break
                        else:
                            logger.warning(f"Authentication returned status {response.status}")
                except Exception as e:
                    logger.error(f"Failed to authenticate (attempt {attempt + 1}/{max_retries}): {str(e)}")
                    if attempt < max_retries - 1:
                        await asyncio.sleep(2)
                    else:
                        logger.error("All authentication attempts failed")
            
            # Обновляем заголовки после установки cookie
            self.session.headers.update({
                'Authorization': f'Bearer {self.api_token}',
                'Content-Type': 'application/json'
            })
        return self.session
    
    async def close(self):
        """Закрытие HTTP сессии"""
        if self.session and not self.session.closed:
            await self.session.close()
    
    async def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        """Выполнение HTTP запроса к API"""
        session = await self._get_session()
        url = f"{self.base_url}{endpoint}"
        
        try:
            async with session.request(method, url, json=data, params=params) as response:
                if response.status == 200 or response.status == 201:
                    return await response.json()
                else:
                    error_text = await response.text()
                    logger.error(f"API request failed: {method} {url} - Status: {response.status}, Error: {error_text}")
                    return None
        except Exception as e:
            logger.error(f"API request exception: {method} {url} - {str(e)}")
            return None
    
    async def create_user(self, telegram_id: int, username: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Создание пользователя в панели"""
        panel_username = f"USER_wl-{telegram_id}"
        
        # Вычисляем дату истечения (например, через 30 дней)
        from datetime import datetime, timedelta
        expire_at = (datetime.utcnow() + timedelta(days=30)).isoformat() + 'Z'
        
        user_data = {
            "username": panel_username,
            "telegramId": telegram_id,  # Должен быть integer, а не string
            "expireAt": expire_at,  # Обязательное поле
            "tags": [settings.USER_TAG],
            "externalSquad": settings.EXTERNAL_SQUAD,
            "internalSquad": settings.INTERNAL_SQUAD,
            "hwidLimit": settings.HWID_LIMIT
        }
        
        logger.info(f"Creating user in panel: {panel_username} (TG ID: {telegram_id})")
        result = await self._request('POST', '/api/users', data=user_data)
        
        if result:
            logger.success(f"User created successfully: {panel_username}")
            logger.debug(f"create_user response: {result}")
        else:
            logger.error(f"Failed to create user: {panel_username}")
        
        return result
        return result
    
    async def get_user_by_telegram_id(self, telegram_id: int) -> Optional[Dict[str, Any]]:
        """Получение пользователя по Telegram ID"""
        result = await self._request('GET', f'/api/users/by-telegram-id/{telegram_id}')
        logger.debug(f"get_user_by_telegram_id response: {result}")
        
        # API возвращает объект с ключом 'response', содержащий массив пользователей
        if result and 'response' in result and len(result['response']) > 0:
            return result['response'][0]  # Возвращаем первого пользователя
        
        return None
    
    async def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """Получение пользователя по username"""
        result = await self._request('GET', f'/api/users/by-username/{username}')
        logger.debug(f"get_user_by_username response: {result}")
        
        # API возвращает объект с ключом 'response'
        if result and 'response' in result:
            return result['response']
        
        return None
    
    async def get_user_by_uuid(self, uuid: str) -> Optional[Dict[str, Any]]:
        """Получение пользователя по UUID"""
        result = await self._request('GET', f'/api/users/{uuid}')
        return result
    
    async def revoke_user_subscription(self, uuid: str) -> Optional[Dict[str, Any]]:
        """Отзыв подписки пользователя"""
        logger.info(f"Revoking subscription for user UUID: {uuid}")
        result = await self._request('POST', f'/api/users/{uuid}/actions/revoke', data={})
        
        if result:
            logger.success(f"Subscription revoked for user UUID: {uuid}")
        else:
            logger.error(f"Failed to revoke subscription for user UUID: {uuid}")
        
        return result
    
    async def disable_user(self, uuid: str) -> Optional[Dict[str, Any]]:
        """Отключение пользователя"""
        logger.info(f"Disabling user UUID: {uuid}")
        result = await self._request('POST', f'/api/users/{uuid}/actions/disable')
        
        if result:
            logger.success(f"User disabled: {uuid}")
        else:
            logger.error(f"Failed to disable user: {uuid}")
        
        return result
    
    async def enable_user(self, uuid: str) -> Optional[Dict[str, Any]]:
        """Включение пользователя"""
        logger.info(f"Enabling user UUID: {uuid}")
        result = await self._request('POST', f'/api/users/{uuid}/actions/enable')
        
        if result:
            logger.success(f"User enabled: {uuid}")
        else:
            logger.error(f"Failed to enable user: {uuid}")
        
        return result
    
    async def delete_user(self, uuid: str) -> Optional[Dict[str, Any]]:
        """Удаление пользователя"""
        logger.info(f"Deleting user UUID: {uuid}")
        result = await self._request('DELETE', f'/api/users/{uuid}')
        
        if result:
            logger.success(f"User deleted: {uuid}")
        else:
            logger.error(f"Failed to delete user: {uuid}")
        
        return result
    
    async def get_user_accessible_nodes(self, uuid: str) -> Optional[Dict[str, Any]]:
        """Получение доступных нод для пользователя"""
        result = await self._request('GET', f'/api/users/{uuid}/accessible-nodes')
        return result


# Глобальный экземпляр API клиента
api_client = RemnawaveAPI()
