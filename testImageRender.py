import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import *

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 image - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
    
        # Create widget
        label = QLabel(self)
        pixmap = QPixmap('C:\Program Files (x86)\Steam\SteamApps\common\Star Wars Empire at War\corruption\Mods\Rise-Of-The-Sith-Lords\Rise-Of-The-Sith-Lords.ico')
        pixmap = pixmap.scaled(50, 50, Qt.KeepAspectRatio, Qt.FastTransformation)
        label.setPixmap(pixmap)
        self.resize(50,50)
        
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
