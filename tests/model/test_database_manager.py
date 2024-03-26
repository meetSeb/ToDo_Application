import unittest
from unittest.mock import Mock
from application.model.database_manager import DatabaseManager

class TestDatabaseManager(unittest.TestCase):
    def setUp(self):
        self.db_manager = DatabaseManager(':memory:')
        self.db_manager.connect()
        self.db_manager.create_table()

    def tearDown(self):
        self.db_manager.close_connection()

    def test_insert_todo_item(self):
        # Create a mock ToDoItem
        todo_item = Mock()
        todo_item.id = 1
        todo_item.title = 'Buy milk'
        todo_item.priority = 'High'
        todo_item.status = 'To Do'
        todo_item.due_date = '2022-01-01'

        # Insert the ToDoItem into the database
        self.db_manager.insert_todo_item(todo_item)

        # Retrieve the inserted ToDoItem from the database
        retrieved_todo_item = self.db_manager.get_todo_item(1)

        # Check that the retrieved ToDoItem matches the inserted ToDoItem
        self.assertEqual(retrieved_todo_item.id, todo_item.id)
        self.assertEqual(retrieved_todo_item.title, todo_item.title)
        self.assertEqual(retrieved_todo_item.priority, todo_item.priority)
        self.assertEqual(retrieved_todo_item.status, todo_item.status)
        self.assertEqual(retrieved_todo_item.due_date.format('YYYY-MM-DD'), todo_item.due_date)

    def test_update_todo_item(self):
        # Create a mock ToDoItem
        todo_item = Mock()
        todo_item.id = 1
        todo_item.title = 'Buy milk'
        todo_item.priority = 'High'
        todo_item.status = 'To Do'
        todo_item.due_date = '2022-01-01'

        # Insert the ToDoItem into the database
        self.db_manager.insert_todo_item(todo_item)

        # Update the ToDoItem's title
        todo_item.title = 'Buy eggs'

        # Update the ToDoItem in the database
        self.db_manager.update_todo_item(todo_item)

        # Retrieve the updated ToDoItem from the database
        retrieved_todo_item = self.db_manager.get_todo_item(1)

        # Check that the retrieved ToDoItem's title was updated
        self.assertEqual(retrieved_todo_item.title, 'Buy eggs')

    def test_delete_todo_item(self):
        # Create a mock ToDoItem
        todo_item = Mock()
        todo_item.id = 1
        todo_item.title = 'Buy milk'
        todo_item.priority = 'High'
        todo_item.status = 'To Do'
        todo_item.due_date = '2022-01-01'

        # Insert the ToDoItem into the database
        self.db_manager.insert_todo_item(todo_item)

        # Delete the ToDoItem from the database
        self.db_manager.delete_todo_item(1)

        # Retrieve the deleted ToDoItem from the database
        retrieved_todo_item = self.db_manager.get_todo_item(1)

        # Check that the retrieved ToDoItem is None (indicating deletion)
        self.assertIsNone(retrieved_todo_item)

    def test_list_todo_items(self):
        # Create some mock ToDoItems
        todo_item1 = Mock()
        todo_item1.id = 1
        todo_item1.title = 'Buy milk'
        todo_item1.priority = 'High'
        todo_item1.status = 'To Do'
        todo_item1.due_date = '2022-01-01'

        todo_item2 = Mock()
        todo_item2.id = 2
        todo_item2.title = 'Walk the dog'
        todo_item2.priority = 'Low'
        todo_item2.status = 'In Progress'
        todo_item2.due_date = '2022-01-02'

        # Insert the ToDoItems into the database
        self.db_manager.insert_todo_item(todo_item1)
        self.db_manager.insert_todo_item(todo_item2)

        # Retrieve all ToDoItems from the database
        todo_items = self.db_manager.list_todo_items()

        # Check that the retrieved ToDoItems match the inserted ToDoItems
        self.assertEqual(len(todo_items), 2)
        self.assertEqual(todo_items[0].id, todo_item1.id)
        self.assertEqual(todo_items[0].title, todo_item1.title)
        self.assertEqual(todo_items[0].priority, todo_item1.priority)
        self.assertEqual(todo_items[0].status, todo_item1.status)
        self.assertEqual(todo_items[0].due_date.format('YYYY-MM-DD'), todo_item1.due_date)
        self.assertEqual(todo_items[1].id, todo_item2.id)
        self.assertEqual(todo_items[1].title, todo_item2.title)
        self.assertEqual(todo_items[1].priority, todo_item2.priority)
        self.assertEqual(todo_items[1].status, todo_item2.status)
        self.assertEqual(todo_items[1].due_date.format('YYYY-MM-DD'), todo_item2.due_date)

if __name__ == '__main__':
    unittest.main()