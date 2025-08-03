#!/usr/bin/env python3
"""
TeleBot 启动测试脚本
验证机器人是否可以正常启动
"""
import sys
import os
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_imports():
    """测试所有必要的模块是否可以正常导入"""
    try:
        print("🔍 测试模块导入...")
        
        # 测试基础导入
        from src.bot.main import main
        print("✅ main 模块导入成功")
        
        from src.bot.utils.config import get_bot_token, setup_logging
        print("✅ config 模块导入成功")
        
        from src.bot.handlers.commands import start_command, help_command, update_command
        print("✅ commands 模块导入成功")
        
        from src.bot.handlers.messages import handle_text_message
        print("✅ messages 模块导入成功")
        
        # 测试第三方依赖
        import telegram
        print(f"✅ python-telegram-bot {telegram.__version__} 导入成功")
        
        import loguru
        print("✅ loguru 导入成功")
        
        import dotenv
        print("✅ python-dotenv 导入成功")
        
        return True
        
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        return False
    except Exception as e:
        print(f"❌ 未知错误: {e}")
        return False

def test_config():
    """测试配置是否正确"""
    try:
        print("\n🔍 测试配置...")
        
        from dotenv import load_dotenv
        load_dotenv()
        
        token = os.getenv("TELEGRAM_BOT_TOKEN")
        if not token:
            print("❌ TELEGRAM_BOT_TOKEN 未设置")
            return False
        elif token == "your_bot_token_here":
            print("⚠️  TELEGRAM_BOT_TOKEN 仍是示例值")
            return False
        else:
            print("✅ TELEGRAM_BOT_TOKEN 已配置")
            
        log_level = os.getenv("LOG_LEVEL", "INFO")
        print(f"✅ LOG_LEVEL: {log_level}")
        
        debug = os.getenv("DEBUG", "False")
        print(f"✅ DEBUG: {debug}")
        
        return True
        
    except Exception as e:
        print(f"❌ 配置测试错误: {e}")
        return False

def main_test():
    """主测试函数"""
    print("🚀 TeleBot 启动验证测试")
    print("=" * 50)
    
    # 测试导入
    imports_ok = test_imports()
    
    # 测试配置
    config_ok = test_config()
    
    print("\n" + "=" * 50)
    print("📋 测试结果:")
    
    if imports_ok and config_ok:
        print("✅ 所有测试通过！机器人应该可以正常启动")
        print("\n🎯 要启动机器人，请运行:")
        print("   python run.py")
        return True
    else:
        print("❌ 部分测试失败，请检查上述错误")
        return False

if __name__ == "__main__":
    success = main_test()
    sys.exit(0 if success else 1)
