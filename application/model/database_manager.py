import sqlite3
import os
import arrow
from application.model.todo_item import ToDoItem

class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = None
        self.cursor = None
        self.connect()
        self.create_table()

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
        try:
            formatted_due_date = todo_item.due_date.format('YYYY-MM-DD') if todo_item.due_date else None
            self.cursor.execute('''
                INSERT INTO todo_items (title, priority, status, due_date)
                VALUES (?, ?, ?, ?)
            ''', (todo_item.title, todo_item.priority, todo_item.status, formatted_due_date))
            self.connection.commit()
        except Exception as e: # Catch all exceptions
            print(f"An error occurred: {e}")

    def get_todo_item(self, id):
        self.cursor.execute('SELECT * FROM todo_items WHERE id = ?', (id,))
        row = self.cursor.fetchone()
        if row is not None:
            return ToDoItem(row[0], row[1], row[2], row[3], arrow.get(row[4]) if row[4] else None)
        else:
            return None

    def update_todo_item(self, todo_item):
        # Fetch the current values from the database
        current_todo_item = self.get_todo_item(todo_item.id)
        
        # Use the current values as defaults if no new value is provided
        title = todo_item.title if todo_item.title is not None else current_todo_item.title
        priority = todo_item.priority if todo_item.priority is not None else current_todo_item.priority
        status = todo_item.status if todo_item.status is not None else current_todo_item.status
        due_date = todo_item.due_date if todo_item.due_date is not None else current_todo_item.due_date

        # Format the due date
        formatted_due_date = due_date.format('YYYY-MM-DD') if due_date else None

        # Update the database
        self.cursor.execute('''
            UPDATE todo_items
            SET title = ?, priority = ?, status = ?, due_date = ?
            WHERE id = ?
        ''', (title, priority, status, formatted_due_date, todo_item.id))
        self.connection.commit()
        
    # Add the get_last_inserted_id method to the DatabaseManager class to retrieve the last inserted ID from the database after inserting a new ToDoItem. 
    def get_last_inserted_id(self):
        return self.cursor.lastrowid

    def delete_todo_item(self, id):
        self.cursor.execute('DELETE FROM todo_items WHERE id = ?', (id,))
        self.connection.commit()
        
    def list_todo_items(self):
        self.cursor.execute('SELECT * FROM todo_items')
        rows = self.cursor.fetchall()
        return [ToDoItem(row[0], row[1], row[2], row[3], arrow.get(row[4]) if row[4] else None) for row in rows]

    def get_todo_items_sorted_by(self, field):
        if field == 'priority':
            self.cursor.execute('''
                SELECT * FROM todo_items
                ORDER BY CASE priority
                    WHEN 'High' THEN 1
                    WHEN 'Medium' THEN 2
                    WHEN 'Low' THEN 3
                    ELSE 4
                END
            ''')
        else:
            self.cursor.execute(f"SELECT * FROM todo_items ORDER BY {field}")

        rows = self.cursor.fetchall()
        todo_items = []
        for row in rows:
            id, title, priority, status, due_date = row
            due_date = arrow.get(due_date) if due_date else None
            todo_item = ToDoItem(id, title, priority, status, due_date)
            todo_items.append(todo_item)

        return todo_items
        
        
    def update_todo_status(self, id, status):
        self.cursor.execute("UPDATE todo_items SET status = ? WHERE id = ?", (status, id))
        self.connection.commit()


    def close_connection(self):
        self.connection.close()