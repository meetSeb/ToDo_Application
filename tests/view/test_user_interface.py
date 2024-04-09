import pytest
from unittest.mock import MagicMock, patch
from PySide6.QtWidgets import QApplication, QListWidgetItem, QWidget
from PySide6.QtCore import Qt, QEvent, QPointF
from PySide6.QtGui import QMouseEvent
from application.view.user_interface import UserInterface, CustomListWidget
from application.controller.task_manager import TaskManager

@pytest.fixture(scope="function", autouse=True)
def setup_teardown_application():
    # Setup: Create QApplication instance if it doesn't exist
    app = QApplication.instance()
    if app is None:
        app = QApplication([])

    yield

    # Teardown: Delete QApplication instance
    app.quit()
    del app

class TestUserInterface:
    def test_add_todo(self, mocker):
        # Arrange
        mock_create_todo_item = mocker.patch('application.controller.task_manager.TaskManager.create_todo_item')
        mock_model = mocker.MagicMock()
        mock_controller = mocker.MagicMock()
        user_interface = UserInterface(mock_model, mock_controller)
        user_interface.todo_input = mocker.MagicMock()
        user_interface.todo_input.text.return_value = "Test ToDo Item"

        # Act
        user_interface.add_todo()

        # Assert
        mock_create_todo_item.assert_called_once_with("Test ToDo Item")
        user_interface.todo_input.clear.assert_called_once()

    def test_create_labeled_widget(self):
        # Arrange
        widget = QWidget()
        user_interface = UserInterface(None, None)

        # Act
        result = user_interface.create_labeled_widget("Label", widget)

        # Assert
        assert result.layout().count() == 2
        assert result.layout().itemAt(0).widget().text() == "Label"
        assert result.layout().itemAt(1).widget() == widget



class TestCustomListWidget:
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

    def test_custom_list_widget_drag(self):
        # Arrange
        user_interface = UserInterface(None, None)
        custom_list_widget = CustomListWidget(user_interface)
        item = QListWidgetItem()
        item.setData(Qt.UserRole, 123)
        custom_list_widget.addItem(item)
        custom_list_widget.setCurrentItem(item)  # Select the item

        # Act
        custom_list_widget.startDrag(Qt.CopyAction)

        # Assert
        mime_data = custom_list_widget.mimeData([item])
        assert mime_data.text() == "123"

    def test_custom_list_widget_drop(self):
        # Arrange
        user_interface = UserInterface(None, None)
        custom_list_widget = CustomListWidget(user_interface, status="In Progress")
        item = QListWidgetItem()
        item.setData(Qt.UserRole, 123)
        custom_list_widget.addItem(item)

        # Mock the controller and the UserInterface's update_kanban_board method
        mock_controller = MagicMock()
        custom_list_widget.controller = mock_controller  # Set the controller of the CustomListWidget instance
        user_interface.update_kanban_board = MagicMock()

        # Act
        event = MagicMock()
        event.mimeData().text.return_value = "123"  # Return a string
        custom_list_widget.dropEvent(event)

        # Assert
        mock_controller.update_todo_status.assert_called_once_with(123, "In Progress")


    def test_custom_list_widget_right_click(self):
        # Arrange
        user_interface = UserInterface(None, None)
        custom_list_widget = CustomListWidget(user_interface)
        item = QListWidgetItem()
        custom_list_widget.addItem(item)

        # Mock the itemRightClicked signal
        signal_mock = MagicMock()
        custom_list_widget.itemRightClicked = signal_mock

        # Act
        event = QMouseEvent(QEvent.MouseButtonPress, QPointF(10, 10), Qt.RightButton, Qt.RightButton, Qt.NoModifier)
        custom_list_widget.mousePressEvent(event)

        # Assert
        signal_mock.emit.assert_called_once()
        
        