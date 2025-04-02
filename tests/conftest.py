import os
import asyncio
import pytest
from typing import AsyncGenerator
from unittest.mock import AsyncMock, MagicMock

from discord.ext import commands

from bot.config.settings import BotConfig, BotConstants
from bot.core.bot import BotManager
from bot.database.sqlite import SQLiteDatabaseManager

@pytest.fixture
def event_loop_policy() -> asyncio.AbstractEventLoopPolicy:
    """Создает политику цикла событий для тестов."""
    return asyncio.get_event_loop_policy()

@pytest.fixture
async def test_db() -> AsyncGenerator[SQLiteDatabaseManager, None]:
    """Create a test database instance."""
    test_db_path = "test_tasks.db"
    if os.path.exists(test_db_path):
        os.remove(test_db_path)
    
    db = SQLiteDatabaseManager(db_path=test_db_path)
    await db.init()
    
    yield db
    
    await db.close()
    if os.path.exists(test_db_path):
        os.remove(test_db_path)

@pytest.fixture
def bot_config() -> BotConfig:
    """Create a test bot configuration."""
    return BotConfig(
        token="test_token",
        prefix="!",
        log_level=BotConstants.LOG_LEVEL,
        log_format=BotConstants.LOG_FORMAT,
        log_file="test_bot.log"
    )

@pytest.fixture
async def mock_bot() -> AsyncGenerator[commands.Bot, None]:
    """Create a mock bot instance."""
    bot = MagicMock(spec=commands.Bot)
    bot.command = MagicMock()
    bot.event = MagicMock()
    bot.add_listener = AsyncMock()
    bot.start = AsyncMock()
    bot.close = AsyncMock()
    
    yield bot

@pytest.fixture
def mock_ctx() -> MagicMock:
    """Create a mock context for command testing."""
    from bot.commands.base import CommandContext
    import logging
    
    logger = MagicMock(spec=logging.Logger)
    
    # Создаем AsyncMock для send
    send_mock = AsyncMock()
    
    # Создаем CommandContext с правильным user_id
    ctx = CommandContext(
        user_id=123456789,
        channel=MagicMock(),
        send=send_mock,
        logger=logger
    )
    
    # Добавляем дополнительные атрибуты, которые могут понадобиться в тестах
    ctx.author = MagicMock()
    ctx.author.id = 123456789
    ctx.reply = AsyncMock()
    
    return ctx

@pytest.fixture
async def bot_manager(bot_config: BotConfig, test_db: SQLiteDatabaseManager, mock_bot: commands.Bot) -> AsyncGenerator[BotManager, None]:
    """Create a bot manager instance for testing."""
    manager = BotManager(bot_config)
    manager.db = test_db
    manager.bot = mock_bot
    
    # Инициализация обработчиков команд
    from bot.commands.task import TaskCommandHandler
    from bot.commands.help import HelpCommandHandler
    
    manager.task_handler = TaskCommandHandler(test_db, manager.logger)
    manager.help_handler = HelpCommandHandler(manager.logger)
    
    yield manager
    
    await manager.cleanup() 