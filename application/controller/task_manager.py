import arrow
from application.model.todo_item import ToDoItem
from application.model.database_manager import DatabaseManager, DatabaseError



class TaskManager:
    """ This class is responsible for managing the ToDoItems in the application. It interacts with the DatabaseManager to perform CRUD operations on the ToDoItems."""
    
    def __init__(self, db_manager):
        """ The constructor initializes the DatabaseManager object.
        Args:
            db_manager (DatabaseManager): An instance of the DatabaseManager class. """
            
        self.db_manager = DatabaseManager('/Users/sebastianahlburg/Documents/Studium/Studium Informatik/IU/Module/Projekt Software Engineering/ToDo_Application/todo_list.db') 
        
    def create_todo_item(self, title, priority=None, status=None, due_date=None):
        """ This method creates a new ToDoItem and inserts it into the database. It returns the created ToDoItem object.
            Args:
                title (str): The title of the ToDoItem.
                priority (str): The priority of the ToDoItem.
                status (str): The status of the ToDoItem.
                due_date (str): The due date of the ToDoItem in the format YYYY-MM-DD.
                Returns:
                    ToDoItem: The created ToDoItem object.
                    Raises:
                        ValueError: If the title is empty.
                        DatabaseError: If an error occurs while creating the ToDoItem."""
        if not title:
            raise ValueError("Title cannot be empty")
        todo_item = ToDoItem(None, title, priority, status, due_date)
        try:
            self.db_manager.insert_todo_item(todo_item)
            todo_item.id = self.db_manager.get_last_inserted_id()  # Retrieve the ID from the database and set it on the object 
        except Exception as e:
            raise DatabaseError("An error occurred while creating the ToDo item.", original_exception=e, operation="INSERT") from e
        return todo_item

    def get_todo_item(self, id):
        """ This method retrieves a ToDoItem from the database based on its ID. It returns the ToDoItem object if found, otherwise raises a ValueError.
        Args:
            id (int): The ID of the ToDoItem to retrieve.
            Returns:
                ToDoItem: The ToDoItem object with the specified ID.
            Raises:
                ValueError: If no ToDoItem is found with the specified ID.
                DatabaseError: If an error occurs while retrieving the ToDoItem."""
        try:
            # Check if the ID is valid
            todo_item = self.db_manager.get_todo_item(id)
            if todo_item is None:
                raise ValueError(f"No ToDoItem found with id {id}")
            return todo_item
        except Exception as e:
            raise DatabaseError("An error occurred while retrieving the ToDo item.", original_exception=e, operation="SELECT") from e

    def update_todo_item(self, id, title, priority, status, due_date):
        """ This method updates a ToDoItem in the database."""
        try:
            self.db_manager.update_todo_item(ToDoItem(id, title, priority, status, due_date))
        except Exception as e:
            raise DatabaseError("An error occurred while updating the ToDo item.", original_exception=e, operation="UPDATE") from e

    def delete_todo_item(self, id):
        """ This method deletes a ToDoItem from the database based on its ID."""
        try:
            self.db_manager.delete_todo_item(id)
        except Exception as e:
            raise DatabaseError("An error occurred while deleting the ToDo item.", original_exception=e, operation="DELETE") from e # Raise a DatabaseError with additional information about the operation that failed 

    def list_todo_items(self):
        """ This method retrieves all ToDoItems from the database and returns a list of ToDoItem objects."""
        return self.db_manager.list_todo_items()
    
    def sort_todo_items_by_due_date(self):
        """ This method retrieves all ToDoItems from the database and returns a list of ToDoItem objects sorted by due date."""
        return self.db_manager.get_todo_items_sorted_by('due_date')

    def sort_todo_items_by_priority(self):
        """ This method retrieves all ToDoItems from the database and returns a list of ToDoItem objects sorted by priority."""
        return self.db_manager.get_todo_items_sorted_by('priority')
    
    
    def handle_submit(self, todo_id, title, priority, status, due_date_str):
        """ This method handles the submission of the update form and updates the ToDoItem in the database. It returns True if the update was successful, otherwise an error message. 
        Args: 
            todo_id (int): The ID of the ToDoItem to update.
            title (str): The updated title of the ToDoItem.
            priority (str): The updated priority of the ToDoItem.
            status (str): The updated status of the ToDoItem.
            due_date_str (str): The updated due date of the ToDoItem in the format YYYY/MM/DD.
            Returns:
                bool or str: True if the update was successful, otherwise an error message."""
        
        # If the date string is not empty, try to parse it
        if due_date_str:
            try:
                # Try to parse the date string
                due_date = arrow.get(due_date_str, 'YYYY/MM/DD').format('YYYY-MM-DD')
            except arrow.parser.ParserError:
                # If a ParserError is raised, return an error message
                return "Use YYYY/MM/DD format"
            except ValueError:
                # If a ValueError is raised, return a different error message
                return "Invalid date. Please check the month and day values."
        else:
            due_date = None  # If the date string is empty, set due_date to None

        # If the user input is empty, replace it with None
        title = title if title.strip() else None
        priority = priority if priority.strip() else None
        status = status if status.strip() else None

        # If no error was raised, continue with updating the ToDo
        self.update_todo_item(todo_id, title, priority, status, due_date)

        # Return True to indicate that the update was successful
        return True
    
    def update_todo_status(self, id, status):
        """ This method updates the status of a ToDoItem in the database based on its ID.
        Args:
            id (int): The ID of the ToDoItem to update.
            status (str): The new status of the ToDoItem."""
        self.db_manager.update_todo_status(id, status)
        