from PyQt5.QtWidgets import QHeaderView, QTableWidget

class PyQtUtil:
    def construct_table_widget(label, columns):
        '''Constructs an arbitrary table widget'''
        tableWidget: QTableWidget = QTableWidget()
        tableWidget.setColumnCount(columns)
        tableWidget.setHorizontalHeaderLabels(label)
        tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        tableWidget.verticalHeader().setVisible(False)
        return tableWidget