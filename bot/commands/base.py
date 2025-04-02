from dataclasses import dataclass
from typing import Callable, Any
import discord
import logging
import traceback
from ..database.base import DatabaseManager, DatabaseError

@dataclass
class CommandContext:
    """Контекст выполнения команды."""
    user_id: int
    channel: discord.TextChannel
    send: Callable[..., Any]
    logger: logging.Logger
    
    async def reply(self, message: str, **kwargs) -> None:
        """Удобный метод для ответа в канал."""
        await self.send(message, **kwargs)

class BaseCommandHandler:
    """Базовый класс для обработчиков команд."""

    def __init__(self, db: DatabaseManager = None, logger: logging.Logger = None):
        self.db = db
        self.logger = logger
        
    async def execute(self, ctx: CommandContext, *args, **kwargs) -> Any:
        """Выполнить команду с обработкой ошибок."""
        try:
            return await self.handle(ctx, *args, **kwargs)
        except Exception as e:
            await self._handle_error(ctx, e, "выполнении команды")
            return None
            
    async def handle(self, ctx: CommandContext, *args, **kwargs) -> Any:
        """Основной метод обработки команды. Должен быть переопределен в дочерних классах."""
        raise NotImplementedError("Метод handle должен быть переопределен")

    async def _handle_database_error(self, ctx: CommandContext, error: Exception, operation: str):
        """Обработка ошибок базы данных."""
        if isinstance(error, DatabaseError):
            await ctx.send(f"❌ Ошибка базы данных при {operation}: {str(error)}")
            self.logger.error(f"Database error in {operation}: {error}")
        else:
            await ctx.send("❌ Произошла непредвиденная ошибка")
            self.logger.error(f"Unexpected error in {operation}: {error}", exc_info=True)
            
    async def _handle_error(self, ctx: CommandContext, error: Exception, operation: str):
        """Универсальная обработка ошибок."""
        if isinstance(error, DatabaseError):
            await self._handle_database_error(ctx, error, operation)
        else:
            await ctx.send(f"❌ Ошибка при {operation}: {str(error)}")
            self.logger.error(f"Error in {operation}: {error}\n{traceback.format_exc()}")