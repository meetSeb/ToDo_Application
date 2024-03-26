import sys
from application.controller.task_manager import TaskManager
from application.model.database_manager import DatabaseManager
from application.view.user_interface import UserInterface



if __name__ == "__main__":
    # Erstellen Sie Instanzen von Ihrem Modell und Controller
    model = DatabaseManager('todo_list.db') 
    controller = TaskManager(db_manager='todo_list.db')  

    # Erstellen Sie eine Instanz von UserInterface und übergeben Sie das Modell und den Controller
    ui = UserInterface(model, controller)

    # Zeigen Sie das Hauptfenster an
    ui.display_main_window()

    # Update the KanBan Board
    ui.update_kanban_board()

    # Starten Sie die Anwendung
    sys.exit(ui.app.exec())