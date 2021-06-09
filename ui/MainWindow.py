from typing import List
import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QAction, QPushButton, QCheckBox, QComboBox, QFileDialog, QHeaderView, QLabel, QMainWindow, QMenu, QMenuBar, QDialog, QSplitter, \
    QTableWidget, QTableWidgetItem, QTabWidget, QVBoxLayout, QWidget
from ui.Utilities import PyQtUtil
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Axes, Figure
from ui.DraggablePoint import DraggablePoint

class GalacticMap(QWidget):
    planetSelectedSignal = QtCore.pyqtSignal(list)

    def __init__(self, parent = None):
        super(GalacticMap, self).__init__()
        self.mapWidget: QWidget = QWidget(parent)
        self.mapWidget.setLayout(QVBoxLayout())

        self.mapCanvas: FigureCanvas = FigureCanvas(Figure())

        # self.mapCanvas.mpl_connect('pick_event', self.__planetSelect)
        # self.mapCanvas.mpl_connect('motion_notify_event', self.__planetHover)

        self.mapWidget.layout().addWidget(self.mapCanvas)
        self.__axes: Axes = self.mapCanvas.figure.add_subplot(111, aspect = "equal")
        self.__axes.set_xlim(-500,500)
        self.__axes.set_ylim(-500,500)
        self.__annotate = self.__axes.annotate("", xy = (0,0), xytext = (10, 10), textcoords = "offset points", bbox = dict(boxstyle="round", fc="w"), arrowprops = dict(arrowstyle="->"))
        self.__annotate.set_visible(False)
        self.__planetNames = []
        self.__planetsScatter = None
        self.list_points = []
        self.plotDraggablePoints()

    def plotDraggablePoints(self, size=20.05):

        """Plot and define the 2 draggable points of the baseline"""
  
        # del(self.list_points[:])
        self.list_points.append(DraggablePoint(self, 415, 221, size))
        self.list_points.append(DraggablePoint(self, 318, 321, size))
        self.list_points.append(DraggablePoint(self, 120.5, 421.5, size))
        self.list_points.append(DraggablePoint(self, 125.6, 300.5, size))
        self.list_points.append(DraggablePoint(self, 12.7, 491.5, size))
        self.list_points.append(DraggablePoint(self, 0, 0, size))
        self.updateFigure()


    def clearFigure(self):

        """Clear the graph"""

        self.axes.clear()
        self.axes.grid(True)
        del(self.list_points[:])
        self.updateFigure()


    def updateFigure(self):

        """Update the graph. Necessary, to call after each plot"""

        self.mapCanvas.draw()
    def plotGalaxy(self, planets, tradeRoutes, allPlanets, autoPlanetConnectionDistance: int = 0) -> None:
        '''Plots all planets as alpha = 0.1, then overlays all selected planets and trade routes'''
        self.mapAxis.clear()

        #Has to be set again here for the planet hover labels to work
        self.__annotate = self.mapAxis.annotate("", xy = (0,0), xytext = (10, 10), textcoords = "offset points", bbox = dict(boxstyle="round", fc="w"), arrowprops = dict(arrowstyle="->"))
        self.__annotate.set_visible(False)

        self.__planetNames = []

        x = []
        y = []

        for p in allPlanets:
            x.append(p.x)
            y.append(p.y)
            self.__planetNames.append(p.name)

        self.__planetsScatter = self.mapAxis.scatter(x, y, c = 'b', alpha = 0.1, picker = 5)

        x1 = 0        
        y1 = 0
        x2 = 0
        y2 = 0

        # loop through routes
        for t in tradeRoutes:
            x1 = t.start.x
            y1 = t.start.y
            x2 = t.end.x
            y2 = t.end.y
            # plot each route (start, end)            
            self.mapAxis.plot([x1, x2], [y1, y2], 'k-', alpha=0.4)
        
        #Create automatic connections between planets
        if autoPlanetConnectionDistance > 0:
            for p1 in planets:
                for p2 in planets:
                    if p1 == p2:
                        break
                    dist: float = p1.distanceTo(p2)
                    if dist < autoPlanetConnectionDistance:
                        self.mapAxis.plot([p1.x, p2.x], [p1.y, p2.y], 'k-', alpha=0.1)



        x = []
        y = []

        for p in planets:
            x.append(p.x)
            y.append(p.y)

        self.mapAxis.scatter(x, y, c = 'b')

        self.mapCanvas.draw_idle()


    def getWidget(self):
        '''Returns the plot widget'''
        return self.mapWidget

    def __planetSelect(self, event) -> None:
        '''Event handler for selecting a planet on the map'''
        planet_index = event.ind
        self.planetSelectedSignal.emit(list(planet_index))

    def __planetHover(self, event) -> None:
        '''Handler for hovering on a planet in the plot'''
        visible = self.__annotate.get_visible()

        if event.inaxes == self.mapAxis:
            contains, ind = self.__planetsScatter.contains(event)

            if contains:
                pos = self.__planetsScatter.get_offsets()[ind["ind"][0]]
                self.__annotate.xy = pos
                text = "{}".format(" ".join([self.__planetNames[n] for n in ind["ind"]]))
                self.__annotate.set_text(text)
                self.__annotate.set_visible(True)
                self.galacticMap.draw_idle()
            else:
                if visible:
                    self.__annotate.set_visible(False)
                    self.galacticMap.draw_idle()

