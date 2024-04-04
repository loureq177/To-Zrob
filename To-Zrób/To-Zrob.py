import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Signals(QLineEdit):
    def __init__(self):
        super().__init__()
        self.editingFinished.connect(clicker)

def getStylesheet():
    with open("styl.qss","r") as file:
        str = file.read()
        return str

def addCategoryBar(categoriesLayout, confirmButton, categoryBar): #UNFINISHED
    categoriesLayout.addWidget(categoryBar)
    categoriesLayout.addWidget(confirmButton)
    print("addCategoryBar")

def confirmCategory(categoriesLayout, categoryBar, confirmButton, categoryButton): #UNFINISHED
    categoryBar.copy(categoryBar)
    categoriesLayout.addWidget(categoryButton)
    categoriesLayout.removeWidget(confirmButton)
    print("confirmCategory")

def removeCategory(categoriesLayout, categoryBar): #UNFINISHED
    categoriesLayout.removeWidget(categoryBar)
    print("removeCategory")

def clicker():
    print("ouch")
 
def main():
    app = QApplication(sys.argv)
    window = QWidget()

    # layouts
    outerOuterLayout = QHBoxLayout() #UNFINISHED
    rigtOuterLayout = QVBoxLayout()  #UNFINISHED
    leftOuterLayout = QVBoxLayout()
    categoriesLayout = QVBoxLayout()
    searchBarLayout = QFormLayout()

    # labels
    categoryLabel = QLabel("Kategorie")
    emptyLabel = QLabel("  ")

    #buttons
    addCategoryButton = QPushButton("Dodaj kategorię")
    categoryButton = QPushButton()
    confirmButton = QPushButton("Zatwierdź")
    removeButton = QPushButton("Usuń")
    
    #bars
    searchBar = QLineEdit()
    categoryBar = QLineEdit()

    searchBarLayout.addRow("Szukaj:", searchBar)
    categoriesLayout.addWidget(emptyLabel)
    categoriesLayout.addWidget(categoryLabel)
    categoriesLayout.addWidget(emptyLabel)
    categoriesLayout.addWidget(addCategoryButton)
    categoriesLayout.addWidget(removeButton)
    addCategoryButton.clicked.connect(lambda: addCategoryBar(categoriesLayout, confirmButton, categoryBar))
    confirmButton.clicked.connect(lambda: confirmCategory(categoriesLayout, categoryBar, confirmButton, categoryButton))
    removeButton.clicked.connect(lambda: removeCategory(categoriesLayout, categoryBar))
    window.setLayout(leftOuterLayout)
    window.setStyleSheet(getStylesheet())
    window.setWindowTitle("To-Zrób")
    leftOuterLayout.addLayout(searchBarLayout)
    leftOuterLayout.addLayout(categoriesLayout)
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
#hhhhh
hellodfdlksjhf