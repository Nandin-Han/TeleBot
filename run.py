#!/usr/bin/env python3
"""
TeleBot 启动脚本
项目的主入口点，用于启动 Telegram 机器人
"""
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.bot.main import main
from loguru import logger

def run_bot() -> None:
    """
    启动机器人的主函数
    处理启动流程和异常
    """
    try:
        logger.info("正在启动 TeleBot...")
        print("🚀 启动 TeleBot - Telegram 机器人")
        print("📋 项目基于 Python 3.13 和 python-telegram-bot v22")
        print("=" * 50)
        
        # 运行同步主函数
        main()
        
    except KeyboardInterrupt:
        print("\n" + "=" * 50)
        print("👋 机器人已被用户手动停止")
        logger.info("机器人已被用户手动停止")
        
    except Exception as error:
        print("\n" + "=" * 50)
        print(f"❌ 启动失败: {error}")
        logger.error(f"机器人启动失败: {error}")
        sys.exit(1)
        
    finally:
        print("🔚 TeleBot 已完全停止")

if __name__ == "__main__":
    run_bot()
