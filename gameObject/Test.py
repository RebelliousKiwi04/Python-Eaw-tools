import sys
from PyQt5.QtGui import QWindow, QFont
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class ExampleWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.buildExamplePopup()

    def buildExamplePopup(self):
        exPopup = Window(self)
        exPopup.show()


class AddUnitWindow:
    def __init__(self):
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
        self.TechLevel.setGeometry(QRect(100, 60, 41, 31))
        self.TechLabel.setText(QCoreApplication.translate("AddUnitWindow", u"Tech Level", None))
        self.techLayout.addWidget(self.TechLabel)
        self.techLayout.addWidget(self.TechLevel)


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



        self.UnitTypeSelection = QComboBox()
        self.UnitTypeSelection.addItem("")
        self.UnitTypeSelection.setObjectName(u"UnitTypeSelection")
        self.UnitTypeSelection.setGeometry(QRect(10, 10, 191, 31))
        self.UnitTypeSelection.setLayoutDirection(Qt.LeftToRight)
        

        self.ownerLayout = QHBoxLayout()
        self.OwnerLabel = QLabel()
        self.OwnerLabel.setObjectName(u"OwnerLabel")
        self.OwnerLabel.setGeometry(QRect(10, 140, 81, 31))
        self.OwnerLabel.setFont(font)
        self.OwnerSelection = QComboBox()
        self.OwnerSelection.addItem("")
        self.OwnerSelection.setObjectName(u"OwnerSelection")
        self.OwnerSelection.setGeometry(QRect(70, 140, 131, 31))
        self.ownerLayout.addWidget(self.OwnerLabel)
        self.ownerLayout.addWidget(self.OwnerSelection)

        self.buttonLayout = QHBoxLayout()
        self.OkCancelButtons = QDialogButtonBox()
        self.OkCancelButtons.setObjectName(u"OkCancelButtons")
        self.OkCancelButtons.setGeometry(QRect(10, 190, 193, 28))
        self.OkCancelButtons.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonLayout.addWidget(self.OkCancelButtons)

        

        self.UnitTypeSelection.setItemText(0, QCoreApplication.translate("AddUnitWindow", u"Unit Type", None))

        self.OwnerLabel.setText(QCoreApplication.translate("AddUnitWindow", u"Owner", None))
        self.OwnerSelection.setItemText(0, QCoreApplication.translate("AddUnitWindow", u"Empire", None))

        self.layout.addWidget(self.UnitTypeSelection)
        self.layout.addLayout(self.techLayout)
        self.layout.addLayout(self.ownerLayout)
        self.layout.addLayout(self.QuantityLayout)
        self.layout.addLayout(self.buttonLayout)
        
        self.dialogWindow.setWindowTitle('Add Starting Forces')
        self.dialogWindow.setLayout(self.layout)
        self.dialogWindow.exec()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = AddUnitWindow()

    sys.exit(app.exec_())