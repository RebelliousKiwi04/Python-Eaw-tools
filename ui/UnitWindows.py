from PyQt5.QtGui import QWindow, QFont, QIcon
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys

class ChooseUnitTypeWindow:
    def __init__(self):
        self.dialogWindow = QDialog()
        self.dialogWindow.setWindowIcon(QIcon('eawIcon.png'))
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