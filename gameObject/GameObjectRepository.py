from gameObject.planet import Planet
from gameObject.campaign import Campaign
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
                    self.planets.append(Planet(child))
        for file in self.campaign_files:
            root = et.parse(file).getroot()
            for child in root:
                if child.tag == 'Campaign':
                    self.campaigns[child.get('Name')] = Campaign(child, self.planets)
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
        for name, campaign in self.campaigns.items():
            ui.select_GC.addItem(name)
            ui.map.plotGalaxy(campaign.planets, [], self.planets)
            ui.update_selected_planets(campaign.planets, self.planets)

        
    def onCellChanged(self, item):
        LastStateRole = QtCore.Qt.UserRole
        # item = self.ui.planet_list.item(row, column)
        lastState = item.data(LastStateRole)
        currentState = item.checkState()
        if currentState != lastState:
            if currentState == QtCore.Qt.Checked:
                campaign = self.campaigns[self.ui.select_GC.currentText()]
                if self.planets[item.row()] not in campaign.planets:
                    campaign.planets.append(self.planets[item.row()])
                else:
                    campaign.planets.remove(self.planets[item.row()])
                 #print("checked", item.text())
            else:
                campaign = self.campaigns[self.ui.select_GC.currentText()]
                if self.planets[item.row()] not in campaign.planets:
                    print("Item Not Already Listed!")
                else:
                    campaign.planets.remove(self.planets[item.row()])
                 #print("unchecked", item.text())
            self.ui.map.plotGalaxy(campaign.planets, [], self.planets)
            self.ui.update_selected_planets(campaign.planets, self.planets)
            item.setData(LastStateRole, currentState)
    #    for p in planets:
    #         self.planet_list.item(p, 0).setCheckState(QtCore.Qt.Checked)