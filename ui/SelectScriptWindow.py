#Open Script window
from PyQt5.QtWidgets import *
from PyQt5.Qt import QStandardItemModel, QStandardItem
from PyQt5.QtGui import QFont,QColor
import os
class StandardItem(QStandardItem):
    def __init__(self, txt='', font_size=12, set_bold=False, color=QColor(0, 0, 0)):
        super().__init__()
        fnt=QFont()
        fnt.setBold(set_bold)
        self.setEditable(False)
        self.setForeground(color)
        self.setFont(fnt)
        self.setText(txt)


class SelectScriptWindow(QDialog):
    def __init__(self,parent,script_dir,mod_dir):
        super().__init__()
       # self.setWindowFlags(self.windowFlags() | Qt.Tool |Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.mod_dir = mod_dir
        self.dir = script_dir
        os.chdir(self.dir)
        self.setWindowTitle('Select Script')
        self.resize(500, 700)
        self.setLayout(QVBoxLayout())

        self.treeView = QTreeView()
        self.treeView.setHeaderHidden(True)

        self.treeModel = QStandardItemModel()
        self.rootNode = self.treeModel.invisibleRootItem()


        Scripts = StandardItem('Scripts')
        self.fullPaths= {}
        self.directories = []
        for i in os.listdir():
            fullPath = os.path.abspath(i)
            newItem = StandardItem(i)
            Scripts.appendRow(newItem)
            self.fullPaths[i] = fullPath
            if os.path.isdir(i):
                self.directories.append(fullPath)
                self.addToTree(fullPath,newItem)  
                os.chdir(self.dir)         
        self.parent = parent
        self.rootNode.appendRow(Scripts)

        self.treeView.setModel(self.treeModel)
        self.layout().addWidget(self.treeView)
        self.treeView.expandAll()
        self.treeView.doubleClicked.connect(self.getValue)
        self.exec()
    def getValue(self, val):
        self.parent.load_file(self.fullPaths[val.data()])
        self.accept()

        os.chdir(self.mod_dir)
    def addToTree(self,fullPath, item):
        os.chdir(fullPath)
        for i in os.listdir(fullPath):
            absPath = os.path.abspath(i)
            if os.path.isfile(i):
                self.fullPaths[i] = absPath
                secondaryItem = StandardItem(i)
                item.appendRow(secondaryItem)
            elif os.path.isdir(i):
                secondaryItem = StandardItem(i)
                item.appendRow(secondaryItem)
                self.addToTree(absPath, secondaryItem)
                os.chdir(fullPath)