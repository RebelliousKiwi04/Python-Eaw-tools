from typing import List
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from matplotlib.backends.backend_qt5agg import FigureCanvas, \
    NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Axes, Figure
import sys

class EditTradeRoute:
    def __init__(self, planets, text):
        self.size = float(25)
        self.planets = planets
        self.text = text
        self.dialogWindow = QDialog()
        self.layout = QHBoxLayout()
        self.dialogWindow.setLayout(self.layout)
        self.dialogWindow.setWindowTitle("Edit Trade Route")
        self.x = 0
        self.y = 0
        font = QFont()
        font.setPointSize(10)
    

        self.setPointSizeAction = QPushButton()
        self.setPointSizeAction.clicked.connect(self.change_point_size)

        self.LeftSideLayout = QVBoxLayout()
        self.planetSelection = QComboBox()

        self.planetNameLayout = QVBoxLayout()
        self.PlanetNameText = QLabel()
        self.PlanetNameText.setFont(font)
        self.PlanetNameText.setText("Trade Route Name:")
        self.PlanetName = QLineEdit()
        self.planetNameLayout.addWidget(self.PlanetNameText)
        self.planetNameLayout.addWidget(self.PlanetName)


        self.OkCancelButtons = QDialogButtonBox()
        self.OkCancelButtons.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Save)



        


        self.LeftSideLayout.addWidget(self.planetSelection)
        self.LeftSideLayout.addItem(QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))
        self.LeftSideLayout.addLayout(self.planetNameLayout)
        self.LeftSideLayout.addItem(QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))

       
        self.layout.addLayout(self.LeftSideLayout)
        self.dialogWindow.setFixedSize(900, 540)


        self.mapWidget: QWidget = QWidget()
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
        self.times = 0
        self.layout.addWidget(self.mapWidget)
        self.OkCancelButtons.rejected.connect(self.dialogWindow.accept)
        #self.OkCancelButtons.accepted.connect(self.save_to_file)
    def on_index_changed(self):
        planet_name = self.planetSelection.currentText()
        if planet_name in [x.name for x in self.planets]:
            planet_index = [x.name for x in self.planets].index(planet_name)
        self.plotGalaxy(self.planets)
        self.plotSelectedPlanet(self.planets[planet_index])
        planet = self.planets[planet_index]
        self.PlanetModelName.setText(planet.get_model_name())
        if planet.get_text_key() in self.text.keys():
            self.PlanetName.setText(self.text[planet.get_text_key()])
        else:
            self.PlanetName.setText("Planet Has No Text")
    def show(self):
        self.plotGalaxy(self.planets)
        self.dialogWindow.exec()
    def plotGalaxy(self, allPlanets) -> None:
        '''Plots all planets as alpha = 0.1, then overlays all selected planets and trade routes'''
        self.axes.clear()

        #Has to be set again here for the planet hover labels to work
        self.__annotate = self.axes.annotate("", xy = (0,0), xytext = (10, 10), textcoords = "offset points", bbox = dict(boxstyle="round", fc="w"), arrowprops = dict(arrowstyle="->"))
        self.__annotate.set_visible(False)

        self.__planetNames = []

        x = []
        y = []

        for planet in allPlanets:
            if planet.name != self.planetSelection.currentText():
                x.append(planet.x)
                y.append(planet.y)
                self.__planetNames.append(planet.name)
            else:
                x.append(0)
                y.append(0)
                self.__planetNames.append("Dummy Planet")

        self.__planetsScatter = self.axes.scatter(x, y, c = 'b', alpha = 0.1,picker = 5)
        self.mapCanvas.draw_idle()
        self.times = self.times +1
    def __planetSelect(self, event) -> None:
        '''Event handler for selecting a planet on the map'''
        planet_index = event.ind
        planet_name = self.planets[planet_index[0]].name
        self.planetSelection.setCurrentIndex(planet_index[0])
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
        self.dialogWindow.accept()
  