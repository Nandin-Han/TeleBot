"""
消息处理器
处理用户发送的普通文本消息
"""
from telegram import Update
from telegram.ext import ContextTypes
from loguru import logger

async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    处理用户发送的文本消息
    """
    user = update.effective_user
    message_text = update.message.text
    
    logger.info(f"收到来自用户 {user.first_name} (ID: {user.id}) 的消息: {message_text}")
    
    # 简单的回复逻辑
    reply_text = f"你好 {user.first_name}! 👋\n\n你发送的消息是: \"{message_text}\"\n\n我收到了！如需帮助，请发送 /help"
    
    await update.message.reply_text(reply_text)
