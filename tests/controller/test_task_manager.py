import unittest
from application.model.todo_item import ToDoItem
from application.model.database_manager import DatabaseManager
from application.controller.task_manager import TaskManager

class TestTaskManager(unittest.TestCase):
    def setUp(self):
        self.db_manager = DatabaseManager(':memory:')  # Use an in-memory SQLite database for testing
        self.task_manager = TaskManager(self.db_manager)

    def test_create_todo_item(self):
        todo_item = self.task_manager.create_todo_item('Test title', 'High', 'In Progress', '2022-01-01')
        self.assertEqual(todo_item.title, 'Test title')
        self.assertEqual(todo_item.priority, 'High')
        self.assertEqual(todo_item.status, 'In Progress')
        self.assertEqual(todo_item.due_date, '2022-01-01')

    def test_get_todo_item(self):
        todo_item = self.task_manager.create_todo_item('Test title', 'High', 'In Progress', '2022-01-01')
        retrieved_item = self.task_manager.get_todo_item(todo_item.id)
        self.assertEqual(retrieved_item.id, todo_item.id)

    def test_update_todo_item(self):
        todo_item = self.task_manager.create_todo_item('Test title', 'High', 'In Progress', '2022-01-01')
        self.task_manager.update_todo_item(todo_item.id, title='Updated title')
        updated_item = self.task_manager.get_todo_item(todo_item.id)
        self.assertEqual(updated_item.title, 'Updated title')

    def test_delete_todo_item(self):
        todo_item = self.task_manager.create_todo_item('Test title', 'High', 'In Progress', '2022-01-01')
        self.task_manager.delete_todo_item(todo_item.id)
        with self.assertRaises(ValueError):
            self.task_manager.get_todo_item(todo_item.id)

    def test_list_todo_items(self):
        todo_item1 = self.task_manager.create_todo_item('Test title 1', 'High', 'In Progress', '2022-01-01')
        todo_item2 = self.task_manager.create_todo_item('Test title 2', 'Low', 'Done', '2022-02-02')
        todo_items = self.task_manager.list_todo_items()
        self.assertEqual(len(todo_items), 2)

    def test_search_todo_items(self):
        todo_item1 = self.task_manager.create_todo_item('Test title 1', 'High', 'In Progress', '2022-01-01')
        todo_item2 = self.task_manager.create_todo_item('Test title 2', 'Low', 'Done', '2022-02-02')
        matching_items = self.task_manager.search_todo_items('1')
        self.assertEqual(len(matching_items), 1)
        self.assertEqual(matching_items[0].id, todo_item1.id)

    def tearDown(self):
        self.db_manager.close_connection()

if __name__ == '__main__':
    unittest.main()