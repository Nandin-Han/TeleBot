"""
项目配置设置
"""
import os
from typing import Optional

class Settings:
    """应用配置类"""
    
    def __init__(self):
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.admin_user_id = os.getenv("ADMIN_USER_ID")
        self.debug = os.getenv("DEBUG", "False").lower() == "true"
    
    def validate(self) -> bool:
        """验证必要的配置是否存在"""
        if not self.bot_token:
            raise ValueError("TELEGRAM_BOT_TOKEN 环境变量未设置")
        return True

# 全局配置实例
settings = Settings()
