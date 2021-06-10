from gameObject.planet import Planet
from gameObject.campaign import Campaign
from gameObject.traderoutes import TradeRoute
import os, sys, lxml.etree as et, pickle, shutil
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
def serialize(gameObjectRepo):
    '''some pickle stuff'''

class ModRepository:
    def __init__(self, mod_directory):
        self.mod_dir = mod_directory
        self.game_object_files = self.get_game_object_files()
        self.campaign_files = self.get_galactic_conquests()
        self.hardpoint_files = self.get_hardpoint_files()
        self.tradeRoute_files = self.get_trade_routes()
        self.ui = None
        self.planets = []
        self.units = {}
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
            for child in root:
                if child.tag == 'Planet':
                    self.planets.append(Planet(child, file))
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
    def update_ui(self, ui):
        self.ui = ui
        LastStateRole = QtCore.Qt.UserRole
        for planet in self.planets:
            rowCount = ui.planet_list.rowCount()
            ui.planet_list.setRowCount(rowCount + 1)
            item= QTableWidgetItem(planet.name)
            item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            item.setCheckState(QtCore.Qt.Unchecked)
            item.setData(LastStateRole, item.checkState())
            ui.planet_list.setItem(rowCount, 0, item)
        for route in self.trade_routes:
            rowCount = ui.tradeRoute_list.rowCount()
            ui.tradeRoute_list.setRowCount(rowCount + 1)
            item= QTableWidgetItem(route.name)
            item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            item.setCheckState(QtCore.Qt.Unchecked)
            item.setData(LastStateRole, item.checkState())
            ui.tradeRoute_list.setItem(rowCount, 0, item)
        for name, campaign in self.campaigns.items():
            ui.select_GC.addItem(name)
            ui.map.plotGalaxy(campaign.planets, campaign.trade_routes, self.planets)
        self.ui.planet_list.itemChanged.connect(self.onCellChanged)
        self.ui.tradeRoute_list.itemChanged.connect(self.ontradeRouteCellChanged)
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
    def update_forces_tab(self):
        index = self.ui.planetComboBox.currentText()
        self.ui.planetComboBox.clear()
        for p in self.campaigns[self.ui.select_GC.currentText()].planets:
            self.ui.planetComboBox.addItem(p.name)
        if index in [x.name for x in self.campaigns[self.ui.select_GC.currentText()].planets]:
            self.ui.planetComboBox.setCurrentText(index)
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
        print(planet.name)
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
