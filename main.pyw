from PyQt5.QtWidgets import QApplication,QFileDialog,QMessageBox
import sys, os
from PyQt5 import QtCore
from PyQt5 import QtGui
import lxml.etree as et
from UI_Manager import UI_Presenter
from ui.MainWindow import MainUIWindow
#sys.setrecursionlimit(10**6)

originalPath = os.path.dirname(sys.argv[0])

def validate_datapath(config):
    if config.dataPath == None or not config.dataPath.endswith(('DATA', 'Data', 'data')):
        msg = QMessageBox()
        msg.setWindowTitle('Error!')
        msg.setText('Point To a Vaild EaW Mod Data Folder!')
        msg.exec_()
        directory = str(QFileDialog.getExistingDirectory())
        if directory.endswith(('DATA', 'Data', 'data')):
            config.dataPath = directory
        return False
    else:
        return True
class Config:
    def __init__(self):
        self.configFile = "config.xml"
        if not os.path.isfile(self.configFile):
            self.dataPath = str(QFileDialog.getExistingDirectory())
        else:
            self.configRoot = et.parse(self.configFile).getroot()
            self.dataPath = self.configRoot.find("DataPath").text

class EaWModTool:
    def __init__(self, config, MainWindow, originalPath) -> None:
        self.config = config
        self.ui = MainWindow
        self.originalPath = originalPath
        self.presenter = UI_Presenter(self.ui, config.dataPath)
        self.repository = self.presenter.repository
        self.presenter.update_tabs()

        self.ui.setDataFolderAction.triggered.connect(self.set_datapath)
    def set_datapath(self):
        directory = str(QFileDialog.getExistingDirectory())
        if directory != self.config.dataPath:
            self.config.dataPath = directory
            if validate_datapath(self.config):
                self.presenter.disconnect_triggers()
                self.ui.select_GC.clear()
                self.ui.ownerSelection.clear()
                self.ui.planetComboBox.clear()
                self.ui.forcesListWidget.clear()
                self.ui.forcesListWidget.setRowCount(0)
                self.ui.planet_list.clear()
                self.ui.planet_list.setHorizontalHeaderLabels(["Planets"])
                self.ui.planet_list.setRowCount(0)
                self.ui.tradeRoute_list.clear()
                self.ui.tradeRoute_list.setRowCount(0)
                self.ui.tradeRoute_list.setHorizontalHeaderLabels(["Trade Routes"])

                self.presenter = UI_Presenter(self.ui, self.config.dataPath)
                self.repository = self.presenter.repository
        
                self.repository.update_tabs()



app = QApplication(sys.argv)

config = Config()


MainWindow = MainUIWindow()
#MainWindow.map.plotGalaxy(checkedPlanets, [], planets)
validate_datapath(config)
EaWModToolApp = EaWModTool(config, MainWindow, originalPath)


sys.exit(app.exec_())