from typing import Optional, List

from .base import BaseCommandHandler, CommandContext
from ..config.settings import CommandConstants
from ..database.models import Task

class TaskCommandHandler(BaseCommandHandler):
    """Обработчик команд для управления задачами."""

    async def _validate_task_id(self, ctx: CommandContext, task_id: str) -> Optional[int]:
        """Валидация ID задачи."""
        if not task_id.isdigit():
            await ctx.send("❌ ID задачи должен быть положительным целым числом.")
            return None
            
        task_id = int(task_id)
        if task_id <= 0:
            await ctx.send("❌ ID задачи должен быть положительным целым числом.")
            return None
            
        return task_id

    async def add_task(self, ctx: CommandContext, description: str) -> None:
        """Добавление новой задачи."""
        if not description or description.isspace():
            await ctx.send("❌ Описание задачи не может быть пустым.")
            return
            
        try:
            task_id = await self.db.add_task(ctx.user_id, description)
            await ctx.send(f"✅ Задача добавлена с ID #{task_id}: {description}")
            self.logger.info(f"User {ctx.user_id} added task {task_id}")
        except Exception as e:
            await self._handle_database_error(ctx, e, "добавлении задачи")

    async def list_tasks(self, ctx: CommandContext, page: int = 1) -> None:
        """Вывод списка задач с пагинацией."""
        if page < 1:
            await ctx.send("❌ Номер страницы должен быть не менее 1.")
            return
            
        offset = (page - 1) * CommandConstants.TASKS_PER_PAGE
        
        try:
            tasks: List[Task] = await self.db.get_tasks(ctx.user_id, CommandConstants.TASKS_PER_PAGE, offset)
            total_tasks = await self.db.count_tasks(ctx.user_id)
            
            if not tasks:
                if page == 1:
                    await ctx.send("📋 У вас нет задач!")
                else:
                    await ctx.send(f"❌ Страница {page} не существует. Всего у вас {total_tasks} задач.")
                return
                
            total_pages = (total_tasks + CommandConstants.TASKS_PER_PAGE - 1) // CommandConstants.TASKS_PER_PAGE
            header = f"📋 Задачи (Страница {page}/{total_pages}, всего {total_tasks}):\n"
            
            task_lines = []
            for task in tasks:
                status_icon = '✓' if task.status else '✗'
                task_lines.append(f"#{task.id}: {task.description} ({status_icon})")
            
            response = header + '\n'.join(task_lines)
            
            if total_pages > 1:
                response += f"\n\nИспользуйте `!list {page+1}` для просмотра следующих задач." if page < total_pages else ""
            
            await ctx.send(response)
            self.logger.info(f"User {ctx.user_id} listed tasks (page {page})")
        except Exception as e:
            await self._handle_database_error(ctx, e, "выводе списка задач")

    async def mark_task_status(self, ctx: CommandContext, task_id: str, status: bool) -> None:
        """Изменение статуса задачи."""
        task_id = await self._validate_task_id(ctx, task_id)
        if task_id is None:
            return
        
        try:
            success = await self.db.mark_task_done(ctx.user_id, task_id, status)
            if success:
                status_text = "выполнена" if status else "не выполнена"
                await ctx.send(f"✅ Задача #{task_id} помечена как {status_text}!")
                self.logger.info(f"User {ctx.user_id} marked task {task_id} as {status_text}")
            else:
                await ctx.send(f"❌ Задача #{task_id} не найдена или у вас нет прав на её изменение.")
                self.logger.warning(f"User {ctx.user_id} attempted to mark non-existent task {task_id}")
        except Exception as e:
            await self._handle_database_error(ctx, e, "изменении статуса задачи")

    async def delete_task(self, ctx: CommandContext, task_id: str) -> None:
        """Удаление задачи."""
        task_id = await self._validate_task_id(ctx, task_id)
        if task_id is None:
            return
        
        try:
            success = await self.db.delete_task(ctx.user_id, task_id)
            if success:
                await ctx.send(f"🗑️ Задача #{task_id} удалена!")
                self.logger.info(f"User {ctx.user_id} deleted task {task_id}")
            else:
                await ctx.send(f"❌ Задача #{task_id} не найдена или у вас нет прав на её удаление.")
                self.logger.warning(f"User {ctx.user_id} attempted to delete non-existent task {task_id}")
        except Exception as e:
            await self._handle_database_error(ctx, e, "удалении задачи") 