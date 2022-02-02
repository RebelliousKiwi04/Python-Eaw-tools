from PyQt5.QtGui import QWindow, QFont, QIcon
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class AddUnitWindow:
    def __init__(self, planet_name):
        self.planet = planet_name
        self.dialogWindow = QDialog()
        self.dialogWindow.setWindowIcon(QIcon('eawIcon.png'))
        self.layout = QVBoxLayout()

        font = QFont()
        font.setPointSize(10)



        self.QuantityLayout = QHBoxLayout()
        self.QuantityLabel = QLabel()
        self.QuantityLabel.setObjectName(u"QuantityLabel")
        self.QuantityLabel.setGeometry(QRect(10, 100, 81, 31))
        self.QuantityLabel.setFont(font)
        self.Quantity = QSpinBox()
        self.Quantity.setMaximum(1000)
        self.Quantity.setObjectName(u"Quantity")
        self.Quantity.setMinimum(1)
        self.Quantity.setGeometry(QRect(80, 100, 51, 31))
        self.QuantityLabel.setText(QCoreApplication.translate("AddUnitWindow", u"Quantity", None))
        self.QuantityLayout.addWidget(self.QuantityLabel)
        self.QuantityLayout.addWidget(self.Quantity)
        self.Quantity.setValue(1)


        self.UnitTypeSelection = QComboBox()
        self.UnitTypeSelection.setObjectName(u"UnitTypeSelection")
        self.UnitTypeSelection.setGeometry(QRect(10, 10, 191, 31))
        self.UnitTypeSelection.setLayoutDirection(Qt.LeftToRight)
        self.searchUnits = QLineEdit()
        self.searchUnits.setPlaceholderText("Search Units...")
        
        self.ownerLayout = QHBoxLayout()
        self.OwnerLabel =QLabel()
        self.OwnerLabel.setFont(font)
        self.OwnerLabel.setText("Owner:")
        self.OwnerDropdown = QComboBox()
        self.ownerLayout.addWidget(self.OwnerLabel)
        self.ownerLayout.addWidget(self.OwnerDropdown)

        self.buttonLayout = QHBoxLayout()
        self.addtoall = QPushButton("Add To All Planets")
        self.add = QPushButton("Add")
        self.cancel = QPushButton("Cancel")

        self.buttonLayout.addWidget(self.addtoall)
        self.buttonLayout.addWidget(self.add)
        self.buttonLayout.addWidget(self.cancel)

        

        self.layout.addWidget(self.UnitTypeSelection)
        self.layout.addWidget(self.searchUnits)
        self.layout.addLayout(self.QuantityLayout)
        self.layout.addLayout(self.ownerLayout)
        self.layout.addLayout(self.buttonLayout)
        
        self.dialogWindow.setWindowTitle('Add Starting Forces')
        self.dialogWindow.setLayout(self.layout)
        self.signal = pyqtSignal(list)
        self.cancel.clicked.connect(self.dialogWindow.reject)
    def update_unit_box(self, unit_list):
        for i in unit_list:
            self.UnitTypeSelection.addItem(i.name)
    def show(self):
        self.dialogWindow.exec()
    def on_completion(self):
        quantity = self.Quantity.value()
        unit_name = self.UnitTypeSelection.currentText()
        self.signal.emit(list(quantity, unit_name, self.planet))
        

class EditUnitWindow:
    def __init__(self, object,campaign, repository):
        self.obj = object
        self.campaign  = campaign
        self.repository = repository
        self.dialogWindow = QDialog()
        self.dialogWindow.setWindowIcon(QIcon('eawIcon.png'))
        self.layout = QVBoxLayout()

        font = QFont()
        font.setPointSize(10)



        self.QuantityLayout = QHBoxLayout()
        self.QuantityLabel = QLabel()
        self.QuantityLabel.setObjectName(u"QuantityLabel")
        self.QuantityLabel.setGeometry(QRect(10, 100, 81, 31))
        self.QuantityLabel.setFont(font)
        self.Quantity = QSpinBox()
        self.Quantity.setMaximum(1000)
        self.Quantity.setObjectName(u"Quantity")
        self.Quantity.setGeometry(QRect(80, 100, 51, 31))
        self.QuantityLabel.setText("Quantity")
        self.QuantityLayout.addWidget(self.QuantityLabel)
        self.QuantityLayout.addWidget(self.Quantity)
        self.Quantity.setValue(1)


        self.UnitTypeSelection = QComboBox()
        self.UnitTypeSelection.setObjectName(u"UnitTypeSelection")
        self.UnitTypeSelection.setGeometry(QRect(10, 10, 191, 31))
        self.UnitTypeSelection.setLayoutDirection(Qt.LeftToRight)
        

        self.ownerLayout = QHBoxLayout()
        self.OwnerLabel =QLabel()
        self.OwnerLabel.setFont(font)
        self.OwnerLabel.setText("Owner:")
        self.OwnerDropdown = QComboBox()
        self.ownerLayout.addWidget(self.OwnerLabel)
        self.ownerLayout.addWidget(self.OwnerDropdown)

        self.SaveButton = QPushButton("Save Forces Entry")
        self.DeleteButton = QPushButton("Delete Forces Entry")
        self.CancelButton = QPushButton("Cancel ")


        self.Quantity.setValue(self.obj.quantity)
        for i in self.repository.factions:
            self.OwnerDropdown.addItem(i.name)
        for i in self.repository.units:
            self.UnitTypeSelection.addItem(i.name)
        self.OwnerDropdown.setCurrentText(self.obj.owner)
        self.UnitTypeSelection.setCurrentText(self.obj.unit)


        self.layout.addWidget(self.UnitTypeSelection)
        self.layout.addLayout(self.QuantityLayout)
        self.layout.addLayout(self.ownerLayout)
        self.layout.addWidget(self.SaveButton)        
        self.layout.addWidget(self.DeleteButton)  
        self.layout.addWidget(self.CancelButton)  

        self.dialogWindow.setWindowTitle('Edit Starting Forces')
        self.dialogWindow.setLayout(self.layout)
        self.CancelButton.clicked.connect(self.dialogWindow.accept)
        self.DeleteButton.clicked.connect(self.deleteObject)
        self.SaveButton.clicked.connect(self.SaveObject)
    def deleteObject(self):
        self.campaign.starting_forces.remove_obj(self.obj)
        self.dialogWindow.accept()
    def SaveObject(self):
        self.obj.unit = self.UnitTypeSelection.currentText()
        self.obj.owner = self.OwnerDropdown.currentText()
        self.obj.quantity = self.Quantity.value()
        self.dialogWindow.accept()
