import sqlite3

class DB:
    def __init__(self):
        self.create_table()

    def create_table(self):
        with sqlite3.connect('tasks.db') as conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS tasks (
                              id INTEGER PRIMARY KEY AUTOINCREMENT,
                              user_id INTEGER,
                              description TEXT,
                              status BOOLEAN DEFAULT 0)''')
            conn.commit()

    def add_task(self, user_id, description):
        with sqlite3.connect('tasks.db') as conn:
            conn.execute("INSERT INTO tasks (user_id, description) VALUES (?, ?)", (user_id, description))
            conn.commit()

    def get_tasks(self, user_id, limit=10, offset=0):
        with sqlite3.connect('tasks.db') as conn:
            cursor = conn.execute("SELECT * FROM tasks WHERE user_id = ? LIMIT ? OFFSET ?", (user_id, limit, offset))
            return cursor.fetchall()
       
    def update_task_status(self, user_id, task_id, status):
        with sqlite3.connect('tasks.db') as conn:
            cursor = conn.execute("SELECT id FROM tasks WHERE id = ? AND user_id = ?", (task_id, user_id))
            task = cursor.fetchone()
            if not task:
                return False  # Task not found
            conn.execute("UPDATE tasks SET status = ? WHERE id = ? AND user_id = ?", (status, task_id, user_id))
            conn.commit()
            return True  # Successfully updated

    def delete_task(self, user_id, task_id):
        with sqlite3.connect('tasks.db') as conn:
            cursor = conn.execute("SELECT id FROM tasks WHERE id = ? AND user_id = ?", (task_id, user_id))
            task = cursor.fetchone()
            if not task:
                return False  # Task not found
            conn.execute("DELETE FROM tasks WHERE id = ? AND user_id = ?", (task_id, user_id))
            conn.commit()
            return True  # Successfully deleted
