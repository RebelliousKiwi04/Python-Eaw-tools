from ui.AddUnitWindow import AddUnitWindow, EditUnitWindow
from ui.CampaignProperties import CampaignPropertiesWindow
from ui.addFactionWindow import AddFactionWindow
from ui.NewSetWindow import CreateNewGCWindow
from ui.TradeRouteWindows import CreateTradeRouteWindow
from gameObject.GameObjectRepository import ModRepository
from gameObject.campaignset import CampaignSet
import os, sys, lxml.etree as et, copy
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
import gc


print(sys.getrecursionlimit())

class InterfaceHandler:
    def __init__(self, ui, mod_dir,logfile):
        self.ui = ui
        self.mod_dir = mod_dir
        self.repository = ModRepository(mod_dir,logfile)
        self.selected_set = None
        self.selected_campaign = None
    def connect_triggers(self):
        self.repository.logfile.write(f'Connecting Button Triggers\n')
        self.ui.planet_list.itemChanged.connect(self.planetStatusModified)
        self.ui.tradeRoute_list.itemChanged.connect(self.ontradeRouteCellChanged)
        self.ui.tradeRouteSearch.returnPressed.connect(self.searchTradeRoutes)
        self.ui.add_unit_to_planet.clicked.connect(self.add_unit_to_starting_forces)
        self.ui.planetComboBox.currentIndexChanged.connect(self.update_starting_forces_table)
        self.ui.select_all_planets.clicked.connect(self.check_all_planets)
        self.ui.deselect_all_planets.clicked.connect(self.uncheck_all_planets)
        self.ui.select_all_tradeRoutes.clicked.connect(self.check_all_tradeRoutes)
        self.ui.modify_entry.clicked.connect(self.delete_starting_forces_entry)
        self.ui.add_faction.clicked.connect(self.addFactionToCampaign)
        self.ui.newTradeRouteAction.triggered.connect(self.create_new_traderoutes)
        self.ui.saveAction.triggered.connect(self.repository.save_to_file)
        self.ui.planetsSearch.returnPressed.connect(self.searchPlanets)
        self.ui.deselect_all_tradeRoutes.clicked.connect(self.uncheck_all_tradeRoutes)
        self.ui.select_GC.currentIndexChanged.connect(self.select_GC)
        self.ui.newCampaignAction.triggered.connect(self.create_new_set)
        self.ui.select_faction.currentIndexChanged.connect(self.select_faction)
        self.ui.map.planetSelectedSignal.connect(self.onPlanetSelection)
        self.ui.edit_gc_properties.clicked.connect(self.show_campaign_properties)
        self.ui.main_window.setWindowTitle("EaW Galactic Conquest Editor - " + self.ui.select_GC.currentText() + " - " + self.ui.select_faction.currentText())
    def disconnect_triggers(self):
        self.repository.logfile.write(f'Disonnecting Button Triggers\n')
        self.ui.planet_list.itemChanged.disconnect(self.planetStatusModified)
        self.ui.tradeRouteSearch.returnPressed.disconnect(self.searchTradeRoutes)
        self.ui.planetsSearch.returnPressed.connect(self.searchPlanets)
        self.ui.tradeRoute_list.itemChanged.disconnect(self.ontradeRouteCellChanged)
        self.ui.add_unit_to_planet.clicked.disconnect(self.add_unit_to_starting_forces)
        self.ui.planetComboBox.currentIndexChanged.disconnect(self.update_starting_forces_table)
        self.ui.select_all_planets.clicked.disconnect(self.check_all_planets)
        self.ui.add_faction.clicked.disconnect(self.addFactionToCampaign)
        self.ui.newCampaignAction.triggered.disconnect(self.create_new_set)
        self.ui.newTradeRouteAction.triggered.disconnect(self.create_new_traderoutes)
        self.ui.saveAction.triggered.disconnect(self.repository.save_to_file)
        self.ui.deselect_all_planets.clicked.disconnect(self.uncheck_all_planets)
        self.ui.select_all_tradeRoutes.clicked.disconnect(self.check_all_tradeRoutes)
        self.ui.modify_entry.clicked.disconnect(self.delete_starting_forces_entry)
        self.ui.deselect_all_tradeRoutes.clicked.disconnect(self.uncheck_all_tradeRoutes)
        self.ui.select_GC.currentIndexChanged.disconnect(self.select_GC)
        self.ui.select_faction.currentIndexChanged.disconnect(self.select_faction)
        self.ui.map.planetSelectedSignal.disconnect(self.onPlanetSelection)

        self.ui.edit_gc_properties.clicked.disconnect(self.show_campaign_properties)
    def clear_data(self):
        self.repository.logfile.write(f'Resetting UI\n')
        self.disconnect_triggers()
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
    def update_tabs(self):
        self.repository.logfile.write(f'Updating UI Elements\n')
        for planet in self.repository.planets:
            rowCount = self.ui.planet_list.rowCount()
            self.ui.planet_list.setRowCount(rowCount + 1)
            item= QTableWidgetItem(planet.name)
            item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            item.setCheckState(QtCore.Qt.Unchecked)
            self.ui.planet_list.setItem(rowCount, 0, item)
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
        self.ui.map.plotGalaxy(campaign.planets, campaign.trade_routes, self.repository.planets, self.selected_campaign, self.repository)

        self.connect_triggers()
        self.update_selected_planets()
        self.update_seleceted_trade_routes()
        self.update_planets_box()
        self.update_starting_forces_table()
        
    def select_GC(self):
        self.repository.logfile.write(f'New GC Set With Name {self.ui.select_GC.currentText()} Selected\n')
        index = self.ui.select_GC.currentText()
        campaignset = self.repository.campaign_sets[index]
        self.selected_set = campaignset
        self.disconnect_triggers()
        self.ui.select_faction.clear()

        self.repository.logfile.write(f'Adding Playable Factions For Set To Combobox\n')
        for faction, campaign in campaignset.playableFactions.items():
            self.ui.select_faction.addItem(campaign.activeFaction)
        self.connect_triggers()
        campaign = campaignset.getactivecampaign(self.ui.select_faction.currentText())
        self.selected_campaign = campaign
        self.update_selected_planets()
        self.update_seleceted_trade_routes()
        self.update_planets_box()
        self.update_starting_forces_table()
        self.repository.logfile.write(f'Plotting Galactic Map...\n')
        self.ui.map.plotGalaxy(campaign.planets, campaign.trade_routes, self.repository.planets,self.selected_campaign, self.repository)
    def select_faction(self):
        self.repository.logfile.write(f'Playable Faction {self.ui.select_faction.currentText()} selected for set {self.ui.select_GC.currentText()}\n')
        index = self.ui.select_faction.currentText()
        self.ui.main_window.setWindowTitle("EaW Galactic Conquest Editor - "+ self.ui.select_GC.currentText() + " - " + index)
        campaign = self.selected_set.getactivecampaign(self.ui.select_faction.currentText())
        self.selected_campaign = campaign
        self.update_selected_planets()
        self.update_seleceted_trade_routes()
        self.update_planets_box()
        self.update_starting_forces_table()
        self.repository.logfile.write(f'Plotting Galactic Map...\n')
        self.ui.map.plotGalaxy(campaign.planets, campaign.trade_routes, self.repository.planets,self.selected_campaign, self.repository)
    def update_seleceted_trade_routes(self):
        self.repository.logfile.write(f'Updating Selected Trade Routes For GC {self.selected_campaign.name}\n')
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
            if item != None:
                currentState = item.checkState()
                if currentState == QtCore.Qt.Unchecked:
                    item.setCheckState(QtCore.Qt.Checked)
        self.ui.tradeRoute_list.itemChanged.connect(self.ontradeRouteCellChanged)
    def update_selected_planets(self):
        self.repository.logfile.write(f'Updating Selected Planets For GC {self.selected_campaign.name}\n')
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
            if item != None:
                currentState = item.checkState()
                if currentState == QtCore.Qt.Unchecked:
                    item.setCheckState(QtCore.Qt.Checked)
        self.update_planets_box()
        self.ui.planet_list.itemChanged.connect(self.planetStatusModified)
    def update_starting_forces_table(self):
        self.repository.logfile.write(f'Updating Starting Forces Table For GC {self.selected_campaign.name}\n')
        self.ui.forcesListWidget.clear()
        self.ui.forcesListWidget.setRowCount(0)
        self.ui.forcesListWidget.setHorizontalHeaderLabels(["Unit", "Owner", "Quantity"])

        planet_name = self.ui.planetComboBox.currentText()
        planet_index = None
        if planet_name in [x.name for x in self.repository.planets]:
            planet_index = [x.name for x in self.repository.planets].index(planet_name)
        
        if planet_index == None:
            self.repository.logfile.write(f'\n Error During Planet Indexing planet {planet_name} failed to index when updating starting forces\n')
            return
        planet = self.repository.planets[planet_index]
        starting_forces = self.selected_campaign.starting_forces[planet]

        for obj in starting_forces:
            rowCount = self.ui.forcesListWidget.rowCount()
            self.ui.forcesListWidget.setRowCount(rowCount + 1)
            item= QTableWidgetItem(obj.unit)
            self.ui.forcesListWidget.setItem(rowCount, 0, item)
            item= QTableWidgetItem(str(obj.owner))
            self.ui.forcesListWidget.setItem(rowCount, 1, item)
            item = QTableWidgetItem(str(obj.quantity))
            self.ui.forcesListWidget.setItem(rowCount, 2, item)
        self.ui.forcesListWidget.setEditTriggers(QTableWidget.NoEditTriggers)
    def update_planets_box(self):
        self.ui.planetComboBox.currentIndexChanged.disconnect(self.update_starting_forces_table)
        index = self.ui.planetComboBox.currentText()
        self.ui.planetComboBox.clear()
        for p in self.selected_campaign.planets:
            self.ui.planetComboBox.addItem(p.name)
        # if index in [x.name for x in self.selected_campaign.planets]:
        #     self.ui.planetComboBox.setCurrentText(index)
        self.ui.planetComboBox.currentIndexChanged.connect(self.update_starting_forces_table)
    def planetStatusModified(self, item):
        print(item.text())
        index = [x.name for x in self.repository.planets].index(item.text())
        planet = self.repository.planets[index]
        campaign = self.selected_campaign
        if not planet in campaign.planets:
            campaign.planets.append(planet)
        else:
            campaign.planets.remove(planet)
        self.update_planets_box()
        self.ui.map.plotGalaxy(campaign.planets, campaign.trade_routes, self.repository.planets,self.selected_campaign, self.repository)
    def ontradeRouteCellChanged(self, item):
        print(item.text())
        index = [x.name for x in self.repository.trade_routes].index(item.text())
        tradeRoute = self.repository.trade_routes[index]
        campaign = self.selected_campaign
        if not tradeRoute in campaign.trade_routes:
            campaign.trade_routes.append(tradeRoute)
        else:
            campaign.trade_routes.remove(tradeRoute)

        self.ui.map.plotGalaxy(campaign.planets, campaign.trade_routes, self.repository.planets,self.selected_campaign, self.repository)


    def onPlanetSelection(self, table):
        planet = self.repository.planets[table[0]]
        self.repository.logfile.write(f'Planet {planet.name} Selected On Galactic Plot\n')
        print(self.ui.tabWidget.currentIndex())
        if self.ui.tabWidget.currentIndex() == 1:
            self.ui.planetComboBox.setCurrentText(planet.name)
        else:
            item = self.ui.planet_list.item(table[0], 0)
            campaign = self.selected_campaign
            if not planet in campaign.planets:
                addingPlanet = True
                campaign.planets.append(planet)
            else:
                campaign.planets.remove(planet)
                addingPlanet = False
            self.ui.map.plotGalaxy(campaign.planets, campaign.trade_routes, self.repository.planets,self.selected_campaign, self.repository)
            self.update_selected_planets()

    def add_unit_to_starting_forces(self):
        self.addUnitWindow = AddUnitWindow(self.ui.planetComboBox.currentText())
        self.addUnitWindow.add.clicked.connect(self.complete_unit_adding)
        self.addUnitWindow.addtoall.clicked.connect(self.add_to_all)
        self.addUnitWindow.update_unit_box(self.repository.units)
        for faction in self.repository.factions:
            self.addUnitWindow.OwnerDropdown.addItem(faction.name)
        self.addUnitWindow.show()
    def add_to_all(self):
        self.repository.logfile.write(f'Adding Unit To Starting Forces On All Planets\n')
        quantity = self.addUnitWindow.Quantity.value()
        unit_name = self.addUnitWindow.UnitTypeSelection.currentText()
        owner_name = self.addUnitWindow.OwnerDropdown.currentText()
        if unit_name in [x.name for x in self.repository.units]:
            unit_index = [x.name for x in self.repository.units].index(unit_name)
        if owner_name in [x.name for x in self.repository.factions]:
            owner_index = [x.name for x in self.repository.factions].index(owner_name)
        unit = self.repository.units[unit_index]
        owner = self.repository.factions[owner_index]
        forces = self.selected_campaign.starting_forces
        for i in self.selected_campaign.planets:
            forces.addItem(i.name, unit.name, owner.name, quantity)


        rowCount = self.ui.forcesListWidget.rowCount()
        self.ui.forcesListWidget.setRowCount(rowCount + 1)
        item= QTableWidgetItem(unit.name)
        self.ui.forcesListWidget.setItem(rowCount, 0, item)
        item= QTableWidgetItem(str(owner.name))
        self.ui.forcesListWidget.setItem(rowCount, 1, item)
        item = QTableWidgetItem(str(quantity))
        self.ui.forcesListWidget.setItem(rowCount, 2, item)
        self.addUnitWindow.dialogWindow.accept()
        self.ui.map.plotGalaxy(self.selected_campaign.planets, self.selected_campaign.trade_routes, self.repository.planets,self.selected_campaign, self.repository)
    def complete_unit_adding(self):
        planet_name = self.addUnitWindow.planet
        self.repository.logfile.write(f'Adding Unit To Starting Forces At Planet {planet_name}\n')
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
        forces = self.selected_campaign.starting_forces
        forces.addItem(self.repository.planets[planet_index].name, unit.name, owner.name, quantity)


        rowCount = self.ui.forcesListWidget.rowCount()
        self.ui.forcesListWidget.setRowCount(rowCount + 1)
        item= QTableWidgetItem(unit.name)
        self.ui.forcesListWidget.setItem(rowCount, 0, item)
        item= QTableWidgetItem(str(owner.name))
        self.ui.forcesListWidget.setItem(rowCount, 1, item)
        item = QTableWidgetItem(str(quantity))
        self.ui.forcesListWidget.setItem(rowCount, 2, item)
        self.addUnitWindow.dialogWindow.accept()
        self.ui.map.plotGalaxy(self.selected_campaign.planets, self.selected_campaign.trade_routes, self.repository.planets,self.selected_campaign, self.repository)
    #Check Uncheck all planets/traderoutes, is associated with layout tab
    def check_all_planets(self):
        self.ui.planet_list.itemChanged.disconnect(self.planetStatusModified)
        rowCount = self.ui.planet_list.rowCount()
        for i in range(rowCount):
            self.ui.planet_list.item(i,0).setCheckState(QtCore.Qt.Checked)
        campaign = self.selected_campaign
        campaign.planets = self.repository.planets
        self.ui.planet_list.itemChanged.connect(self.planetStatusModified)
        self.ui.map.plotGalaxy(campaign.planets, campaign.trade_routes, self.repository.planets,self.selected_campaign, self.repository)
    def uncheck_all_planets(self):
        self.ui.planet_list.itemChanged.disconnect(self.planetStatusModified)
        rowCount = self.ui.planet_list.rowCount()
        for i in range(rowCount):
            self.ui.planet_list.item(i,0).setCheckState(QtCore.Qt.Unchecked)
        self.selected_campaign.planets = []
        self.ui.planet_list.itemChanged.connect(self.planetStatusModified)
        self.ui.map.plotGalaxy(self.selected_campaign.planets, self.selected_campaign.trade_routes, self.repository.planets,self.selected_campaign, self.repository)
    def check_all_tradeRoutes(self):
        self.ui.tradeRoute_list.itemChanged.disconnect(self.ontradeRouteCellChanged)
        rowCount = self.ui.tradeRoute_list.rowCount()
        for i in range(rowCount):
            self.ui.tradeRoute_list.item(i,0).setCheckState(QtCore.Qt.Checked)
        self.selected_campaign.trade_routes = self.repository.trade_routes

        self.ui.tradeRoute_list.itemChanged.connect(self.ontradeRouteCellChanged)
        self.ui.map.plotGalaxy(self.selected_campaign.planets, self.selected_campaign.trade_routes, self.repository.planets,self.selected_campaign, self.repository)
    def uncheck_all_tradeRoutes(self):
        self.ui.tradeRoute_list.itemChanged.disconnect(self.ontradeRouteCellChanged)
        rowCount = self.ui.tradeRoute_list.rowCount()
        for i in range(rowCount):
            self.ui.tradeRoute_list.item(i,0).setCheckState(QtCore.Qt.Unchecked)
        self.selected_campaign.trade_routes = []
        self.ui.tradeRoute_list.itemChanged.connect(self.ontradeRouteCellChanged)
        self.ui.map.plotGalaxy(self.selected_campaign.planets, self.selected_campaign.trade_routes, self.repository.planets,self.selected_campaign, self.repository)
    def show_campaign_properties(self):
        window = CampaignPropertiesWindow(self.selected_set, self.selected_campaign, self.repository)
        i = window.dialogWindow.exec_()
        del window
    def addFactionToCampaign(self):
        test = AddFactionWindow(self.selected_set, self.repository)
        i = test.dialogWindow.exec_()
        if i ==1:
            self.repository.logfile.write(f'Adding Faction {test.faction.currentText()} To Campaign Set\n')
            new = self.selected_set.addFaction(test.faction.currentText())
            self.repository.campaigns[new.name] = new

            self.select_GC()
        del test
    def delete_starting_forces_entry(self):
        row = self.ui.forcesListWidget.currentRow()
        if row < 0:
            return
      
        obj = self.selected_campaign.starting_forces[self.ui.planetComboBox.currentText()][row]

        window = EditUnitWindow(obj,self.selected_campaign,self.repository)
        window.dialogWindow.exec_()
        self.update_starting_forces_table()
        self.ui.map.plotGalaxy(self.selected_campaign.planets, self.selected_campaign.trade_routes, self.repository.planets,self.selected_campaign, self.repository)
    def create_new_set(self):
        gcwindow = CreateNewGCWindow(self.repository)
        if gcwindow.dialogWindow.exec_() == 1:
            if os.path.isdir('xml'):
                xmlPath = '\\xml\\'
            else:
                xmlPath = '\\XML\\'
            self.repository.logfile.write(f'Creating new GC Set With Name {gcwindow.location.text()}\n')
            self.repository.campaign_files.append(self.mod_dir+xmlPath+gcwindow.location.text())

            setname = gcwindow.setname.text()

            template = copy.deepcopy(self.repository.campaigns[gcwindow.template.currentText()])
            #template.copy(self.repository.campaigns[gcwindow.template.currentText()])
            template.activeFaction = gcwindow.faction.currentText()
            template.name = setname+'_'+gcwindow.faction.currentText()
            template.text_name = 'TEXT_CONQUEST_'+template.name.upper()
            template.desc_name = 'TEXT_DESC_CONQUEST_'+template.name.upper()

            template.fileLocation = self.mod_dir+xmlPath+gcwindow.location.text()

            self.repository.campaigns[template.name] = template
            campaignset = CampaignSet(setname)
            campaignset.addCampaign(template)
            self.repository.campaign_sets[setname] = campaignset
            self.ui.select_GC.addItem(setname) 
        del gcwindow
    def create_new_traderoutes(self):
        window = CreateTradeRouteWindow(self.repository, self.selected_campaign)
        if window.show() == 1:
            newRoute = copy.deepcopy(self.repository.trade_routes[0])
            newRoute.name = window.selected_planets[0].name+'_'+window.selected_planets[1].name
            self.repository.logfile.write(f'Creating new Trade Route With Name {newRoute.name}\n')
            newRoute.point_A = window.selected_planets[0].name.lower()
            newRoute.point_B = window.selected_planets[1].name.lower()
            newRoute.points = []
            newRoute.set_point_planets(self.repository.planets)
            if newRoute.name not in [x.name for x in self.repository.trade_routes]:
                self.ui.tradeRoute_list.itemChanged.disconnect(self.ontradeRouteCellChanged)
                self.repository.trade_routes.append(newRoute)

                rowCount = self.ui.tradeRoute_list.rowCount()
                self.ui.tradeRoute_list.setRowCount(rowCount + 1)
                item= QTableWidgetItem(newRoute.name)
                item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                item.setCheckState(QtCore.Qt.Unchecked)
                self.ui.tradeRoute_list.setItem(rowCount, 0, item)
                self.ui.tradeRoute_list.itemChanged.connect(self.ontradeRouteCellChanged)
        del window
    def searchPlanets(self):
        self.ui.planet_list.itemChanged.disconnect(self.planetStatusModified)
        self.ui.planet_list.clear()
        self.ui.planet_list.setHorizontalHeaderLabels(['Planets'])
        self.ui.planet_list.setRowCount(0)
        gc.collect()
        searchString = self.ui.planetsSearch.text()
        if searchString.isspace():
            pass
        self.ui.planet_list.clear()
        self.ui.planet_list.setHorizontalHeaderLabels(['Planets'])
        self.ui.planet_list.setRowCount(0)
        planetNames = [x.name for x in self.repository.planets]
        campaignPlanets = [x.name for x in self.selected_campaign.planets]
        for i in planetNames:
            if searchString.lower() in i.lower():
                rowCount = self.ui.planet_list.rowCount()
                self.ui.planet_list.setRowCount(rowCount + 1)
                item= QTableWidgetItem(i)
                item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                
                self.ui.planet_list.setItem(rowCount, 0, item)
                if i in campaignPlanets:
                    item.setCheckState(QtCore.Qt.Checked)
                else:
                    item.setCheckState(QtCore.Qt.Unchecked)
        self.ui.planet_list.itemChanged.connect(self.planetStatusModified)
    def searchTradeRoutes(self):
        self.ui.tradeRoute_list.itemChanged.disconnect(self.ontradeRouteCellChanged)
        self.ui.tradeRoute_list.clear()
        self.ui.tradeRoute_list.setHorizontalHeaderLabels(['Trade Routes'])
        self.ui.tradeRoute_list.setRowCount(0)
        gc.collect()
        searchString = self.ui.tradeRouteSearch.text()
        if searchString.isspace():
            pass
        planetNames = [x.name for x in self.repository.trade_routes]
        campaignPlanets = [x.name for x in self.selected_campaign.trade_routes]
        for i in planetNames:
            if searchString.lower() in i.lower():
                rowCount = self.ui.tradeRoute_list.rowCount()
                self.ui.tradeRoute_list.setRowCount(rowCount + 1)
                item= QTableWidgetItem(i)
                item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                
                self.ui.tradeRoute_list.setItem(rowCount, 0, item)
                if i in campaignPlanets:
                    item.setCheckState(QtCore.Qt.Checked)
                else:
                    item.setCheckState(QtCore.Qt.Unchecked)
        self.ui.tradeRoute_list.itemChanged.connect(self.ontradeRouteCellChanged)