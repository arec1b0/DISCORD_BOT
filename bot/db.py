import aiosqlite
import asyncio
from contextlib import asynccontextmanager

class DB:
    def __init__(self):
        self.db_path = 'tasks.db'
        self.lock = asyncio.Lock()

    async def init(self):
        # Initializing the database.
        async with self.get_db() as db:
            await db.execute('''CREATE TABLE IF NOT EXISTS tasks (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                user_id INTEGER,
                                description TEXT,
                                status BOOLEAN DEFAULT 0)''')
            await db.execute("CREATE INDEX IF NOT EXISTS idx_user_id ON tasks(user_id);")
            await db.commit()

    @asynccontextmanager
    async def get_db(self):
        #Context manager to manage the database connection.
        conn = await aiosqlite.connect(self.db_path)
        conn.row_factory = aiosqlite.Row  # For easy key access
        try:
            yield conn
        finally:
            await conn.close()

    async def add_task(self, user_id, description):
        # Adding a new task.
        try:
            async with self.get_db() as db:
                await db.execute("INSERT INTO tasks (user_id, description) VALUES (?, ?)",
                                 (user_id, description))
                await db.commit()
        except Exception as e:
            print(f"Error when adding a task: {e}")

    async def get_tasks(self, user_id, limit=10, offset=0):
        # Get the list of tasks with pagination.
        try:
            async with self.get_db() as db:
                cursor = await db.execute("SELECT * FROM tasks WHERE user_id = ? LIMIT ? OFFSET ?",
                                          (user_id, limit, offset))
                return await cursor.fetchall()
        except Exception as e:
            print(f"Error when getting tasks: {e}")
            return []

    async def update_task_status(self, user_id, task_id, status):
        # Updating the task status.
        try:
            async with self.get_db() as db:
                cursor = await db.execute("SELECT id FROM tasks WHERE id = ? AND user_id = ?",
                                          (task_id, user_id))
                task = await cursor.fetchone()
                if not task:
                    return False  # Task not found
                await db.execute("UPDATE tasks SET status = ? WHERE id = ? AND user_id = ?",
                                 (status, task_id, user_id))
                await db.commit()
                return True  # Successfully updated
        except Exception as e:
            print(f"Error when updating task status: {e}")
            return False

    async def delete_task(self, user_id, task_id):
        # Deleting a task.
        try:
            async with self.get_db() as db:
                cursor = await db.execute("SELECT id FROM tasks WHERE id = ? AND user_id = ?",
                                          (task_id, user_id))
                task = await cursor.fetchone()
                if not task:
                    return False  # Task not found
                await db.execute("DELETE FROM tasks WHERE id = ? AND user_id = ?",
                                 (task_id, user_id))
                await db.commit()
                return True  # Successfully deleted
        except Exception as e:
            print(f"Error when deleting a task: {e}")
            return False