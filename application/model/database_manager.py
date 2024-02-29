
import sqlite3
import arrow
from application.model.todo_item import ToDoItem

class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS todo_items(
                id INTEGER PRIMARY KEY,
                title TEXT,
                priority TEXT,
                status TEXT,
                due_date TEXT
            )
        ''')
        self.connection.commit()

    def insert_todo_item(self, todo_item):
        self.cursor.execute('''
        INSERT INTO todo_items(id, title, priority, status, due_date)
        VALUES (?, ?, ?, ?, ?)
    ''', (todo_item.id, todo_item.title, todo_item.priority, todo_item.status, todo_item.due_date.format('YYYY-MM-DD')))
        self.connection.commit()

    def get_todo_item(self, id):
        self.cursor.execute('''
        SELECT * FROM todo_items WHERE id = ?
        ''', (id,))
        row = self.cursor.fetchone()
        if row is not None:
            return ToDoItem(row[0], row[1], row[2], row[3], arrow.get(row[4]))
        else:
            return None

    def update_todo_item(self, todo_item):
        self.cursor.execute('''
            UPDATE todo_items
            SET title = ?, priority = ?, status = ?, due_date = ?
            WHERE id = ?
        ''', (todo_item.title, todo_item.priority, todo_item.status, todo_item.due_date.format('YYYY-MM-DD'), todo_item.id))
        self.connection.commit()

    def delete_todo_item(self, id):
        self.cursor.execute('''
            DELETE FROM todo_items WHERE id = ?
        ''', (id,))
        self.connection.commit()
        
    def list_todo_items(self):
        self.cursor.execute('SELECT * FROM todo_items')
        rows = self.cursor.fetchall()
        return [ToDoItem(row[0], row[1], row[2], row[3], arrow.get(row[4])) for row in rows]
    

    def close_connection(self):
        self.connection.close()
        
        
