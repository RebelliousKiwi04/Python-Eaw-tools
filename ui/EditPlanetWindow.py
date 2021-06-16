from typing import List
import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from matplotlib.backends.backend_qt5agg import FigureCanvas, \
    NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Axes, Figure
from matplotlib.pyplot import grid
from ui.DraggablePoint import DraggablePoint
import sys

class PlanetWindow:
    def __init__(self, planets):
        self.size = float(25)
        self.planets = planets
        self.dialogWindow = QDialog()
        self.layout = QHBoxLayout()
        self.dialogWindow.setLayout(self.layout)
        self.dialogWindow.setWindowTitle("Edit Planet")
        self.x = 0
        self.y = 0
        font = QFont()
        font.setPointSize(10)
    

        self.setPointSizeAction = QPushButton()
        self.setPointSizeAction.clicked.connect(self.change_point_size)

        self.LeftSideLayout = QVBoxLayout()
        self.planetSelection = QComboBox()
        self.ModelNameLayout = QVBoxLayout()
        self.modelNameSublayout = QHBoxLayout()
        self.ModelNameLabel = QLabel()
        self.ModelNameLabel.setFont(font)
        self.ModelNameLabel.setText("Model Name:")
        self.PlanetModelName = QLineEdit()
        self.PlanetModelName.setEnabled(False)

        self.SetModel = QToolButton()
        self.SetModel.setText("...")
        self.SetModel.clicked.connect(self.set_model)
        self.ModelNameLayout.addWidget(self.ModelNameLabel)
        self.modelNameSublayout.addWidget(self.PlanetModelName)
        self.modelNameSublayout.addWidget(self.SetModel)
        self.ModelNameLayout.addLayout(self.modelNameSublayout)



        self.positionLayout = QVBoxLayout()
        self.currentPositionlabel = QLabel()
        self.currentPositionlabel.setFont(font)
        self.currentPositionlabel.setText("Current Position:")
        self.positionLayout.addWidget(self.currentPositionlabel)



        self.xLayout = QHBoxLayout()
        self.xLabel = QLabel()
        self.xLabel.setFont(font)
        self.xLabel.setText("X:")

        self.XPosition = QLineEdit()

        self.xLayout.addWidget(self.xLabel)
        self.xLayout.addWidget(self.XPosition)



        self.yLayout = QHBoxLayout()
        self.yLabel = QLabel()
        self.yLabel.setFont(font)
        self.yLabel.setText("Y:")

        self.yPosition = QLineEdit()

        self.yLayout.addWidget(self.yLabel)
        self.yLayout.addWidget(self.yPosition)


        self.positionLayout.addLayout(self.xLayout)
        self.positionLayout.addLayout(self.yLayout)

        self.resetPosition = QPushButton()
        self.resetPosition.setText('Reset Planet Position')


        self.XPosition.setEnabled(False)
        self.yPosition.setEnabled(False)

        self.OkCancelButtons = QDialogButtonBox()
        self.OkCancelButtons.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Save)


        self.SpaceMapLayout = QVBoxLayout()

        self.SpaceMapLabel = QLabel()
        self.SpaceMapLabel.setFont(font)
        self.SpaceMapLabel.setText("Space Tactical Map:")
        self.SpaceMapSubLayout = QHBoxLayout()
        self.SpaceMap = QLineEdit()
        self.SpaceMap.setEnabled(False)

        self.changeSpaceLayout = QToolButton()
        self.changeSpaceLayout.setText("...")
        self.changeSpaceLayout.clicked.connect(self.set_space_map)
        self.SpaceMapLayout.addWidget(self.SpaceMapLabel)
        self.SpaceMapSubLayout.addWidget(self.SpaceMap)
        self.SpaceMapSubLayout.addWidget(self.changeSpaceLayout)
        self.SpaceMapLayout.addLayout(self.SpaceMapSubLayout)
        self.LandMapLayout = QVBoxLayout()

        self.LandMapLabel = QLabel()
        self.LandMapLabel.setFont(font)
        self.LandMapLabel.setText("Land Tactical Map:")
        self.LandMapSubLayout = QHBoxLayout()
        self.LandMap = QLineEdit()
        self.LandMap.setEnabled(False)
        self.changeLandLayout = QToolButton()
        self.changeLandLayout.setText("...")
        self.changeLandLayout.clicked.connect(self.set_land_map)
        self.LandMapLayout.addWidget(self.LandMapLabel)
        self.LandMapSubLayout.addWidget(self.LandMap)
        self.LandMapSubLayout.addWidget(self.changeLandLayout)
        self.LandMapLayout.addLayout(self.LandMapSubLayout)


        self.LeftSideLayout.addWidget(self.planetSelection)
        self.LeftSideLayout.addItem(QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))
        self.LeftSideLayout.addLayout(self.ModelNameLayout)
        self.LeftSideLayout.addItem(QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))
        self.LeftSideLayout.addLayout(self.SpaceMapLayout)
        self.LeftSideLayout.addLayout(self.LandMapLayout)
        self.LeftSideLayout.addItem(QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))
        self.LeftSideLayout.addLayout(self.positionLayout)
        self.LeftSideLayout.addItem(QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))
        self.LeftSideLayout.addWidget(self.resetPosition)
        self.LeftSideLayout.addItem(QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))

        self.HideGridButton = QPushButton()
        self.HideGridButton.setText("Show Grid")
        self.LeftSideLayout.addWidget(self.HideGridButton)
        #self.LeftSideLayout.addItem(QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))
        self.setPointSizeAction.setText("Set Point Size")
        self.LeftSideLayout.addWidget(self.setPointSizeAction)
        self.LeftSideLayout.addItem(QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))
        self.HideGridButton.clicked.connect(self.toggle_grid)
        self.LeftSideLayout.addWidget(self.OkCancelButtons)
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
        self.OkCancelButtons.rejected.connect(sys.exit)
        #self.OkCancelButtons.accepted.connect(self.save_to_file)
    def change_point_size(self):
        size = QInputDialog.getInt(self.mapWidget, "Enter Planet Movement Point Size", "Enter Planet Movement Point Size", self.size, 0, 100, 1)
        if size[1] != False:
            self.size = float(size[0])
            self.selected_planet.point.remove()
            self.selected_planet = DraggablePoint(self, self.x, self.y, self.size)
    def toggle_grid(self):
        if self.HideGridButton.text() == 'Show Grid':
            self.axes.grid(True)
            self.HideGridButton.setText("Hide Grid")
            self.mapCanvas.draw()
        else:
            self.axes.grid(False)
            self.HideGridButton.setText("Show Grid")
            self.mapCanvas.draw()
    def on_index_changed(self):
        planet_name = self.planetSelection.currentText()
        if planet_name in [x.name for x in self.planets]:
            planet_index = [x.name for x in self.planets].index(planet_name)
        self.plotGalaxy(self.planets)
        self.plotSelectedPlanet(self.planets[planet_index])
        planet = self.planets[planet_index]
        self.PlanetModelName.setText(planet.get_model_name())

        self.LandMap.setText(planet.land_map)
        self.SpaceMap.setText(planet.space_map)
        self.XPosition.setText(str(planet.x))
        self.yPosition.setText(str(planet.y))
    def show(self):
        
        planet_name = self.planetSelection.currentText()
        if planet_name in [x.name for x in self.planets]:
            planet_index = [x.name for x in self.planets].index(planet_name)
        planet = self.planets[planet_index]
        self.plotGalaxy(self.planets)
        self.plotSelectedPlanet(self.planets[planet_index])
        self.planetSelection.currentIndexChanged.connect(self.on_index_changed)
        self.resetPosition.clicked.connect(self.reset_position)
        self.PlanetModelName.setText(planet.get_model_name())
        self.LandMap.setText(planet.land_map)
        self.SpaceMap.setText(planet.space_map)
        self.XPosition.setText(str(planet.x))
        self.yPosition.setText(str(planet.y))
        self.dialogWindow.exec()
    def reset_position(self):
        self.selected_planet.point.remove()
        planet_name = self.planetSelection.currentText()
        if planet_name in [x.name for x in self.planets]:
            planet_index = [x.name for x in self.planets].index(planet_name)
        self.plotSelectedPlanet(self.planets[planet_index])
        planet = self.planets[planet_index]
        self.XPosition.setText(str(planet.x))
        self.yPosition.setText(str(planet.y))
    def plotSelectedPlanet(self, planet, size=25):
        # del(self.list_points[:])
        self.x = planet.x 
        self.y = planet.y
        self.selected_planet = DraggablePoint(self, planet.x, planet.y,self.size)
        self.connect()
        self.mapCanvas.draw()
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
    def set_model(self):
        directory = str(QFileDialog.getOpenFileName())
        if not directory.lower().endswith('.alo'):
            pass
        else:
            self.PlanetModelName.setText(directory)
    def set_land_map(self):
        directory = str(QFileDialog.getOpenFileName())
        if not directory.lower().endswith('.ted'):
            pass
        else:
            self.LandMap.setText(directory)
    def set_space_map(self):
        directory = str(QFileDialog.getOpenFileName())
        if not directory.lower().endswith('.ted'):
            pass
        else:
            self.SpaceMap.setText(directory)
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
    def connect(self):
        self.cidpress = self.selected_planet.point.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.cidrelease = self.selected_planet.point.figure.canvas.mpl_connect('button_release_event', self.on_release)
        self.cidmotion = self.selected_planet.point.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)
    def on_press(self, event):

        if event.inaxes != self.selected_planet.point.axes: return
        if DraggablePoint.lock is not None: return
        contains, attrd = self.selected_planet.point.contains(event)
        if not contains: return
        self.press = (self.selected_planet.point.center), event.xdata, event.ydata
        DraggablePoint.lock = self

        canvas = self.selected_planet.point.figure.canvas
        axes = self.selected_planet.point.axes
        self.selected_planet.point.set_animated(True)
        canvas.draw()
        self.background = canvas.copy_from_bbox(self.selected_planet.point.axes.bbox)

        axes.draw_artist(self.selected_planet.point)

        canvas.blit(axes.bbox)

    def on_motion(self, event):

        if DraggablePoint.lock is not self:
            return
        if event.inaxes != self.selected_planet.point.axes: return
        self.selected_planet.point.center, xpress, ypress = self.press
        dx = event.xdata - xpress
        dy = event.ydata - ypress
        self.selected_planet.point.center = (self.selected_planet.point.center[0]+dx, self.selected_planet.point.center[1]+dy)

        canvas = self.selected_planet.point.figure.canvas
        axes = self.selected_planet.point.axes
        # restore the background region
        canvas.restore_region(self.background)

        # redraw just the current rectangle
        axes.draw_artist(self.selected_planet.point)

        self.x = self.selected_planet.point.center[0]
        self.y = self.selected_planet.point.center[1]
        self.XPosition.setText(str(self.x))
        self.yPosition.setText(str(self.y))
        # blit just the redrawn area
        canvas.blit(axes.bbox)


    def on_release(self, event):

        'on release we reset the press data'
        if DraggablePoint.lock is not self:
            return

        self.press = None
        DraggablePoint.lock = None

        # turn off the rect animation property and reset the background
        self.selected_planet.point.set_animated(False)

        self.background = None

        # redraw the full figure
        self.selected_planet.point.figure.canvas.draw()

        self.x = self.selected_planet.point.center[0]
        self.y = self.selected_planet.point.center[1]
        self.XPosition.setText(str(self.x))
        self.yPosition.setText(str(self.y))
    def hide(self):
        self.dialogWindow.accept()
  