from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem
from calc_utils import set

class TableWidget(QWidget):
    def resizeEvent(self, event) -> None:
        set(self.tabwid, self, 0, 0, 1, 1)

        w = int(round(self.tabwid.width() / self.tabwid.columnCount(), 0))
        for i in range(self.tabwid.columnCount()):
            self.tabwid.setColumnWidth(i, w)

        if self.tabwid.rowCount() == 0:
            h = 0
        else:
            h = int(round(self.tabwid.height() / self.tabwid.rowCount(), 0))
        for i in range(self.tabwid.rowCount()):
            self.tabwid.setRowHeight(i, h)

    def __init__(self):
        super().__init__()
        self.tabwid = QTableWidget(self)
        self.tabwid.setRowCount(1)
        self.tabwid.setColumnCount(1)
        self.setGeometry(300, 300, 1000, 500)

    def initialize(self, table):
        self.font = QFont()
        self.font.setPointSize(20)
        self.tabwid.setColumnCount( len(table[0]) )
        self.tabwid.setRowCount( len(table) - 1 )
        self.tabwid.setHorizontalHeaderLabels(table[0])
        self.tabwid.setVerticalHeaderLabels([''] * len(table))
        for i in range(1, len(table)):
            for j in range(len(table[0])):
                item = QTableWidgetItem()
                item.setText( table[i][j] )
                item.setTextAlignment(Qt.AlignCenter)
                item.setFont(self.font)
                self.tabwid.setItem(i - 1, j, item)