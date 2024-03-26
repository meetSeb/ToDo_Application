import unittest
from application.model.todo_item import ToDoItem

class TestToDoItem(unittest.TestCase):
    def test_todo_item_initialization(self):
        # Create a ToDoItem instance
        todo_item = ToDoItem(1, 'Buy milk', 'High', 'To Do', '2022-01-01')

        # Check that the attributes are set correctly
        self.assertEqual(todo_item.id, 1)
        self.assertEqual(todo_item.title, 'Buy milk')
        self.assertEqual(todo_item.priority, 'High')
        self.assertEqual(todo_item.status, 'To Do')
        self.assertEqual(todo_item.due_date, '2022-01-01')

if __name__ == '__main__':
    unittest.main()