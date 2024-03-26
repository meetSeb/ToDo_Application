from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QListWidgetItem, QWidget, QLineEdit, QPushButton, QSizePolicy, QDateEdit, QDialog
from PySide6.QtCore import Qt
from application.controller.task_manager import TaskManager

class UserInterface:
    def __init__(self, model, controller):
        self.model = model
        self.controller = TaskManager(controller)
        self.app = QApplication([])
        self.window = QMainWindow()

        self.todo_list_widget = QListWidget()
        self.in_progress_list_widget = QListWidget()
        self.done_list_widget = QListWidget()
        
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

            # Check the status of the ToDo and add it to the corresponding QListWidget
            if todo.status == 'To Do' or todo.status is None:
                self.todo_list_widget.addItem(item)
            elif todo.status == 'In Progress':
                self.in_progress_list_widget.addItem(item)
            elif todo.status == 'Done':
                self.done_list_widget.addItem(item)

    def open_todo_window(self, item):
            # Create a QDialog
            dialog = QDialog()
            layout = QVBoxLayout()
            dialog.setLayout(layout)

            # Create QLineEdit widgets for the title, priority, status, and a QDateEdit for the due_date
            title_input = QLineEdit(item.text())
            priority_input = QLineEdit()
            status_input = QLineEdit()
            due_date_input = QDateEdit()

            # Add the widgets to the layout
            layout.addWidget(title_input)
            layout.addWidget(priority_input)
            layout.addWidget(status_input)
            layout.addWidget(due_date_input)

            # Connect the accepted signal of the QDialog to a method that updates the ToDo
            dialog.accepted.connect(lambda: self.update_todo(item, title_input.text(), priority_input.text(), status_input.text(), due_date_input.date()))

            # Show the QDialog
            dialog.exec()



    def display_main_window(self):
        self.window.show()