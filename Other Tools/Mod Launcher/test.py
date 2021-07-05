from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import sys
class Window(QScrollArea):
    def __init__(self):
        super(Window, self).__init__()
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignTop)
        for index in range(100):
            layout.addWidget(QLabel('Label %02d' % index))
        self.setWidget(widget)
        self.setWidgetResizable(True)


app = QApplication(sys.argv)

window = QMainWindow()
basicWidget = QWidget()
ui = Window()

window.setCentralWidget(ui)
window.show()


sys.exit(app.exec_())
