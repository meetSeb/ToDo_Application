import pytest
from application.model.todo_item import ToDoItem
from application.model.database_manager import DatabaseManager, DatabaseError
from application.controller.task_manager import TaskManager

class TestTaskManager:
    @classmethod
    def setup_class(cls):
        cls.database_manager = DatabaseManager(':memory:')
        cls.task_manager = TaskManager(cls.database_manager)

    @classmethod
    def teardown_class(cls):
        cls.task_manager.delete_all_todo_items()

    @pytest.fixture(autouse=True)
    def setup(self):
        self.database_manager = TestTaskManager.database_manager
        self.task_manager = TestTaskManager.task_manager
        self.task_manager.delete_all_todo_items()


    def test_create_todo_item(self):
        todo_item = self.task_manager.create_todo_item('Test title', 'High', 'In Progress', '2022-01-01')
        assert isinstance(todo_item, ToDoItem)
        assert todo_item.title == 'Test title'
        assert todo_item.priority == 'High'
        assert todo_item.status == 'In Progress'
        assert todo_item.due_date == '2022-01-01'

    def test_get_todo_item(self):
        todo_item = self.task_manager.create_todo_item('Test title', 'High', 'In Progress', '2022-01-01')
        retrieved_item = self.task_manager.get_todo_item(todo_item.id)
        assert retrieved_item.due_date.format('YYYY-MM-DD') == todo_item.due_date

    def test_update_todo_item(self):
        todo_item = self.task_manager.create_todo_item('Test title', 'High', 'In Progress', '2022-01-01')
        self.task_manager.update_todo_item(todo_item.id, 'Updated title', 'Low', 'Done', '2022-02-02')
        updated_item = self.task_manager.get_todo_item(todo_item.id)
        assert updated_item.title == 'Updated title'
        assert updated_item.priority == 'Low'
        assert updated_item.status == 'Done'
        assert updated_item.due_date.format('YYYY-MM-DD') == '2022-02-02'

    def test_delete_todo_item(self):
        item1 = self.task_manager.create_todo_item('Test title 1', 'High', 'In Progress', '2022-01-01')
        item2 = self.task_manager.create_todo_item('Test title 2', 'Medium', 'Done', '2022-02-02')
        item3 = self.task_manager.create_todo_item('Test title 3', 'Low', 'Not Started', '2022-03-03')
        self.task_manager.delete_todo_item(item2.id)
        todo_items = self.task_manager.list_todo_items()
        assert 'Test title 2' not in [item.title for item in todo_items]
            
    def test_delete_all_todo_items(self):
        self.task_manager.create_todo_item('Test title 1', 'High', 'In Progress', '2022-01-01')
        self.task_manager.create_todo_item('Test title 2', 'Medium', 'Done', '2022-02-02')
        self.task_manager.create_todo_item('Test title 3', 'Low', 'Not Started', '2022-03-03')
        self.task_manager.delete_all_todo_items()
        todo_items = self.task_manager.list_todo_items()
        assert len(todo_items) == 0

    def test_list_todo_items(self):
        self.todo_items = [self.task_manager.create_todo_item(f'Test title {i}', 'High', 'In Progress', '2022-01-01') for i in range(10)]
        todo_items = self.task_manager.list_todo_items()
        assert len(todo_items) == len(self.todo_items)
        for item in self.todo_items:
            assert any(item.id == todo_item.id for todo_item in todo_items)

    def test_create_todo_item_with_empty_title(self):
        with pytest.raises(ValueError):
            self.task_manager.create_todo_item('', 'High', 'In Progress', '2022-01-01')

    def test_get_nonexistent_todo_item(self):
        with pytest.raises(DatabaseError):
            self.task_manager.get_todo_item(9999)