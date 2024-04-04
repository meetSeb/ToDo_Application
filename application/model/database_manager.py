import sqlite3
import arrow
from application.model.todo_item import ToDoItem

class DatabaseManager:
    """ This class is responsible for managing the database connection and executing SQL queries."""
    
    def __init__(self, db_path):
        """ The constructor initializes the database path and calls the connect and create_table methods."""
        self.db_path = db_path
        self.connection = None
        self.cursor = None
        self.connect()
        self.create_table()

    def connect(self):
        """ This method establishes a connection to the database and creates a cursor object."""
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()

    def create_table(self):
        """ This method creates the todo_items table if it does not exist."""
    
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
        """ This method inserts a new todo item into the database."""
        
        # Use the format method of the Arrow library to format the due date in the YYYY-MM-DD format
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
        """ This method retrieves a todo item from the database based on its ID."""
        
        self.cursor.execute('SELECT * FROM todo_items WHERE id = ?', (id,))
        row = self.cursor.fetchone()
        if row is not None: # Check if a row was returned
            return ToDoItem(row[0], row[1], row[2], row[3], arrow.get(row[4]) if row[4] else None)
        else:
            return None

    def update_todo_item(self, todo_item):
        """ This method updates an existing todo item in the database."""
        
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
        
    def get_last_inserted_id(self):
        """ This method retrieves the ID of the last inserted row in the database."""
        return self.cursor.lastrowid

    def delete_todo_item(self, id):
        """ This method deletes a todo item from the database based on its ID."""
        self.cursor.execute('DELETE FROM todo_items WHERE id = ?', (id,))
        self.connection.commit()
        
    def list_todo_items(self):
        """ This method retrieves all todo items from the database and returns them as a list of ToDoItem objects."""
        self.cursor.execute('SELECT * FROM todo_items')
        rows = self.cursor.fetchall()
        return [ToDoItem(row[0], row[1], row[2], row[3], arrow.get(row[4]) if row[4] else None) for row in rows]

    def get_todo_items_sorted_by(self, field):
        """ This method retrieves all todo items from the database and returns them as a list of ToDoItem objects sorted by the specified field."""
        
        # Sort the todo items based on the specified field
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

        # Fetch all rows from the result set and create ToDoItem objects from them
        rows = self.cursor.fetchall()
        todo_items = []
        for row in rows:
            id, title, priority, status, due_date = row
            due_date = arrow.get(due_date) if due_date else None
            todo_item = ToDoItem(id, title, priority, status, due_date)
            todo_items.append(todo_item)

        return todo_items
        
        
    def update_todo_status(self, id, status):
        """ This method updates the status of a todo item in the database."""
        self.cursor.execute("UPDATE todo_items SET status = ? WHERE id = ?", (status, id))
        self.connection.commit()


    def close_connection(self):
        """ This method closes the database connection."""
        self.connection.close()