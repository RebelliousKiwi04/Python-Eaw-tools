from PyQt5.QtGui import QWindow, QFont
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class AddUnitWindow:
    def __init__(self, planet_name):
        self.planet = planet_name
        self.dialogWindow = QDialog()
        self.layout = QVBoxLayout()

        self.techLayout = QHBoxLayout()
        self.TechLabel = QLabel()
        self.TechLabel.setObjectName(u"TechLabel")
        self.TechLabel.setGeometry(QRect(10, 60, 81, 31))
        font = QFont()
        font.setPointSize(10)
        self.TechLabel.setFont(font)
        self.TechLevel = QSpinBox()
        self.TechLevel.setObjectName(u"TechLevel")
        self.TechLabel.setText(QCoreApplication.translate("AddUnitWindow", u"Tech Level", None))
        self.techLayout.addWidget(self.TechLabel)
        self.techLayout.addWidget(self.TechLevel)
        self.TechLevel.setValue(1)


        self.QuantityLayout = QHBoxLayout()
        self.QuantityLabel = QLabel()
        self.QuantityLabel.setObjectName(u"QuantityLabel")
        self.QuantityLabel.setGeometry(QRect(10, 100, 81, 31))
        self.QuantityLabel.setFont(font)
        self.Quantity = QSpinBox()
        self.Quantity.setObjectName(u"Quantity")
        self.Quantity.setGeometry(QRect(80, 100, 51, 31))
        self.QuantityLabel.setText(QCoreApplication.translate("AddUnitWindow", u"Quantity", None))
        self.QuantityLayout.addWidget(self.QuantityLabel)
        self.QuantityLayout.addWidget(self.Quantity)
        self.Quantity.setValue(1)


        self.UnitTypeSelection = QComboBox()
        self.UnitTypeSelection.setObjectName(u"UnitTypeSelection")
        self.UnitTypeSelection.setGeometry(QRect(10, 10, 191, 31))
        self.UnitTypeSelection.setLayoutDirection(Qt.LeftToRight)
        



        self.buttonLayout = QHBoxLayout()
        self.OkCancelButtons = QDialogButtonBox()
        self.OkCancelButtons.setObjectName(u"OkCancelButtons")
        self.OkCancelButtons.setGeometry(QRect(10, 190, 193, 28))
        self.OkCancelButtons.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonLayout.addWidget(self.OkCancelButtons)

    

        self.layout.addWidget(self.UnitTypeSelection)
        self.layout.addLayout(self.techLayout)
        self.layout.addLayout(self.QuantityLayout)
        self.layout.addLayout(self.buttonLayout)
        
        self.dialogWindow.setWindowTitle('Add Starting Forces')
        self.dialogWindow.setLayout(self.layout)
        self.signal = pyqtSignal(list)
        self.OkCancelButtons.rejected.connect(self.dialogWindow.accept)
    def update_unit_box(self, unit_list):
        for i in unit_list:
            self.UnitTypeSelection.addItem(i.name)
    def show(self):
        self.dialogWindow.exec()
    def on_completion(self):
        techLevel = self.TechLevel.value()
        quantity = self.Quantity.value()
        unit_name = self.UnitTypeSelection.currentText()
        self.signal.emit(list(techLevel, quantity, unit_name, self.planet))
        