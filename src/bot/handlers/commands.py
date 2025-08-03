"""
Telegram Bot 命令处理器
处理用户发送的各种命令
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from telegram.ext import ContextTypes
from loguru import logger
from typing import Optional
import asyncio

def get_safe_user_name(update: Update) -> str:
    """安全地获取用户显示名称"""
    user = update.effective_user
    if not user:
        return "朋友"
    
    # 优先使用 first_name，然后是 username，最后是默认值
    if user.first_name:
        return user.first_name
    elif user.username:
        return f"@{user.username}"
    else:
        return "用户"

def get_user_id_safe(update: Update) -> Optional[int]:
    """安全地获取用户ID"""
    user = update.effective_user
    return user.id if user else None


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    处理 /start 命令
    当用户首次启动机器人或发送 /start 时调用
    """
    user_name = get_safe_user_name(update)
    user_id = get_user_id_safe(update)
    
    if user_id:
        logger.info(f"用户 {user_name} (ID: {user_id}) 发送了 /start 命令")
    else:
        logger.info("未知用户发送了 /start 命令")
    
    welcome_message = f"""
🎉 欢迎使用 TeleBot, {user_name}!

我是一个基于 Python 3.13 和 python-telegram-bot v22 开发的机器人。

📋 可用命令:
/start - 显示欢迎信息
/help - 获取帮助信息
/update - 更新发布GitLab项目代码

🚀 让我们开始吧!

---
💡 提示: 发送任何消息我都会回复你哦！
"""
    
    # 确保消息存在再回复
    if update.message:
        await update.message.reply_text(
            welcome_message,
            parse_mode='HTML'
        )
    else:
        logger.warning("无法回复消息：update.message 为 None")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    处理 /help 命令
    显示机器人的帮助信息和功能说明
    """
    user_name = get_safe_user_name(update)
    user_id = get_user_id_safe(update)
    if user_id:
        logger.info(f"用户 {user_name} (ID: {user_id}) 请求帮助信息")
    else:
        logger.info("未知用户请求帮助信息")
    help_message = """
🤖 <b>TeleBot 帮助文档</b>

<b>基础命令:</b>
/start - 开始使用机器人
/help - 显示此帮助信息
/update - 选择环境进行代码更新

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
    if update.message:
        await update.message.reply_text(
            help_message,
            parse_mode='HTML'
        )
    else:
        logger.warning("无法回复消息：update.message 为 None")

async def update_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    处理 /update 命令
    显示环境选择按钮
    """
    user_name = get_safe_user_name(update)
    user_id = get_user_id_safe(update)
    if user_id:
        logger.info(f"用户 {user_name} (ID: {user_id}) 请求代码更新")
    else:
        logger.info("未知用户请求代码更新")
    # 创建内联键盘
    keyboard = [
        [
            InlineKeyboardButton("🔧 演示环境", callback_data='update_demo'),
            InlineKeyboardButton("🚀 生产环境", callback_data='update_prod')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = """
🔄 <b>代码更新系统</b>

需要更新哪个环境？请选择：

🔧 <b>演示环境</b> - 用于测试和演示
🚀 <b>生产环境</b> - 正式运行环境

请点击下方按钮选择要更新的环境：
"""
    # 确保消息存在再回复
    if update.message:
        await update.message.reply_text(
            message,
            parse_mode='HTML',
            reply_markup=reply_markup
        )
    else:
        logger.warning("无法回复消息：update.message 为 None")


async def handle_update_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    处理更新环境选择的回调
    """
    """
    处理更新环境选择的回调
    """
    query = update.callback_query
    if not query:
        logger.error("回调查询为空")
        return
    
    user = query.from_user
    if not user:
        logger.error("无法获取回调用户信息")
        await query.answer("❌ 用户信息错误")
        return
    
    # 确认回调查询
    await query.answer()
    
    callback_data = query.data
    if not callback_data:
        logger.error("回调数据为空")
        await query.edit_message_text("❌ 数据错误，请重新尝试。")
        return
    
    # 安全地获取用户信息
    user_name = user.first_name or user.username or "用户"
    user_id = user.id
    
    if callback_data == 'update_demo':
        environment = "演示环境"
        env_emoji = "🔧"
        logger.info(f"用户 {user_name} (ID: {user_id}) 选择更新演示环境")
    elif callback_data == 'update_prod':
        environment = "生产环境"
        env_emoji = "🚀"
        logger.info(f"用户 {user_name} (ID: {user_id}) 选择更新生产环境")
    else:
        await query.edit_message_text("❌ 未知的选择，请重新尝试。")
        return
    
    # 这里可以添加实际的更新逻辑
    response_message = f"""
{env_emoji} <b>{environment}更新请求已确认</b>

✅ 正在准备更新 {environment}
📋 更新内容：GitLab项目代码
⏳ 预计完成时间：2-3分钟

<i>更新过程中请稍候...</i>

---
💡 更新完成后会自动通知您结果
"""
    
    # 编辑原消息
    await query.edit_message_text(
        response_message,
        parse_mode='HTML'
    )
    
    # 这里可以添加实际的更新逻辑
    # 例如：调用GitLab API、执行部署脚本等
    await simulate_update_with_progress(query, environment, env_emoji)

async def simulate_update_with_progress(query: CallbackQuery, environment: str, env_emoji: str):
    """
    带进度显示的更新过程
    """
    steps = [
        ("检查代码变更", 1),
        ("备份当前版本", 2),
        ("下载新版本", 2),
        ("部署应用", 3),
        ("重启服务", 1),
        ("验证部署", 2)
    ]
    
    total_time = sum(step[1] for step in steps)
    elapsed_time = 0
    
    for i, (step_name, duration) in enumerate(steps, 1):
        # 更新进度消息
        progress_message = f"""
{env_emoji} <b>{environment}更新中...</b>

<b>当前步骤:</b> {step_name}
<b>进度:</b> {i}/{len(steps)} 步骤

⏳ 预计剩余时间: {total_time - elapsed_time}秒

{'▓' * i}{'░' * (len(steps) - i)} {int(i/len(steps)*100)}%
"""
        
        await query.edit_message_text(
            progress_message,
            parse_mode='HTML'
        )
        
        # 模拟步骤执行时间
        await asyncio.sleep(duration)
        elapsed_time += duration
    
    # 完成消息
    completion_message = f"""
{env_emoji} <b>{environment}更新完成！</b>

✅ 所有步骤已成功完成
🕐 总用时: {total_time}秒
🎉 {environment}已恢复正常运行

---
✨ 更新操作成功完成！
"""
    
    await query.edit_message_text(
        completion_message,
        parse_mode='HTML'
    )