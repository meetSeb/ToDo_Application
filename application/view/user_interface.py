import arrow
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QListWidgetItem, QWidget, QLineEdit, QPushButton, QSizePolicy, QDialog, QMessageBox, QComboBox, QAbstractItemView
from PySide6.QtCore import Qt, QMimeData, Signal
from PySide6.QtGui import QDrag, QPixmap, QPainter, QCursor, QFontMetrics, QPen, QColor
from application.controller.task_manager import TaskManager

            
class UserInterface:
    """ The UserInterface class is responsible for creating the main window of the application and handling user interactions. 
        It uses the TaskManager class to interact with the model and controller."""
    def __init__(self, model, controller):
        """ Initialize the UserInterface with the provided model and controller."""
        self.model = model
        self.controller = TaskManager(self)
        self.app = QApplication([])
        self.window = QMainWindow()
        
        self.window.setWindowTitle("Simply Done - Your Simple Task Organizer") # Set the window title
        self.todo_list_widget = CustomListWidget(self, status='To Do') # Create a custom QListWidget for the To Do items
        self.in_progress_list_widget = CustomListWidget(self, status='In Progress') # Create a custom QListWidget for the In Progress items
        self.done_list_widget = CustomListWidget(self, status='Done') # Create a custom QListWidget for the Done items
        
        # Create a QLineEdit widget for the input field and a QPushButton for adding To-Do items
        self.todo_input = QLineEdit("") 
        self.todo_input.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed) 
        self.add_todo_button = QPushButton("Add To-Do") 

        # Create a horizontal layout for the input field and button
        self.input_layout = QHBoxLayout()
        self.input_layout.addStretch(1)
        self.input_layout.addWidget(self.todo_input)
        self.input_layout.addWidget(self.add_todo_button)
        self.input_layout.addStretch(1)
        
        # Create a horizontal layout for the To Do, In Progress, and Done columns
        self.todo_layout = QHBoxLayout()
        self.todo_layout.addWidget(self.create_labeled_widget('To Do', self.todo_list_widget))
        self.todo_layout.addWidget(self.create_labeled_widget('In Progress', self.in_progress_list_widget))
        self.todo_layout.addWidget(self.create_labeled_widget('Done', self.done_list_widget))

        # Add a button to sort the ToDos
        self.sort_button = QPushButton("...")
        self.input_layout.addWidget(self.sort_button)

        # Create the main layout and set it as the central widget of the window
        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(self.input_layout)
        self.main_layout.addLayout(self.todo_layout)

        # Create a central widget and set the main layout
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.main_layout)
        self.window.setCentralWidget(self.central_widget)
        
        # Connect the button to the add_todo method
        self.add_todo_button.clicked.connect(self.add_todo)
        # Connect the returnPressed signal of the QLineEdit widget to the add_todo method
        self.todo_input.returnPressed.connect(self.add_todo)
        
        # Connect the itemDoubleClicked signal of the QListWidgets to the open_todo_window method
        self.todo_list_widget.itemDoubleClicked.connect(self.open_todo_window)
        self.in_progress_list_widget.itemDoubleClicked.connect(self.open_todo_window)
        self.done_list_widget.itemDoubleClicked.connect(self.open_todo_window)
        
        # Connect the itemRightClicked signal of the QListWidgets to the open_delete_dialog method 
        self.todo_list_widget.itemRightClicked.connect(self.open_delete_dialog)
        self.in_progress_list_widget.itemRightClicked.connect(self.open_delete_dialog)
        self.done_list_widget.itemRightClicked.connect(self.open_delete_dialog)

        # Connect the clicked signal of the sort_button to the open_sort_dialog method
        self.sort_button.clicked.connect(self.open_sort_dialog)
    
        
    # Add a KanBan board column to the UI
    def create_labeled_widget(self, label_text, widget, input_field=None, button=None):
        """ Create a labeled widget with an optional input field and button. 
            Args: 
            label_text (str): The text to display as the label.
            widget (QWidget): The widget to display below the label.
            input_field (QWidget): An optional input field widget.
            button (QWidget): An optional button widget.
            Returns:
                QWidget: The container widget with the label, widget, input field, and button."""
        layout = QVBoxLayout()  
        label = QLabel(label_text) 
        label.setAlignment(Qt.AlignCenter) # center the label
        layout.addWidget(label) 
        layout.addWidget(widget) 
        if input_field and button:  # if input_field and button are provided, it adds them to the layout
            layout.addWidget(input_field)
            layout.addWidget(button)
        container = QWidget() 
        container.setLayout(layout)
        return container
    
    def add_todo(self):
        """ Add a new ToDo item to the database and update the Kanban board."""
        todo_text = self.todo_input.text()
        if todo_text:  # make sure the input field is not empty
            try:
                self.controller.create_todo_item(todo_text)
                self.update_kanban_board()
                self.todo_input.clear()  # clear the input field
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to add ToDo item: {str(e)}")
    
                
    def update_kanban_board(self, todos=None):
        """ Update the Kanban board with the provided list of ToDos or fetch the current list from the database if not provided."""
        
        # Fetch the current list of ToDos from the database through the controller if not provided
        if todos is None:
            todos = self.controller.list_todo_items()

        # Clear the current items in the QListWidgets
        self.todo_list_widget.clear()
        self.in_progress_list_widget.clear()
        self.done_list_widget.clear()

        # Iterate over the list of ToDos
        for todo in todos:
            item = QListWidgetItem(todo.title)  # create a QListWidgetItem with the title of the ToDo
            item.setData(Qt.UserRole, todo.id)  # store the id of the ToDoItem in the QListWidgetItem

            # Check the status of the ToDo and add it to the corresponding QListWidget
            if todo.status == 'To Do' or todo.status is None:
                self.todo_list_widget.addItem(item)
            elif todo.status == 'In Progress':
                self.in_progress_list_widget.addItem(item)
            elif todo.status == 'Done':
                self.done_list_widget.addItem(item)



    def open_todo_window(self, item):
        """ Open a dialog window to display and edit the details of a ToDoItem 
            Args:
            item (QListWidgetItem): The item that was double-clicked in the QListWidget"""
        
        # Get the id of the ToDoItem from the QListWidgetItem
        id = item.data(Qt.UserRole)

        # Get the ToDoItem object from the database
        todo = self.controller.get_todo_item(id)
        
        # Create a QDialog
        dialog = QDialog()
        layout = QVBoxLayout()
        dialog.setLayout(layout)

        # Create QLabel and QLineEdit for the title, and set the current title
        title_label = QLabel("Title")
        title_input = QLineEdit(todo.title)
        layout.addWidget(title_label)
        layout.addWidget(title_input)

        # Create QLabel and QComboBox for the priority, and set the current priority
        priority_label = QLabel("Priority")
        priority_input = QComboBox()
        priority_input.addItem("")  # For NULL option
        priority_input.addItem("Low")
        priority_input.addItem("Medium")
        priority_input.addItem("High")

        # Set the current priority
        current_priority_index = priority_input.findText(todo.priority)
        if current_priority_index >= 0:  # -1 means the text was not found
            priority_input.setCurrentIndex(current_priority_index)

        layout.addWidget(priority_label)
        layout.addWidget(priority_input)

        # Create QLabel and QComboBox for the status, and set the current status
        status_label = QLabel("Status")
        status_input = QComboBox()
        status_input.addItem("")  # For NULL option
        status_input.addItem("To Do")
        status_input.addItem("In Progress")
        status_input.addItem("Done")

        # Set the current status
        current_status_index = status_input.findText(todo.status)
        if current_status_index >= 0:  # -1 means the text was not found
            status_input.setCurrentIndex(current_status_index)

        layout.addWidget(status_label)
        layout.addWidget(status_input)

        # Create QLabel and QLineEdit for the due_date, and set the current due_date
        due_date_label = QLabel("Due Date")
        due_date_input = QLineEdit(arrow.get(todo.due_date).format('YYYY/MM/DD') if todo.due_date else "")
        layout.addWidget(due_date_label)
        layout.addWidget(due_date_input)

        # Create a QPushButton for the submit action
        submit_button = QPushButton("Submit")
        layout.addWidget(submit_button)

        # Connect the clicked signal of the QPushButton to a method that updates the ToDo
        submit_button.clicked.connect(lambda: self.handle_submit_and_close_dialog(todo.id, title_input.text(), priority_input.currentText(), status_input.currentText(), due_date_input.text(), dialog))

        # Show the QDialog
        dialog.exec()

    def handle_submit_and_close_dialog(self, todo_id, title, priority, status, due_date_str, dialog):
        """ Handle the submit action from the dialog window and close the dialog.
            Args:
            todo_id (int): The ID of the ToDoItem
            title (str): The new title of the ToDoItem
            priority (str): The new priority of the ToDoItem
            status (str): The new status of the ToDoItem
            due_date_str (str): The new due date of the ToDoItem in string format
            dialog (QDialog): The dialog window to close"""

        # Handle the submit action and show an error message if needed
        result = self.controller.handle_submit(todo_id, title, priority, status, due_date_str)
        if result is not True:
            QMessageBox.critical(None, "Error", result)
        else:
            self.update_kanban_board()
            dialog.accept()
            
            
    
    def open_delete_dialog(self, item):
        """ Open a dialog window to confirm the deletion of a ToDoItem
            Args:
            item (QListWidgetItem): The item that was right-clicked in the QListWidget"""
        
        # Create a QDialog
        dialog = QDialog()
        layout = QVBoxLayout()
        dialog.setLayout(layout)

        # Create a QLabel with the question and a QPushButton for confirmation
        question_label = QLabel("Want to delete the ToDo?")
        confirm_button = QPushButton("Confirm")

        layout.addWidget(question_label)
        layout.addWidget(confirm_button)

        # Connect the clicked signal of the QPushButton to a method that deletes the ToDo and closes the dialog
        confirm_button.clicked.connect(lambda: self.handle_delete_and_close_dialog(dialog, item))

        # Show the QDialog
        dialog.exec_()

    def handle_delete_and_close_dialog(self, dialog, item):
        """ Handle the deletion of a ToDoItem and close the dialog
            Args:
            dialog (QDialog): The dialog window to close
            item (QListWidgetItem): The item to delete from the QListWidget"""
        
        # Get the ID of the ToDo from the item and delete it from the database through the controller
        todo_id = item.data(Qt.UserRole)
        self.controller.delete_todo_item(todo_id)
        self.update_kanban_board()
        dialog.accept()

    def display_main_window(self):
        """ Display the main window of the application."""
        self.window.show()

    def open_sort_dialog(self):
        """ Open a dialog window to select the sorting option for the ToDo items."""
        
        # Create a QDialog
        dialog = QDialog()
        layout = QVBoxLayout()
        dialog.setLayout(layout)

        # Create a QLabel and QComboBox for the sorting options
        sort_label = QLabel("Sort by")
        layout.addWidget(sort_label)

        # Add the sorting options to the QComboBox
        sort_combo_box = QComboBox()
        sort_combo_box.addItem("Due Date")
        sort_combo_box.addItem("Priority")
        layout.addWidget(sort_combo_box)

        # Create a QPushButton for the sort action
        sort_button = QPushButton("Sort")
        layout.addWidget(sort_button)

        # Connect the clicked signal of the QPushButton to a method that sorts the ToDo items and closes the dialog
        sort_button.clicked.connect(lambda: (self.sort_todo_items(sort_combo_box.currentText()), dialog.accept()))

        # Show the QDialog
        dialog.exec_()

    def sort_todo_items(self, sort_option):
        """ Sort the ToDo items based on the selected sorting option and update the Kanban board.
            Args:
            sort_option (str): The selected sorting option"""
            
        # Sort the ToDo items based on the selected sorting option
        sorted_items = []
        if sort_option == "Due Date":
            sorted_items = self.controller.sort_todo_items_by_due_date()
        elif sort_option == "Priority":
            sorted_items = self.controller.sort_todo_items_by_priority()

        self.update_kanban_board(sorted_items)


