from gameObject.planet import Planet
from gameObject.campaign import Campaign
from gameObject.traderoutes import TradeRoute
from gameObject.unit import Unit
from ui.AddUnitWindow import AddUnitWindow
import os, sys, lxml.etree as et, pickle, shutil
from PyQt5.QtWidgets import *
from PyQt5 import QtCore

class ModRepository:
    def __init__(self, mod_directory, ui):
        self.mod_dir = mod_directory
        self.game_object_files = self.get_game_object_files()
        self.campaign_files = self.get_galactic_conquests()
        self.hardpoint_files = self.get_hardpoint_files()
        self.tradeRoute_files = self.get_trade_routes()
        self.planetFiles = []
        self.ui = ui
        self.planets = []
        self.units = []
        self.hardpoints = {}
        self.text = {}
        self.campaigns = {}
        self.trade_routes = []
        self.dir = mod_directory
        self.init_repo()
    def get_trade_routes(self):
        tradeRoute_files = []
        if os.path.isdir('xml'):
            xmlPath = '/xml/'
        else:
            xmlPath = '/XML/'
        tradeRouteFiles = et.parse(self.mod_dir+xmlPath+'/traderoutefiles.xml')
        for child in tradeRouteFiles.getroot():
            if child.tag == 'File':
                tradeRoute_files.append(self.mod_dir+xmlPath+child.text)
        return tradeRoute_files
    def get_hardpoint_files(self):
        hardPoint_files = []
        if os.path.isdir('xml'):
            xmlPath = '/xml/'
        else:
            xmlPath = '/XML/'
        hardpointdatafiles = et.parse(self.mod_dir+xmlPath+'/hardpointdatafiles.xml')
        for child in hardpointdatafiles.getroot():
            if child.tag == 'File':
                hardPoint_files.append(self.mod_dir+xmlPath+child.text)
        return hardPoint_files
    def get_game_object_files(self):
        game_object_files = []
        if os.path.isdir('xml'):
            xmlPath = '/xml/'
        else:
            xmlPath = '/XML/'
        gameObjectFiles = et.parse(self.mod_dir+xmlPath+'/gameobjectfiles.xml')
        for child in gameObjectFiles.getroot():
            if child.tag == 'File':
                game_object_files.append(self.mod_dir+xmlPath+child.text)
        return game_object_files
    def get_galactic_conquests(self):
        campaign_files = []
        if os.path.isdir('xml'):
            xmlPath = '/xml/'
        else:
            xmlPath = '/XML/'
        campaignFiles = et.parse(self.mod_dir+xmlPath+'/campaignfiles.xml')
        for child in campaignFiles.getroot():
            if child.tag == 'File':
                campaign_files.append(self.mod_dir+xmlPath+child.text)
        return campaign_files
    def init_repo(self):
        for file in self.game_object_files:
            root = et.parse(file).getroot()
            if root.tag == 'Planets':
                self.planetFiles.append(file)
            for child in root:
                if child.tag == 'Planet':
                    self.planets.append(Planet(child, file))
                    if not file in self.planetFiles:
                        self.planetFiles.append(file)
                if child.tag == 'SpaceUnit' or child.tag == 'UniqueUnit' or child.tag == 'GroundInfantry' or child.tag == 'GroundVehicle' or child.tag == 'HeroUnit' or child.tag == 'GroundUnit' or child.tag == 'Squadron':
                    self.units.append(Unit(child,file))
        for file in self.tradeRoute_files:
            root = et.parse(file).getroot()
            for child in root:
                if child.tag == 'TradeRoute':
                    route = TradeRoute(child, file)
                    route.set_point_planets(self.planets)
                    self.trade_routes.append(route)
        for file in self.campaign_files:
            root = et.parse(file).getroot()
            for child in root:
                if child.tag == 'Campaign':
                    self.campaigns[child.get('Name')] = Campaign(child, self.planets, self.trade_routes, file)
    def update_ui(self):
        LastStateRole = QtCore.Qt.UserRole
        for planet in self.planets:
            rowCount = self.ui.planet_list.rowCount()
            self.ui.planet_list.setRowCount(rowCount + 1)
            item= QTableWidgetItem(planet.name)
            item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            item.setCheckState(QtCore.Qt.Unchecked)
            item.setData(LastStateRole, item.checkState())
            self.ui.planet_list.setItem(rowCount, 0, item)
            planet.reset_starting_forces_table(self.campaigns)
        for route in self.trade_routes:
            rowCount = self.ui.tradeRoute_list.rowCount()
            self.ui.tradeRoute_list.setRowCount(rowCount + 1)
            item= QTableWidgetItem(route.name)
            item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            item.setCheckState(QtCore.Qt.Unchecked)
            item.setData(LastStateRole, item.checkState())
            self.ui.tradeRoute_list.setItem(rowCount, 0, item)
        for name, campaign in self.campaigns.items():
            self.ui.select_GC.addItem(name)
        campaign = self.campaigns[self.ui.select_GC.currentText()]
        self.ui.map.plotGalaxy(campaign.planets, campaign.trade_routes, self.planets)
        self.ui.planet_list.itemChanged.connect(self.onCellChanged)
        self.ui.tradeRoute_list.itemChanged.connect(self.ontradeRouteCellChanged)
        self.ui.add_unit_to_planet.clicked.connect(self.add_unit)
        self.ui.planetComboBox.currentIndexChanged.connect(self.update_forces_table)
        self.update_selected_planets()
        self.update_seleceted_trade_routes()
    def ontradeRouteCellChanged(self, item):
        tradeRoute = self.trade_routes[item.row()]
        campaign = self.campaigns[self.ui.select_GC.currentText()]
        if not tradeRoute in campaign.trade_routes:
            addingTradeRoute = True
            campaign.trade_routes.append(tradeRoute)
        else:
            campaign.trade_routes.remove(tradeRoute)
            addingTradeRoute = False

        currentState = item.checkState()
        if currentState == QtCore.Qt.Unchecked:
            if addingTradeRoute:
                item.setCheckState(QtCore.Qt.Checked)
        elif currentState == QtCore.Qt.Checked:
            if not addingTradeRoute:
                item.setCheckState(QtCore.Qt.Unchecked)
        self.ui.map.plotGalaxy(campaign.planets, campaign.trade_routes, self.planets)
    def update_seleceted_trade_routes(self):
        self.ui.tradeRoute_list.itemChanged.disconnect(self.ontradeRouteCellChanged)
        rowCount = self.ui.tradeRoute_list.rowCount()
        for row in range(rowCount):
            self.ui.tradeRoute_list.item(row, 0).setCheckState(QtCore.Qt.Unchecked)
        selectedPlanets = []
        planets = self.campaigns[self.ui.select_GC.currentText()].trade_routes
        for p in planets:
            selectedPlanets.append([x.name for x in self.trade_routes].index(p.name))
        for p in selectedPlanets:
            item = self.ui.tradeRoute_list.item(p, 0)
            currentState = item.checkState()
            if currentState == QtCore.Qt.Unchecked:
                item.setCheckState(QtCore.Qt.Checked)
        self.ui.tradeRoute_list.itemChanged.connect(self.ontradeRouteCellChanged)
    def update_selected_planets(self):
        self.ui.planet_list.itemChanged.disconnect(self.onCellChanged)
        rowCount = self.ui.planet_list.rowCount()
        for row in range(rowCount):
            self.ui.planet_list.item(row, 0).setCheckState(QtCore.Qt.Unchecked)
        selectedPlanets = []
        planets = self.campaigns[self.ui.select_GC.currentText()].planets
        for p in planets:
            selectedPlanets.append([x.name for x in self.planets].index(p.name))
        for p in selectedPlanets:
            item = self.ui.planet_list.item(p, 0)
            currentState = item.checkState()
            if currentState == QtCore.Qt.Unchecked:
                item.setCheckState(QtCore.Qt.Checked)
        self.update_forces_tab()
        self.ui.planet_list.itemChanged.connect(self.onCellChanged)
    def update_forces_table(self):
        self.ui.forcesListWidget.clear()
        self.ui.forcesListWidget.setRowCount(0)
        self.ui.forcesListWidget.setHorizontalHeaderLabels(["Unit", "Power", "Tech"])
        campaign = self.campaigns[self.ui.select_GC.currentText()]
        planet_name = self.ui.planetComboBox.currentText()
        if planet_name in [x.name for x in self.planets]:
            planet_index = [x.name for x in self.planets].index(planet_name)
        planet = self.planets[planet_index]
        starting_forces = planet.starting_forces[self.ui.select_GC.currentText()]
        for tech, forces_table in zip(list(range(1,len(starting_forces)+1)), starting_forces):
            for unit in forces_table:
                print(unit.name)
                rowCount = self.ui.forcesListWidget.rowCount()
                self.ui.forcesListWidget.setRowCount(rowCount + 1)
                item= QTableWidgetItem(unit.name)
                self.ui.forcesListWidget.setItem(rowCount, 0, item)
                item= QTableWidgetItem(str(unit.aicp))
                self.ui.forcesListWidget.setItem(rowCount, 1, item)
                item= QTableWidgetItem(str(tech))
                self.ui.forcesListWidget.setItem(rowCount, 2, item)
    def update_forces_tab(self):
        self.ui.planetComboBox.currentIndexChanged.disconnect(self.update_forces_table)
        index = self.ui.planetComboBox.currentText()
        self.ui.planetComboBox.clear()
        for p in self.campaigns[self.ui.select_GC.currentText()].planets:
            self.ui.planetComboBox.addItem(p.name)
        if index in [x.name for x in self.campaigns[self.ui.select_GC.currentText()].planets]:
            self.ui.planetComboBox.setCurrentText(index)
        self.ui.planetComboBox.currentIndexChanged.connect(self.update_forces_table)
    def onCellChanged(self, item):
        LastStateRole = QtCore.Qt.UserRole
        planet = self.planets[item.row()]
        campaign = self.campaigns[self.ui.select_GC.currentText()]
        if not planet in campaign.planets:
            addingPlanet = True
            campaign.planets.append(planet)
        else:
            campaign.planets.remove(planet)
            addingPlanet = False

        currentState = item.checkState()
        if currentState == QtCore.Qt.Unchecked:
            if addingPlanet:
                item.setCheckState(QtCore.Qt.Checked)
        elif currentState == QtCore.Qt.Checked:
            if not addingPlanet:
                item.setCheckState(QtCore.Qt.Unchecked)
        self.update_forces_tab()
        self.ui.map.plotGalaxy(campaign.planets, campaign.trade_routes, self.planets)
    def onPlanetSelection(self, table):
        planet = self.planets[table[0]]
        item = self.ui.planet_list.item(table[0], 0)
        campaign = self.campaigns[self.ui.select_GC.currentText()]
        if not planet in campaign.planets:
            addingPlanet = True
            campaign.planets.append(planet)
        else:
            campaign.planets.remove(planet)
            addingPlanet = False
        self.ui.map.plotGalaxy(campaign.planets, campaign.trade_routes, self.planets)
        self.update_selected_planets()
    def select_GC(self):
        index = self.ui.select_GC.currentText()
        self.ui.main_window.setWindowTitle("EaW Mod Tool - " + index)
        self.update_selected_planets()
        self.update_forces_table()
        self.update_seleceted_trade_routes()
        campaign = self.campaigns[index]
        self.ui.map.plotGalaxy(campaign.planets, campaign.trade_routes, self.planets)
    def save(self):
        openedFiles = {}
        #for file in self.game_object_files:          
        for file in self.campaign_files:
            for name,campaign in self.campaigns.items():
                if campaign.fileLocation == file:
                    if campaign.fileLocation not in openedFiles.keys():
                        openedFiles[file] = open(file, 'w')
    def add_unit(self):
        self.addUnitWindow = AddUnitWindow(self.ui.planetComboBox.currentText())
        self.addUnitWindow.OkCancelButtons.accepted.connect(self.addUnitToStartingForces)
        self.addUnitWindow.update_unit_box(self.units)
        self.addUnitWindow.show()
    def addUnitToStartingForces(self):
        planet_name = self.addUnitWindow.planet
        techLevel = self.addUnitWindow.TechLevel.value()
        quantity = self.addUnitWindow.Quantity.value()
        owner = self.addUnitWindow.OwnerSelection.currentText()
        unit_name = self.addUnitWindow.UnitTypeSelection.currentText()
        
        if unit_name in [x.name for x in self.units]:
            unit_index = [x.name for x in self.units].index(unit_name)
        print(unit_index)
        if planet_name in [x.name for x in self.planets]:
            planet_index = [x.name for x in self.planets].index(planet_name)
        print(planet_index)
        unit = self.units[unit_index]
        planet = self.planets[planet_index]
        forces = planet.starting_forces[self.ui.select_GC.currentText()]
        if techLevel > len(forces):
            for i in range(1,(techLevel-len(forces)+1)):
                forces.append([])
        for i in range(1,quantity+1):
            forces[techLevel-1].append(unit)
        print('finished func')
        self.addUnitWindow.OkCancelButtons.accepted.disconnect(self.addUnitToStartingForces)


        for i in range(1,quantity+1):
            rowCount = self.ui.forcesListWidget.rowCount()
            self.ui.forcesListWidget.setRowCount(rowCount + 1)
            item= QTableWidgetItem(unit.name)
            self.ui.forcesListWidget.setItem(rowCount, 0, item)
            item= QTableWidgetItem(str(unit.aicp))
            self.ui.forcesListWidget.setItem(rowCount, 1, item)
            item= QTableWidgetItem(str(techLevel))
            self.ui.forcesListWidget.setItem(rowCount, 2, item)
        self.addUnitWindow.dialogWindow.accept()
