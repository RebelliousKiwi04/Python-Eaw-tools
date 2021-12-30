from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Axes, Figure
from matplotlib.patches import Ellipse
import sys

class PyQtUtil:
    def construct_table_widget(label=[], columns=1):
        '''Constructs an arbitrary table widget'''
        tableWidget: QTableWidget = QTableWidget()
        tableWidget.setColumnCount(columns)
        tableWidget.setHorizontalHeaderLabels(label)
        tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        tableWidget.verticalHeader().setVisible(False)
        return tableWidget

class MainWindow:
    def __init__(self):
        self.mainWindow = QMainWindow()

        self.splitter = QSplitter(self.mainWindow)

        self.mainWindow.setCentralWidget(self.splitter)

        self.mainWindow.setWindowTitle("EaW Galactic Conquest Editor")

        #Layout Tab

        self.select_GC = QComboBox()

        self.faction_layout = QHBoxLayout()
        self.select_faction = QComboBox()
        self.add_faction = QPushButton("Add")
        self.faction_layout.addWidget(self.select_faction)
        self.faction_layout.addWidget(self.add_faction)

        self.edit_gc_properties= QPushButton("Edit Campaign Properties")

        self.planet_list = PyQtUtil.construct_table_widget(["Planets"])

        self.planet_list.setContextMenuPolicy(Qt.CustomContextMenu)

        self.tradeRoute_list = PyQtUtil.construct_table_widget(["Trade Routes"])

        self.select_all_planets = QPushButton("Select All Planets")

        self.deselect_all_planets = QPushButton("Deselect All Planets")

        self.select_all_traderoutes = QPushButton("Select All Trade Routes")
        
        self.deselect_all_traderoutes = QPushButton("Deselect All Trade Routes")

        #Forces Tab

        self.planetComboBox = QComboBox()
        self.add_unit_to_planet = QPushButton("Add Unit...")

        font = QFont()
        font.setPointSize(10)

        self.forcesListWidget = PyQtUtil.construct_table_widget(["Unit", "Owner", "Tech", "Quantity"], 4) 
        header = self.forcesListWidget.horizontalHeader()       
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)

        #Menu Bar
        self.__menuBar = QMenuBar()
        self.__fileMenu = QMenu("File", self.mainWindow)
        self.__addMenu = QMenu("New", self.mainWindow)
        self.__editMenu = QMenu("Edit", self.mainWindow)
        self.__optionsMenu = QMenu("Options", self.mainWindow)

        self.edit_planet_action = QAction("Planet", self.mainWindow)
        
        self.__newCampaignAction: QAction = QAction("Galactic Conquest...", self.mainWindow)

        self.__newTradeRouteAction: QAction = QAction("Trade Route...", self.mainWindow)

        self.setDataFolderAction: QAction = QAction("Set Data Folder", self.mainWindow)

        self.__saveAction: QAction = QAction("Save", self.mainWindow)

        self.__quitAction: QAction = QAction("Quit", self.mainWindow)
        self.__quitAction.triggered.connect(sys.exit)

        self.__fileMenu.addAction(self.__saveAction)
        self.__fileMenu.addAction(self.setDataFolderAction)
        self.__fileMenu.addAction(self.__quitAction)
        self.__editMenu.addAction(self.edit_planet_action)
        self.__addMenu.addAction(self.__newCampaignAction)
        self.__addMenu.addAction(self.__newTradeRouteAction)
        
        self.__menuBar.addMenu(self.__fileMenu)
        self.__menuBar.addMenu(self.__addMenu)
        self.__menuBar.addMenu(self.__editMenu)
        self.__menuBar.addMenu(self.__optionsMenu)
        self.mainWindow.setMenuWidget(self.__menuBar)

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
        self.splitter.addWidget(self.__leftTabsWidget)

        self.__planetsTradeRoutes.layout().addWidget(self.select_GC)
        self.__planetsTradeRoutes.layout().addLayout(self.faction_layout)
        self.__planetsTradeRoutes.layout().addWidget(self.edit_gc_properties)
        self.__planetsTradeRoutes.layout().addWidget(self.planet_list)
        self.__planetsTradeRoutes.layout().addWidget(self.select_all_planets)
        self.__planetsTradeRoutes.layout().addWidget(self.deselect_all_planets)
        self.__planetsTradeRoutes.layout().addWidget(self.tradeRoute_list)
        self.__planetsTradeRoutes.layout().addWidget(self.select_all_traderoutes)
        self.__planetsTradeRoutes.layout().addWidget(self.deselect_all_traderoutes)

        self.__startingForces.layout().addWidget(self.planetComboBox)
        self.__startingForces.layout().addWidget(self.add_unit_to_planet)
        self.__startingForces.layout().addWidget(self.forcesListWidget)

        self.map = GalacticMap(self.splitter)

        self.splitter.addWidget(self.map)
        self.mainWindow.show()

class GalacticMap(QWidget):
    planetSelectedSignal = pyqtSignal(list)

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
        self.times = 0


    def updateFigure(self):
        self.mapCanvas.draw()
    def plotGalaxy(self, planets, tradeRoutes, allPlanets, autoPlanetConnectionDistance: int = 0) -> None:
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

        self.__planetsScatter = self.axes.scatter(x, y, c = 'b', alpha = 0.1,picker = 5)
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
            self.axes.plot([x1, x2], [y1, y2], 'k-', alpha=0.4)

        x = []
        y = []
        for p in planets:
            x.append(p.x)
            y.append(p.y)

        self.axes.scatter(x, y, c = 'b')
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


class DraggablePoint:
    lock = None
    def __init__(self, parent, x=0.1, y=0.1, size=0.1):

        self.parent = parent
        self.point = Ellipse((x, y), size, size, fc='r', alpha=0.5, edgecolor='r')
        self.x = x
        self.y = y

        parent.mapCanvas.figure.axes[0].add_patch(self.point)
        self.press = None
        self.background = None
    def get_point(self):
        return self.point

app = QApplication(sys.argv)
MainWindow = MainWindow()
sys.exit(app.exec_())