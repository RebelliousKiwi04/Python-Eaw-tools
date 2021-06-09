from PyQt5.QtWidgets import QApplication
import sys, os
import lxml.etree as et

from ui.MainWindow import MainUIWindow

originalPath = os.path.dirname(sys.argv[0])

class Config:
    def __init__(self):
        self.configFile = "config.xml"
        self.configRoot = et.parse(self.configFile).getroot()
        self.dataPath = self.configRoot.find("DataPath").text
        self.autoPlanetConnectionDistance = int(self.configRoot.find("MaximumFleetMovementDistance").text)

        if not self.dataPath:
            self.dataPath = os.getcwd()

class EaWModTool:
    def __init__(self, config, MainWindow, originalPath) -> None:
        self.config = config
        self.ui = MainWindow
        #self.gameObjectRepository = GameObjectRepository()
        self.game_object_files = []
        self.originalPath = originalPath
        self.listAllModFile()
        

    def init_repository(self) -> None:
        return None
    def listAllModFile(self):
        if os.path.isdir('xml'):
            xmlPath = '/xml/'
        else:
            xmlPath = '/XML/'
        gameObjectFiles = et.parse(os.getcwd()+xmlPath+'/gameobjectfiles.xml')
        print(gameObjectFiles.getroot())
        for child in gameObjectFiles.getroot():
            if child.tag == 'File':
                self.game_object_files.append(os.getcwd()+xmlPath+child.text)
                print(child.tag, child.text)
        for i in self.game_object_files:
            print(i)


config = Config()
os.chdir(config.dataPath)
numArgs = len(sys.argv)

if numArgs > 1:
    path = sys.argv[1]
else:
    path = config.dataPath

file = open('''C:/Program Files (x86)/Steam/SteamApps/common/Star Wars Empire at War/corruption/Mods/Rise-Of-The-Sith-Lords/Data/testFile.py''', 'w')

app = QApplication(sys.argv)

MainWindow = MainUIWindow()

EaWModToolApp = EaWModTool(config, MainWindow, originalPath)

sys.exit(app.exec_())