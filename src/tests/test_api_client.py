"""
Тесты для API клиента
"""
import pytest
from unittest.mock import AsyncMock, patch
from src.api_client import RemnawaveAPI


@pytest.fixture
def api_client():
    """Фикстура для API клиента"""
    return RemnawaveAPI()


@pytest.mark.asyncio
async def test_create_user(api_client):
    """Тест создания пользователя"""
    with patch.object(api_client, '_request', new_callable=AsyncMock) as mock_request:
        mock_request.return_value = {
            'success': True,
            'data': {
                'uuid': 'test-uuid-123',
                'username': 'USER_wl-123456789'
            }
        }
        
        result = await api_client.create_user(123456789, 'testuser')
        
        assert result is not None
        assert result['success'] is True
        assert 'uuid' in result['data']
        mock_request.assert_called_once()


@pytest.mark.asyncio
async def test_get_user_by_telegram_id(api_client):
    """Тест получения пользователя по Telegram ID"""
    with patch.object(api_client, '_request', new_callable=AsyncMock) as mock_request:
        mock_request.return_value = {
            'success': True,
            'data': {
                'uuid': 'test-uuid-123',
                'telegramId': '123456789'
            }
        }
        
        result = await api_client.get_user_by_telegram_id(123456789)
        
        assert result is not None
        assert result['success'] is True


@pytest.mark.asyncio
async def test_revoke_user_subscription(api_client):
    """Тест отзыва подписки"""
    with patch.object(api_client, '_request', new_callable=AsyncMock) as mock_request:
        mock_request.return_value = {
            'success': True,
            'message': 'Subscription revoked'
        }
        
        result = await api_client.revoke_user_subscription('test-uuid-123')
        
        assert result is not None
        assert result['success'] is True
        mock_request.assert_called_once()


@pytest.mark.asyncio
async def test_api_error_handling(api_client):
    """Тест обработки ошибок API"""
    with patch.object(api_client, '_request', new_callable=AsyncMock) as mock_request:
        mock_request.return_value = None
        
        result = await api_client.create_user(123456789)
        
        assert result is None
