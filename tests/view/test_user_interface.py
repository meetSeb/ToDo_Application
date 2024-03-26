import unittest
from unittest.mock import MagicMock, patch
from application.view.user_interface import UserInterface
from application.controller.task_manager import TaskManager

class TestUserInterface(unittest.TestCase):
    @patch.object(TaskManager, 'create_todo_item')
    def test_add_todo(self, mock_create_todo_item):
        # Arrange
        mock_model = MagicMock()
        mock_controller = MagicMock()
        user_interface = UserInterface(mock_model, mock_controller)
        user_interface.todo_input = MagicMock()
        user_interface.todo_input.text.return_value = "Test ToDo Item"

        # Act
        user_interface.add_todo()

        # Assert
        mock_create_todo_item.assert_called_once_with("Test ToDo Item")
        user_interface.todo_input.clear.assert_called_once()

if __name__ == '__main__':
    unittest.main()