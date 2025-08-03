#!/usr/bin/env python3
"""
Telegram Bot 启动脚本 - 异步版本
使用方法: python run.py
"""
import asyncio
import sys
import os
import signal
import platform

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.bot.main import main

async def handle_shutdown(task):
    """处理优雅关闭"""
    print("\n👋 正在停止机器人...")
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        print("✅ 机器人已安全停止")

def setup_signal_handlers(task):
    """设置信号处理器"""
    if platform.system() != 'Windows':
        # Unix系统信号处理
        loop = asyncio.get_event_loop()
        for sig in (signal.SIGTERM, signal.SIGINT):
            loop.add_signal_handler(
                sig, 
                lambda: asyncio.create_task(handle_shutdown(task))
            )

async def run_bot():
    """异步运行机器人"""
    try:
        print("🚀 正在启动 Telegram Bot...")
        
        # 创建主任务
        main_task = asyncio.create_task(main())
        
        # 设置信号处理
        setup_signal_handlers(main_task)
        
        # 等待任务完成
        await main_task
        
    except KeyboardInterrupt:
        print("\n👋 机器人已停止运行")
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        raise

if __name__ == "__main__":
    # 检查是否有运行中的事件循环
    try:
        # 尝试获取当前事件循环
        loop = asyncio.get_running_loop()
        print("⚠️  检测到运行中的事件循环，使用 create_task 方式")
        # 如果有运行的循环，创建任务
        asyncio.create_task(run_bot())
    except RuntimeError:
        # 没有运行的循环，正常启动
        try:
            if platform.system() == 'Windows':
                # Windows系统使用ProactorEventLoop
                asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
            
            asyncio.run(run_bot())
        except KeyboardInterrupt:
            print("\n👋 程序已退出")
        except Exception as e:
            print(f"❌ 运行失败: {e}")
            sys.exit(1)
