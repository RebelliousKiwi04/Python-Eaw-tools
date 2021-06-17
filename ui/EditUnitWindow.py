from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from ui.Utilities import PyQtUtil
from PyQt5 import QtCore
import sys
class EditUnitWindow:
    def __init__(self, units, text):
        self.units = units
        self.text = text
        self.dialogWindow = QDialog()
        self.layout = QHBoxLayout()
        self.dialogWindow.setLayout(self.layout)
        self.dialogWindow.setWindowTitle("Edit Unit")
        font = QFont()
        font.setPointSize(10)

        self.LeftSideLayout = QVBoxLayout()

        self.SelectUnit = QComboBox()
        self.UnitNameLayout = QHBoxLayout()
        self.UnitNameLabel = QLabel()
        self.UnitNameLabel.setText("Unit Name")
        self.UnitNameLabel.setFont(font)

        self.UnitName = QLineEdit()

        self.UnitNameLayout.addWidget(self.UnitNameLabel)
        self.UnitNameLayout.addWidget(self.UnitName)

        self.ModelNameLayout = QVBoxLayout()
        self.ModelNameLabel = QLabel()
        self.ModelNameLabel.setFont(font)
        self.ModelNameLabel.setText("Model Name")
        self.ModelNameSubLayout = QHBoxLayout()
        self.ModelName = QLineEdit()
        self.ModelName.setEnabled(False)
        self.SetModelName = QToolButton()
        self.SetModelName.setText("...")
        self.ModelNameSubLayout.addWidget(self.ModelName)
        self.ModelNameSubLayout.addWidget(self.SetModelName)
        self.ModelNameLayout.addWidget(self.ModelNameLabel)
        self.ModelNameLayout.addLayout(self.ModelNameSubLayout)



        self.CreditCostLayout = QHBoxLayout()
        self.CreditCostLabel = QLabel()
        self.CreditCostLabel.setFont(font)
        self.CreditCostLabel.setText("Credit Cost")
        self.CreditCost = QSpinBox()
        self.CreditCost.setMaximum(1000000)
        self.CreditCostLayout.addWidget(self.CreditCostLabel)
        self.CreditCostLayout.addWidget(self.CreditCost)


        self.BuildTimeLayout = QHBoxLayout()
        self.BuildTimeLabel = QLabel()
        self.BuildTimeLabel.setFont(font)
        self.BuildTimeLabel.setText("Build Time")
        self.BuildTime = QSpinBox()
        self.BuildTime.setMaximum(1000000)
        self.BuildTimeLayout.addWidget(self.BuildTimeLabel)
        self.BuildTimeLayout.addWidget(self.BuildTime)


        self.HullLayout = QHBoxLayout()
        self.HullLabel = QLabel()
        self.HullLabel.setFont(font)
        self.HullLabel.setText("Hull")
        self.Hull = QSpinBox()
        self.Hull.setMaximum(1000000)
        self.HullLayout.addWidget(self.HullLabel)
        self.HullLayout.addWidget(self.Hull)


        self.ShieldLayout = QHBoxLayout()
        self.ShieldLabel = QLabel()
        self.ShieldLabel.setFont(font)
        self.ShieldLabel.setText("Shield")
        self.Shield = QSpinBox()
        self.Shield.setMaximum(1000000)
        self.ShieldLayout.addWidget(self.ShieldLabel)
        self.ShieldLayout.addWidget(self.Shield)


        self.RefreshRateLayout = QHBoxLayout()
        self.RefreshRateLabel = QLabel()
        self.RefreshRateLabel.setFont(font)
        self.RefreshRateLabel.setText("Refresh Rate")
        self.RefreshRate = QSpinBox()
        self.RefreshRate.setMaximum(1000000)
        self.RefreshRateLayout.addWidget(self.RefreshRateLabel)
        self.RefreshRateLayout.addWidget(self.RefreshRate)

        self.RequiredShipyardLayout = QHBoxLayout()
        self.RequiredShipyardLabel = QLabel()
        self.RequiredShipyardLabel.setFont(font)
        self.RequiredShipyardLabel.setText("Required Shipyard Level")
        self.RequiredShipyard = QSpinBox()
        self.RequiredShipyard.setMaximum(5)
        self.RequiredShipyardLayout.addWidget(self.RequiredShipyardLabel)
        self.RequiredShipyardLayout.addWidget(self.RequiredShipyard)

        self.TurnRateLayout = QHBoxLayout()
        self.TurnRateLabel = QLabel()
        self.TurnRateLabel.setFont(font)
        self.TurnRateLabel.setText("Rate Of Turn")
        self.TurnRate = QDoubleSpinBox()
        self.TurnRate.setMaximum(1000000)
        self.TurnRateLayout.addWidget(self.TurnRateLabel)
        self.TurnRateLayout.addWidget(self.TurnRate)

        self.MaxSpeedLayout = QHBoxLayout()
        self.MaxSpeedLabel = QLabel()
        self.MaxSpeedLabel.setFont(font)
        self.MaxSpeedLabel.setText("Max Speed")
        self.MaxSpeed = QDoubleSpinBox()
        self.MaxSpeed.setMaximum(1000000)
        self.MaxSpeedLayout.addWidget(self.MaxSpeedLabel)
        self.MaxSpeedLayout.addWidget(self.MaxSpeed)

        self.AccelerationLayout = QHBoxLayout()
        self.AccelerationLabel = QLabel()
        self.AccelerationLabel.setFont(font)
        self.AccelerationLabel.setText("Acceleration")
        self.Acceleration = QDoubleSpinBox()
        self.Acceleration.setMaximum(1000000)
        self.AccelerationLayout.addWidget(self.AccelerationLabel)
        self.AccelerationLayout.addWidget(self.Acceleration)

        self.DecelerationLayout = QHBoxLayout()
        self.DecelerationLabel = QLabel()
        self.DecelerationLabel.setFont(font)
        self.DecelerationLabel.setText("Deceleration")
        self.Deceleration = QDoubleSpinBox()
        self.Deceleration.setMaximum(1000000)
        self.DecelerationLayout.addWidget(self.DecelerationLabel)
        self.DecelerationLayout.addWidget(self.Deceleration)

        self.HyperspaceSpeedLayout = QHBoxLayout()
        self.HyperspaceSpeedLabel = QLabel()
        self.HyperspaceSpeedLabel.setFont(font)
        self.HyperspaceSpeedLabel.setText("Hyperspace Speed")
        self.HyperspaceSpeed = QDoubleSpinBox()
        self.HyperspaceSpeed.setMaximum(1000000)
        self.HyperspaceSpeedLayout.addWidget(self.HyperspaceSpeedLabel)
        self.HyperspaceSpeedLayout.addWidget(self.HyperspaceSpeed)

        self.PopCapLayout = QHBoxLayout()
        self.PopCapLabel = QLabel()
        self.PopCapLabel.setFont(font)
        self.PopCapLabel.setText("Population Capacity")
        self.PopCap = QSpinBox()
        self.PopCap.setMaximum(1000000)
        self.PopCapLayout.addWidget(self.PopCapLabel)
        self.PopCapLayout.addWidget(self.PopCap)

        self.AICP = QSpinBox()
        self.AICP.setMaximum(10000000)
        self.AICPLabel = QLabel()
        self.AICPLabel.setFont(font)
        self.AICPLabel.setText("AI Combat Power")
        self.AICPLayout = QHBoxLayout()
        self.AICPLayout.addWidget(self.AICPLabel)
        self.AICPLayout.addWidget(self.AICP)

        self.EditBuildPrereqs = QPushButton()
        self.EditBuildPrereqs.setText("Edit Build Prerequisites")


        self.ShieldTypeLayout = QHBoxLayout()
        self.ShieldTypeLabel = QLabel()
        self.ShieldTypeLabel.setFont(font)
        self.ShieldTypeLabel.setText("Shield Type")
        self.ShieldType = QComboBox()
        self.ShieldTypeLayout.addWidget(self.ShieldTypeLabel)
        self.ShieldTypeLayout.addWidget(self.ShieldType)

        self.ArmourTypeLayout = QHBoxLayout()
        self.ArmourTypeLabel = QLabel()
        self.ArmourTypeLabel.setFont(font)
        self.ArmourTypeLabel.setText("Armour Type")
        self.ArmourType = QComboBox()
        self.ArmourTypeLayout.addWidget(self.ArmourTypeLabel)
        self.ArmourTypeLayout.addWidget(self.ArmourType)


        self.OkCancelButtons = QDialogButtonBox()
        self.OkCancelButtons.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Save)

        self.LeftSideLayout.addWidget(self.SelectUnit)
        self.LeftSideLayout.addLayout(self.UnitNameLayout)
        self.LeftSideLayout.addLayout(self.ModelNameLayout)
        self.LeftSideLayout.addLayout(self.CreditCostLayout)
        self.LeftSideLayout.addLayout(self.BuildTimeLayout)
        self.LeftSideLayout.addLayout(self.HullLayout)
        self.LeftSideLayout.addLayout(self.ShieldLayout)
        self.LeftSideLayout.addLayout(self.RefreshRateLayout)
        self.LeftSideLayout.addLayout(self.RequiredShipyardLayout)
        self.LeftSideLayout.addLayout(self.TurnRateLayout)
        self.LeftSideLayout.addLayout(self.MaxSpeedLayout)
        self.LeftSideLayout.addLayout(self.AccelerationLayout)
        self.LeftSideLayout.addLayout(self.DecelerationLayout)
        self.LeftSideLayout.addLayout(self.HyperspaceSpeedLayout)
        self.LeftSideLayout.addLayout(self.PopCapLayout)
        self.LeftSideLayout.addLayout(self.AICPLayout)
        self.LeftSideLayout.addLayout(self.ShieldTypeLayout)
        self.LeftSideLayout.addLayout(self.ArmourTypeLayout)
        self.LeftSideLayout.addWidget(self.EditBuildPrereqs)
        self.LeftSideLayout.addWidget(self.OkCancelButtons)


        self.RightSideLayout = QVBoxLayout()

        self.HardPointLabel = QLabel()
        self.HardPointLabel.setFont(font)
        self.HardPointLabel.setText("Hardpoints")
        labels = ["Bone", "HardPoint Name", "HardPoint Type"]
        self.HardPoints = PyQtUtil.construct_table_widget(labels, 3)
        self.EditHardpoints = QPushButton()
        self.EditHardpoints.setText("Edit Hardpoints")
        self.HardPointLabel.setAlignment(Qt.AlignCenter)

        self.ToolTipLabel = QLabel()
        self.ToolTipLabel.setFont(font)
        self.ToolTipLabel.setText("Tooltip Entries")
        self.ToolTipLabel.setAlignment(Qt.AlignCenter)
        self.Tooltips = PyQtUtil.construct_table_widget(["Text Identifier", "Text"], 2)


        self.EditTooltip = QPushButton()
        self.EditTooltip.setText("Edit Tooltip Entries")

        self.RightSideLayout.addWidget(self.HardPointLabel)
        self.RightSideLayout.addWidget(self.HardPoints)
        self.RightSideLayout.addWidget(self.EditHardpoints)
        self.RightSideLayout.addWidget(self.ToolTipLabel)
        self.RightSideLayout.addWidget(self.Tooltips)
        self.RightSideLayout.addWidget(self.EditTooltip)

        self.layout.addLayout(self.LeftSideLayout)
        self.layout.addLayout(self.RightSideLayout)
    def on_index_changed(self):
        unitName = self.SelectUnit.currentText()
        if unitName in [x.name for x in self.units]:
            unit_index = [x.name for x in self.units].index(unitName)
        unit = self.units[unit_index]
        
        if unit.get_text_key() in self.text.keys():
            self.UnitName.setText(self.text[unit.get_text_key()])
        else:
            self.UnitName.setText("Unit Has No Text")
        self.ModelName.setText(unit.model_path)
        self.CreditCost.setValue(unit.cost)
        self.BuildTime.setValue(unit.build_time)
        self.Hull.setValue(unit.hull)
        self.Shield.setValue(unit.shield)
        self.RefreshRate.setValue(unit.get_refresh_rate())
        self.RequiredShipyard.setValue(unit.get_shipyard_level())
        self.TurnRate.setValue(unit.get_max_turn_rate())
        self.MaxSpeed.setValue(unit.get_max_speed())
        self.Acceleration.setValue(unit.get_acceleration())
        self.Deceleration.setValue(unit.get_deceleration())
        self.HyperspaceSpeed.setValue(unit.get_hyperspace_speed())
        self.PopCap.setValue(unit.get_pop())
        self.AICP.setValue(unit.get_aicp())
        self.HardPoints.clear()
        self.HardPoints.setRowCount(0)
        for name in unit.get_hardpoints():
            rowCount = self.HardPoints.rowCount()
            self.HardPoints.setRowCount(rowCount + 1)
            item= QTableWidgetItem(name)
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.HardPoints.setItem(rowCount, 1, item)
        self.Tooltips.clear()
        self.Tooltips.setRowCount(0)
        for text_id in unit.get_tooltip():
            rowCount = self.Tooltips.rowCount()
            self.Tooltips.setRowCount(rowCount + 1)
            item= QTableWidgetItem(text_id)
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.Tooltips.setItem(rowCount, 0, item)
            if text_id in self.text.keys():
                item= QTableWidgetItem(self.text[text_id])
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                self.Tooltips.setItem(rowCount, 1, item)
            else:
                item= QTableWidgetItem("Unit Has No Text!")
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                self.Tooltips.setItem(rowCount, 1, item)
        self.Tooltips.setHorizontalHeaderLabels(["Text Identifier", "Text"])
        self.HardPoints.setHorizontalHeaderLabels(["Bone", "HardPoint Name", "HardPoint Type"])
    def show(self):
        unitName = self.SelectUnit.currentText()
        if unitName in [x.name for x in self.units]:
            unit_index = [x.name for x in self.units].index(unitName)
        unit = self.units[unit_index]
        
        if unit.get_text_key() in self.text.keys():
            self.UnitName.setText(self.text[unit.get_text_key()])
        else:
            self.UnitName.setText("Unit Has No Text")
        self.ModelName.setText(unit.model_path)
        self.CreditCost.setValue(unit.cost)
        self.BuildTime.setValue(unit.build_time)
        self.Hull.setValue(unit.hull)
        self.Shield.setValue(unit.shield)
        self.RefreshRate.setValue(unit.get_refresh_rate())
        self.RequiredShipyard.setValue(unit.get_shipyard_level())
        self.TurnRate.setValue(unit.get_max_turn_rate())
        self.MaxSpeed.setValue(unit.get_max_speed())
        self.AICP.setValue(unit.get_aicp())
        self.Acceleration.setValue(unit.get_acceleration())
        self.Deceleration.setValue(unit.get_deceleration())
        self.HyperspaceSpeed.setValue(unit.get_hyperspace_speed())
        self.PopCap.setValue(unit.get_pop())
        self.HardPoints.clear()
        for name in unit.get_hardpoints():
            rowCount = self.HardPoints.rowCount()
            self.HardPoints.setRowCount(rowCount + 1)
            item= QTableWidgetItem(name)
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.HardPoints.setItem(rowCount, 1, item)
        self.Tooltips.clear()
        for text_id in unit.get_tooltip():
            rowCount = self.Tooltips.rowCount()
            self.Tooltips.setRowCount(rowCount + 1)
            item= QTableWidgetItem(text_id)
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.Tooltips.setItem(rowCount, 0, item)
            if text_id in self.text.keys():
                item= QTableWidgetItem(self.text[text_id])
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                self.Tooltips.setItem(rowCount, 1, item)
            else:
                item= QTableWidgetItem("Unit Has No Text!")
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                self.Tooltips.setItem(rowCount, 1, item)
        self.Tooltips.setHorizontalHeaderLabels(["Text Identifier", "Text"])
        self.HardPoints.setHorizontalHeaderLabels(["Bone", "HardPoint Name", "HardPoint Type"])
        self.SelectUnit.currentIndexChanged.connect(self.on_index_changed)
        self.dialogWindow.exec()