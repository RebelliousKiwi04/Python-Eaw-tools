import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from ui.Utilities import PyQtUtil
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Axes, Figure
from ui.DraggablePoint import DraggablePoint


class GalacticMap(QWidget):
    planetSelectedSignal = QtCore.pyqtSignal(list)

    def __init__(self, parent = None):
        super(GalacticMap, self).__init__()
        self.mapWidget: QWidget = QWidget(parent)
        self.mapWidget.setLayout(QVBoxLayout())
        
        self.mapCanvas: FigureCanvas = FigureCanvas(Figure())
        self.mapCanvas.mpl_connect('pick_event', self.__planetSelect)
        self.mapCanvas.mpl_connect('motion_notify_event', self.__planetHover)
        self.navbar = NavigationToolbar(self.mapCanvas, self.mapWidget)
        self.mapWidget.layout().addWidget(self.navbar)
        self.mapWidget.layout().addWidget(self.mapCanvas)
        self.axes: Axes = self.mapCanvas.figure.add_subplot(111, aspect = "equal")
        self.axes.set_xlim(-600,700)
        self.axes.set_ylim(-600,850)
        self.axes.grid(True)
        self.__annotate = self.axes.annotate("", xy = (0,0), xytext = (10, 10), textcoords = "offset points", bbox = dict(boxstyle="round", fc="w"), arrowprops = dict(arrowstyle="->"))
        self.__annotate.set_visible(False)
        self.__planetNames = []
        self.__planetsScatter = None
        self.list_points = []
        #self.plotDraggablePoints()
        self.times = 0
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

    def updateFigure(self):

        """Update the graph. Necessary, to call after each plot"""

        self.mapCanvas.draw()
    def plotGalaxy(self, planets, tradeRoutes, allPlanets, campaign,repository,autoPlanetConnectionDistance: int = 0) -> None:
        '''Plots all planets as alpha = 0.1, then overlays all selected planets and trade routes'''
        self.axes.clear()

        #Has to be set again here for the planet hover labels to work
        self.__annotate = self.axes.annotate("", xy = (0,0), xytext = (10, 10), textcoords = "offset points", bbox = dict(boxstyle="round", fc="w"), arrowprops = dict(arrowstyle="->"))
        self.__annotate.set_visible(False)

        self.__planetNames = []

        x = []
        y = []

        for planet in allPlanets:
            #print(p.x,p.y)
            x.append(planet.x)
            y.append(planet.y)
            self.__planetNames.append(planet.name)

        self.__planetsScatter = self.axes.scatter(x, y, c = 'b', alpha = 0.1,picker = 5, zorder=2)
        x1 = 0        
        y1 = 0
        x2 = 0
        y2 = 0

        # loop through routes
        for t in tradeRoutes:
            x1 = t.points[0].x
            y1 = t.points[0].y
            x2 = t.points[1].x
            y2 = t.points[1].y
            # plot each route (start, end)            
            self.axes.plot([x1, x2], [y1, y2], 'k-', alpha=0.4, zorder=1)
        
        # #Create automatic connections between planets
        # if autoPlanetConnectionDistance > 0:
        #     for p1 in planets:
        #         for p2 in planets:
        #             if p1 == p2:
        #                 break
        #             dist: float = p1.distanceTo(p2)
        #             if dist < autoPlanetConnectionDistance:
        #                 self.axes.plot([p1.x, p2.x], [p1.y, p2.y], 'k-', alpha=0.1)



        x = []
        y = []
        color = []
        for p in planets:
            x.append(p.x)
            y.append(p.y)
            forces = campaign.starting_forces[p]
            if len(forces) > 0:
                index = [x.name for x in repository.factions].index(forces[0].owner)
                faction = repository.factions[index]
                color.append(tuple(faction.color))
            else:
                index = [x.name for x in repository.factions].index('Neutral')
                faction = repository.factions[index]
                color.append(tuple(faction.color))

        #print(color)
            #color.append(tuple(f.color))

        # for p in planets:
        #     x.append(p.x)
        #     y.append(p.y)

        self.axes.scatter(x, y, c = color,edgecolors = 'black', zorder=4)
        self.mapCanvas.draw_idle()
        self.times = self.times +1

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

        if event.inaxes == self.axes:
            contains, ind = self.__planetsScatter.contains(event)

            if contains:
                pos = self.__planetsScatter.get_offsets()[ind["ind"][0]]
                self.__annotate.xy = pos
                text = "{}".format(" ".join([self.__planetNames[n] for n in ind["ind"]]))
                self.__annotate.set_text(text)
                self.__annotate.set_visible(True)
                self.mapCanvas.draw_idle()
            else:
                if visible:
                    self.__annotate.set_visible(False)
                    self.mapCanvas.draw_idle()



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
        
        self.faction_layout = QHBoxLayout()
        self.select_faction = QComboBox()
        self.add_faction = QPushButton("Add")
        self.faction_layout.addWidget(self.select_faction)
        self.faction_layout.addWidget(self.add_faction)


        self.edit_gc_properties= QPushButton("Edit Campaign Properties")


        self.planetsSearch = QLineEdit()
        self.planetsSearch.setPlaceholderText("Search Planets...")
        self.planet_list = PyQtUtil.construct_table_widget(["Planets"])
        self.planet_list.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

        self.tradeRouteSearch = QLineEdit()
        self.tradeRouteSearch.setPlaceholderText("Search Trade Routes...")
        self.tradeRoute_list = PyQtUtil.construct_table_widget(["Trade Routes"])

        self.select_all_planets = QPushButton("Select All Planets")

        self.deselect_all_planets = QPushButton("Deselect All Planets")

        self.select_all_tradeRoutes = QPushButton("Select All Trade Routes")

        self.deselect_all_tradeRoutes = QPushButton("Deselect All Trade Routes")

        #Left pane, Forces tab
        self.planetComboBox: QComboBox = QComboBox()
        self.add_unit_to_planet= QPushButton("Add Unit...")

        font = QFont()
        font.setPointSize(10)


        self.forcesListWidget = PyQtUtil.construct_table_widget(["Unit", "Owner", "Quantity"], 3)        
        header = self.forcesListWidget.horizontalHeader()       
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        #Far Right tab
        self.scriptModeComboBox = QComboBox()

        #set up menu and menu options
        self.__menuBar: QMenuBar = QMenuBar()
        self.__optionsMenu: QMenu = QMenu("Options", self.main_window)
        self.__fileMenu: QMenu = QMenu("File", self.main_window)
        self.__addMenu: QMenu = QMenu("New", self.main_window)
        self.__editMenu: QMenu = QMenu("Edit", self.main_window)
        
        self.newCampaignAction: QAction = QAction("Galactic Conquest...", self.main_window)

        self.newTradeRouteAction: QAction = QAction("Trade Route...", self.main_window)

        self.setDataFolderAction: QAction = QAction("Set Data Folder", self.main_window)

        self.saveAction: QAction = QAction("Save", self.main_window)

        self.__quitAction: QAction = QAction("Quit", self.main_window)
        self.__quitAction.triggered.connect(sys.exit)
        
        self.editUnitAction: QAction = QAction("Units", self.main_window)
        self.editPlanetAction: QAction = QAction("Planets", self.main_window)
        
        self.__fileMenu.addAction(self.saveAction)
        self.__fileMenu.addAction(self.setDataFolderAction)
        self.__fileMenu.addAction(self.__quitAction)
        self.__addMenu.addAction(self.newCampaignAction)
        self.__addMenu.addAction(self.newTradeRouteAction)
        self.__editMenu.addAction(self.editUnitAction)
        self.__editMenu.addAction(self.editPlanetAction)
        self.__menuBar.addMenu(self.__fileMenu)
        self.__menuBar.addMenu(self.__addMenu)
        self.__menuBar.addMenu(self.__editMenu)
        #self.__menuBar.addMenu(self.__optionsMenu)
        self.main_window.setMenuWidget(self.__menuBar)

        #Set up left pane tabs
        self.tabWidget: QWidget = QTabWidget()
        self.__planetsTradeRoutes: QWidget = QWidget()
        self.__startingForces: QWidget = QWidget()
        self.scriptingTab = QWidget()

        self.tabWidget.addTab(self.__planetsTradeRoutes, "Layout")
        self.tabWidget.addTab(self.__startingForces, "Forces")
        # self.tabWidget.addTab(self.scriptingTab, 'Scripting')
        self.__planetsTradeRoutes.setLayout(QVBoxLayout())
        self.__startingForces.setLayout(QVBoxLayout())
        self.scriptingTab.setLayout(QVBoxLayout())
        self.window_splitter.addWidget(self.tabWidget)

        self.__planetsTradeRoutes.layout().addWidget(self.select_GC)
        self.__planetsTradeRoutes.layout().addLayout(self.faction_layout)
        self.__planetsTradeRoutes.layout().addWidget(self.edit_gc_properties)
        self.__planetsTradeRoutes.layout().addWidget(self.planetsSearch)
        self.__planetsTradeRoutes.layout().addWidget(self.planet_list)
        self.__planetsTradeRoutes.layout().addWidget(self.select_all_planets)
        self.__planetsTradeRoutes.layout().addWidget(self.deselect_all_planets)
        self.__planetsTradeRoutes.layout().addWidget(self.tradeRouteSearch)
        self.__planetsTradeRoutes.layout().addWidget(self.tradeRoute_list)
        self.__planetsTradeRoutes.layout().addWidget(self.select_all_tradeRoutes)
        self.__planetsTradeRoutes.layout().addWidget(self.deselect_all_tradeRoutes)

        self.scriptingTab.layout().addWidget(self.scriptModeComboBox)


        self.__startingForces.layout().addWidget(self.planetComboBox)
        self.__startingForces.layout().addWidget(self.add_unit_to_planet)
        self.__startingForces.layout().addWidget(self.forcesListWidget)
        self.modify_entry = QPushButton("Modify Selected Entry")
        self.__startingForces.layout().addWidget(self.modify_entry)
        self.map = GalacticMap(self.window_splitter)
        #plot = GalacticMap()
        self.window_splitter.addWidget(self.map.mapWidget)
        self.main_window.setWindowIcon(QIcon('eawIcon.png'))
        self.main_window.show()
    