import pytest
import asyncio

from bot.core.bot import BotManager
from bot.commands.base import CommandContext

pytestmark = pytest.mark.asyncio

class TestBotDatabaseIntegration:
    """Интеграционные тесты взаимодействия бота с базой данных."""
    
    async def test_bot_initialization(self, bot_manager: BotManager):
        """Тест инициализации бота с базой данных."""
        assert bot_manager.db is not None
        assert bot_manager.task_handler is not None
        assert bot_manager.help_handler is not None
    
    async def test_task_workflow(self, bot_manager: BotManager, mock_ctx: CommandContext):
        """Тест полного цикла работы с задачей через бот."""
        # Добавление задачи
        await bot_manager.task_handler.add_task(mock_ctx, "Integration test task")
        
        # Проверка списка задач
        tasks = await bot_manager.db.get_tasks(mock_ctx.author.id)
        assert len(tasks) == 1
        task = tasks[0]
        assert task.description == "Integration test task"
        assert not task.status
        
        # Отметка задачи как выполненной
        await bot_manager.task_handler.mark_task_status(mock_ctx, str(task.id), True)
        tasks = await bot_manager.db.get_tasks(mock_ctx.author.id)
        assert tasks[0].status
        
        # Удаление задачи
        await bot_manager.task_handler.delete_task(mock_ctx, str(task.id))
        tasks = await bot_manager.db.get_tasks(mock_ctx.author.id)
        assert len(tasks) == 0
    
    async def test_concurrent_operations(self, bot_manager: BotManager, mock_ctx: CommandContext):
        """Тест конкурентных операций с базой данных."""
        # Создаем несколько задач одновременно
        tasks = []
        for i in range(10):
            tasks.append(bot_manager.task_handler.add_task(mock_ctx, f"Concurrent task {i}"))
        
        await asyncio.gather(*tasks)
        
        # Проверяем, что все задачи созданы
        db_tasks = await bot_manager.db.get_tasks(mock_ctx.author.id)
        assert len(db_tasks) == 10
        
        # Одновременно отмечаем все задачи как выполненные
        mark_tasks = []
        for task in db_tasks:
            mark_tasks.append(bot_manager.task_handler.mark_task_status(mock_ctx, str(task.id), True))
        
        await asyncio.gather(*mark_tasks)
        
        # Проверяем, что все задачи отмечены
        db_tasks = await bot_manager.db.get_tasks(mock_ctx.author.id)
        assert all(task.status for task in db_tasks)
    
    async def test_error_handling(self, bot_manager: BotManager, mock_ctx: CommandContext):
        """Тест обработки ошибок при взаимодействии с базой данных."""
        # Попытка удаления несуществующей задачи
        await bot_manager.task_handler.delete_task(mock_ctx, "999")
        mock_ctx.send.assert_called_with("❌ Задача #999 не найдена или у вас нет прав на её удаление.")
        
        # Попытка отметки несуществующей задачи
        mock_ctx.send.reset_mock()
        await bot_manager.task_handler.mark_task_status(mock_ctx, "999", True)
        mock_ctx.send.assert_called_with("❌ Задача #999 не найдена или у вас нет прав на её изменение.")
        
        # Попытка добавления пустой задачи
        mock_ctx.send.reset_mock()
        await bot_manager.task_handler.add_task(mock_ctx, "")
        mock_ctx.send.assert_called_with("❌ Описание задачи не может быть пустым.") 