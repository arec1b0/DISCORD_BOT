import aiosqlite
import asyncio
import logging
from contextlib import asynccontextmanager
from typing import Optional, List

from .base import DatabaseManager, DatabaseConnection, DatabaseError
from .models import Task
from ..config.settings import DatabaseConstants

class SQLiteDatabaseManager(DatabaseManager):
    """Реализация менеджера базы данных для SQLite."""

    def __init__(self, db_path: str = DatabaseConstants.DB_PATH):
        self.db_path = db_path
        self.lock = asyncio.Lock()
        self.logger = logging.getLogger('discord_bot.db')
        self._connection: Optional[DatabaseConnection] = None

    @asynccontextmanager
    async def get_db(self) -> DatabaseConnection:
        """Контекстный менеджер для работы с базой данных."""
        if self._connection is None:
            self._connection = await aiosqlite.connect(self.db_path)
            self._connection.row_factory = aiosqlite.Row
        
        try:
            async with self._connection.cursor():
                yield self._connection
        except Exception as e:
            self.logger.error(f"Database operation failed: {e}")
            await self._connection.rollback()
            raise DatabaseError(f"Database operation failed: {e}")

    async def init(self) -> None:
        """Инициализация базы данных с созданием необходимых таблиц и индексов."""
        try:
            async with self.get_db() as db:
                await self._create_tables(db)
                await self._create_indexes(db)
                await db.commit()
            self.logger.info("Database initialized successfully")
        except Exception as e:
            self.logger.error(f"Database initialization failed: {e}")
            raise DatabaseError(f"Failed to initialize database: {e}")

    async def _create_tables(self, db: DatabaseConnection) -> None:
        """Создание таблиц базы данных."""
        max_len = DatabaseConstants.MAX_DESCRIPTION_LENGTH
        await db.execute(f'''CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            description TEXT NOT NULL CHECK(length(description) <= {max_len}),
            status BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

    async def _create_indexes(self, db: DatabaseConnection) -> None:
        """Создание индексов для оптимизации запросов."""
        await db.execute("CREATE INDEX IF NOT EXISTS idx_user_id ON tasks(user_id);")
        await db.execute("CREATE INDEX IF NOT EXISTS idx_user_task ON tasks(user_id, id);")

    async def close(self) -> None:
        """Закрытие соединения с базой данных."""
        if self._connection is not None:
            await self._connection.close()
            self._connection = None
            self.logger.info("Database connection closed")

    async def add_task(self, user_id: int, description: str) -> int:
        """Добавление новой задачи."""
        if not isinstance(user_id, int):
            raise ValueError("user_id must be an integer")
            
        if len(description) > DatabaseConstants.MAX_DESCRIPTION_LENGTH:
            description = description[:DatabaseConstants.MAX_DESCRIPTION_LENGTH]
            self.logger.warning(f"Task description truncated for user {user_id}")
        
        try:
            async with self.get_db() as db:
                cursor = await db.execute(
                    "INSERT INTO tasks (user_id, description) VALUES (?, ?)",
                    (user_id, description)
                )
                await db.commit()
                return cursor.lastrowid
        except Exception as e:
            self.logger.error(f"Error adding task: {e}")
            raise DatabaseError(f"Failed to add task: {e}")

    async def get_tasks(self, user_id: int, limit: int = DatabaseConstants.DEFAULT_TASK_LIMIT, offset: int = 0) -> List[Task]:
        """Получение списка задач с пагинацией."""
        if not isinstance(user_id, int):
            raise ValueError("user_id must be an integer")
            
        try:
            async with self.get_db() as db:
                cursor = await db.execute(
                    "SELECT * FROM tasks WHERE user_id = ? ORDER BY id LIMIT ? OFFSET ?",
                    (user_id, limit, offset)
                )
                rows = await cursor.fetchall()
                return [Task.from_db_row(dict(row)) for row in rows]
        except Exception as e:
            self.logger.error(f"Error getting tasks: {e}")
            raise DatabaseError(f"Failed to retrieve tasks: {e}")

    async def mark_task_done(self, user_id: int, task_id: int, status: bool) -> bool:
        """Обновление статуса задачи."""
        if not isinstance(user_id, int) or not isinstance(task_id, int):
            raise ValueError("user_id and task_id must be integers")
            
        try:
            async with self.get_db() as db:
                cursor = await db.execute(
                    "UPDATE tasks SET status = ? WHERE id = ? AND user_id = ?",
                    (status, task_id, user_id)
                )
                await db.commit()
                return cursor.rowcount > 0
        except Exception as e:
            self.logger.error(f"Error marking task {task_id} as {'done' if status else 'not done'}: {e}")
            raise DatabaseError(f"Failed to update task status: {e}")

    async def delete_task(self, user_id: int, task_id: int) -> bool:
        """Удаление задачи."""
        if not isinstance(user_id, int) or not isinstance(task_id, int):
            raise ValueError("user_id and task_id must be integers")
            
        try:
            async with self.get_db() as db:
                cursor = await db.execute(
                    "DELETE FROM tasks WHERE id = ? AND user_id = ?",
                    (task_id, user_id)
                )
                await db.commit()
                return cursor.rowcount > 0
        except Exception as e:
            self.logger.error(f"Error deleting task {task_id}: {e}")
            raise DatabaseError(f"Failed to delete task: {e}")

    async def count_tasks(self, user_id: int, status: Optional[bool] = None) -> int:
        """Подсчет количества задач с опциональной фильтрацией по статусу."""
        if not isinstance(user_id, int):
            raise ValueError("user_id must be an integer")
            
        try:
            async with self.get_db() as db:
                if status is None:
                    cursor = await db.execute(
                        "SELECT COUNT(*) FROM tasks WHERE user_id = ?", 
                        (user_id,)
                    )
                else:
                    cursor = await db.execute(
                        "SELECT COUNT(*) FROM tasks WHERE user_id = ? AND status = ?", 
                        (user_id, status)
                    )
                result = await cursor.fetchone()
                return result[0]
        except Exception as e:
            self.logger.error(f"Error counting tasks: {e}")
            raise DatabaseError(f"Failed to count tasks: {e}") 