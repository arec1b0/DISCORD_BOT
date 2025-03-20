import sqlite3

class DB:
    def __init__(self):
        self.conn = sqlite3.connect('tasks.db')
        self.create_table()

    def create_table(self):
        self.conn.execute('''CREATE TABLE IF NOT EXISTS tasks (
                              id INTEGER PRIMARY KEY AUTOINCREMENT,
                              user_id INTEGER,
                              description TEXT,
                              status BOOLEAN DEFAULT 0)''')
        self.conn.commit()

    def add_task(self, user_id, description):
        self.conn.execute("INSERT INTO tasks (user_id, description) VALUES (?, ?)", (user_id, description))
        self.conn.commit()

    def get_tasks(self, user_id):
        cursor = self.conn.execute("SELECT * FROM tasks WHERE user_id = ?", (user_id,))
        return cursor.fetchall()

    def update_task_status(self, user_id, task_id, status):
        cursor = self.conn.execute("SELECT id FROM tasks WHERE id = ? AND user_id = ?", (task_id, user_id))
        task = cursor.fetchone()
        if not task:
            return False  # Task not found
        self.conn.execute("UPDATE tasks SET status = ? WHERE id = ? AND user_id = ?", (status, task_id, user_id))
        self.conn.commit()
        return True  # Successfully updated

    def delete_task(self, user_id, task_id):
        cursor = self.conn.execute("SELECT id FROM tasks WHERE id = ? AND user_id = ?", (task_id, user_id))
        task = cursor.fetchone()
        if not task:
            return False  # Task not found
        self.conn.execute("DELETE FROM tasks WHERE id = ? AND user_id = ?", (task_id, user_id))
        self.conn.commit()
        return True # Successfully deleted 