class MainUIWindow:
    '''Qt based window'''
    def __init__(self):
        self.__allPlanetsChecked = False
        self.__allTradeRoutesChecked = False

        self.main_window = QMainWindow()
        self.window_splitter = QSplitter(self.main_window)
        self.main_window.setCentralWidget(self.window_splitter)
        self.main_window.setWindowTitle("EaW Mod Tool")


        self.select_GC = QComboBox()
        #self.select_GC.activated.connect(self.on_gc_selection)
        self.edit_gc_properties= QPushButton("Edit Campaign Properties")
        #self.edit_gc_properties.clicked.connect(self.edit_gc_propertiesClicked)

        self.QtUtil = PyQtUtil()

        self.planet_list = self.QtUtil.construct_table_widget(["Planets"])
       # self.planet_list.itemClicked.connect(self.__onPlanetTableWidgetItemClicked)
        self.planet_list.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        #self.planet_list.customContextMenuRequested.connect(self.__showPlanetContextMenu)

        self.tradeRoute_list = self.QtUtil.construct_table_widget(["Trade Routes"])
       # self.tradeRoute_list.itemClicked.connect(self.__onTradeRouteTableWidgetItemClicked)

        self.select_all_planets = QPushButton("Select All Planets")
        #self.select_all_planets.clicked.connect(lambda: self.__selectAllPlanetsButtonClicked(self.planet_list, True))

        self.deselect_all_planets = QPushButton("Deselect All Planets")
        #self.deselect_all_planets.clicked.connect(lambda: self.__selectAllPlanetsButtonClicked(self.planet_list, False))

        self.select_all_tradeRoutes = QPushButton("Select All Trade Routes")
        #self.select_all_tradeRoutes.clicked.connect(lambda: self.__selectAllTradeRoutesButtonClicked(self.tradeRoute_list, True))

        self.deselect_all_tradeRoutes = QPushButton("Deselect All Trade Routes")
        # self.deselect_all_tradeRoutes.clicked.connect(lambda: self.__selectAllTradeRoutesButtonClicked(self.tradeRoute_list, False))

        #Left pane, Forces tab
        self.__planetComboBox: QComboBox = QComboBox()
        self.add_unit_to_planet= QPushButton("Add Unit...")
        self.__forcesListWidget = self.QtUtil.construct_table_widget(["Unit", "Power"], 2)        


        #Far Right tab
        self.scriptModeComboBox = QComboBox()

        #set up menu and menu options
        self.__menuBar: QMenuBar = QMenuBar()
        self.__optionsMenu: QMenu = QMenu("Options", self.main_window)
        self.__fileMenu: QMenu = QMenu("File", self.main_window)
        self.__addMenu: QMenu = QMenu("New", self.main_window)
        self.__editMenu: QMenu = QMenu("Edit", self.main_window)


        self.__openAutoConnectionSettingsAction: QAction = QAction("Auto connection settings", self.main_window)
        #self.__openAutoConnectionSettingsAction.triggered.connect(self.__showAutoConnectionSettings)
        
        self.__newCampaignAction: QAction = QAction("Galactic Conquest...", self.main_window)
        #self.__newCampaignAction.triggered.connect(self.__newCampaign)

        self.__newTradeRouteAction: QAction = QAction("Trade Route...", self.main_window)
        #self.__newTradeRouteAction.triggered.connect(self.__newTradeRoute)

        self.__setDataFolderAction: QAction = QAction("Set Data Folder", self.main_window)
        #self.__setDataFolderAction.triggered.connect(self.__openFolder)

        self.__saveAction: QAction = QAction("Save", self.main_window)
        #self.__saveAction.triggered.connect(self.__saveFile)

        self.__quitAction: QAction = QAction("Quit", self.main_window)
        self.__quitAction.triggered.connect(sys.exit)
        
        self.__optionsMenu.addAction(self.__openAutoConnectionSettingsAction)
        
        self.__fileMenu.addAction(self.__saveAction)
        self.__fileMenu.addAction(self.__setDataFolderAction)
        self.__fileMenu.addAction(self.__quitAction)

        self.__addMenu.addAction(self.__newCampaignAction)
        self.__addMenu.addAction(self.__newTradeRouteAction)
        
        self.__menuBar.addMenu(self.__fileMenu)
        self.__menuBar.addMenu(self.__addMenu)
        self.__menuBar.addMenu(self.__optionsMenu)
        self.main_window.setMenuWidget(self.__menuBar)

        #Set up left pane tabs
        self.__leftTabsWidget: QWidget = QTabWidget()
        self.__planetsTradeRoutes: QWidget = QWidget()
        self.__startingForces: QWidget = QWidget()
        self.scriptingTab = QWidget()

        self.__leftTabsWidget.addTab(self.__planetsTradeRoutes, "Layout")
        self.__leftTabsWidget.addTab(self.__startingForces, "Forces")
        self.__leftTabsWidget.addTab(self.scriptingTab, 'Scripting')
        self.__planetsTradeRoutes.setLayout(QVBoxLayout())
        self.__startingForces.setLayout(QVBoxLayout())
        self.scriptingTab.setLayout(QVBoxLayout())
        self.window_splitter.addWidget(self.__leftTabsWidget)

        self.__planetsTradeRoutes.layout().addWidget(self.select_GC)
        self.__planetsTradeRoutes.layout().addWidget(self.edit_gc_properties)
        self.__planetsTradeRoutes.layout().addWidget(self.planet_list)
        self.__planetsTradeRoutes.layout().addWidget(self.select_all_planets)
        self.__planetsTradeRoutes.layout().addWidget(self.deselect_all_planets)
        self.__planetsTradeRoutes.layout().addWidget(self.tradeRoute_list)
        self.__planetsTradeRoutes.layout().addWidget(self.select_all_tradeRoutes)
        self.__planetsTradeRoutes.layout().addWidget(self.deselect_all_tradeRoutes)

        self.scriptingTab.layout().addWidget(self.scriptModeComboBox)


        self.__startingForces.layout().addWidget(self.__planetComboBox)
        self.__startingForces.layout().addWidget(self.add_unit_to_planet)
        self.__startingForces.layout().addWidget(self.__forcesListWidget)
        mapWidget = GalacticMap(self.window_splitter)
        #plot = GalacticMap()
        self.window_splitter.addWidget(mapWidget.mapWidget)
        self.main_window.show()
    