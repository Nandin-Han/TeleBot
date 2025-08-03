"""
Telegram Bot 命令处理器
处理用户发送的各种命令
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from telegram.ext import ContextTypes
from loguru import logger
from typing import Optional
import asyncio
import re
import subprocess
import datetime


def validate_tag_format(tag: str) -> bool:
    """验证tag格式是否正确"""
    # 使用正则表达式验证tag格式：v数字.数字.数字
    pattern = r'^v\d+\.\d+\.\d+$'
    return re.match(pattern, tag) is not None

async def handle_tag_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """处理用户输入的tag"""
    if not update.message or not update.message.text:
        return
    
    # 检查用户是否在等待tag输入状态
    if not context.user_data or context.user_data.get('waiting_for_tag') != True:
        return
    
    user_input = update.message.text.strip()
    user_name = get_safe_user_name(update)
    user_id = get_user_id_safe(update)
    
    logger.info(f"用户 {user_name} (ID: {user_id}) 输入了tag: {user_input}")
    
    # 验证tag格式
    if validate_tag_format(user_input):
        # 格式正确，保存tag并继续到确认页面
        context.user_data['selected_tag'] = user_input
        context.user_data['waiting_for_tag'] = False
        
        # 获取之前保存的信息
        action_type = context.user_data.get('action_type')
        project_name = context.user_data.get('selected_project')
        environment = context.user_data.get('environment')
        
        logger.info(f"用户 {user_name} (ID: {user_id}) tag格式验证通过: {user_input}")
        
        # 创建一个临时的CallbackQuery对象来调用确认函数
        # 这里需要用不同的方式，因为这是文本消息而不是回调
        keyboard = [
            [
                InlineKeyboardButton("✅ 确认", callback_data=f'confirm_{action_type}_{environment}_{user_input}_{project_name}'),
                InlineKeyboardButton("❌ 取消", callback_data='back_to_main')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        action_text = "更新" if action_type == "update" else "回滚"
        env_text = ""
        if environment:
            env_display = "演示环境" if environment == "pre" else "生产环境"
            env_text = f"\n环境: <b>{env_display}</b>"
        
        tag_text = f"\nTag版本: <b>{user_input}</b>"
        
        message = f"""
⚠️ <b>确认操作</b>

项目: <b>{project_name}</b>{env_text}{tag_text}
操作: <b>{action_text}</b>

请确认是否要{action_text}此项目？

<b>注意：</b>
• 此操作将对服务器进行修改
• 请确保操作的必要性
• {action_text}操作可能需要几分钟时间

确认要继续吗？
"""
        
        await update.message.reply_text(
            message,
            parse_mode='HTML',
            reply_markup=reply_markup
        )
        
    else:
        # 格式错误，显示错误信息和选项
        keyboard = [
            [
                InlineKeyboardButton("🔄 重新输入", callback_data='retry_tag_input'),
                InlineKeyboardButton("⏹️ 停止操作", callback_data='back_to_main')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        error_message = f"""
❌ <b>Tag格式错误</b>

您输入的tag: <code>{user_input}</code>

<b>错误原因：</b>
tag格式不符合要求

<b>正确格式：</b>
• 必须以 v 开头
• 格式：v主版本.次版本.修订版本
• 示例：v1.1.3, v2.0.5, v1.12.8

请选择下一步操作：
"""
        
        await update.message.reply_text(
            error_message,
            parse_mode='HTML',
            reply_markup=reply_markup
        )

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
/startupdate - 启动项目管理菜单

🚀 让我们开始吧!

---
💡 提示: 使用 /startupdate 来管理项目！
"""
    
    # 确保消息存在再回复
    if update.message:
        await update.message.reply_text(
            welcome_message,
            parse_mode='HTML'
        )
    else:
        logger.warning("无法回复消息：update.message 为 None")

async def start_update_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    处理 /start-update 命令
    显示主菜单
    """
    user_name = get_safe_user_name(update)
    user_id = get_user_id_safe(update)
    
    if user_id:
        logger.info(f"用户 {user_name} (ID: {user_id}) 启动了项目管理")
    else:
        logger.info("未知用户启动了项目管理")
    
    await show_main_menu(update)

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
/startupdate - 启动项目管理菜单

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

async def show_main_menu(update: Update) -> None:
    """显示主菜单"""
    keyboard = [
        [
            InlineKeyboardButton("⬆️ 更新", callback_data='main_update'),
            InlineKeyboardButton("🔄 回滚", callback_data='main_rollback'),
            InlineKeyboardButton("⏹️ 停止", callback_data='main_stop')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = """
