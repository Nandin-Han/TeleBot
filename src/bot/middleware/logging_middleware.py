"""
日志中间件
为机器人添加统一的日志记录功能
"""
from loguru import logger
from telegram.ext import BaseHandler
from telegram import Update

class LoggingMiddleware:
    """日志中间件类"""
    
    @staticmethod
    async def log_update(update: Update, context):
        """记录所有收到的更新"""
        if update.message:
            user = update.effective_user
            chat = update.effective_chat
            message_type = "command" if update.message.text and update.message.text.startswith('/') else "message"
            
            logger.info(
                f"收到 {message_type} | "
                f"用户: {user.first_name} ({user.id}) | "
                f"聊天: {chat.type} ({chat.id}) | "
                f"内容: {update.message.text[:50]}{'...' if len(update.message.text or '') > 50 else ''}"
            )
