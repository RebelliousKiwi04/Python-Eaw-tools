from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class AddFactionWindow:
    def __init__(self, campaignset, repository):
        self.campaignset = campaignset
        self.repository = repository
        self.dialogWindow = QDialog()
        self.dialogWindow.setWindowTitle("Add Faction")
        self.layout = QVBoxLayout()

        self.factionLayout = QHBoxLayout()
        self.factionLabel = QLabel("Faction: ")
        self.faction = QComboBox()
        self.factionLayout.addWidget(self.factionLabel)
        self.factionLayout.addWidget(self.faction)

        self.buttons = QDialogButtonBox()
        self.buttons.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.layout.addLayout(self.factionLayout)
        self.layout.addWidget(self.buttons)
        self.dialogWindow.setLayout(self.layout)
        
        for faction in repository.factions:
            if faction.name not in campaignset.playableFactions.keys():
                self.faction.addItem(faction.name)
        #[p.name for p in repository.factions]
        self.buttons.accepted.connect(self.dialogWindow.accept)
        self.buttons.rejected.connect(self.dialogWindow.reject)
        