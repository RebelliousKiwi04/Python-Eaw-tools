from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore
from PyQt5 import Qsci
import sys,sched, time,os

class TextEditor(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.toolbar = QToolBar()
        self.setLayout(QVBoxLayout())
        self.toolbar.setIconSize(QSize(30, 30))
        self.textWindow = LuaEditor()

        self.layout().addWidget(self.toolbar)

        open_file_action = QAction(QIcon(os.path.join('images', 'blue-folder-open-document.png')), "Open file...", self)
        open_file_action.setStatusTip("Open file")
        self.toolbar.addAction(open_file_action)

        save_file_action = QAction(QIcon(os.path.join('images', 'disk.png')), "Save", self)
        save_file_action.setStatusTip("Save current page")
        self.toolbar.addAction(save_file_action)

        saveas_file_action = QAction(QIcon(os.path.join('images', 'disk--pencil.png')), "Save As...", self)
        saveas_file_action.setStatusTip("Save current page to specified file")
        self.toolbar.addAction(saveas_file_action)

        print_action = QAction(QIcon(os.path.join('images', 'printer.png')), "Print...", self)
        print_action.setStatusTip("Print current page")
        self.toolbar.addAction(print_action)


        undo_action = QAction(QIcon(os.path.join('images', 'arrow-curve-180-left.png')), "Undo", self)
        undo_action.setStatusTip("Undo last change")

        redo_action = QAction(QIcon(os.path.join('images', 'arrow-curve.png')), "Redo", self)
        redo_action.setStatusTip("Redo last change")
        self.toolbar.addAction(redo_action)


        cut_action = QAction(QIcon(os.path.join('images', 'scissors.png')), "Cut", self)
        cut_action.setStatusTip("Cut selected text")
        cut_action.setShortcut(QKeySequence.Cut)
        self.toolbar.addAction(cut_action)

        copy_action = QAction(QIcon(os.path.join('images', 'document-copy.png')), "Copy", self)
        copy_action.setStatusTip("Copy selected text")
        cut_action.setShortcut(QKeySequence.Copy)
        self.toolbar.addAction(copy_action)

        paste_action = QAction(QIcon(os.path.join('images', 'clipboard-paste-document-text.png')), "Paste", self)
        paste_action.setStatusTip("Paste from clipboard")
        cut_action.setShortcut(QKeySequence.Paste)
        self.toolbar.addAction(paste_action)

        select_action = QAction(QIcon(os.path.join('images', 'selection-input.png')), "Select all", self)
        select_action.setStatusTip("Select all text")
        cut_action.setShortcut(QKeySequence.SelectAll)


        # Connect to the signal producing the text of the current selection. Convert the string to float
        # and set as the pointsize. We could also use the index + retrieve from FONT_SIZES.




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
    Script.TerminalWindow.setText("Lua Test Terminal V1.0\n\n"+str('>>> '+"ERROR! Syntax Error on line: [2]"))
    Script.dialogWindow.exec()


