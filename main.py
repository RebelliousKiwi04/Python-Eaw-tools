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
        self.all_mod_files = []
        self.mod_dict = {
            "file_name": 'absolute_path'
        }
        self.originalPath = originalPath
        self.listAllModFile()
    def init_repository(self) -> None:
        return None
    def listAllModFile(self):
            if os.path.isdir(self.config.dataPath + '/xml'):
                modPath = self.config.dataPath + '/xml/'
            else:
                modPath = self.config.dataPath + '/XML/'
            os.chdir(modPath)
            basedir = os.listdir()
            pathsToIterate = []
            for file in basedir:
                if os.path.isfile(file):
                    print(os.path.abspath(file))
                    self.all_mod_files.append(os.path.abspath(file))
                elif os.path.isdir(file):
                    if file.upper() != 'AI' and file.upper() != 'ENUM':
                        subdir = modPath+ file
                        pathsToIterate.append(subdir)
            for path in pathsToIterate:
                currentPath = path
                print(path)
                os.chdir(path)
                subdirectory = os.listdir()
                for file in subdirectory:
                    if os.path.isfile(file):
                        print(os.path.abspath(file))
                        self.all_mod_files.append(os.path.abspath(file))
                    elif os.path.isdir(file):
                        path = currentPath + "\\"+file
                        pathsToIterate.append(path)
                os.chdir(self.originalPath)

config = Config()
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