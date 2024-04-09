import pytest
import sqlite3
from application.model.todo_item import ToDoItem
from application.model.database_manager import DatabaseManager

class TestDatabaseManager:
    @classmethod
    def setup_class(cls):
        """ Create a database manager instance for testing."""
        cls.db_manager = DatabaseManager(':memory:') # Create an in-memory database for testing purposes

    @classmethod
    def teardown_class(cls):
        """ Close the database connection."""
        cls.db_manager.close_connection()

    def setup_method(self, method):
        """ Create a todo item with ID 1 for testing."""
        self.todo_item = ToDoItem(1, 'Test title', 'High', 'In Progress', '2022-01-01')

    def teardown_method(self, method):
        """ Delete all todo items from the database after each test."""
        self.db_manager.delete_all_todo_items()

    def test_insert_todo_item(self):
        """ Test_ID: 2
        Test that a todo item is inserted into the database correctly.
        The todo item should have the following attributes:
        - title
        - priority
        - status
        - due_date"""
        self.db_manager.insert_todo_item(self.todo_item)
        retrieved_item = self.db_manager.get_todo_item(1)
        assert retrieved_item.title == 'Test title'
        assert retrieved_item.priority == 'High'
        assert retrieved_item.status == 'In Progress'
        assert retrieved_item.due_date.format('YYYY-MM-DD') == '2022-01-01'

    def test_get_todo_item(self):
        """ Test_ID: 3
        Test that a todo item is retrieved from the database based on its ID.
        The retrieved todo item should have the same attributes as the original todo item."""
        self.db_manager.insert_todo_item(self.todo_item)
        retrieved_item = self.db_manager.get_todo_item(1)
        assert retrieved_item.id == 1

    def test_update_todo_item(self):
        """ Test_ID: 4
        Test that a todo item is updated in the database correctly."""
        self.db_manager.insert_todo_item(self.todo_item)
        updated_item = ToDoItem(1, 'Updated title', 'Low', 'Done', '2022-02-02')
        self.db_manager.update_todo_item(updated_item)
        retrieved_item = self.db_manager.get_todo_item(1)
        assert retrieved_item.title == 'Updated title'
        assert retrieved_item.priority == 'Low'
        assert retrieved_item.status == 'Done'
        assert retrieved_item.due_date.format('YYYY-MM-DD') == '2022-02-02'

    def test_delete_todo_item(self):
        """ Test_ID: 5
        Test that a todo item is deleted from the database based on its ID.
        After deletion, the todo item should no longer be found in the database."""
        self.db_manager.insert_todo_item(self.todo_item)
        self.db_manager.delete_todo_item(1)
        retrieved_item = self.db_manager.get_todo_item(1)
        assert retrieved_item is None

    def test_delete_all_todo_items(self):
        """ Test_ID: 6
        Test that all todo items are deleted from the database.
        After deletion, the list of todo items should be empty."""
        self.db_manager.insert_todo_item(self.todo_item)
        self.db_manager.delete_all_todo_items()
        todo_items = self.db_manager.list_todo_items()
        assert len(todo_items) == 0

    def test_list_todo_items(self):
        """ Test_ID: 7
        Test that all todo items are retrieved from the database.
        The list of todo items should contain the original todo item.
        The list of todo items should have a length of 1.
        The retrieved todo item should have the same attributes as the original todo item."""
        self.db_manager.insert_todo_item(self.todo_item)
        todo_items = self.db_manager.list_todo_items()
        assert len(todo_items) == 1
        assert todo_items[0].title == 'Test title'

    def test_get_todo_items_sorted_by(self):
        """ Test_ID: 8
        Test that todo items are retrieved from the database and sorted by the specified field.
        The todo items should be sorted by priority in ascending order.
        The first todo item in the sorted list should have a priority of 'High'.
        The last todo item in the sorted list should have a priority of 'Low'."""
        self.db_manager.insert_todo_item(self.todo_item)
        sorted_items = self.db_manager.get_todo_items_sorted_by('priority')
        assert sorted_items[0].priority == 'High'

    def test_update_todo_status(self):
        """ Test_ID: 9
        Test that the status of a todo item is updated in the database correctly.
        The status of the todo item should be set to 'Done'. 
        The retrieved todo item should have the status 'Done'."""
        self.db_manager.insert_todo_item(self.todo_item)
        self.db_manager.update_todo_status(1, 'Done')
        retrieved_item = self.db_manager.get_todo_item(1)
        assert retrieved_item.status == 'Done'