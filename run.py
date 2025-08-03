#!/usr/bin/env python3
"""
Telegram Bot 启动脚本
使用方法: python run.py
"""
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.bot.main import main

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 机器人已停止运行")
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        sys.exit(1)
