"""
Telegram Bot 命令处理器
处理用户发送的各种命令
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from telegram.ext import ContextTypes
from loguru import logger
from typing import Optional
import asyncio
import subprocess
import datetime


# 会话状态定义
WAITING_FOR_TAG = 1

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
        logger.info(f"用户 {user_name} (ID: {user_id}) 请求项目更新")
    else:
        logger.info("未知用户请求项目更新")

    # 显示项目选择界面
    await project_command(update, context)

async def project_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    显示项目选择界面
    """
    # 创建项目选择键盘
    keyboard = [
        [
            InlineKeyboardButton("🛠️ pd-admin", callback_data='project_pd-admin'),
            InlineKeyboardButton("🌐 pgames-h5", callback_data='project_pgames-h5')
        ],
        [
            InlineKeyboardButton("🧩 pgame-api", callback_data='project_pgame-api'),
            InlineKeyboardButton("🧱 tongits-php", callback_data='project_tongits-php'),
            InlineKeyboardButton("🗃️ go-server-api", callback_data='project_go-server-api')
        ],
        [
            InlineKeyboardButton("🔙 返回", callback_data='back_to_main')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = """
🚀 <b>项目选择</b>

请选择要更新的项目：

🛠️ <b>pd-admin</b> - 管理后台系统
🌐 <b>pgames-h5</b> - 前端网站资源
🧩 <b>pgame-api</b> - PG项目API
🧱 <b>tongits-php</b> - 三方对接API
🗃️ <b>go-server-api</b> - Go服务API

请点击下方按钮选择项目：
"""
    
    if update.message:
        await update.message.reply_text(
            message,
            parse_mode='HTML',
            reply_markup=reply_markup
        )
    elif update.callback_query:
        await update.callback_query.edit_message_text(
            message,
            parse_mode='HTML',
            reply_markup=reply_markup
        )

async def handle_project_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    处理项目选择的回调
    """
    query = update.callback_query
    if not query:
        logger.error("回调查询为空")
        return
    
    # 确认回调查询
    await query.answer()

    # 确保 user_data 已初始化
    if context.user_data is None:
        context.user_data = {}

    # 安全地获取用户信息
    user = query.from_user
    if not user:
        logger.error("无法获取回调用户信息")
        await query.answer("❌ 用户信息错误")
        return
    
    user_name = user.first_name or user.username or "用户"
    user_id = user.id


    callback_data = query.data
    if not callback_data:
        logger.error("回调数据为空")
        await query.edit_message_text("❌ 数据错误，请重新尝试。")
        return
    
    user_name = user.first_name or user.username or "用户"
    user_id = user.id
    
    # 处理返回主菜单
    if callback_data == 'back_to_main':
        await show_main_menu(query)
        return
    
    # 处理项目选择
    if callback_data.startswith('project_'):
        project_name = callback_data.replace('project_', '')
        
        # 保存项目信息到用户上下文
        context.user_data['selected_project'] = project_name
        context.user_data['user_name'] = user_name
        context.user_data['user_id'] = user_id
        context.user_data['start_time'] = datetime.datetime.now()
        
        logger.info(f"用户 {user_name} (ID: {user_id}) 选择了项目: {project_name}")
        
        # 显示环境选择
        await show_environment_selection(query, project_name)
        return
    # 处理未知回调
    logger.warning(f"未知的回调数据: {callback_data}")
    await query.edit_message_text("❌ 未知的选择，请重新尝试。")


async def show_environment_selection(query: CallbackQuery, project_name: str) -> None:
    """显示环境选择界面"""
    keyboard = [
        [
            InlineKeyboardButton("🔧 测试环境", callback_data=f'env_test_{project_name}'),
            InlineKeyboardButton("🚀 生产环境", callback_data=f'env_prod_{project_name}')
        ],
        [
            InlineKeyboardButton("🔙 返回项目选择", callback_data='back_to_projects')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = f"""
🏗️ <b>环境选择 - {project_name}</b>

请选择要更新的环境：

🔧 <b>测试环境</b> - 用于测试和验证
🚀 <b>生产环境</b> - 线上正式环境

<b>注意：</b>
• 测试环境更新较快
• 生产环境需要谨慎操作

请选择目标环境：
"""
    
    await query.edit_message_text(
        message,
        reply_markup=reply_markup,
        parse_mode='HTML'
    )

async def show_main_menu(query: CallbackQuery) -> None:
    """显示主菜单"""
    keyboard = [
        [
            InlineKeyboardButton("🚀 项目选择", callback_data='show_projects'),
            InlineKeyboardButton("ℹ️ 帮助信息", callback_data='show_help')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = """
🤖 <b>TeleBot 主菜单</b>

欢迎使用 TeleBot 项目管理系统！

可用功能：
🚀 项目选择 - 选择要操作的项目
ℹ️ 帮助信息 - 查看使用说明

请选择您需要的功能：
"""
    
    await query.edit_message_text(
        message,
        reply_markup=reply_markup,
        parse_mode='HTML'
    )

async def handle_environment_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    处理环境选择的回调
    """
    query = update.callback_query
    if not query:
        return
    
    await query.answer()
    
    # 安全地获取 callback_data
    callback_data = query.data
    if not callback_data:
        logger.error("回调数据为空")
        await query.edit_message_text("❌ 数据错误，请重新尝试")
        return
    
    # 确保 user_data 已初始化
    if context.user_data is None:
        context.user_data = {}

    if callback_data.startswith('env_'):
        environment = "演示环境" if callback_data == 'env_demo' else "生产环境"
        env_emoji = "🔧" if callback_data == 'env_demo' else "🚀"
        
        # 保存环境信息
        context.user_data['environment'] = environment
        context.user_data['env_emoji'] = env_emoji
        
        project_name = context.user_data.get('selected_project', 'unknown')
        
        # 请求用户输入 tag
        await query.edit_message_text(
            f"""
{env_emoji} <b>{project_name} - {environment}</b>

请输入 GitLab tag 版本号：

<b>格式要求：</b>
• 必须以 'v' 开头
• 格式: v1.1.67
• 示例: v1.2.3, v2.0.1

请直接输入版本号：
""",
            parse_mode='HTML'
        )
        
        return WAITING_FOR_TAG
    
    return

async def execute_git_operations(project_name: str, tag: str) -> tuple[bool, str]:
    """
    执行 Git 标签创建和推送操作
    """
    try:
        # 构造完整的标签名
        full_tag = f"{project_name}-{tag}"
        
        logger.info(f"开始执行 Git 操作，标签: {full_tag}")
        
        # 执行 git tag 命令
        tag_process = await asyncio.create_subprocess_exec(
            'git', 'tag', full_tag,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd='/opt/infra-deploy'  # 确保在正确的目录执行
        )
        
        tag_stdout, tag_stderr = await tag_process.communicate()

        if tag_process.returncode != 0:
            error_msg = tag_stderr.decode('utf-8') if tag_stderr else "创建标签失败"
            logger.error(f"Git tag 失败: {error_msg}")
            return False, f"创建标签失败: {error_msg}"

        # 记录成功的标签创建
        success_msg = tag_stdout.decode('utf-8') if tag_stdout else ""
        logger.info(f"Git tag 创建成功: {success_msg}")

        
        # 执行 git push 命令
        push_process = await asyncio.create_subprocess_exec(
            'git', 'push', 'origin', full_tag,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd='/opt/infra-deploy'  # 确保在正确的目录执行
        )
        
        push_stdout, push_stderr = await push_process.communicate()
        
        if push_process.returncode != 0:
            error_msg = push_stderr.decode('utf-8') if push_stderr else "推送标签失败"
            logger.error(f"Git push 失败: {error_msg}")
            return False, f"推送标签失败: {error_msg}"
        
        # 记录成功的推送
        push_success_msg = push_stdout.decode('utf-8') if push_stdout else ""
        logger.info(f"Git push 成功: {push_success_msg}")

        logger.info(f"Git 操作成功完成，标签: {full_tag}")
        return True, "操作成功"
        
    except Exception as e:
        logger.error(f"Git 操作异常: {str(e)}")
        return False, f"操作异常: {str(e)}"
