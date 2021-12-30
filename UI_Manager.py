from ui.AddUnitWindow import AddUnitWindow
from ui.EditPlanetWindow import PlanetWindow
from gameObject.GameObjectRepository import ModRepository
from gameObject.StartingForcesObject import StartingForcesObject
import os, sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import *
from ui.CampaignProperties import CampaignPropertiesWindow

class UI_Presenter:
    def __init__(self, ui, mod_dir):
        self.logFile = open('logfile.txt', 'w')
        self.ui = ui
        self.mod_dir = mod_dir
        self.repository = ModRepository(mod_dir)
        self.selected_set = None
        self.selected_campaign = None
    def connect_triggers(self):
        self.ui.planet_list.itemChanged.connect(self.planetStatusModified)
        self.ui.tradeRoute_list.itemChanged.connect(self.ontradeRouteCellChanged)
        self.ui.add_unit_to_planet.clicked.connect(self.add_unit_to_starting_forces)
        self.ui.planetComboBox.currentIndexChanged.connect(self.update_starting_forces_table)
        self.ui.edit_planet_action.triggered.connect(self.edit_planet)
        self.ui.select_all_planets.clicked.connect(self.check_all_planets)
        self.ui.deselect_all_planets.clicked.connect(self.uncheck_all_planets)
        self.ui.select_all_tradeRoutes.clicked.connect(self.check_all_tradeRoutes)
        self.ui.deselect_all_tradeRoutes.clicked.connect(self.uncheck_all_tradeRoutes)
        self.ui.select_GC.currentIndexChanged.connect(self.select_GC)
        self.ui.select_faction.currentIndexChanged.connect(self.select_faction)
        self.ui.map.planetSelectedSignal.connect(self.onPlanetSelection)
        self.ui.edit_gc_properties.clicked.connect(self.show_campaign_properties)
        self.ui.main_window.setWindowTitle("EaW Galactic Conquest Editor - " + self.ui.select_GC.currentText() + " - " + self.ui.select_faction.currentText())
    def disconnect_triggers(self):
        self.ui.planet_list.itemChanged.disconnect(self.planetStatusModified)
        self.ui.tradeRoute_list.itemChanged.disconnect(self.ontradeRouteCellChanged)
        self.ui.add_unit_to_planet.clicked.disconnect(self.add_unit_to_starting_forces)
        self.ui.planetComboBox.currentIndexChanged.disconnect(self.update_starting_forces_table)
        self.ui.edit_planet_action.triggered.disconnect(self.edit_planet)
        self.ui.select_all_planets.clicked.disconnect(self.check_all_planets)
        self.ui.deselect_all_planets.clicked.disconnect(self.uncheck_all_planets)
        self.ui.select_all_tradeRoutes.clicked.disconnect(self.check_all_tradeRoutes)
        self.ui.deselect_all_tradeRoutes.clicked.disconnect(self.uncheck_all_tradeRoutes)
        self.ui.select_GC.currentIndexChanged.disconnect(self.select_GC)
        self.ui.select_faction.currentIndexChanged.disconnect(self.select_faction)
        self.ui.map.planetSelectedSignal.disconnect(self.onPlanetSelection)

        self.ui.edit_gc_properties.clicked.disconnect(self.show_campaign_properties)
    def update_tabs(self):
        for planet in self.repository.planets:
            rowCount = self.ui.planet_list.rowCount()
            self.ui.planet_list.setRowCount(rowCount + 1)
            item= QTableWidgetItem(planet.name)
            item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            item.setCheckState(QtCore.Qt.Unchecked)
            self.ui.planet_list.setItem(rowCount, 0, item)
            planet.reset_starting_forces_table(self.repository.campaigns)
        for route in self.repository.trade_routes:
            rowCount = self.ui.tradeRoute_list.rowCount()
            self.ui.tradeRoute_list.setRowCount(rowCount + 1)
            item= QTableWidgetItem(route.name)
            item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            item.setCheckState(QtCore.Qt.Unchecked)
            self.ui.tradeRoute_list.setItem(rowCount, 0, item)
        for name, campaignset in self.repository.campaign_sets.items():
            self.ui.select_GC.addItem(name)

        campaignset = self.repository.campaign_sets[self.ui.select_GC.currentText()]
        self.selected_set = campaignset
        for faction, campaign in campaignset.playableFactions.items():
            self.ui.select_faction.addItem(campaign.activeFaction)

        campaign = campaignset.getactivecampaign(self.ui.select_faction.currentText())
        self.selected_campaign = campaign
        self.ui.map.plotGalaxy(campaign.planets, campaign.trade_routes, self.repository.planets)

        self.connect_triggers()
        self.update_selected_planets()
        self.update_seleceted_trade_routes()
        self.update_planets_box()
        self.update_starting_forces_table()
        
    def select_GC(self):
        index = self.ui.select_GC.currentText()
        campaignset = self.repository.campaign_sets[index]
        self.selected_set = campaignset
        self.disconnect_triggers()
        self.ui.select_faction.clear()
        for faction, campaign in campaignset.playableFactions.items():
            self.ui.select_faction.addItem(campaign.activeFaction)
        self.connect_triggers()
        campaign = campaignset.getactivecampaign(self.ui.select_faction.currentText())
        self.selected_campaign = campaign
        self.update_selected_planets()
        self.update_seleceted_trade_routes()
        self.update_planets_box()
        self.update_starting_forces_table()

        self.ui.map.plotGalaxy(campaign.planets, campaign.trade_routes, self.repository.planets)
    def select_faction(self):
        index = self.ui.select_faction.currentText()
        self.ui.main_window.setWindowTitle("EaW Galactic Conquest Editor - "+ self.ui.select_GC.currentText() + " - " + index)
        campaign = self.selected_set.getactivecampaign(self.ui.select_faction.currentText())
        self.selected_campaign = campaign
        self.update_selected_planets()
        self.update_seleceted_trade_routes()
        self.update_planets_box()
        self.update_starting_forces_table()
        self.ui.map.plotGalaxy(campaign.planets, campaign.trade_routes, self.repository.planets)
    def update_seleceted_trade_routes(self):
        self.ui.tradeRoute_list.itemChanged.disconnect(self.ontradeRouteCellChanged)
        rowCount = self.ui.tradeRoute_list.rowCount()

        for row in range(rowCount):
            self.ui.tradeRoute_list.item(row, 0).setCheckState(QtCore.Qt.Unchecked)
            
        selectedPlanets = []
        traderoutes = self.selected_campaign.trade_routes
        for p in traderoutes:
            selectedPlanets.append([x.name for x in self.repository.trade_routes].index(p.name))
        for p in selectedPlanets:
            item = self.ui.tradeRoute_list.item(p, 0)
            currentState = item.checkState()
            if currentState == QtCore.Qt.Unchecked:
                item.setCheckState(QtCore.Qt.Checked)
        self.ui.tradeRoute_list.itemChanged.connect(self.ontradeRouteCellChanged)
    def update_selected_planets(self):
        self.ui.planet_list.itemChanged.disconnect(self.planetStatusModified)
        rowCount = self.ui.planet_list.rowCount()
        for row in range(rowCount):
            self.ui.planet_list.item(row, 0).setCheckState(QtCore.Qt.Unchecked)
        selectedPlanets = []

        planets = self.selected_campaign.planets
        for p in planets:
            selectedPlanets.append([x.name for x in self.repository.planets].index(p.name))
        for p in selectedPlanets:
            item = self.ui.planet_list.item(p, 0)
            currentState = item.checkState()
            if currentState == QtCore.Qt.Unchecked:
                item.setCheckState(QtCore.Qt.Checked)
        self.update_planets_box()
        self.ui.planet_list.itemChanged.connect(self.planetStatusModified)
    def update_starting_forces_table(self):
        self.ui.forcesListWidget.clear()
        self.ui.forcesListWidget.setRowCount(0)
        self.ui.forcesListWidget.setHorizontalHeaderLabels(["Unit", "Power", "Owner", "Tech"])

        planet_name = self.ui.planetComboBox.currentText()
        planet_index = None
        if planet_name in [x.name for x in self.repository.planets]:
            planet_index = [x.name for x in self.repository.planets].index(planet_name)
        
        if planet_index == None:
            print(planet_name)
            self.logFile.write(f'\n Error During Planet Indexing [Line 157 UI_Manager.py] planet {planet_name} failed to index')
            return
        planet = self.repository.planets[planet_index]
        starting_forces = planet.starting_forces[self.selected_campaign.name]

        for tech, obj in zip(list(range(1,len(starting_forces)+1)), starting_forces):
            rowCount = self.ui.forcesListWidget.rowCount()
            self.ui.forcesListWidget.setRowCount(rowCount + 1)
            item= QTableWidgetItem(obj.unit.name)
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.forcesListWidget.setItem(rowCount, 0, item)
            item= QTableWidgetItem(str(obj.unit.aicp))
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.forcesListWidget.setItem(rowCount, 1, item)
            item= QTableWidgetItem(str(tech))
            self.ui.forcesListWidget.setItem(rowCount, 3, item)
            item = QTableWidgetItem(obj.owner.name)
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.forcesListWidget.setItem(rowCount, 2, item)
        self.ui.forcesListWidget.setEditTriggers(QTableWidget.NoEditTriggers)
    def update_planets_box(self):
        self.ui.planetComboBox.currentIndexChanged.disconnect(self.update_starting_forces_table)
        index = self.ui.planetComboBox.currentText()
        self.ui.planetComboBox.clear()
        for p in self.selected_campaign.planets:
            self.ui.planetComboBox.addItem(p.name)
        if index in [x.name for x in self.selected_campaign.planets]:
            self.ui.planetComboBox.setCurrentText(index)
        self.ui.planetComboBox.currentIndexChanged.connect(self.update_starting_forces_table)
    def planetStatusModified(self, item):
        planet = self.repository.planets[item.row()]
        campaign = self.selected_campaign
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
        self.update_planets_box()
        self.ui.map.plotGalaxy(campaign.planets, campaign.trade_routes, self.repository.planets)
    def ontradeRouteCellChanged(self, item):
        tradeRoute = self.repository.trade_routes[item.row()]
        campaign = self.selected_campaign
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
        self.ui.map.plotGalaxy(campaign.planets, campaign.trade_routes, self.repository.planets)


    def onPlanetSelection(self, table):
        planet = self.repository.planets[table[0]]
        item = self.ui.planet_list.item(table[0], 0)
        campaign = self.selected_campaign
        if not planet in campaign.planets:
            addingPlanet = True
            campaign.planets.append(planet)
        else:
            campaign.planets.remove(planet)
            addingPlanet = False
        self.ui.map.plotGalaxy(campaign.planets, campaign.trade_routes, self.repository.planets)
        self.update_selected_planets()

    def add_unit_to_starting_forces(self):
        self.addUnitWindow = AddUnitWindow(self.ui.planetComboBox.currentText())
        self.addUnitWindow.OkCancelButtons.accepted.connect(self.complete_unit_adding)
        self.addUnitWindow.update_unit_box(self.repository.units)
        for faction in self.repository.factions:
            self.addUnitWindow.OwnerDropdown.addItem(faction.name)
        self.addUnitWindow.show()
    def complete_unit_adding(self):
        planet_name = self.addUnitWindow.planet
        techLevel = self.addUnitWindow.TechLevel.value()
        quantity = self.addUnitWindow.Quantity.value()
        unit_name = self.addUnitWindow.UnitTypeSelection.currentText()
        owner_name = self.addUnitWindow.OwnerDropdown.currentText()
        if unit_name in [x.name for x in self.repository.units]:
            unit_index = [x.name for x in self.repository.units].index(unit_name)
        if planet_name in [x.name for x in self.repository.planets]:
            planet_index = [x.name for x in self.repository.planets].index(planet_name)
        if owner_name in [x.name for x in self.repository.factions]:
            owner_index = [x.name for x in self.repository.factions].index(owner_name)
        unit = self.repository.units[unit_index]
        owner = self.repository.factions[owner_index]
        planet = self.repository.planets[planet_index]
        forces = planet.starting_forces[self.selected_campaign.name]
        forces.append(StartingForcesObject(planet, unit, techLevel, owner, quantity))
        self.addUnitWindow.OkCancelButtons.accepted.disconnect(self.complete_unit_adding)


        rowCount = self.ui.forcesListWidget.rowCount()
        self.ui.forcesListWidget.setRowCount(rowCount + 1)
        item= QTableWidgetItem(unit.name)
        self.ui.forcesListWidget.setItem(rowCount, 0, item)
        item= QTableWidgetItem(str(unit.aicp))
        self.ui.forcesListWidget.setItem(rowCount, 1, item)
        item= QTableWidgetItem(str(techLevel))
        self.ui.forcesListWidget.setItem(rowCount, 3, item)
        item = QTableWidgetItem(owner.name)
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.ui.forcesListWidget.setItem(rowCount, 2, item)
        self.addUnitWindow.dialogWindow.accept()
    def edit_planet(self):
        editWindow = PlanetWindow(self.repository.planets, self.repository.text_dict)
        for planet in self.repository.planets:
            editWindow.planetSelection.addItem(planet.name)
        editWindow.show()

    #Check Uncheck all planets/traderoutes, is associated with layout tab
    def check_all_planets(self):
        self.ui.planet_list.itemChanged.disconnect(self.planetStatusModified)
        rowCount = self.ui.planet_list.rowCount()
        for i in range(rowCount):
            self.ui.planet_list.item(i,0).setCheckState(QtCore.Qt.Checked)
        campaign = self.selected_campaign
        campaign.planets = self.repository.planets
        self.ui.planet_list.itemChanged.connect(self.planetStatusModified)
        self.ui.map.plotGalaxy(campaign.planets, campaign.trade_routes, self.repository.planets)
    def uncheck_all_planets(self):
        self.ui.planet_list.itemChanged.disconnect(self.planetStatusModified)
        rowCount = self.ui.planet_list.rowCount()
        for i in range(rowCount):
            self.ui.planet_list.item(i,0).setCheckState(QtCore.Qt.Unchecked)
        campaign = self.selected_campaign
        campaign.planets = []
        self.ui.planet_list.itemChanged.connect(self.planetStatusModified)
        self.ui.map.plotGalaxy(campaign.planets, campaign.trade_routes, self.repository.planets)
    def check_all_tradeRoutes(self):
        self.ui.tradeRoute_list.itemChanged.disconnect(self.ontradeRouteCellChanged)
        rowCount = self.ui.tradeRoute_list.rowCount()
        for i in range(rowCount):
            self.ui.tradeRoute_list.item(i,0).setCheckState(QtCore.Qt.Checked)
        campaign = self.selected_campaign
        campaign.trade_routes = self.repository.trade_routes

        self.ui.tradeRoute_list.itemChanged.connect(self.ontradeRouteCellChanged)
        self.ui.map.plotGalaxy(campaign.planets, campaign.trade_routes, self.repository.planets)
    def uncheck_all_tradeRoutes(self):
        self.ui.tradeRoute_list.itemChanged.disconnect(self.ontradeRouteCellChanged)
        rowCount = self.ui.tradeRoute_list.rowCount()
        for i in range(rowCount):
            self.ui.tradeRoute_list.item(i,0).setCheckState(QtCore.Qt.Unchecked)
        campaign = self.selected_campaign
        campaign.trade_routes = []
        self.ui.tradeRoute_list.itemChanged.connect(self.ontradeRouteCellChanged)
        self.ui.map.plotGalaxy(campaign.planets, campaign.trade_routes, self.repository.planets)
    def show_campaign_properties(self):
        campaign = self.selected_campaign
        window = CampaignPropertiesWindow(campaign)
        