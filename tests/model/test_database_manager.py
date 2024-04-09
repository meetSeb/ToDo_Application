import pytest
import sqlite3
from application.model.todo_item import ToDoItem
from application.model.database_manager import DatabaseManager

class TestDatabaseManager:
    @classmethod
    def setup_class(cls):
        cls.db_manager = DatabaseManager(':memory:')

    @classmethod
    def teardown_class(cls):
        cls.db_manager.close_connection()

    def setup_method(self, method):
        self.todo_item = ToDoItem(1, 'Test title', 'High', 'In Progress', '2022-01-01')

    def teardown_method(self, method):
        self.db_manager.delete_all_todo_items()

    def test_insert_todo_item(self):
        self.db_manager.insert_todo_item(self.todo_item)
        retrieved_item = self.db_manager.get_todo_item(1)
        assert retrieved_item.title == 'Test title'
        assert retrieved_item.priority == 'High'
        assert retrieved_item.status == 'In Progress'
        assert retrieved_item.due_date.format('YYYY-MM-DD') == '2022-01-01'

    def test_get_todo_item(self):
        self.db_manager.insert_todo_item(self.todo_item)
        retrieved_item = self.db_manager.get_todo_item(1)
        assert retrieved_item.id == 1

    def test_update_todo_item(self):
        self.db_manager.insert_todo_item(self.todo_item)
        updated_item = ToDoItem(1, 'Updated title', 'Low', 'Done', '2022-02-02')
        self.db_manager.update_todo_item(updated_item)
        retrieved_item = self.db_manager.get_todo_item(1)
        assert retrieved_item.title == 'Updated title'
        assert retrieved_item.priority == 'Low'
        assert retrieved_item.status == 'Done'
        assert retrieved_item.due_date.format('YYYY-MM-DD') == '2022-02-02'

    def test_delete_todo_item(self):
        self.db_manager.insert_todo_item(self.todo_item)
        self.db_manager.delete_todo_item(1)
        retrieved_item = self.db_manager.get_todo_item(1)
        assert retrieved_item is None

    def test_delete_all_todo_items(self):
        self.db_manager.insert_todo_item(self.todo_item)
        self.db_manager.delete_all_todo_items()
        todo_items = self.db_manager.list_todo_items()
        assert len(todo_items) == 0

    def test_list_todo_items(self):
        self.db_manager.insert_todo_item(self.todo_item)
        todo_items = self.db_manager.list_todo_items()
        assert len(todo_items) == 1
        assert todo_items[0].title == 'Test title'

    def test_get_todo_items_sorted_by(self):
        self.db_manager.insert_todo_item(self.todo_item)
        sorted_items = self.db_manager.get_todo_items_sorted_by('priority')
        assert sorted_items[0].priority == 'High'

    def test_update_todo_status(self):
        self.db_manager.insert_todo_item(self.todo_item)
        self.db_manager.update_todo_status(1, 'Done')
        retrieved_item = self.db_manager.get_todo_item(1)
        assert retrieved_item.status == 'Done'