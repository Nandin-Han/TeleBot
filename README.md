# TeleBot - Python Telegram Bot

基于 Python 3.13 和 python-telegram-bot v22 的 Telegram 机器人项目。

## 快速开始

### 1. 获取 Bot Token
1. 在 Telegram 中找到 [@BotFather](https://t.me/botfather)
2. 发送 `/newbot` 创建新机器人
3. 按提示设置机器人名称和用户名
4. 获得 Bot Token (格式: `123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ`)

### 2. 配置环境
```bash
# 复制环境变量模板
cp config/.env.example .env

# 编辑 .env 文件，添加你的 Bot Token
TELEGRAM_BOT_TOKEN=your_bot_token_here
```

### 3. 环境设置
```bash
# 使用项目标准虚拟环境
source venv/bin/activate
pip install -r requirements.txt
```

### 4. 启动机器人
```bash
venv/bin/python run.py  # 直接运行主脚本
```

## 项目结构

```
TeleBot/
├── src/bot/                 # 机器人核心代码
│   ├── main.py             # 主入口文件
│   ├── handlers/           # 命令和消息处理器
│   └── utils/              # 工具函数
├── config/                 # 配置文件
├── logs/                   # 日志文件
├── tests/                  # 测试文件
└── docs/                   # 文档
```

## 功能特性

- ✅ `/start` 命令 - 欢迎新用户
- 🔄 **异步处理** - 高性能并发架构
- 📝 日志记录 - 便于调试
- 🔧 模块化设计 - 易于扩展
- ⚡ 优雅启动/停止 - 完整的资源管理

## 开发指南

详细的开发指南和 Telegram Bot API 教程请查看 [docs/telegram_bot_guide.md](docs/telegram_bot_guide.md)

## 许可证

MIT License
