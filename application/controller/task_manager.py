import arrow
from application.model.todo_item import ToDoItem
from application.model.database_manager import DatabaseManager

class TaskManager:
    def __init__(self, db_manager):
        self.db_manager = DatabaseManager(db_manager)   # Cross-check Functionality!!

    def create_todo_item(self, title, priority, status, due_date):
        """ Validate the input data
        Create a ToDoItem instance
        Use the DatabaseManager to store the instance in the database """
        # Create a ToDoItem instance
        todo_item = ToDoItem(None, title, priority, status, due_date)

        # Validate the ToDoItem data
        self.validate_todo_data(todo_item)

        # Use the DatabaseManager to store the instance in the database
        self.db_manager.insert_todo_item(todo_item)

    def get_todo_item(self, id):
        """Use the DatabaseManager to retrieve the ToDoItem with the given id from the database
        Return the ToDoItem instance """
        # Use the DatabaseManager to retrieve the ToDoItem with the given id from the database
        todo_item = self.db_manager.get_todo_item(id)

        # Check if the ToDoItem was found
        if todo_item is None:
            raise ValueError(f"No ToDoItem found with id {id}")

        # Return the ToDoItem instance
        return todo_item

    def update_todo_item(self, id, title=None, priority=None, status=None, due_date=None):
        """ Validate the input data
        Use the DatabaseManager to retrieve the ToDoItem with the given id from the database
        Update the ToDoItem instance
        Use the DatabaseManager to store the updated instance in the database """
        todo_item = self.db_manager.get_todo_item(id)

        # Check if the ToDoItem was found
        if todo_item is None:
            raise ValueError(f"No ToDoItem found with id {id}")

        # Update the ToDoItem's attributes with the provided values, if they were provided
        if title is not None:
            todo_item.title = title
        if priority is not None:
            todo_item.priority = priority
        if status is not None:
            todo_item.status = status
        if due_date is not None:
            todo_item.due_date = due_date

        # Use the DatabaseManager to update the ToDoItem in the database
        self.db_manager.update_todo_item(todo_item)

    def delete_todo_item(self, id):
        """ Use the DatabaseManager to delete the ToDoItem with the given id from the database """
        # Use the DatabaseManager to delete the ToDoItem with the given id from the database
        deleted = self.db_manager.delete_todo_item(id)

        # Check if the ToDoItem was deleted
        if not deleted:
            raise ValueError(f"No ToDoItem found with id {id}")

    def list_todo_items(self):
        """ Use the DatabaseManager to retrieve all ToDoItem instances from the database
        Return the list of ToDoItem instances """
        # Use the DatabaseManager to retrieve all ToDoItems from the database
        todo_items = self.db_manager.list_todo_items()

        # Return the list of ToDoItem instances
        return todo_items
    
    def mark_todo_item(self, id, status):
        # Check if the status is one of the allowed values
        if status not in ['To Do', 'In Progress', 'Done']:
            raise ValueError("Status must be 'To Do', 'In Progress', or 'Done'")

        # Use the DatabaseManager to retrieve the ToDoItem with the given id from the database
        todo_item = self.db_manager.get_todo_item(id)

        # Check if the ToDoItem was found
        if todo_item is None:
            raise ValueError(f"No ToDoItem found with id {id}")

        # Update the ToDoItem's status
        todo_item.status = status

        # Use the DatabaseManager to update the ToDoItem in the database
        self.db_manager.update_todo_item(todo_item)
        
    def search_todo_items(self, keyword):
        # Use the DatabaseManager to retrieve all ToDoItems from the database
        all_todo_items = self.db_manager.list_todo_items()

        # Filter the ToDoItems based on the keyword
        matching_todo_items = [item for item in all_todo_items if keyword.lower() in item.title.lower()]

        # Return the list of matching ToDoItem instances
        return matching_todo_items

    def validate_todo_data(self, todo_item):
        if not todo_item.title:
            raise ValueError("Title cannot be empty")
        if todo_item.priority not in ['Low', 'Medium', 'High']:
            raise ValueError("Priority must be 'Low', 'Medium', or 'High'")
        if todo_item.status not in ['To do', 'In progress', 'Done']:
            raise ValueError("Status must be 'To do', 'In progress', or 'Done'")
        if todo_item.due_date < arrow.now():
            raise ValueError("Due date cannot be in the past")