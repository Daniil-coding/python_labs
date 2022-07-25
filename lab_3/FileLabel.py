from PyQt5.QtWidgets import QLabel

class FileLabel(QLabel):
    def __init__(self, window, name):
        super().__init__(window)
        self.name = name
        self.setStyleSheet("Windows")
        self.setText(name)