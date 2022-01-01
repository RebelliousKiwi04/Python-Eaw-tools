from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys

class CampaignPropertiesWindow:
    def __init__(self, campaign):
        self.dialogWindow = QDialog()
        self.layout = QVBoxLayout()

        
        font = QFont()
        font.setPointSize(9)


        self.CampaignSetLayout = QHBoxLayout()
        self.CampaignSetLabel = QLabel()
        self.CampaignSetLabel.setFont(font)
        self.CampaignSetLabel.setText("Campaign Set Name")
        self.CampaignSet = QLineEdit()
        self.CampaignSetLayout.addWidget(self.CampaignSetLabel)
        self.CampaignSetLayout.addWidget(self.CampaignSet)
        self.NameLayout = QHBoxLayout()
        self.NameLabel = QLabel()
        self.NameLabel.setFont(font)
        self.NameLabel.setText("Campaign Name")
        self.Name = QLineEdit()
        self.NameLayout.addWidget(self.NameLabel)
        self.NameLayout.addWidget(self.Name)
        self.Name.setText(campaign.name)


        self.OkCancelButtons = QDialogButtonBox()
        self.OkCancelButtons.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.OkCancelButtons.accepted.connect(self.dialogWindow.accept)
        self.OkCancelButtons.rejected.connect(self.dialogWindow.reject)
        self.layout.addLayout(self.NameLayout)
        self.layout.addLayout(self.CampaignSetLayout)
        self.layout.addWidget(self.OkCancelButtons)
        self.dialogWindow.setWindowTitle('Campaign Properties')
        self.dialogWindow.setLayout(self.layout)
        self.dialogWindow.exec()
        
# app = QApplication(sys.argv)
# ui = CampaignPropertiesWindow()
# ui.dialogWindow.exec()
# sys.exit(app.exec_())