from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
import sys, os,pickle
from TextHandler import *


class DatEditorWindow:
    def __init__(self):
        self.mainWindow = QMainWindow()
        self.dialogWindow = QWidget()
        self.mainWindow.setCentralWidget(self.dialogWindow)
        self.mainWindow.setGeometry(720, 720, 720, 720)
        self.layout = QVBoxLayout()
        self.dialogWindow.setLayout(self.layout)
        self.x = 0
        self.y = 0
        font = QFont()
        font.setPointSize(10)

        self.searchLabel = QLabel()
        self.searchLabel.setFont(font)
        self.searchLabel.setText("Search:")
        self.searchLayout = QHBoxLayout()
        self.searchLayout.addWidget(self.searchLabel)
        self.searchBox = QLineEdit()
        self.searchButton = QPushButton()
        self.searchButton.setText("🔍")
        self.searchLayout.addWidget(self.searchBox)
        self.searchLayout.addWidget(self.searchButton)

        self.layout.addLayout(self.searchLayout)

        tableWidget: QTableWidget = QTableWidget()
        tableWidget.setColumnCount(2)
        tableWidget.setHorizontalHeaderLabels(["Identifier", "Text String"])
        tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        tableWidget.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        tableWidget.verticalHeader().setVisible(False)
        self.textTable = tableWidget
        self.layout.addWidget(self.textTable)


        self.mainWindow.setWindowTitle("Text Editor")
        self.__menuBar: QMenuBar = QMenuBar()
        self.__fileMenu: QMenu = QMenu("File", self.mainWindow)
        self.__menuBar.addMenu(self.__fileMenu)
        self.mainWindow.setMenuWidget(self.__menuBar)

        self.__quitAction: QAction = QAction("Quit", self.mainWindow)
        self.__quitAction.triggered.connect(sys.exit)
        self.saveAction = QAction("Save", self.mainWindow)
        self.openAction = QAction("Open", self.mainWindow)
        self.testAction = QAction("Testing", self.mainWindow)
        self.SaveAsAction = QAction("Save As", self.mainWindow)
        self.__fileMenu.addAction(self.openAction)
        self.__fileMenu.addAction(self.saveAction)
        self.__fileMenu.addAction(self.SaveAsAction)
        self.__fileMenu.addAction(self.__quitAction)

        self.__newMenu = QMenu("New", self.mainWindow)
        self.newStringActino = QAction("Text String", self.mainWindow)
        self.__newMenu.addAction(self.newStringActino)
        self.__menuBar.addMenu(self.__newMenu)

def serialize_path(obj):
    file = open('local.bin', 'wb')
    obj = pickle.dump(obj, file)
    file.close()
def loadFile(filename):
    file = open(filename, 'rb')
    obj = pickle.load(file)
    file.close()
    return obj
class TextEditor:
    def __init__(self):
        self.app = QApplication(sys.argv)            
        self.ui = DatEditorWindow()
        self.ui.saveAction.triggered.connect(self.save)
        self.ui.openAction.triggered.connect(self.open_file)
        self.ui.searchButton.clicked.connect(self.search)
        self.ui.newStringActino.triggered.connect(self.new_string)
        self.ui.SaveAsAction.triggered.connect(self.save_as)
        if os.path.isfile('local.bin'):
            self.open_file(loadFile('local.bin'))
        self.ui.mainWindow.show()
        sys.exit(self.app.exec_())
    def open_file(self, file=False):
        if not os.path.isfile(file):
            file = QFileDialog.getOpenFileName()[0]
        if not str(file.lower()).endswith('.dat'):
            print(file.endswith(('.DAT', '.dat', '.Dat')))
            msg = QMessageBox()
            msg.setWindowTitle('Error!')
            msg.setText('Point To a Vaild Dat File!')
            msg.exec_()
            pass
        else:
            serialize_path(file)
            self.ui.textTable.clear()
            self.ui.textTable.setHorizontalHeaderLabels(["Identifier", "Text String"])
            self.Text = TextFile(file)
            self.textDict = self.Text.decompileDat()
            self.currentDict = self.textDict
            self.ui.textTable.setRowCount(0)
            for identifier, string in self.textDict.items():
                rowCount = self.ui.textTable.rowCount()
                self.ui.textTable.setRowCount(rowCount + 1)
                item= QTableWidgetItem(identifier)
                self.ui.textTable.setItem(rowCount, 0, item)
                item= QTableWidgetItem(string)
                self.ui.textTable.setItem(rowCount, 1, item)
    def update_current_dict(self):
        newDict = {}
        for row in range(self.ui.textTable.rowCount()):
            identifier = self.ui.textTable.item(row, 0).text()
            string = self.ui.textTable.item(row, 1).text()
            newDict[identifier] = string
        return newDict
    def search(self):
        searchString = self.ui.searchBox.text()
        if searchString == "" or " " or searchString.isspace():
            pass
        self.currentDict = self.update_current_dict()
        self.ui.textTable.clear()
        self.ui.textTable.setHorizontalHeaderLabels(["Identifier", "Text String"])
        self.ui.textTable.setRowCount(0)

        for identifier, string in self.textDict.items():
            if searchString.lower() in identifier.lower() or searchString.lower() in string.lower():
                rowCount = self.ui.textTable.rowCount()
                self.ui.textTable.setRowCount(rowCount + 1)
                item= QTableWidgetItem(identifier)
                self.ui.textTable.setItem(rowCount, 0, item)
                item= QTableWidgetItem(string)
                self.ui.textTable.setItem(rowCount, 1, item)
    def save(self):
        self.Text.compileDat(self.update_current_dict())
    def save_as(self):
        self.Text.compileDat(self.update_current_dict(), True)
    def new_string(self):
        textDict = self.update_current_dict()
        self.ui.textTable.clear()
        self.ui.textTable.setHorizontalHeaderLabels(["Identifier", "Text String"])
        self.ui.textTable.setRowCount(0)
        self.ui.textTable.setRowCount(1)
        for identifier, string in textDict.items():
            rowCount = self.ui.textTable.rowCount()
            self.ui.textTable.setRowCount(rowCount + 1)
            item= QTableWidgetItem(identifier)
            self.ui.textTable.setItem(rowCount, 0, item)
            item= QTableWidgetItem(string)
            self.ui.textTable.setItem(rowCount, 1, item)


TextEditor()