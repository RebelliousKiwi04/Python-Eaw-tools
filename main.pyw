from PyQt5.QtWidgets import QApplication,QFileDialog,QMessageBox
import sys, os
from PyQt5 import QtCore
from PyQt5 import QtGui
import lxml.etree as et
from gameObject.GameObjectRepository import ModRepository
from ui.MainWindow import MainUIWindow
#sys.setrecursionlimit(10**6)

originalPath = os.path.dirname(sys.argv[0])

def validate_datapath(config):
    while config.dataPath == None or not config.dataPath.endswith(('DATA', 'Data', 'data')):
        msg = QMessageBox()
        msg.setWindowTitle('Error!')
        msg.setText('Point To a Vaild EaW Mod Data Folder!')
        msg.exec_()
        directory = str(QFileDialog.getExistingDirectory())
        if directory.endswith(('DATA', 'Data', 'data')):
            config.dataPath = directory
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
        self.repository = ModRepository(config.dataPath, self.ui)
        self.repository.update_ui()
        self.ui.select_GC.currentIndexChanged.connect(self.repository.select_GC)
        self.ui.map.planetSelectedSignal.connect(self.repository.onPlanetSelection)
        self.ui.main_window.setWindowTitle("EaW Mod Tool - " + self.ui.select_GC.currentText())
        self.ui.setDataFolderAction.triggered.connect(self.set_datapath)
    def set_datapath(self):
        directory = str(QFileDialog.getExistingDirectory())
        if directory != self.config.dataPath:
            self.config.dataPath = directory
            validate_datapath(self.config)
            self.ui.planet_list.itemChanged.disconnect(self.repository.onCellChanged)
            self.ui.map.planetSelectedSignal.disconnect(self.repository.onPlanetSelection)
            self.ui.tradeRoute_list.itemChanged.disconnect(self.repository.ontradeRouteCellChanged)
            self.ui.add_unit_to_planet.clicked.disconnect(self.repository.add_unit)
            self.ui.planetComboBox.currentIndexChanged.disconnect(self.repository.update_forces_table)
            self.ui.ownerSelection.currentIndexChanged.disconnect(self.repository.change_planet_owner)
            self.ui.select_GC.currentIndexChanged.disconnect(self.repository.select_GC)
            self.ui.select_GC.clear()
            self.ui.ownerSelection.clear()
            self.ui.planetComboBox.clear()
            self.ui.forcesListWidget.clear()
            self.ui.forcesListWidget.setRowCount(0)
            self.ui.planet_list.clear()
            self.ui.planet_list.setRowCount(0)
            self.ui.tradeRoute_list.clear()
            self.ui.tradeRoute_list.setRowCount(0)

            self.repository = ModRepository(config.dataPath, self.ui)
            self.repository.update_ui()
            self.ui.select_GC.currentIndexChanged.connect(self.repository.select_GC)
            self.ui.map.planetSelectedSignal.connect(self.repository.onPlanetSelection)


app = QApplication(sys.argv)

config = Config()


MainWindow = MainUIWindow()
#MainWindow.map.plotGalaxy(checkedPlanets, [], planets)
validate_datapath(config)
EaWModToolApp = EaWModTool(config, MainWindow, originalPath)


sys.exit(app.exec_())