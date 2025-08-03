"""
测试命令处理器
"""
import pytest
from unittest.mock import AsyncMock, MagicMock
from src.bot.handlers.commands import start_command, help_command

class TestCommandHandlers:
    """命令处理器测试类"""

    @pytest.mark.asyncio
    async def test_start_command(self):
        """测试 /start 命令"""
        # 模拟 Update 对象
        update = MagicMock()
        update.effective_user.first_name = "TestUser"
        update.effective_user.id = 123456
        update.effective_chat.id = 123456
        update.message.reply_text = AsyncMock()
        
        # 模拟 Context 对象
        context = MagicMock()
        
        # 执行命令
        await start_command(update, context)
        
        # 验证回复消息被调用
        update.message.reply_text.assert_called_once()
        
        # 验证回复内容包含用户名
        call_args = update.message.reply_text.call_args
        assert "TestUser" in call_args[0][0]

    @pytest.mark.asyncio
    async def test_help_command(self):
        """测试 /help 命令"""
        # 模拟 Update 对象
        update = MagicMock()
        update.effective_user.first_name = "TestUser"
        update.effective_user.id = 123456
        update.message.reply_text = AsyncMock()
        
        # 模拟 Context 对象
        context = MagicMock()
        
        # 执行命令
        await help_command(update, context)
        
        # 验证回复消息被调用
        update.message.reply_text.assert_called_once()
        
        # 验证回复内容包含帮助信息
        call_args = update.message.reply_text.call_args
        assert "帮助文档" in call_args[0][0]
