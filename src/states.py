"""
Состояния FSM для бота
"""
from aiogram.fsm.state import State, StatesGroup


class BroadcastStates(StatesGroup):
    """Состояния для рассылки сообщений"""
    waiting_for_message = State()
    confirm_broadcast = State()


class UserManagementStates(StatesGroup):
    """Состояния для управления пользователями"""
    waiting_for_user_id = State()
    waiting_for_action = State()
    confirm_action = State()


class SettingsStates(StatesGroup):
    """Состояния для настроек"""
    waiting_for_setting = State()
    waiting_for_value = State()
