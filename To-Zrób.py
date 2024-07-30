from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QListWidget, QPushButton,
                              QLineEdit, QGridLayout, QLabel, QListWidgetItem, QMessageBox)
import csv

class TaskList:
    def __init__(self):
        self.tasks = []
        self.categories = []

    def add_task(self, task, category):
        self.tasks.append((task, category))

    def get_tasks_for_category(self, category):
        return [task for task, cat in self.tasks if cat == category]
    
    def __del__(self):
        destructorString = "Destruktor został wywołany."
        print(destructorString)
        print(f'długość ciągu znaków w zmiennej destructorString wynosi: {len(destructorString)}')

class Category:
    def __init__(self, name):
        self.name = name
        self.tasks = []
  
    def add_task(self, task):
        self.tasks.append(task)

    def get_tasks(self):
        return self.tasks

    def remove_task(self, task):
        if task in self.tasks:
            self.tasks.remove(task)
    
    def __str__(self):
        return self.name

class MainApplicationWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.task_list = TaskList()
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        layout = QGridLayout(central_widget)

        self.category_widget = QListWidget()
        self.category_widget.clicked.connect(self.category_clicked)
        add_category_button = QPushButton('Dodaj Kategorię')
        remove_category_button = QPushButton('Usuń Kategorię')
        layout.addWidget(self.category_widget, 0, 0, 1, 2)

        self.task_widget = QListWidget()
        add_task_button = QPushButton('Dodaj zadanie')
        remove_task_button = QPushButton('Usuń zadanie')
        layout.addWidget(self.task_widget, 0, 2, 1, 2)

        layout.removeWidget(self)

        self.category_label = QLabel('Kategoria:')
        self.category_input = QLineEdit()
        self.category_input.returnPressed.connect(self.add_category)
        layout.addWidget(self.category_label, 1, 0)
        layout.addWidget(self.category_input, 1, 1)

        self.task_label = QLabel('Zadanie:')
        self.task_input = QLineEdit()
        self.task_input.returnPressed.connect(self.add_task)
        layout.addWidget(self.task_label, 1, 2)
        layout.addWidget(self.task_input, 1, 3)

        add_category_button.clicked.connect(self.add_category)
        add_task_button.clicked.connect(self.add_task)
        remove_category_button.clicked.connect(self.remove_category)
        remove_task_button.clicked.connect(self.remove_task)

        layout.addWidget(add_category_button, 3, 0, 1, 1)
        layout.addWidget(remove_category_button, 3, 1, 1, 1)
        layout.addWidget(add_task_button, 3, 2, 1, 1)
        layout.addWidget(remove_task_button, 3, 3, 1, 1)

        self.setCentralWidget(central_widget)

        self.setWindowTitle('To-Zrób')
        self.setGeometry(100, 100, 400, 400)
        self.setStyleSheet(getStylesheet())

    def save_to_csv(self, file_path):
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)

            # Zapis danych
            for category in self.task_list.categories:
                writer.writerow([category.name, ''])
                for task in category.get_tasks():
                    writer.writerow(['', task])

    def load_from_csv(self, file_path):
        with open(file_path, mode='r') as file:
            reader = csv.reader(file)

            current_category = None
            for row in reader:
                if row:
                    category_name, task = row
                    if category_name:
                        current_category = Category(category_name)
                        self.task_list.categories.append(current_category)
                        item = QListWidgetItem(category_name)
                        self.category_widget.addItem(item)
                    elif task and current_category:
                        current_category.add_task(task)
                        tasks_for_category = current_category.get_tasks()
                        self.task_widget.clear()
                        self.task_widget.addItems(tasks_for_category)

    def add_category(self):
        new_category_name = self.category_input.text()
        if new_category_name:
            new_category = Category(new_category_name)
            self.task_list.categories.append(new_category)
            item = QListWidgetItem(new_category_name)
            self.category_widget.addItem(item)
            self.category_input.clear()

    def add_task(self):
        new_task = self.task_input.text()
        selected_category_item = self.category_widget.currentItem()
        if new_task and selected_category_item:
            selected_category_name = selected_category_item.text()
            selected_category = next((category for category in self.task_list.categories if category.name == selected_category_name), None)
            if selected_category:
                selected_category.add_task(new_task)
                tasks_for_category = selected_category.get_tasks()
                self.task_widget.clear()
                self.task_widget.addItems(tasks_for_category)
                self.task_input.clear()

    def remove_category(self):
        selected_category_item = self.category_widget.currentItem()
        if selected_category_item:
            selected_category_name = selected_category_item.text()
            selected_category = next((category for category in self.task_list.categories if category.name == selected_category_name), None)
            if selected_category:
                self.task_list.categories.remove(selected_category)
                self.category_widget.takeItem(self.category_widget.row(selected_category_item))
                self.task_widget.clear()
            else:
                QMessageBox.warning(self, 'Błąd', 'Nie znaleziono wybranej kategorii.')
        else:
            QMessageBox.warning(self, 'Błąd', 'Nie wybrano żadnej kategorii.')

    def remove_task(self):
        selected_task_items = self.task_widget.selectedItems()
        selected_category_item = self.category_widget.currentItem()
        if selected_task_items and selected_category_item:
            selected_category_name = selected_category_item.text()
            selected_category = next((category for category in self.task_list.categories if category.name == selected_category_name), None)
            if selected_category:
                for task_item in selected_task_items:
                    selected_category.remove_task(task_item.text())
                    self.task_widget.takeItem(self.task_widget.row(task_item))
                self.task_input.clear()
            else:
                QMessageBox.warning(self, 'Błąd', 'Nie znaleziono wybranej kategorii.')
        else:
            QMessageBox.warning(self, 'Błąd', 'Nie wybrano żadnej kategorii.')

    def category_clicked(self, index):
        item = self.category_widget.itemFromIndex(index)
        if item:
            selected_category_name = item.text()
            selected_category = next((category for category in self.task_list.categories if category.name == selected_category_name), None)
            if selected_category:
                tasks_for_category = selected_category.get_tasks()
                self.task_widget.clear()
                self.task_widget.addItems(tasks_for_category)

def getStylesheet():
    with open('arkuszStylów.qss','r') as file:
        str = file.read()
        return str

if __name__ == '__main__':
    app = QApplication([])
    main_window = MainApplicationWindow()
    main_window.load_from_csv('dane.csv')
    main_window.show()
    app.aboutToQuit.connect(lambda: main_window.save_to_csv('dane.csv'))
    app.exec()