class CustomListWidget(QListWidget):
    """ A custom QListWidget that emits a signal when an item is right-clicked."""
    
    # Define a custom signal for the right-clicked event
    itemRightClicked = Signal(QListWidgetItem)

    def __init__(self, UserInterface, status=None, *args, **kwargs):
        """ Initialize the custom QListWidget with the provided UserInterface and status.
            Args:
            UserInterface (UserInterface): The UserInterface instance
            status (str): The status of the ToDo items in the list
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments"""
            
        # Call the parent class constructor
        super().__init__(*args, **kwargs)
        self.status = status
        self.UserInterface = UserInterface
        self.controller = TaskManager(self)
        self.setDragDropMode(QAbstractItemView.InternalMove)
    
    def startDrag(self, actions):
        """ Start the drag operation with the item's ID and a custom pixmap.
            Args:
            actions: The drag actions to perform"""
            
        # Create a drag object
        drag = QDrag(self)
        
        # Create a QMimeData object and set the text to the ID of the item
        mimeData = QMimeData()
        mimeData.setText(str(self.currentItem().data(Qt.UserRole)))  # Store the id of the item
        
        # Set the mime data for the drag object
        drag.setMimeData(mimeData)

        # Calculate the size of the text
        fontMetrics = QFontMetrics(self.currentItem().font())
        textSize = fontMetrics.size(0, self.currentItem().text())

        # Create a pixmap with the size of the text
        pixmap = QPixmap(textSize.width(), textSize.height())
        pixmap.fill(Qt.transparent)  # Fill the pixmap with a transparent color

        painter = QPainter(pixmap) # Create a QPainter object

        # Set the color of the text to green
        textColor = QColor('green')

        # Draw the icon and text on the pixmap
        painter.setPen(QPen(textColor))  # Set the color of the text
        painter.drawPixmap(pixmap.rect(), self.currentItem().icon().pixmap(textSize)) # Draw the icon
        painter.drawText(pixmap.rect(), Qt.AlignCenter, self.currentItem().text()) # Draw the text
        painter.end()

        # Set the pixmap and hotspot for the drag object
        drag.setPixmap(pixmap)
        drag.setHotSpot(self.mapFromGlobal(QCursor.pos()) - self.visualItemRect(self.currentItem()).topLeft())

        # Execute the drag operation
        drag.exec_(actions)

    def mimeData(self, items):
        """ Return the mime data for the drag operation.
            Args:
            items: The items to drag"""
            
        # Create a QMimeData object and set the text to the ID of the item
        mimeData = QMimeData()
        id = self.currentItem().data(Qt.UserRole)
        mimeData.setText(str(id))
        return mimeData

    def dragEnterEvent(self, event):
        """ Accept the drag event if it has text data.
            Args:
            event: The drag event"""
            
        # Accept the drag event if it has text data
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        """ Accept the drag move event if it has text data.
            Args:
            event: The drag move event"""
        
        # Accept the drag move event if it has text data
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        """ Handle the drop event by updating the status of the ToDo item.
            Args:
            event: The drop event"""
        
        # Get the ID of the ToDo item from the mime data
        id = int(event.mimeData().text())
        if self.status is not None:  # Only update the status if it's not None
            self.controller.update_todo_status(id, self.status)
            self.UserInterface.update_kanban_board()  # Refresh the Kanban board
        event.acceptProposedAction()

    def mousePressEvent(self, event):
        """ Handle the mouse press event and emit the itemRightClicked signal if the right mouse button is clicked.
            Args:
            event: The mouse press event"""
        
        # Call the parent class mousePressEvent method
        super().mousePressEvent(event)
        if event.button() == Qt.RightButton: # Check if the right mouse button is clicked
            item = self.itemAt(event.pos()) # Get the item at the mouse position
            if item is not None:
                self.itemRightClicked.emit(item) # Emit the itemRightClicked signal with the item

