from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore
import sys

class ScriptTestWindow:
    def __init__(self) -> None:
        Fontdb = QFontDatabase()
        idd = Fontdb.addApplicationFont("CascadiaCodePL.ttf")
        print(idd)
        self.dialogWindow = QDialog()
        self.layout = QHBoxLayout()
        self.dialogWindow.setLayout(self.layout)
        self.dialogWindow.setWindowTitle("Edit Unit")
        font = QFont()
        font.setPointSize(10)

        self.leftSideLayout = QVBoxLayout()
        self.leftSideLayout.addWidget(QPushButton("TestButton"))

        self.layout.addLayout(self.leftSideLayout)

        self.RightSideLayout = QVBoxLayout()
        tableWidget: QTableWidget = QTableWidget()
        tableWidget.setColumnCount(1)
        tableWidget.setHorizontalHeaderLabels(["Test"])
        tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        tableWidget.verticalHeader().setVisible(False)
        self.tableWidget= tableWidget
        self.RightSideLayout.addWidget(self.tableWidget)

        self.TerminalWindow = QTextEdit()
        self.TerminalWindow.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.TerminalWindow.setTextColor(QColor(255,255,255))
        terminalfont = QFont()
        terminalfont.setFamily("Cascadia Code PL")
        terminalfont.setPointSize(8)
        self.TerminalWindow.setFont(terminalfont)
        self.TerminalWindow.setReadOnly(True)
        self.TerminalWindow.setText("Lua Test Terminal V1.0\n>>>")
        self.RightSideLayout.addWidget(self.TerminalWindow)
        self.layout.addLayout(self.RightSideLayout)



app = QApplication(sys.argv)


import lupa
from lupa import LuaRuntime
lua = LuaRuntime()
class GameObject:
    def __init__(self):
        self.hi = "Hello"

lua.globals().GameObject = GameObject
try:
    lua.execute('''
    require("RequireTest")
    classInstance = GameObject()
    print(classInstance.hi)
    TestRequire('Hiiii Lua')
    adw
    ''')
except Exception as e:
    print("Error!", e)
    Script = ScriptTestWindow()
    Script.TerminalWindow.setText("Lua Test Terminal V1.0\n\n"+str(e))
    Script.dialogWindow.exec()


