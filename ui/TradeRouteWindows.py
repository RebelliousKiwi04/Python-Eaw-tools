from typing import List
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QIcon
from matplotlib.backends.backend_qt5agg import FigureCanvas, \
    NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Axes, Figure
import sys

class CreateTradeRouteWindow:
    def __init__(self, repository, campaign):
        self.dialogWindow = QDialog()
        self.dialogWindow.setWindowIcon(QIcon('eawIcon.png'))
        self.layout = QVBoxLayout()
        self.dialogWindow.setLayout(self.layout)
        self.dialogWindow.setWindowTitle("Create Trade Route")


        self.campaign = campaign
       
        #self.dialogWindow.setFixedSize(900, 540)


        self.mapWidget: QWidget = QWidget()
        self.mapWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
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
        self.__annotate = self.axes.annotate("", xy = (0,0), xytext = (10, 10), textcoords = "offset points", bbox = dict(boxstyle="round", fc="w"), arrowprops = dict(arrowstyle="->"))
        self.__annotate.set_visible(False)
        self.__planetNames = []
        self.__planetsScatter = None
        self.selected_planet = None
        self.layout.addWidget(self.mapWidget)

        self.label = QLabel("Create Trade Route\n Select 2 planets on the map, then press the button below to create route")

        self.label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)


        self.buttonLayout = QHBoxLayout()
        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.clicked.connect(self.hide)
        self.okButton = QPushButton("Create TradeRoute")
        self.okButton.clicked.connect(self.accept)
        self.cancelButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.okButton.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        self.buttonLayout.addWidget(self.cancelButton)
        self.buttonLayout.addWidget(self.okButton)

        self.layout.addWidget(self.label)
        self.layout.addLayout(self.buttonLayout)


        self.repository = repository
        self.selected_planets = []
    def show(self):
        self.plotGalaxy(self.campaign.planets)
        return self.dialogWindow.exec_()
    def plotGalaxy(self, allPlanets) -> None:
        self.axes.clear()

        #Has to be set again here for the planet hover labels to work
        self.__annotate = self.axes.annotate("", xy = (0,0), xytext = (10, 10), textcoords = "offset points", bbox = dict(boxstyle="round", fc="w"), arrowprops = dict(arrowstyle="->"))
        self.__annotate.set_visible(False)

        self.__planetNames = []

        x = []
        y = []

        for planet in allPlanets:
            x.append(planet.x)
            y.append(planet.y)
            self.__planetNames.append(planet.name)

        self.__planetsScatter = self.axes.scatter(x, y, c = 'b', alpha = 0.1,picker = 5)

        x = []
        y = []
        for p in self.selected_planets:
            x.append(p.x)
            y.append(p.y)

        self.axes.scatter(x, y, c = 'b')

        self.mapCanvas.draw_idle()
    def __planetSelect(self, event) -> None:
        '''Event handler for selecting a planet on the map'''
        planet_index = event.ind
        planet = self.campaign.planets[planet_index[0]]
        if planet in self.selected_planets:
            self.selected_planets.pop(self.selected_planets.index(planet))
        else:
            self.selected_planets.append(planet)
        self.plotGalaxy(self.campaign.planets)
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
    def hide(self):
        self.dialogWindow.reject()
    def accept(self):
        if len(self.selected_planets) == 2:
            self.dialogWindow.accept()
        else:
            messageBox = QMessageBox()
            title = "Invalid Selection!"
            message = "Please Select 2 Planets In Order To Create Trade Routes"
        
            reply = messageBox.warning(None, title, message, messageBox.Ok, messageBox.Ok)