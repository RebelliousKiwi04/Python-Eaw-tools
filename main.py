from PyQt5.QtWidgets import QApplication
import sys, os
from PyQt5 import QtCore
import lxml.etree as et
from gameObject.GameObjectRepository import ModRepository
from ui.MainWindow import MainUIWindow
import marshal
#sys.setrecursionlimit(10**6)

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

config = Config()

app = QApplication(sys.argv)

MainWindow = MainUIWindow()
#MainWindow.map.plotGalaxy(checkedPlanets, [], planets)
EaWModToolApp = EaWModTool(config, MainWindow, originalPath)

def onPlanetSelection(table):
        planet = EaWModToolApp.repository.planets[table[0]]
        print(planet.name)
        item = MainWindow.planet_list.item(table[0], 0)
        campaign = EaWModToolApp.repository.campaigns[MainWindow.select_GC.currentText()]
        if not planet in campaign.planets:
            addingPlanet = True
            campaign.planets.append(planet)
        else:
            campaign.planets.remove(planet)
            addingPlanet = False
        MainWindow.map.plotGalaxy(campaign.planets, campaign.trade_routes, EaWModToolApp.repository.planets)
        EaWModToolApp.repository.update_selected_planets()


MainWindow.map.planetSelectedSignal.connect(EaWModToolApp.repository.onPlanetSelection)


sys.exit(app.exec_())