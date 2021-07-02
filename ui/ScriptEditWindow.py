from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore
from PyQt5 import Qsci
from ui.Utilities import PyQtUtil
import sys,sched, time,os,re
from ScriptHandling.EaWFunctionLibrary import *
from ui.SelectScriptWindow import *
from slpp import slpp as luadecoder

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
    ARROW_MARKER_NUM = 8
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setLexer(Qsci.QsciLexerLua(self))
        font = QFont()
        font.setPointSize(10)
        fontmetrics = QFontMetrics(font)
        self.setMarginsFont(font)
        self.setMarginWidth(0, fontmetrics.width("0000") + 6)
        self.setMarginLineNumbers(0, True)
        self.setCallTipsVisible(0)
        self.setMarginsBackgroundColor(QColor("#cccccc"))
        #self.setAutocompletionSource(Qsci.QsciScintilla.AcsAll)
        self.setMarginSensitivity(1, True)
        self.marginClicked.connect(self.on_margin_clicked)
        self.markerDefine(Qsci.QsciScintilla.RightArrow,self.ARROW_MARKER_NUM)
        self.setMarkerBackgroundColor(QColor("#ee1111"),self.ARROW_MARKER_NUM)
        self.setBraceMatching(Qsci.QsciScintilla.SloppyBraceMatch)
        self.setIndentationGuides(True)
        self.setCaretLineVisible(True)
        self.setCaretLineBackgroundColor(QColor("#ffe4e4"))
        self.setAutoIndent(True)
        self.SendScintilla(Qsci.QsciScintilla.SCI_SETHSCROLLBAR, 0)
    def on_margin_clicked(self, nmargin, nline, modifiers):
        # Toggle marker for the line the margin was clicked on
        if self.markersAtLine(nline) != 0:
            self.markerDelete(nline, self.ARROW_MARKER_NUM)
        else:
            self.markerAdd(nline, self.ARROW_MARKER_NUM)
        

