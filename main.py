from PyQt5.QtWidgets import QApplication
import sys, os
import lxml.etree as et
from gameObject.GameObjectRepository import ModRepository
from ui.MainWindow import MainUIWindow
import marshal
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
        self.originalPath = originalPath
        self.repository = ModRepository(config.dataPath)
        self.repository.update_ui(self.ui)

def loadFile(file):
    file = open(file, 'rb')
    obj = marshal.load(file)
    file.close()
    return obj
checkedPlanets = loadFile('''C:/Users/Christopher/Desktop/Python EaW tool/checkedplanets''')
planets = loadFile('''C:/Users/Christopher/Desktop/Python EaW tool/planets''')
config = Config()
numArgs = len(sys.argv)
print(checkedPlanets)
if numArgs > 1:
    path = sys.argv[1]
else:
    path = config.dataPath

file = open('''C:/Program Files (x86)/Steam/SteamApps/common/Star Wars Empire at War/corruption/Mods/Rise-Of-The-Sith-Lords/Data/testFile.py''', 'w')



app = QApplication(sys.argv)

MainWindow = MainUIWindow()
#MainWindow.map.plotGalaxy(checkedPlanets, [], planets)
EaWModToolApp = EaWModTool(config, MainWindow, originalPath)

def selectedPlanet(table):
    for i in table:
        for name, campaign in EaWModToolApp.repository.campaigns.items():
            if EaWModToolApp.repository.planets[i] not in campaign.planets:
                campaign.planets.append(EaWModToolApp.repository.planets[i])
            else:
                campaign.planets.remove(EaWModToolApp.repository.planets[i])
            MainWindow.map.plotGalaxy(campaign.planets, [], EaWModToolApp.repository.planets)
MainWindow.map.planetSelectedSignal.connect(selectedPlanet)



sys.exit(app.exec_())