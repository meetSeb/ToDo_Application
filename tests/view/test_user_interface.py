import pytest
from unittest.mock import MagicMock, patch
from PySide6.QtWidgets import QApplication, QListWidgetItem, QWidget
from PySide6.QtCore import Qt, QEvent, QPointF
from PySide6.QtGui import QMouseEvent
from application.view.user_interface import UserInterface, CustomListWidget
from application.controller.task_manager import TaskManager

@pytest.fixture(scope="function", autouse=True) # This fixture will run before and after each test function
def setup_teardown_application():
    """Setup: Create QApplication instance if it doesn't exist"""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])

    yield

    # Teardown: Delete QApplication instance
    app.quit()
    del app

class TestUserInterface:
    def test_add_todo(self, mocker):
        """ Test that the add_todo method calls the create_todo_item method of the TaskManager class.
        The method should also clear the todo_input field."""
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
        """ Test that the create_labeled_widget method creates a widget with a QLabel and another widget as children.
        The QLabel should have the text 'Label' and the other widget should be the widget passed as an argument.
        The method should return the created widget."""
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
    def test_custom_list_widget_drag(self):
        """ Test that the startDrag method of the CustomListWidget class sets the correct MIME data.
        The MIME data should contain the ID of the ToDoItem associated with the selected item.
        The method should return the MIME data."""
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
        """ Test that the dropEvent method of the CustomListWidget class calls the update_todo_status method of the controller with the correct arguments.
        The method should call the UserInterface's update_kanban_board method.
        The method should update the status of the ToDoItem associated with the dropped item.
        The method should return None."""
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
        """ Test that the mousePressEvent method of the CustomListWidget class emits the itemRightClicked signal when the right mouse button is pressed.
        The method should emit the signal once."""
        
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
        
        