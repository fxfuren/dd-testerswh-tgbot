from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')
    
    # Telegram Bot
    BOT_TOKEN: str
    ADMIN_IDS: str
    
    # Group Settings
    GROUP_ID: int
    TOPIC_ID: int
    
    # Remnawave Panel API
    PANEL_URL: str
    PANEL_SECRET_KEY: str
    PANEL_API_TOKEN: str
    
    # User Settings
    USER_TAG: str = "ADMIN"
    EXTERNAL_SQUAD: str = "WL-ADMIN-squad"
    INTERNAL_SQUAD: str = "ADMIN-WHITE-LIST"
    HWID_LIMIT: int = 1
    TRAFFIC_LIMIT_GB: int = 15  # Лимит трафика в ГБ в день
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    @property
    def admin_ids_list(self) -> List[int]:
        """Преобразование строки ADMIN_IDS в список целых чисел"""
        return [int(admin_id.strip()) for admin_id in self.ADMIN_IDS.split(',') if admin_id.strip()]


settings = Settings()
