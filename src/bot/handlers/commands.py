"""
Telegram Bot 命令处理器
处理用户发送的各种命令
"""
from telegram import Update
from telegram.ext import ContextTypes
from loguru import logger

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    处理 /start 命令
    当用户首次启动机器人或发送 /start 时调用
    """
    user = update.effective_user
    chat_id = update.effective_chat.id
    
    logger.info(f"用户 {user.first_name} (ID: {user.id}) 发送了 /start 命令")
    
    welcome_message = f"""
🎉 欢迎使用 TeleBot, {user.first_name}!

我是一个基于 Python 3.13 和 python-telegram-bot v22 开发的机器人。

📋 可用命令:
/start - 显示欢迎信息
/help - 获取帮助信息

🚀 让我们开始吧!

---
💡 提示: 发送任何消息我都会回复你哦！
"""
    
    await update.message.reply_text(
        welcome_message,
        parse_mode='HTML'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    处理 /help 命令
    显示机器人的帮助信息和功能说明
    """
    user = update.effective_user
    logger.info(f"用户 {user.first_name} (ID: {user.id}) 请求帮助信息")
    
    help_message = """
🤖 <b>TeleBot 帮助文档</b>

<b>基础命令:</b>
/start - 开始使用机器人
/help - 显示此帮助信息

<b>关于本机器人:</b>
• 基于 Python 3.13 开发
• 使用 python-telegram-bot v22 框架
• 支持异步处理，响应迅速
• 模块化设计，易于扩展

<b>技术特性:</b>
✅ 异步消息处理
✅ 日志记录系统
✅ 环境配置管理
✅ 错误处理机制

<b>开发者信息:</b>
如需更多功能或遇到问题，请联系开发者。

---
💖 感谢使用 TeleBot!
"""
    
    await update.message.reply_text(
        help_message,
        parse_mode='HTML'
    )