class ActionsWidget(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setLayout(QVBoxLayout())
        self.ActiveEnvironmentLayout = QVBoxLayout()
        self.sublayout1 = QHBoxLayout()
        font = QFont()
        font.setPointSize(10)
        self.ActiveEnvironmentLabel = QLabel("Active Environment:")
        self.ActiveEnvironmentLabel.setFont(font)
        self.ActiveEnvironment = QComboBox()
        self.sublayout1.addWidget(self.ActiveEnvironmentLabel)
        self.sublayout1.addWidget(self.ActiveEnvironment)
        self.EnvironmentProperties = QPushButton("Environment Properties")
        self.ActiveEnvironmentLayout.addLayout(self.sublayout1)
        self.ActiveEnvironment.addItem("Default Environment")
        self.ButtonLayout = QHBoxLayout()
        self.NewEnviro = QPushButton("New Environment")
        self.ButtonLayout.addWidget(self.NewEnviro)
        self.ButtonLayout.addWidget(self.EnvironmentProperties)
        self.ActiveEnvironmentLayout.addLayout(self.ButtonLayout)
        self.layout().addLayout(self.ActiveEnvironmentLayout)

        self.enviroActions = QHBoxLayout()
        self.SpawnUnit = QPushButton("Add Unit To Environment")
        self.RemoveUnit = QPushButton("Remove Unit From Environment")
        self.enviroActions.addWidget(self.SpawnUnit)
        self.enviroActions.addWidget(self.RemoveUnit)

        self.layout().addLayout(self.enviroActions)

        self.scriptLayout = QHBoxLayout()
        self.scriptLabel = QLabel("Current Active Script:")
        self.scriptLayout.addWidget(self.scriptLabel)
        self.scriptLabel.setFont(font)

        self.scriptName = QLineEdit()
        self.scriptLayout.addWidget(self.scriptName)
        self.openScriptButton = QPushButton()
        self.openScriptButton.setText("Load New Script")
        self.scriptLayout.addWidget(self.openScriptButton)

        self.layout().addLayout(self.scriptLayout)
        self.actionsLabel =QLabel("Actions:")
        self.layout().addWidget(self.actionsLabel)
        self.actionsLabel.setFont(font)
        self.ActionsLayout = QHBoxLayout()
        self.funcLayout = QVBoxLayout()
        self.triggerFunc = QPushButton("        Trigger Function        ")
        #self.ActionsLayout.addLayout(self.funcLayout)
        


        self.globalValueLayout = QVBoxLayout()
        self.GlobalValueTable = PyQtUtil.construct_table_widget(["Lua Globals"],1) 

        self.globalValueLayout.addWidget(self.GlobalValueTable)

        self.ManageGlobalvalues = QPushButton("Manage Lua Globals")

        self.globalValueLayout.addWidget(self.ManageGlobalvalues)
        self.ActionsLayout.addLayout(self.globalValueLayout)
        self.globalValueLayout.addWidget(self.triggerFunc)
        self.layout().addLayout(self.ActionsLayout)
        #self.layout().addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))




class ScriptTestWindow:
    def __init__(self, mod_dir, gameobjectrepo) -> None:
        self.mod_dir = mod_dir
        self.script_dir = mod_dir + "/Scripts/"
        self.library = self.script_dir + 'Library/'
        self.story = self.script_dir +'Story/'
        self.misc = self.script_dir +'Miscallaneous/'
        self.repository = gameobjectrepo
        Fontdb = QFontDatabase()
        idd = Fontdb.addApplicationFont("CascadiaCodePL.ttf")
        self.dialogWindow = QDialog()
        self.layout = QHBoxLayout()
        self.dialogWindow.setLayout(self.layout)
        self.dialogWindow.setWindowTitle("Edit/Test Script")
        font = QFont()
        font.setPointSize(10)

        self.EditFile = QTextEdit()
        self.editor = TextEditor()
        self.layout.addWidget(self.editor)

        self.RightSideLayout = QVBoxLayout()
        self.actionsLayout = ActionsWidget()


        self.RightSideLayout.addWidget(self.actionsLayout)

        self.TerminalWindow = QTextEdit()
        self.TerminalWindow.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.TerminalWindow.setTextColor(QColor(255,255,255))
        terminalfont = QFont()
        terminalfont.setFamily("Cascadia Code PL")
        terminalfont.setPointSize(8)
        self.TerminalWindow.setFont(terminalfont)
        self.TerminalWindow.setReadOnly(True)
        self.TerminalWindow.setText("Lua Test Terminal V1.1")
        self.RightSideLayout.addWidget(self.TerminalWindow)
        self.layout.addLayout(self.RightSideLayout)
        self.load_file()
        screenSize = QApplication.primaryScreen().size()
        self.actionsLayout.openScriptButton.clicked.connect(self.select_file)
        #self.dialogWindow.setGeometry(QRect(screenSize.width(), screenSize.height()))
        self.dialogWindow.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowMaximizeButtonHint)
    def append_text(self,text):
        currentText = text
        currentText = currentText.replace('cjsan', 'Chloe')
        currentText = currentText.replace('Christopher', 'Chloe')
        self.TerminalWindow.append('\n'+currentText)
    def select_file(self):
        selectWindow = SelectScriptWindow(self,self.script_dir,self.mod_dir)
        os.chdir(self.mod_dir)
    def load_file(self, filename=None):
        if filename == None:
            file = open(self.library+'PGBase.lua', 'r')
            filename = self.library+'PGBase.lua'
        else:
            file = open(filename, 'r')
        contents = file.read()
        file.close()
        self.editor.textWindow.setText(contents)
        fileContents = contents
        if filename.lower() != 'pgbase.lua':
            fileContents = '''require("PGBase")\n'''+fileContents


        if 'function definitions(' in fileContents.lower():
            fileContents = fileContents +'\n Definitions()'

        fileString=filename.lower().replace('library/', '')
        fileString=fileString.replace('story/','')
        fileString=fileString.replace('miscallaneous/','')
        self.actionsLayout.scriptName.setText(fileString)
    
        try:
            cwd = os.getcwd()
            os.chdir(self.library)
            lua = init_galactic_eaw_environment(mod_dir = self.mod_dir, gameObjectRepo=self.repository,file=filename).lua
            for i in lua.globals():
                print(i)
                rowCount = self.actionsLayout.GlobalValueTable.rowCount()
                self.actionsLayout.GlobalValueTable.setRowCount(rowCount + 1)
                item= QTableWidgetItem(i)
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                self.actionsLayout.GlobalValueTable.setItem(rowCount, 0, item)
            lua.execute(fileContents)

            os.chdir(cwd)
            self.append_text("No Initial Error Encountered In File: " +filename)
        except Exception as e:
            self.append_text('Critical Lua Error!\n'+str(e))
            
        
   # def trigger_func(self):

