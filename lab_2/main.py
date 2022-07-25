import sys
from PyQt5.QtWidgets import QApplication
from main_window import MainWindow

app = QApplication(sys.argv)
win = MainWindow(500, 500)
win.show()
sys.exit(app.exec_())
