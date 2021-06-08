from PyQt5.QtWidgets import QApplication
import sys, os
import lxml.etree as et

from ui.MainWindow import MainUIWindow

class Config:
    def __init__(self):
        self.configFile = "config.xml"
        self.configRoot = et.parse(self.configFile).getroot()
        self.dataPath = self.configRoot.find("DataPath").text
        self.autoPlanetConnectionDistance = int(self.configRoot.find("MaximumFleetMovementDistance").text)

        if not self.dataPath:
            self.dataPath = os.getcwd()

class EaWModTool:
    def __init__(self, config, MainWindow) -> None:
        self.config = config
        self.ui = MainWindow
        #self.gameObjectRepository = GameObjectRepository()
        self.init_repository()
    def init_repository(self) -> None:
        return None


config = Config()
numArgs = len(sys.argv)

if numArgs > 1:
    path = sys.argv[1]
else:
    path = config.dataPath



app = QApplication(sys.argv)

MainWindow = MainUIWindow()

#EaWModToolApp = EaWModTool(config, MainWindow)

sys.exit(app.exec_())