import pytest
from typing import AsyncGenerator, Tuple
import discord

from bot.core.bot import BotManager
from bot.config.settings import create_config
from bot.database.sqlite import SQLiteDatabaseManager

pytestmark = pytest.mark.asyncio

class MockGuild:
    """Мок гильдии Discord."""
    def __init__(self, guild_id: int):
        self.id = guild_id
        self.name = f"Test Guild {guild_id}"

class MockChannel:
    """Мок канала Discord."""
    def __init__(self, channel_id: int):
        self.id = channel_id
        self.name = f"test-channel-{channel_id}"
        self.messages = []
    
    async def send(self, content: str = None, *, embed: discord.Embed = None):
        """Имитация отправки сообщения."""
        message = MockMessage(
            content=content,
            embed=embed,
            channel=self,
            author=MockUser(0, "Bot", True)
        )
        self.messages.append(message)
        return message

class MockUser:
    """Мок пользователя Discord."""
    def __init__(self, user_id: int, name: str, is_bot: bool = False):
        self.id = user_id
        self.name = name
        self.bot = is_bot

class MockMessage:
    """Мок сообщения Discord."""
    def __init__(self, content: str = None, embed: discord.Embed = None, channel: MockChannel = None, author: MockUser = None):
        self.content = content
        self.embed = embed
        self.channel = channel
        self.author = author

@pytest.fixture
async def e2e_environment() -> AsyncGenerator[Tuple[BotManager, MockGuild, MockChannel, MockUser], None]:
    """Создание окружения для E2E тестов."""
    config = create_config()
    
    # Создаем тестовое окружение
    guild = MockGuild(1)
    channel = MockChannel(1)
    user = MockUser(123456789, "Test User")
    
    # Создаем менеджер бота
    bot_manager = BotManager(config)
    bot_manager.db = SQLiteDatabaseManager(db_path="e2e_test.db")
    await bot_manager.db.init()
    
    # Инициализируем бота и обработчики команд
    await bot_manager.initialize()
    
    # Создаем обработчики команд
    from bot.commands.task import TaskCommandHandler
    from bot.commands.help import HelpCommandHandler
    
    bot_manager.task_handler = TaskCommandHandler(bot_manager.db, bot_manager.logger)
    bot_manager.help_handler = HelpCommandHandler(bot_manager.logger)
    
    yield bot_manager, guild, channel, user
    
    await bot_manager.cleanup()

class TestBotEndToEnd:
    """End-to-end тесты бота."""
    
    async def test_complete_task_workflow(self, e2e_environment: Tuple[BotManager, MockGuild, MockChannel, MockUser]):
        """Тест полного цикла работы с задачей."""
        bot_manager, guild, channel, user = e2e_environment
        
        # Создаем контекст команды
        from bot.commands.base import CommandContext
        
        ctx = CommandContext(
            user_id=user.id,
            channel=channel,
            send=channel.send,
            logger=bot_manager.logger
        )
        
        # Непосредственно вызываем обработчики команд вместо process_commands
        
        # Добавление задачи
        await bot_manager.task_handler.add_task(ctx, "Test E2E task")
        
        # Проверяем, что задача добавлена
        response = channel.messages[-1]
        assert "✅" in response.content
        assert "Test E2E task" in response.content
        
        # Получаем ID задачи из ответа
        task_id = response.content.split("#")[1].split(":")[0]
        
        # Запрос списка задач
        await bot_manager.task_handler.list_tasks(ctx, page=1)
        
        # Проверяем список задач
        response = channel.messages[-1]
        assert "Test E2E task" in response.content
        assert "✗" in response.content  # Задача не выполнена
        
        # Отметка задачи как выполненной
        await bot_manager.task_handler.mark_task_status(ctx, task_id, True)
        
        # Проверяем статус задачи
        response = channel.messages[-1]
        assert "✅" in response.content
        assert "выполнена" in response.content
        
        # Удаление задачи
        await bot_manager.task_handler.delete_task(ctx, task_id)
        
        # Проверяем удаление задачи
        response = channel.messages[-1]
        assert "🗑️" in response.content
        assert "удалена" in response.content
    
    async def test_help_command(self, e2e_environment: Tuple[BotManager, MockGuild, MockChannel, MockUser]):
        """Тест команды помощи."""
        bot_manager, guild, channel, user = e2e_environment
        
        # Создаем контекст команды
        from bot.commands.base import CommandContext
        
        ctx = CommandContext(
            user_id=user.id,
            channel=channel,
            send=channel.send,
            logger=bot_manager.logger
        )
        
        # Вызываем справку напрямую
        await bot_manager.help_handler.show_help(ctx)
        
        response = channel.messages[-1]
        assert response.embed is not None
        assert "Task Manager Bot" in response.embed.title
        
        # Проверяем наличие всех команд в справке
        field_names = [field.name for field in response.embed.fields]
        assert any("!add" in name for name in field_names)
        assert any("!list" in name for name in field_names)
        assert any("!done" in name for name in field_names)
        assert any("!delete" in name for name in field_names)
    
    async def test_error_handling(self, e2e_environment: Tuple[BotManager, MockGuild, MockChannel, MockUser]):
        """Тест обработки ошибок."""
        bot_manager, guild, channel, user = e2e_environment
        
        # Создаем контекст команды
        from bot.commands.base import CommandContext
        
        ctx = CommandContext(
            user_id=user.id,
            channel=channel,
            send=channel.send,
            logger=bot_manager.logger
        )
        
        # Тест некорректного ID задачи
        await bot_manager.task_handler.mark_task_status(ctx, "invalid_id", True)
        
        response = channel.messages[-1]
        assert "❌" in response.content
        assert "ID задачи должен быть положительным целым числом" in response.content
        
        # Тест пустого описания задачи
        await bot_manager.task_handler.add_task(ctx, "")
        
        response = channel.messages[-1]
        assert "❌" in response.content
        assert "Описание задачи не может быть пустым" in response.content 