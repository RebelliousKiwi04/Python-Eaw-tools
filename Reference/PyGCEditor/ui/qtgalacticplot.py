from PyQt5.QtWidgets import QVBoxLayout, QWidget
from PyQt5.QtCore import pyqtSignal
from matplotlib.backends.backend_qt5agg import FigureCanvas, \
    NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Axes, Figure


class GalacticMap(QWidget):
    planetSelectedSignal = pyqtSignal(list)

    def __init__(self, parent: QWidget = None):
        super(GalacticMap, self).__init__()
        self.mapWidget: QWidget = QWidget(parent)
        self.mapWidget.setLayout(QVBoxLayout())

        self.mapCanvas: FigureCanvas = FigureCanvas(Figure())

        self.mapCanvas.mpl_connect('pick_event', self.__planetSelect)
        self.mapCanvas.mpl_connect('motion_notify_event', self.__planetHover)

        self.__galacticPlotNavBar: NavigationToolbar = NavigationToolbar(self.mapCanvas, self.mapWidget)
        self.mapWidget.layout().addWidget(self.__galacticPlotNavBar)
        self.mapWidget.layout().addWidget(self.mapCanvas)
        self.__axes: Axes = self.mapCanvas.figure.add_subplot(111, aspect = "equal")

        self.__annotate = self.__axes.annotate("", xy = (0,0), xytext = (10, 10), textcoords = "offset points", bbox = dict(boxstyle="round", fc="w"), arrowprops = dict(arrowstyle="->"))
        self.__annotate.set_visible(False)
        self.__planetNames = []
        self.__planetsScatter = None

    def plotGalaxy(self, planets, tradeRoutes, allPlanets, autoPlanetConnectionDistance: int = 0) -> None:
        '''Plots all planets as alpha = 0.1, then overlays all selected planets and trade routes'''
        self.__axes.clear()

        #Has to be set again here for the planet hover labels to work
        self.__annotate = self.__axes.annotate("", xy = (0,0), xytext = (10, 10), textcoords = "offset points", bbox = dict(boxstyle="round", fc="w"), arrowprops = dict(arrowstyle="->"))
        self.__annotate.set_visible(False)

        self.__planetNames = []

        x = []
        y = []

        for p in allPlanets:
            x.append(p.x)
            y.append(p.y)
            self.__planetNames.append(p.name)

        self.__planetsScatter = self.__axes.scatter(x, y, c = 'b', alpha = 0.1, picker = 5)

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
            self.__axes.plot([x1, x2], [y1, y2], 'k-', alpha=0.4)
        
        #Create automatic connections between planets
        if autoPlanetConnectionDistance > 0:
            for p1 in planets:
                for p2 in planets:
                    if p1 == p2:
                        break
                    dist: float = p1.distanceTo(p2)
                    if dist < autoPlanetConnectionDistance:
                        self.__axes.plot([p1.x, p2.x], [p1.y, p2.y], 'k-', alpha=0.1)

        x = []
        y = []

        for p in planets:
            x.append(p.x)
            y.append(p.y)

        self.__axes.scatter(x, y, c = 'b')

        self.mapCanvas.draw_idle()


    def getWidget(self) -> QWidget:
        '''Returns the plot widget'''
        return self.mapWidget

    def __planetSelect(self, event) -> None:
        '''Event handler for selecting a planet on the map'''
        planet_index = event.ind
        self.planetSelectedSignal.emit(list(planet_index))

    def __planetHover(self, event) -> None:
        '''Handler for hovering on a planet in the plot'''
        visible = self.__annotate.get_visible()

        if event.inaxes == self.__axes:
            contains, ind = self.__planetsScatter.contains(event)

            if contains:
                self.__update_annotation(ind)
                self.__annotate.set_visible(True)
                self.mapCanvas.draw_idle()
            else:
                if visible:
                    self.__annotate.set_visible(False)
                    self.mapCanvas.draw_idle()

    def __update_annotation(self, ind) -> None:
        '''Updates annotation parameters'''
        pos = self.__planetsScatter.get_offsets()[ind["ind"][0]]
        self.__annotate.xy = pos
        text = "{}".format(" ".join([self.__planetNames[n] for n in ind["ind"]]))
        self.__annotate.set_text(text)