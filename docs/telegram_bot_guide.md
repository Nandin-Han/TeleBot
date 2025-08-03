# Telegram Bot 开发完整指南

## 什么是 Telegram Bot？

Telegram Bot 是运行在 Telegram 平台上的自动化程序，可以：
- 响应用户消息和命令
- 发送文本、图片、文件等内容
- 提供交互式键盘
- 处理群组管理
- 集成外部服务

## 核心概念详解

### 1. Bot Token (机器人令牌)
Bot Token 是你的机器人的身份证，格式如：`123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ`

**获取步骤：**
1. 在 Telegram 中搜索 `@BotFather`
2. 发送 `/newbot` 开始创建
3. 输入机器人显示名称（如：My Awesome Bot）
4. 输入机器人用户名（必须以 bot 结尾，如：myawesomebot）
5. 获得 Token，妥善保存

### 2. python-telegram-bot 框架架构

#### Application (应用)
- 机器人的核心管理器
- 处理与 Telegram API 的通信
- 管理更新的接收和分发

```python
# 创建应用
app = Application.builder().token(token).build()
```

#### Handler (处理器)
不同类型的处理器处理不同的消息：

```python
# 命令处理器
CommandHandler("start", start_function)

# 文本消息处理器  
MessageHandler(filters.TEXT, text_function)

# 回调查询处理器
CallbackQueryHandler(callback_function)
```

#### Update 对象
每次用户交互都会生成一个 Update 对象，包含：
- `update.message` - 消息内容
- `update.effective_user` - 发送用户信息
- `update.effective_chat` - 聊天信息
- `update.callback_query` - 内联键盘回调

### 3. 异步编程
python-telegram-bot v22 使用异步编程模式：

```python
async def my_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello!")
```

## 常用功能实现

### 1. 发送不同类型消息

```python
# 文本消息
await update.message.reply_text("普通文本")

# HTML 格式
await update.message.reply_text("<b>粗体</b> <i>斜体</i>", parse_mode='HTML')

# Markdown 格式  
await update.message.reply_text("*粗体* _斜体_", parse_mode='MarkdownV2')

# 发送图片
await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('image.jpg', 'rb'))
```

### 2. 内联键盘

```python
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

keyboard = [
    [InlineKeyboardButton("选项 1", callback_data='1')],
    [InlineKeyboardButton("选项 2", callback_data='2')]
]
reply_markup = InlineKeyboardMarkup(keyboard)

await update.message.reply_text("选择一个选项:", reply_markup=reply_markup)
```

### 3. 自定义键盘

```python
from telegram import KeyboardButton, ReplyKeyboardMarkup

keyboard = [
    [KeyboardButton("按钮 1"), KeyboardButton("按钮 2")],
    [KeyboardButton("分享联系人", request_contact=True)]
]
reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

await update.message.reply_text("选择操作:", reply_markup=reply_markup)
```

## 高级功能

### 1. 会话状态管理

```python
from telegram.ext import ConversationHandler

SELECTING, TYPING = range(2)

def conversation_handler():
    return ConversationHandler(
        entry_points=[CommandHandler('start_conv', start_conversation)],
        states={
            SELECTING: [MessageHandler(filters.TEXT, selecting)],
            TYPING: [MessageHandler(filters.TEXT, typing)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
```

### 2. 文件处理

```python
async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await context.bot.get_file(update.message.document.file_id)
    await file.download_to_drive('downloaded_file.pdf')
    await update.message.reply_text("文件已保存!")
```

### 3. 群组管理

```python
# 检查管理员权限
chat_member = await context.bot.get_chat_member(chat_id, user_id)
if chat_member.status in ['administrator', 'creator']:
    # 执行管理员操作
    pass
```

## 部署选项

### 1. Polling (轮询)
适合开发和小规模应用：
```python
await app.run_polling()
```

### 2. Webhook
适合生产环境：
```python
await app.run_webhook(
    listen="0.0.0.0",
    port=8443,
    url_path="your_token"
)
```

## 最佳实践

1. **错误处理**: 始终包装可能失败的操作
2. **日志记录**: 使用结构化日志记录重要事件
3. **配置管理**: 使用环境变量管理敏感信息
4. **限流**: 注意 Telegram API 的速率限制
5. **用户体验**: 提供清晰的命令说明和错误提示

## 调试技巧

1. **启用日志**:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

2. **测试环境**: 创建测试机器人避免影响生产
3. **使用 @BotFather 的 /setcommands** 设置命令菜单

这个指南应该能帮助你理解 Telegram Bot 开发的各个方面！
