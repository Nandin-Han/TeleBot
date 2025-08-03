"""
装饰器模块
提供各种实用的装饰器函数
"""
import functools
from typing import Callable, Any
from loguru import logger

def log_command(func: Callable) -> Callable:
    """
    命令处理器装饰器
    自动记录命令的执行日志
    """
    @functools.wraps(func)
    async def wrapper(update, context, *args, **kwargs):
        user = update.effective_user
        command = update.message.text.split()[0] if update.message.text else "unknown"
        
        logger.info(f"用户 {user.first_name} (ID: {user.id}) 执行命令: {command}")
        
        try:
            result = await func(update, context, *args, **kwargs)
            logger.debug(f"命令 {command} 执行成功")
            return result
        except Exception as e:
            logger.error(f"命令 {command} 执行失败: {e}")
            raise
    
    return wrapper

def admin_only(func: Callable) -> Callable:
    """
    管理员权限装饰器
    只允许管理员执行的命令
    """
    @functools.wraps(func)
    async def wrapper(update, context, *args, **kwargs):
        from src.bot.utils.config import get_admin_user_id
        
        user = update.effective_user
        admin_id = get_admin_user_id()
        
        if admin_id and user.id != admin_id:
            logger.warning(f"非管理员用户 {user.first_name} (ID: {user.id}) 尝试执行管理员命令")
            await update.message.reply_text("❌ 抱歉，此命令仅限管理员使用。")
            return
        
        return await func(update, context, *args, **kwargs)
    
    return wrapper
