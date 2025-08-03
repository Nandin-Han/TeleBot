"""
配置管理模块
处理环境变量、Bot Token 获取和日志配置
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from loguru import logger

def get_bot_token() -> str:
    """
    获取机器人Token
    从环境变量中读取 TELEGRAM_BOT_TOKEN
    """
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise ValueError(
            "❌ TELEGRAM_BOT_TOKEN 环境变量未设置！\n"
            "请在 .env 文件中设置你的 Bot Token\n"
            "获取方法: 在 Telegram 中联系 @BotFather"
        )
    return token

def setup_logging():
    """
    设置日志系统
    配置 loguru 日志格式和输出
    """
    # 移除默认的 logger
    logger.remove()
    
    # 控制台日志格式
    console_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    )
    
    # 添加控制台输出
    logger.add(
        sys.stdout,
        format=console_format,
        level=os.getenv("LOG_LEVEL", "INFO"),
        colorize=True
    )
    
    # 确保日志目录存在
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # 添加文件日志
    logger.add(
        "logs/telebot.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
        level="DEBUG",
        rotation="1 day",
        retention="7 days",
        compression="zip"
    )
    
    logger.info("日志系统初始化完成")

def get_debug_mode() -> bool:
    """获取调试模式状态"""
    return os.getenv("DEBUG", "False").lower() == "true"

def get_admin_user_id() -> int | None:
    """获取管理员用户ID"""
    admin_id = os.getenv("ADMIN_USER_ID")
    return int(admin_id) if admin_id else None
