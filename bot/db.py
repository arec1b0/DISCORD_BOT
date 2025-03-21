import aiosqlite

class DB:
    def __init__(self):
        pass  # No need for immediate connection setup

    async def create_table(self):
        async with aiosqlite.connect('tasks.db') as db:
            await db.execute('''CREATE TABLE IF NOT EXISTS tasks (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                user_id INTEGER,
                                description TEXT,
                                status BOOLEAN DEFAULT 0)''')
            await db.execute("CREATE INDEX IF NOT EXISTS idx_user_id ON tasks(user_id);")
            await db.commit()

    async def add_task(self, user_id, description):
        async with aiosqlite.connect('tasks.db') as db:
            await db.execute("INSERT INTO tasks (user_id, description) VALUES (?, ?)", (user_id, description))
            await db.commit()

    async def get_tasks(self, user_id, limit=10, offset=0):
        async with aiosqlite.connect('tasks.db') as db:
            cursor = await db.execute("SELECT * FROM tasks WHERE user_id = ? LIMIT ? OFFSET ?", (user_id, limit, offset))
            return await cursor.fetchall()

    async def update_task_status(self, user_id, task_id, status):
        async with aiosqlite.connect('tasks.db') as db:
            cursor = await db.execute("SELECT id FROM tasks WHERE id = ? AND user_id = ?", (task_id, user_id))
            task = await cursor.fetchone()
            if not task:
                return False  # Task not found
            await db.execute("UPDATE tasks SET status = ? WHERE id = ? AND user_id = ?", (status, task_id, user_id))
            await db.commit()
            return True  # Successfully updated

    async def delete_task(self, user_id, task_id):
        async with aiosqlite.connect('tasks.db') as db:
            cursor = await db.execute("SELECT id FROM tasks WHERE id = ? AND user_id = ?", (task_id, user_id))
            task = await cursor.fetchone()
            if not task:
                return False  # Task not found
            await db.execute("DELETE FROM tasks WHERE id = ? AND user_id = ?", (task_id, user_id))
            await db.commit()
            return True  # Successfully deleted
