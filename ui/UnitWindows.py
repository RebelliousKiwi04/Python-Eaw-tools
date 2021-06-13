from PyQt5.QtGui import QWindow, QFont
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys

class ChooseUnitTypeWindow:
    def __init__(self):
        self.dialogWindow = QDialog()
        self.layout = QVBoxLayout()


        self.typeLayout = QHBoxLayout()
        self.TypeLabel = QLabel()
        self.TypeLabel.setObjectName(u"TypeLabel")
        font = QFont()
        font.setPointSize(9)
        self.TypeLabel.setFont(font)
        self.TypeLabel.setText("Unit Type:")
        self.UnitTypeSelection = QComboBox()
        self.UnitTypeSelection.setObjectName(u"UnitTypeSelection")
        self.UnitTypeSelection.setLayoutDirection(Qt.LeftToRight)

        self.typeLayout.addWidget(self.TypeLabel)
        self.typeLayout.addWidget(self.UnitTypeSelection)

        self.buttonLayout = QHBoxLayout()
        self.OkCancelButtons = QDialogButtonBox()
        self.OkCancelButtons.setObjectName(u"OkCancelButtons")
        self.OkCancelButtons.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.OkCancelButtons.move(self.dialogWindow.rect().center())
        self.buttonLayout.addWidget(self.OkCancelButtons)

        self.layout.addLayout(self.typeLayout)
        self.layout.addWidget(self.OkCancelButtons)
        self.dialogWindow.setWindowTitle('Select Unit Type')
        self.dialogWindow.setLayout(self.layout)

