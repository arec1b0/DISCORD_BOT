import pytest
from unittest.mock import MagicMock
import discord

from bot.commands.task import TaskCommandHandler
from bot.commands.help import HelpCommandHandler
from bot.database.sqlite import SQLiteDatabaseManager

pytestmark = pytest.mark.asyncio

class TestTaskCommands:
    """Тесты команд управления задачами."""
    
    @pytest.fixture
    def task_handler(self, test_db: SQLiteDatabaseManager, mock_ctx: MagicMock) -> TaskCommandHandler:
        """Создание обработчика команд для тестов."""
        logger = MagicMock()
        return TaskCommandHandler(test_db, logger)
    
    async def test_add_task(self, task_handler: TaskCommandHandler, mock_ctx: MagicMock):
        """Тест команды добавления задачи."""
        await task_handler.add_task(mock_ctx, "Test task")
        
        mock_ctx.send.assert_called_once()
        message = mock_ctx.send.call_args[0][0]
        assert "✅" in message
        assert "Test task" in message
    
    async def test_list_tasks_empty(self, task_handler: TaskCommandHandler, mock_ctx: MagicMock):
        """Тест команды списка задач когда нет задач."""
        await task_handler.list_tasks(mock_ctx)
        
        mock_ctx.send.assert_called_once()
        message = mock_ctx.send.call_args[0][0]
        assert "У вас нет задач" in message
    
    async def test_list_tasks_with_pagination(self, task_handler: TaskCommandHandler, mock_ctx: MagicMock, test_db: SQLiteDatabaseManager):
        """Тест пагинации списка задач."""
        # Создаем 15 задач
        for i in range(15):
            await test_db.add_task(mock_ctx.author.id, f"Task {i+1}")
        
        # Проверяем первую страницу
        await task_handler.list_tasks(mock_ctx, page=1)
        first_page = mock_ctx.send.call_args[0][0]
        assert "Страница 1/2" in first_page
        assert "Task 1" in first_page
        assert "Task 10" in first_page
        
        # Проверяем вторую страницу
        mock_ctx.send.reset_mock()
        await task_handler.list_tasks(mock_ctx, page=2)
        second_page = mock_ctx.send.call_args[0][0]
        assert "Страница 2/2" in second_page
        assert "Task 11" in second_page
        assert "Task 15" in second_page
    
    async def test_mark_task_done(self, task_handler: TaskCommandHandler, mock_ctx: MagicMock, test_db: SQLiteDatabaseManager):
        """Тест команды отметки задачи как выполненной."""
        task_id = await test_db.add_task(mock_ctx.author.id, "Task to complete")
        
        await task_handler.mark_task_status(mock_ctx, str(task_id), True)
        
        mock_ctx.send.assert_called_once()
        message = mock_ctx.send.call_args[0][0]
        assert "✅" in message
        assert "выполнена" in message
        
        tasks = await test_db.get_tasks(mock_ctx.author.id)
        assert tasks[0].status
    
    async def test_delete_task(self, task_handler: TaskCommandHandler, mock_ctx: MagicMock, test_db: SQLiteDatabaseManager):
        """Тест команды удаления задачи."""
        task_id = await test_db.add_task(mock_ctx.author.id, "Task to delete")
        
        await task_handler.delete_task(mock_ctx, str(task_id))
        
        mock_ctx.send.assert_called_once()
        message = mock_ctx.send.call_args[0][0]
        assert "🗑️" in message
        assert "удалена" in message
        
        tasks = await test_db.get_tasks(mock_ctx.author.id)
        assert len(tasks) == 0

class TestHelpCommand:
    """Тесты команды помощи."""
    
    @pytest.fixture
    def help_handler(self, mock_ctx: MagicMock) -> HelpCommandHandler:
        """Создание обработчика команды help для тестов."""
        logger = MagicMock()
        return HelpCommandHandler(logger)
    
    async def test_show_help(self, help_handler: HelpCommandHandler, mock_ctx: MagicMock):
        """Тест отображения справки."""
        await help_handler.show_help(mock_ctx)
        
        mock_ctx.send.assert_called_once()
        # Проверяем, что аргумент передан в именованный параметр embed
        kwargs = mock_ctx.send.call_args.kwargs
        assert "embed" in kwargs
        
        embed = kwargs["embed"]
        assert isinstance(embed, discord.Embed)
        assert "Task Manager Bot" in embed.title
        assert len(embed.fields) > 0
        
        # Проверяем наличие всех команд в справке
        commands = [field.name for field in embed.fields]
        assert "!add" in "".join(commands)
        assert "!list" in "".join(commands)
        assert "!done" in "".join(commands)
        assert "!delete" in "".join(commands) 