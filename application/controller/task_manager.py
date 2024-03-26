
from application.model.todo_item import ToDoItem
from application.model.database_manager import DatabaseManager


class TaskManager:
    def __init__(self, db_manager):
        self.db_manager = DatabaseManager('/Users/sebastianahlburg/Documents/Studium/Studium Informatik/IU/Module/Projekt Software Engineering/ToDo_Application/todo_list.db') 
    
    def create_todo_item(self, title, priority=None, status=None, due_date=None):
        if not title:
            raise ValueError("Title cannot be empty")
        todo_item = ToDoItem(None, title, priority, status, due_date)
        self.db_manager.insert_todo_item(todo_item)
        todo_item.id = self.db_manager.get_last_inserted_id()  # Retrieve the ID from the database and set it on the object 
        return todo_item

    def get_todo_item(self, id):
        todo_item = self.db_manager.get_todo_item(id)
        if todo_item is None:
            raise ValueError(f"No ToDoItem found with id {id}")
        return todo_item

    def update_todo_item(self, id, title=None, priority=None, status=None, due_date=None):
        self.db_manager.update_todo_item(ToDoItem(id, title, priority, status, due_date))

    def delete_todo_item(self, id):
        self.db_manager.delete_todo_item(id)

    def list_todo_items(self):
        return self.db_manager.list_todo_items()
        
    def search_todo_items(self, keyword):
        all_todo_items = self.db_manager.list_todo_items()
        matching_todo_items = [item for item in all_todo_items if keyword.lower() in item.title.lower()]
        return matching_todo_items
    