class UnitDataWindow:
    def __init__(self):
        self.dialogWindow = QDialog()
        self.layout = QVBoxLayout()

        font = QFont()
        font.setPointSize(10)

        self.NameLayout = QHBoxLayout()
        self.XMLNameLabel = QLabel()
        self.XMLNameLabel.setFont(font)
        self.XMLNameLabel.setText("XML Name:")
        self.xml_name = QLineEdit()

        self.NameLayout.addWidget(self.XMLNameLabel)
        self.NameLayout.addWidget(self.xml_name)


        self.ModelNameLayout = QHBoxLayout()
        self.ModelNameLabel = QLabel()
        self.ModelNameLabel.setFont(font)
        self.ModelNameLabel.setText("Model:")
        self.ModelLocationBox = QLineEdit()
        self.ModelLocationBox.setText('No Model Location')
        self.SetModelLocation = QToolButton()
        self.SetModelLocation.setText("...")

        self.ModelNameLayout.addWidget(self.ModelNameLabel)
        self.ModelNameLayout.addWidget(self.ModelLocationBox)
        self.ModelNameLayout.addWidget(self.SetModelLocation)


        self.CreditCostLayout = QHBoxLayout()
        self.CreditCostLabel = QLabel()
        self.CreditCostLabel.setFont(font)
        self.CreditCostLabel.setText("Credit Cost:")
        self.CreditCost = QSpinBox()
        self.CreditCost.setMaximum(100000000)
        
        self.CreditCostLayout.addWidget(self.CreditCostLabel)
        self.CreditCostLayout.addWidget(self.CreditCost)


        self.BuildTimeLayout = QHBoxLayout()
        self.BuildTimeLabel = QLabel()
        self.BuildTimeLabel.setFont(font)
        self.BuildTimeLabel.setText("Build Time:")
        self.BuildTime = QSpinBox()
        self.BuildTime.setMaximum(100000000)
        
        self.BuildTimeLayout.addWidget(self.BuildTimeLabel)
        self.BuildTimeLayout.addWidget(self.BuildTime)

        self.HullLayout = QHBoxLayout()
        self.HullLabel = QLabel()
        self.HullLabel.setFont(font)
        self.HullLabel.setText("Hull:")
        self.Hull = QSpinBox()
        self.Hull.setMaximum(100000000)
        
        self.HullLayout.addWidget(self.HullLabel)
        self.HullLayout.addWidget(self.Hull)

        self.ShieldLayout = QHBoxLayout()
        self.ShieldLabel = QLabel()
        self.ShieldLabel.setFont(font)
        self.ShieldLabel.setText("Shield:")
        self.Shield = QSpinBox()
        self.Shield.setMaximum(100000000)
        
        self.ShieldLayout.addWidget(self.ShieldLabel)
        self.ShieldLayout.addWidget(self.Shield)

        self.RefreshRateLabel = QLabel()
        self.RefreshRateLabel.setFont(font)
        self.RefreshRateLabel.setText("Refresh Rate:")
        self.RefreshRate = QSpinBox()
        self.RefreshRate.setMaximum(100000000)

        self.ShieldLayout.addWidget(self.RefreshRateLabel)
        self.ShieldLayout.addWidget(self.RefreshRate)


        self.ShipyardLevelLayout = QHBoxLayout()
        self.ShipyardLevelLabel = QLabel()
        self.ShipyardLevelLabel.setFont(font)
        self.ShipyardLevelLabel.setText("Required Shipyard Level:")
        self.ShipyardLevel = QSpinBox()
        self.ShipyardLevel.setMaximum(5)

        self.ShipyardLevelLayout.addWidget(self.ShipyardLevelLabel)
        self.ShipyardLevelLayout.addWidget(self.ShipyardLevel)


        self.TurnRateLayout = QHBoxLayout()
        self.TurnRateLabel = QLabel()
        self.TurnRateLabel.setFont(font)
        self.TurnRateLabel.setText("Rate Of Turn:")
        self.TurnRate = QDoubleSpinBox()
        self.TurnRate.setMaximum(100000000)

        self.TurnRateLayout.addWidget(self.TurnRateLabel)
        self.TurnRateLayout.addWidget(self.TurnRate)

        self.MaxSpeedLayout = QHBoxLayout()
        self.MaxSpeedLabel = QLabel()
        self.MaxSpeedLabel.setFont(font)
        self.MaxSpeedLabel.setText("Max Speed:")
        self.MaxSpeed = QDoubleSpinBox()
        self.MaxSpeed.setMaximum(100000000)

        self.MaxSpeedLayout.addWidget(self.MaxSpeedLabel)
        self.MaxSpeedLayout.addWidget(self.MaxSpeed)



        self.AccelerationLayout = QHBoxLayout()
        self.AccelerationLabel = QLabel()
        self.AccelerationLabel.setFont(font)
        self.AccelerationLabel.setText("Acceleration:")
        self.Acceleration = QDoubleSpinBox()
        self.Acceleration.setMaximum(100000000)

        self.DeccelerationLabel = QLabel()
        self.DeccelerationLabel.setFont(font)
        self.DeccelerationLabel.setText("Deceleration:")
        self.Decceleration = QDoubleSpinBox()
        self.Decceleration.setMaximum(100000000)

        self.AccelerationLayout.addWidget(self.AccelerationLabel)
        self.AccelerationLayout.addWidget(self.Acceleration)
        self.AccelerationLayout.addWidget(self.DeccelerationLabel)
        self.AccelerationLayout.addWidget(self.Decceleration)


        self.HyperspaceSpeedLayout = QHBoxLayout()
        self.HyperspaceSpeedLabel = QLabel()
        self.HyperspaceSpeedLabel.setFont(font)
        self.HyperspaceSpeedLabel.setText("Hyperspace Speed:")
        self.HyperspaceSpeed = QSpinBox()
        self.HyperspaceSpeed.setMaximum(100000000)

        self.HyperspaceSpeedLayout.addWidget(self.HyperspaceSpeedLabel)
        self.HyperspaceSpeedLayout.addWidget(self.HyperspaceSpeed)


        self.GalacticPopLayout = QHBoxLayout()
        self.GalacticPopLabel = QLabel()
        self.GalacticPopLabel.setFont(font)
        self.GalacticPopLabel.setText("Galactic Population Cap:")
        self.GalacticPop = QSpinBox()
        self.GalacticPop.setMaximum(100000000)

        self.GalacticPopLayout.addWidget(self.GalacticPopLabel)
        self.GalacticPopLayout.addWidget(self.GalacticPop)

        self.LandPopLayout = QHBoxLayout()
        self.LandPopLabel = QLabel()
        self.LandPopLabel.setFont(font)
        self.LandPopLabel.setText("Land Population:")
        self.LandPop = QSpinBox()
        self.LandPop.setMaximum(100000000)

        self.LandPopLayout.addWidget(self.LandPopLabel)
        self.LandPopLayout.addWidget(self.LandPop)

        self.SpacePopLabel = QLabel()
        self.SpacePopLabel.setFont(font)
        self.SpacePopLabel.setText("Space:")
        self.SpacePop = QSpinBox()
        self.SpacePop.setMaximum(100000000)

        self.LandPopLayout.addWidget(self.SpacePopLabel)
        self.LandPopLayout.addWidget(self.SpacePop)


        self.ShieldTypeLayout = QHBoxLayout()
        self.ShieldTypeLabel = QLabel()
        self.ShieldTypeLabel.setFont(font)
        self.ShieldTypeLabel.setText("Shield Type:")
        self.ShieldType = QComboBox()

        self.ShieldTypeLayout.addWidget(self.ShieldTypeLabel)
        self.ShieldTypeLayout.addWidget(self.ShieldType)

        self.ArmourTypeLayout = QHBoxLayout()
        self.ArmourTypeLabel = QLabel()
        self.ArmourTypeLabel.setFont(font)
        self.ArmourTypeLabel.setText("Armour Type:")
        self.ArmourType = QComboBox()

        self.ArmourTypeLayout.addWidget(self.ArmourTypeLabel)
        self.ArmourTypeLayout.addWidget(self.ArmourType)

        self.hardpoints = QPushButton()
        self.hardpoints.setText("Manage Hardpoints")

        self.OkCancelButtons = QDialogButtonBox()
        self.OkCancelButtons.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)


        self.layout.addLayout(self.NameLayout)
        self.layout.addLayout(self.ModelNameLayout)
        self.layout.addLayout(self.CreditCostLayout)
        self.layout.addLayout(self.BuildTimeLayout)
        self.layout.addLayout(self.HullLayout)
        self.layout.addLayout(self.ShieldLayout)
        self.layout.addLayout(self.ShipyardLevelLayout)
        self.layout.addLayout(self.TurnRateLayout)
        self.layout.addLayout(self.MaxSpeedLayout)
        self.layout.addLayout(self.AccelerationLayout)
        self.layout.addLayout(self.HyperspaceSpeedLayout)
        self.layout.addLayout(self.GalacticPopLayout)
        self.layout.addLayout(self.LandPopLayout)
        self.layout.addLayout(self.ShieldTypeLayout)
        self.layout.addLayout(self.ArmourTypeLayout)
        self.layout.addWidget(self.hardpoints)
        self.layout.addWidget(self.OkCancelButtons)

        self.dialogWindow.setWindowTitle('Modify Unit Data')
        self.dialogWindow.setLayout(self.layout)
app = QApplication(sys.argv)

unitWindow = UnitDataWindow()
unitWindow.dialogWindow.exec()