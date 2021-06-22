from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore
from PyQt5 import Qsci
import sys,sched, time

class TextEditor(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.toolbar = QToolBar()
        self.setLayout(QVBoxLayout())

        self.textWindow = LuaEditor()

        self.layout().addWidget(self.toolbar)
        self.layout().addWidget(self.textWindow)


class LuaEditor(Qsci.QsciScintilla):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setLexer(Qsci.QsciLexerLua(self))
        self.setText("""function Test(func)  
        
        print('hi')
        end""")
    def set_text(self,text):
        self.setText(text)
    def append_text(self,text):
        currentText = self.text()
        currentText.append("\n"+text)
        self.setText(currentText)

class ScriptTestWindow:
    def __init__(self) -> None:
        Fontdb = QFontDatabase()
        idd = Fontdb.addApplicationFont("CascadiaCodePL.ttf")
        self.dialogWindow = QDialog()
        self.layout = QHBoxLayout()
        self.dialogWindow.setLayout(self.layout)
        self.dialogWindow.setWindowTitle("Edit Unit")
        font = QFont()
        font.setPointSize(10)

        self.EditFile = QTextEdit()
        self.layout.addWidget(TextEditor())

        self.RightSideLayout = QVBoxLayout()
        self.actionsLayout = QWidget()

        self.RightSideLayout.addWidget(self.actionsLayout)

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
    Script.TerminalWindow.setText("Lua Test Terminal V1.0\n\n"+str('>>> '+ str(e)))
    Script.dialogWindow.exec()