🤖 <b>TeleBot 项目管理</b>

请选择您需要的操作：

⬆️ <b>更新</b> - 更新项目到最新版本
🔄 <b>回滚</b> - 回滚项目到之前版本
⏹️ <b>停止</b> - 结束此次操作

请点击下方按钮选择操作：
"""
    
    if hasattr(update, 'message') and update.message:
        await update.message.reply_text(
            message,
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
    elif hasattr(update, 'callback_query') and update.callback_query:
        await update.callback_query.edit_message_text(
            message,
            reply_markup=reply_markup,
            parse_mode='HTML'
        )

async def show_environment_selection(query: CallbackQuery, action_type: str) -> None:
    """显示环境选择界面"""
    keyboard = [
        [
            InlineKeyboardButton("🧪 演示环境", callback_data=f'env_{action_type}_pre'),
            InlineKeyboardButton("🚀 生产环境", callback_data=f'env_{action_type}_prod')
        ],
        [
            InlineKeyboardButton("🔙 返回主菜单", callback_data='back_to_main')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    action_text = "更新" if action_type == "update" else "回滚"
    message = f"""
🏗️ <b>环境选择 - {action_text}</b>

请选择要{action_text}的环境：

🧪 <b>演示环境</b> - 用于测试和验证
🚀 <b>生产环境</b> - 线上正式环境

<b>注意：</b>
• 演示环境更新较快，影响范围小
• 生产环境需要谨慎操作，会影响线上服务

请选择目标环境：
"""
    
    await query.edit_message_text(
        message,
        parse_mode='HTML',
        reply_markup=reply_markup
    )

async def show_project_selection(query: CallbackQuery, action_type: str, environment: Optional[str] = None) -> None:
    """显示项目选择界面"""
    env_prefix = f"_{environment}" if environment else ""
    keyboard = [
        [
            InlineKeyboardButton("🧱 tongits-php", callback_data=f'project_{action_type}{env_prefix}_tongits-php'),
            InlineKeyboardButton("🗃️ go-server-api", callback_data=f'project_{action_type}{env_prefix}_go-server-api')
        ],
        [
            InlineKeyboardButton("🧩 pgame-api", callback_data=f'project_{action_type}{env_prefix}_pgame-api'),
            InlineKeyboardButton("🛠️ pd-admin", callback_data=f'project_{action_type}{env_prefix}_pd-admin'),
            InlineKeyboardButton("🌐 pgames-h5", callback_data=f'project_{action_type}{env_prefix}_pgames-h5')
        ],
        [
            InlineKeyboardButton("🔙 返回主菜单", callback_data='back_to_main')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    action_text = "更新" if action_type == "update" else "回滚"
    env_text = ""
    if environment:
        env_display = "演示环境" if environment == "pre" else "生产环境"
        env_text = f" - {env_display}"
    
    message = f"""
🚀 <b>项目选择 - {action_text}{env_text}</b>

请选择要{action_text}的项目：

🛠️ <b>pd-admin</b> - 管理后台系统
🌐 <b>pgames-h5</b> - 前端网站资源
🧩 <b>pgame-api</b> - PG项目API
🧱 <b>tongits-php</b> - 三方对接API
🗃️ <b>go-server-api</b> - Go服务API

请点击下方按钮选择项目：
"""
    
    await query.edit_message_text(
        message,
        parse_mode='HTML',
        reply_markup=reply_markup
    )

async def show_tag_input_request(query: CallbackQuery, action_type: str, project_name: str, context: ContextTypes.DEFAULT_TYPE, environment: Optional[str] = None) -> None:
    """显示tag输入请求界面"""
    # 设置等待tag输入的状态
    if context.user_data is None:
        context.user_data = {}
    context.user_data['waiting_for_tag'] = True
    
    keyboard = [
        [
            InlineKeyboardButton("❌ 取消操作", callback_data='back_to_main')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    action_text = "更新" if action_type == "update" else "回滚"
    env_text = ""
    if environment:
        env_display = "演示环境" if environment == "pre" else "生产环境"
        env_text = f" - {env_display}"
    
    message = f"""
🏷️ <b>输入Tag版本 - {action_text}{env_text}</b>

项目: <b>{project_name}</b>
操作: <b>{action_text}</b>

请输入要{action_text}的tag版本号：

<b>格式要求：</b>
• 必须以 v 开头
• 格式：v主版本.次版本.修订版本
• 示例：v1.1.3, v2.0.5, v1.12.8

