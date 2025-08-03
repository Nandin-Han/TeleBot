"""
Telegram Bot 主入口文件
"""
import logging
import sys
import os
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler
from loguru import logger

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from src.bot.handlers.commands import start_command, help_command
from src.bot.utils.config import get_bot_token, setup_logging

def main():
    """启动Telegram机器人"""
    # 加载环境变量
    load_dotenv()
    
    # 设置日志
    setup_logging()
    
    # 获取机器人Token
    token = get_bot_token()
    
    # 检查Token是否为示例值
    if token == "your_bot_token_here":
        logger.error("请在 .env 文件中设置真实的 TELEGRAM_BOT_TOKEN")
        print("❌ 请按以下步骤配置机器人:")
        print("1. 在 Telegram 中联系 @BotFather")
        print("2. 发送 /newbot 创建新机器人")
        print("3. 将获得的 Token 复制到 .env 文件中")
        print("4. 替换 TELEGRAM_BOT_TOKEN=your_bot_token_here 中的 your_bot_token_here")
        return
    
    # 创建应用
    logger.info("正在初始化 Telegram Bot Application...")
    app = Application.builder().token(token).build()
    
    # 注册命令处理器
    logger.info("正在注册命令处理器...")
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    
    # 启动机器人
    logger.info("🤖 Telegram Bot 启动成功！正在监听消息...")
    print("🤖 Telegram Bot 正在运行中... (按 Ctrl+C 停止)")
    
    # 运行轮询 - 使用同步版本
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 机器人已停止运行")
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        sys.exit(1)
