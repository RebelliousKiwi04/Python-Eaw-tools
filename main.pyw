from PyQt5.QtWidgets import QApplication,QFileDialog,QMessageBox
import sys, os
import lxml.etree as et,atexit
from UI_Manager import InterfaceHandler
from ui.MainWindow import MainUIWindow

originalPath = os.path.dirname(sys.argv[0])


# Rebuild Intended to work like this
# Will ideally have 3 main components, Main script, Interface, and Interface Handler
# Game Object classes will remain largely the same with better error handling and detection
# Ui windows will all have less action handling implemented in them, will be more separated between UI and action scripts


def validate_datapath(config):
    if config.dataPath == None or not config.dataPath.endswith(('DATA', 'Data', 'data')):
        msg = QMessageBox()
        msg.setWindowTitle('Error!')
        msg.setText('Point To a Vaild EaW Mod Data Folder!')
        msg.exec_()
        directory = str(QFileDialog.getExistingDirectory())
        if directory.endswith(('DATA', 'Data', 'data')):
            config.dataPath = directory
            return True
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
        self.logfile = open('logfile.txt', 'w')
        self.originalPath = originalPath
        self.presenter = InterfaceHandler(self.ui, config.dataPath, self.logfile)
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
                self.ui.select_faction.clear()
                self.ui.planetComboBox.clear()
                self.ui.forcesListWidget.clear()
                self.ui.forcesListWidget.setRowCount(0)
                self.ui.planet_list.clear()
                self.ui.planet_list.setHorizontalHeaderLabels(["Planets"])
                self.ui.planet_list.setRowCount(0)
                self.ui.tradeRoute_list.clear()
                self.ui.tradeRoute_list.setRowCount(0)
                self.ui.tradeRoute_list.setHorizontalHeaderLabels(["Trade Routes"])

                self.presenter = InterfaceHandler(self.ui, self.config.dataPath, self.logfile)
                self.repository = self.presenter.repository
        
                self.presenter.update_tabs()
    def closeEvent(self):   
        messageBox = QMessageBox()
        title = "Quit Application?"
        message = "WARNING !!\n\nIf you quit without saving, any changes made to the file will be lost.\n\nSave file before quitting?"
    
        reply = messageBox.question(None, title, message, messageBox.Yes | messageBox.No,messageBox.No)
        if reply == messageBox.Yes:
            self.save_current_file()
        self.logfile.write("Exiting Application....")
        self.logfile.flush()


























app = QApplication(sys.argv)

config = Config()

MainWindow = MainUIWindow()
#MainWindow.map.plotGalaxy(checkedPlanets, [], planets)
validate_datapath(config)
EaWModToolApp = EaWModTool(config, MainWindow, originalPath)
atexit.register(EaWModToolApp.closeEvent)

    

sys.exit(app.exec_())