<b>请直接发送tag信息：</b>
（例如：v1.1.3）
"""
    
    await query.edit_message_text(
        message,
        parse_mode='HTML',
        reply_markup=reply_markup
    )

async def show_confirmation(query: CallbackQuery, action_type: str, project_name: str, environment: Optional[str] = None, tag: Optional[str] = None) -> None:
    """显示确认界面"""
    env_prefix = f"_{environment}" if environment else ""
    tag_prefix = f"_{tag}" if tag else ""
    keyboard = [
        [
            InlineKeyboardButton("✅ 确认", callback_data=f'confirm_{action_type}{env_prefix}{tag_prefix}_{project_name}'),
            InlineKeyboardButton("❌ 取消", callback_data='back_to_main')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    action_text = "更新" if action_type == "update" else "回滚"
    env_text = ""
    if environment:
        env_display = "演示环境" if environment == "pre" else "生产环境"
        env_text = f"\n环境: <b>{env_display}</b>"
    
    tag_text = ""
    if tag:
        tag_text = f"\nTag版本: <b>{tag}</b>"
    
    message = f"""
⚠️ <b>确认操作</b>

项目: <b>{project_name}</b>{env_text}{tag_text}
操作: <b>{action_text}</b>

请确认是否要{action_text}此项目？

<b>注意：</b>
• 此操作将对服务器进行修改
• 请确保操作的必要性
• {action_text}操作可能需要几分钟时间

确认要继续吗？
"""
    
    await query.edit_message_text(
        message,
        reply_markup=reply_markup,
        parse_mode='HTML'
    )

async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    处理所有回调查询
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
    
    logger.info(f"用户 {user_name} (ID: {user_id}) 点击了回调: {callback_data}")
    
    # 处理主菜单选择
    if callback_data == 'main_update':
        await show_environment_selection(query, 'update')
        return
    elif callback_data == 'main_rollback':
        await show_environment_selection(query, 'rollback')
        return
    elif callback_data == 'main_stop':
        await query.edit_message_text(
            "⏹️ 操作已结束，感谢使用 TeleBot！\n\n如需重新开始，请发送 /startupdate",
            parse_mode='HTML'
        )
        return
    
    # 处理返回主菜单
    if callback_data == 'back_to_main':
        await show_main_menu_callback(query)
        return
    
    # 处理环境选择
    if callback_data.startswith('env_'):
        parts = callback_data.split('_')
        if len(parts) >= 3:
            action_type = parts[1]  # update 或 rollback
            environment = parts[2]  # pre 或 prod
            
            logger.info(f"用户 {user_name} (ID: {user_id}) 选择了环境: {environment}, 操作: {action_type}")
            
            # 跳转到项目选择
            await show_project_selection(query, action_type, environment)
            return
    
    # 处理项目选择
    if callback_data.startswith('project_'):
        parts = callback_data.split('_')
        if len(parts) >= 3:
            action_type = parts[1]  # update 或 rollback
            
            # 检查是否包含环境信息
            if len(parts) >= 4 and parts[2] in ['pre', 'prod']:
                environment = parts[2]  # pre 或 prod
                project_name = '_'.join(parts[3:])  # 项目名称（可能包含连字符）
            else:
                environment = None
                project_name = '_'.join(parts[2:])  # 项目名称（可能包含连字符）
            
            # 保存项目信息到用户上下文
            context.user_data['selected_project'] = project_name
            context.user_data['action_type'] = action_type
            context.user_data['environment'] = environment
            context.user_data['user_name'] = user_name
            context.user_data['user_id'] = user_id
            context.user_data['start_time'] = datetime.datetime.now()
            
            env_text = f", 环境: {environment}" if environment else ""
            logger.info(f"用户 {user_name} (ID: {user_id}) 选择了项目: {project_name}, 操作: {action_type}{env_text}")
            
            # 显示tag输入界面
            await show_tag_input_request(query, action_type, project_name, context, environment)
            return
    
    # 处理重新输入tag
    if callback_data == 'retry_tag_input':
        # 获取保存的信息
        action_type = context.user_data.get('action_type')
        project_name = context.user_data.get('selected_project')
        environment = context.user_data.get('environment')
        
        if action_type and project_name:
            logger.info(f"用户 {user_name} (ID: {user_id}) 选择重新输入tag")
            await show_tag_input_request(query, action_type, project_name, context, environment)
        else:
            logger.error(f"用户 {user_name} (ID: {user_id}) 重新输入tag时缺少必要信息")
            await query.edit_message_text("❌ 操作信息丢失，请重新开始。")
        return
    
    # 处理确认操作
    if callback_data.startswith('confirm_'):
        parts = callback_data.split('_')
        if len(parts) >= 5:  # confirm_action_environment_tag_project
            action_type = parts[1]  # update 或 rollback
            environment = parts[2]  # pre 或 prod
            tag = parts[3]  # tag版本
            project_name = '_'.join(parts[4:])  # 项目名称（可能包含连字符）
            
            # 保存tag信息到用户上下文
            context.user_data['selected_tag'] = tag
            
            env_display = "演示环境" if environment == "pre" else "生产环境"
            logger.info(f"用户 {user_name} (ID: {user_id}) 确认{action_type}项目: {project_name}, 环境: {env_display}, tag: {tag}")
            
            # 执行操作
            await execute_action(query, action_type, project_name, context)
            return
        else:
            logger.error(f"确认回调数据格式错误: {callback_data}")
            await query.edit_message_text("❌ 操作信息格式错误，请重新尝试。")
            return
    
    # 处理未知回调
    logger.warning(f"未知的回调数据: {callback_data}")
    await query.edit_message_text("❌ 未知的选择，请重新尝试。")

async def show_main_menu_callback(query: CallbackQuery) -> None:
    """为回调查询显示主菜单"""
    keyboard = [
        [
            InlineKeyboardButton("⬆️ 更新", callback_data='main_update'),
            InlineKeyboardButton("🔄 回滚", callback_data='main_rollback'),
            InlineKeyboardButton("⏹️ 停止", callback_data='main_stop')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = """
