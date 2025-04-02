from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any

@dataclass
class Task:
    """Модель задачи."""
    id: int
    user_id: int
    description: str
    status: bool
    created_at: datetime

    @classmethod
    def from_db_row(cls, row: Dict[str, Any]) -> 'Task':
        """Создание объекта Task из строки базы данных."""
        return cls(
            id=row['id'],
            user_id=row['user_id'],
            description=row['description'],
            status=bool(row['status']),
            created_at=datetime.fromisoformat(row['created_at'])
        )

    def to_dict(self) -> Dict[str, Any]:
        """Преобразование объекта Task в словарь."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'description': self.description,
            'status': self.status,
            'created_at': self.created_at.isoformat()
        } 