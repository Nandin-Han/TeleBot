"""
消息处理器
处理用户发送的普通文本消息
"""
from telegram import Update
from telegram.ext import ContextTypes
from loguru import logger
from .commands import handle_tag_input

async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    处理用户发送的文本消息
    """
    if not update.message or not update.message.text:
        return
        
    user = update.effective_user
    if not user:
        return
        
    message_text = update.message.text
    
    logger.info(f"收到来自用户 {user.first_name} (ID: {user.id}) 的消息: {message_text}")
    
    # 首先检查是否是tag输入
    if context.user_data and context.user_data.get('waiting_for_tag'):
        await handle_tag_input(update, context)
        return
    
    # 简单的回复逻辑
    user_name = user.first_name or user.username or "用户"
    reply_text = f"你好 {user_name}! 👋\n\n你发送的消息是: \"{message_text}\"\n\n我收到了！如需帮助，请发送 /help"
    
    await update.message.reply_text(reply_text)
