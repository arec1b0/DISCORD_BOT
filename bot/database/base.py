from abc import ABC, abstractmethod
from typing import List, Optional, Protocol, Any
from .models import Task

class DatabaseConnection(Protocol):
    """Протокол для подключения к базе данных."""
    async def execute(self, query: str, params: tuple = ()) -> Any: ...
    async def commit(self) -> None: ...
    async def rollback(self) -> None: ...
    async def close(self) -> None: ...

class DatabaseError(Exception):
    """Базовое исключение для ошибок базы данных."""
    pass

class DatabaseManager(ABC):
    """Абстрактный базовый класс для управления базой данных."""
    
    @abstractmethod
    async def init(self) -> None:
        """Инициализация базы данных."""
        pass

    @abstractmethod
    async def close(self) -> None:
        """Закрытие соединения с базой данных."""
        pass

    @abstractmethod
    async def add_task(self, user_id: int, description: str) -> int:
        """Добавление новой задачи."""
        pass

    @abstractmethod
    async def get_tasks(self, user_id: int, limit: int = 10, offset: int = 0) -> List[Task]:
        """Получение списка задач."""
        pass

    @abstractmethod
    async def mark_task_done(self, user_id: int, task_id: int, status: bool) -> bool:
        """Обновление статуса задачи."""
        pass

    @abstractmethod
    async def delete_task(self, user_id: int, task_id: int) -> bool:
        """Удаление задачи."""
        pass

    @abstractmethod
    async def count_tasks(self, user_id: int, status: Optional[bool] = None) -> int:
        """Подсчет количества задач."""
        pass 