🤖 <b>TeleBot 项目管理</b>

请选择您需要的操作：

⬆️ <b>更新</b> - 更新项目到最新版本
🔄 <b>回滚</b> - 回滚项目到之前版本
⏹️ <b>停止</b> - 结束此次操作

请点击下方按钮选择操作：
"""
    
    await query.edit_message_text(
        message,
        reply_markup=reply_markup,
        parse_mode='HTML'
    )

async def execute_action(query: CallbackQuery, action_type: str, project_name: str, context: ContextTypes.DEFAULT_TYPE) -> None:
    """执行项目操作（更新或回滚）"""
    action_text = "更新" if action_type == "update" else "回滚"
    
    # 从用户上下文获取环境和tag信息
    environment = context.user_data.get('environment') if context.user_data else None
    selected_tag = context.user_data.get('selected_tag') if context.user_data else None
    
    env_display = ""
    if environment:
        env_display = "演示环境" if environment == "pre" else "生产环境"
    
    # 定义执行步骤
    if action_type == "update":
        steps = [
            "🐧 清理临时目录...",
            "📦 拉取最新代码...",
            "🛡️ 备份现有部署...",
            "🚀 同步新代码...",
            "🔧 修正目录权限...",
            "✅ 代码部署完成..."
        ]
    else:  # rollback
        steps = [
            "📋 查找回滚目标...",
            "🛡️ 备份现有部署...",
            "⏪ 恢复代码版本...",
            "🔧 修正目录权限...",
            "✅ 验证回滚结果..."
        ]
    
    total_steps = len(steps)
    
    # 构建环境和tag信息文本
    env_text = f"\n🏗️ 环境: {env_display}" if environment else ""
    tag_text = f"\n🏷️ Tag版本: {selected_tag}" if selected_tag else ""
    
    # 显示开始执行消息
    start_message = f"""
🚀 <b>开始{action_text}</b>

📦 项目: {project_name}{env_text}{tag_text}
🔧 操作: {action_text}
⏰ 开始时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🔄 正在准备{action_text}操作...

进度: [0/{total_steps}] 准备中...
{'░' * 10} 0%
"""
    
    await query.edit_message_text(
        start_message,
        parse_mode='HTML'
    )
    
    try:
        # 逐步执行并显示进度
        for i, step in enumerate(steps, 1):
            # 更新进度显示
            progress_percent = int((i / total_steps) * 100)
            filled_blocks = int((i / total_steps) * 10)
            empty_blocks = 10 - filled_blocks
            progress_bar = '▓' * filled_blocks + '░' * empty_blocks
            
            progress_message = f"""
🚀 <b>{action_text}进行中</b>

📦 项目: {project_name}{env_text}{tag_text}
🔧 操作: {action_text}

当前步骤: {step}

进度: [{i}/{total_steps}] {progress_percent}%
{progress_bar}

