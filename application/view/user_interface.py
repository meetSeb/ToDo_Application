import arrow
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QListWidgetItem, QWidget, QLineEdit, QPushButton, QSizePolicy, QDialog, QMessageBox, QComboBox
from PySide6.QtCore import Qt, Signal
from application.controller.task_manager import TaskManager

            
class UserInterface:
    def __init__(self, model, controller):
        self.model = model
        self.controller = TaskManager(controller)
        self.app = QApplication([])
        self.window = QMainWindow()
        
        self.window.setWindowTitle("Simply Done - Your Simple Task Organizer")
        self.todo_list_widget = CustomListWidget()
        self.in_progress_list_widget = CustomListWidget()
        self.done_list_widget = CustomListWidget()
        
        self.todo_input = QLineEdit("")
        self.todo_input.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.add_todo_button = QPushButton("Add To-Do")

        self.input_layout = QHBoxLayout()
        self.input_layout.addStretch(1)
        self.input_layout.addWidget(self.todo_input)
        self.input_layout.addWidget(self.add_todo_button)
        self.input_layout.addStretch(1)
        
        self.todo_layout = QHBoxLayout()
        self.todo_layout.addWidget(self.create_labeled_widget('To Do', self.todo_list_widget))
        self.todo_layout.addWidget(self.create_labeled_widget('In Progress', self.in_progress_list_widget))
        self.todo_layout.addWidget(self.create_labeled_widget('Done', self.done_list_widget))

        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(self.input_layout)
        self.main_layout.addLayout(self.todo_layout)

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
    
        
    # Add a KanBan board column to the UI
    def create_labeled_widget(self, label_text, widget, input_field=None, button=None):
        layout = QVBoxLayout()  # create a vertical layout
        label = QLabel(label_text) # create a label with the given text provided by the label
        label.setAlignment(Qt.AlignCenter) # center the label
        layout.addWidget(label) # add the label to the layout
        layout.addWidget(widget) # add the widget to the layout
        if input_field and button:  # if input_field and button are provided, it adds them to the layout
            layout.addWidget(input_field)
            layout.addWidget(button)
        container = QWidget() # create a container widget
        container.setLayout(layout) # set the layout of the container to the layout we created
        return container
    
    # Add the add_todo method
    def add_todo(self):
        todo_text = self.todo_input.text()
        if todo_text:  # make sure the input field is not empty
            self.controller.create_todo_item(todo_text)
            self.update_kanban_board()
            self.todo_input.clear()  # clear the input field
    
    def update_kanban_board(self):
        # Fetch the current list of ToDos from the database through the controller
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
        result = self.controller.handle_submit(todo_id, title, priority, status, due_date_str)
        if result is not True:
            QMessageBox.critical(None, "Error", result)
        else:
            self.update_kanban_board()  # Update the kanban board
            dialog.accept()
            
            
    
    def open_delete_dialog(self, item):
        dialog = QDialog()
        layout = QVBoxLayout()
        dialog.setLayout(layout)

        question_label = QLabel("Want to delete the ToDo?")
        confirm_button = QPushButton("Confirm")

        layout.addWidget(question_label)
        layout.addWidget(confirm_button)

        confirm_button.clicked.connect(lambda: self.handle_delete_and_close_dialog(dialog, item))

        dialog.exec_()

    def handle_delete_and_close_dialog(self, dialog, item):
        todo_id = item.data(Qt.UserRole)  # Get the ID of the ToDo from the item
        self.controller.delete_todo_item(todo_id)
        self.update_kanban_board()
        dialog.accept()

    def display_main_window(self):
        self.window.show()



class CustomListWidget(QListWidget):
    itemRightClicked = Signal(QListWidgetItem)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.button() == Qt.RightButton:
            item = self.itemAt(event.pos())
            if item is not None:
                self.itemRightClicked.emit(item)