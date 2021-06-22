import sys
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QTextEdit, QLabel, QShortcut, QFileDialog, QMessageBox
from PyQt5.QtGui import QKeySequence
from PyQt5 import Qt

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.file_path = None

        self.open_new_file_shortcut = QShortcut(QKeySequence('Ctrl+O'), self)
        self.open_new_file_shortcut.activated.connect(self.open_new_file)

        self.save_current_file_shortcut = QShortcut(QKeySequence('Ctrl+S'), self)
        self.save_current_file_shortcut.activated.connect(self.save_current_file)

        vbox = QVBoxLayout()
        text = "Untitled File"
        self.title = QLabel(text)
        self.title.setWordWrap(True)
        self.title.setAlignment(Qt.Qt.AlignCenter)
        vbox.addWidget(self.title)
        self.setLayout(vbox)

        self.scrollable_text_area = QTextEdit()
        vbox.addWidget(self.scrollable_text_area)

    def open_new_file(self):
        self.file_path, filter_type = QFileDialog.getOpenFileName(self, "Open new file","", "All files (*)")
        if self.file_path:
            with open(self.file_path, "r") as f:
                file_contents = f.read()
                self.title.setText(self.file_path)
                self.scrollable_text_area.setText(file_contents)
        else:
            self.invalid_path_alert_message()

    def save_current_file(self):
        if not self.file_path:
            new_file_path, filter_type = QFileDialog.getSaveFileName(self, "Save this file as...", "", "All files (*)")
            if new_file_path:
                self.file_path = new_file_path
            else:
                self.invalid_path_alert_message()
                return False
        file_contents = self.scrollable_text_area.toPlainText()
        with open(self.file_path, "w") as f:
            f.write(file_contents)
        self.title.setText(self.file_path)

    def closeEvent(self, event):
        messageBox = QMessageBox()
        title = "Quit Application?"
        message = "WARNING !!\n\nIf you quit without saving, any changes made to the file will be lost.\n\nSave file before quitting?"
       
        reply = messageBox.question(self, title, message, messageBox.Yes | messageBox.No |
                messageBox.Cancel, messageBox.Cancel)
        if reply == messageBox.Yes:
            return_value = self.save_current_file()
            if return_value == False:
                event.ignore()
        elif reply == messageBox.No:
            event.accept()
        else:
            event.ignore()

    def invalid_path_alert_message(self):
        messageBox = QMessageBox()
        messageBox.setWindowTitle("Invalid file")
        messageBox.setText("Selected filename or path is not valid. Please select a valid file.")
        messageBox.exec()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Window()
    w.showMaximized()
    sys.exit(app.exec_())