⏰ 执行时间: {datetime.datetime.now().strftime('%H:%M:%S')}
"""
            
            await query.edit_message_text(
                progress_message,
                parse_mode='HTML'
            )
            
            # 模拟每个步骤的执行时间
            await asyncio.sleep(2)
        
        # 执行实际的命令逻辑
        success = await execute_project_command(project_name, action_type, selected_tag, environment)
        
        if success:
            # 操作成功
            end_time = datetime.datetime.now()
            start_time = context.user_data.get('start_time', end_time) if context.user_data else end_time
            duration = (end_time - start_time).total_seconds()
            
            success_message = f"""
✅ <b>{action_text}完成</b>

📦 项目: {project_name}{env_text}{tag_text}
🔧 操作: {action_text}
⏰ 完成时间: {end_time.strftime('%Y-%m-%d %H:%M:%S')}
⏱️ 耗时: {duration:.1f} 秒

🎉 项目{action_text}成功！

需要执行其他操作吗？
"""
            
            # 添加返回按钮
            keyboard = [
                [
                    InlineKeyboardButton("🔄 继续操作", callback_data='back_to_main'),
                    InlineKeyboardButton("⏹️ 结束", callback_data='main_stop')
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(
                success_message,
                parse_mode='HTML',
                reply_markup=reply_markup
            )
            
            logger.info(f"项目 {project_name} {action_text}成功，耗时 {duration:.1f} 秒")
        else:
            raise Exception(f"{action_text}操作失败")
        
    except Exception as e:
        error_message = f"""
❌ <b>{action_text}失败</b>

📦 项目: {project_name}{env_text}{tag_text}
🔧 操作: {action_text}
⏰ 失败时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

错误信息: {str(e)}

请联系管理员检查问题。
"""
        
        keyboard = [
            [
                InlineKeyboardButton("🔄 重试", callback_data=f'project_{action_type}_{project_name}'),
                InlineKeyboardButton("📊 返回主菜单", callback_data='back_to_main')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            error_message,
            parse_mode='HTML',
            reply_markup=reply_markup
        )
        
        logger.error(f"项目 {project_name} {action_text}失败: {str(e)}")

async def execute_project_command(project_name: str, action_type: str, tag: Optional[str] = None, environment: Optional[str] = None) -> bool:
    """
    执行实际的项目命令
    返回执行结果
    """
    logger.info(f"执行项目命令: 项目={project_name}, 操作={action_type}, tag={tag}, 环境={environment}")
    
    # 验证必要参数
    if not tag:
        logger.error("Tag参数缺失")
        return False
        
    if not validate_tag_format(tag):
        logger.error(f"无效的tag格式: {tag}")
        return False
        
    if not environment:
        logger.error("环境参数缺失")
        return False
    
    try:
        if environment == "pre":
            # 演示环境命令执行
            logger.info(f"开始在演示环境执行{action_type}操作: 项目={project_name}, tag={tag}")
            
            # 1. 同步脚本到远程服务器
            rsync_command = "su - gitlab-runner -c 'cd /opt/infra-deploy/ && rsync -av --delete ./scripts/ deployer@172.31.40.106:/home/deployer/scripts/'"
            logger.info(f"执行rsync命令: {rsync_command}")
            
            rsync_result = subprocess.run(
                rsync_command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=60  # 60秒超时
            )
            
            if rsync_result.returncode != 0:
                logger.error(f"rsync命令执行失败: {rsync_result.stderr}")
                return False
            
            logger.info("脚本同步成功")
            
            # 2. 执行远程部署命令
            ssh_command = f'ssh -i /opt/vscode/Ops_file/.id_rsa_deployer deployer@172.31.40.106 "bash /home/deployer/scripts/pre/{project_name}.sh {action_type} {tag}"'
            logger.info(f"执行SSH命令: {ssh_command}")
            
            ssh_result = subprocess.run(
                ssh_command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=300  # 5分钟超时
            )
            
            if ssh_result.returncode == 0:
                logger.info(f"项目{project_name}在演示环境{action_type}成功")
                logger.info(f"命令输出: {ssh_result.stdout}")
                return True
            else:
                logger.error(f"项目{project_name}在演示环境{action_type}失败")
                logger.error(f"错误输出: {ssh_result.stderr}")
                return False
                
        elif environment == "prod":
            # 生产环境命令执行（暂时留空，后期添加）
            logger.warning("生产环境部署命令尚未实现，请联系管理员")
            # TODO: 实现生产环境部署逻辑
            return False
            
        else:
            logger.error(f"未知的环境类型: {environment}")
            return False
            
    except subprocess.TimeoutExpired:
        logger.error(f"命令执行超时: 项目={project_name}, 环境={environment}")
        return False
    except Exception as e:
        logger.error(f"命令执行异常: {str(e)}")
        return False
