from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QScrollArea, QVBoxLayout, QFrame
from FileLabel import *
import os

DIALOG_GEOMETRY = (100, 100, 500, 300)

class FileSelector:
    def __init__(self, path):
        self.dialog = QDialog()
        self.dialog.setGeometry(*DIALOG_GEOMETRY)
        self._path = path
        self.dialog.resizeEvent = self.dialog_resize
        self.dialog.moveEvent = self.update_geometry

    def click_item(self, name):
        self.dialog.close()
        self.clear()
        if self._path != '/':
            self._path += '/'
        self._path += name
        try:
            self.initialize(self._path)
        except NotADirectoryError:
            return
        self.dialog.exec()

    def onClick(self, name):
        return lambda event: self.click_item(name)

    def dialog_resize(self, event):
        self.update_geometry(None)
        self.scroll.setGeometry(0, 0, self.dialog.width(), self.dialog.height())

    def update_geometry(self, event):
        x = self.dialog.x()
        y = self.dialog.y()
        w = self.dialog.width()
        h = self.dialog.height()
        global DIALOG_GEOMETRY
        DIALOG_GEOMETRY = (x, y, w, h)

    def initialize(self, path):
        try:
            dir_list = os.listdir(path)
        except NotADirectoryError:
            self.clear()
            self.dialog.close()
            raise NotADirectoryError
        self.labels = QVBoxLayout()
        self.scroll = QScrollArea(self.dialog)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.dialog_resize(None)
        h = self.dialog.height() // 10
        for i, name in enumerate(dir_list):
            label = FileLabel(self.scroll, name)
            label.setGeometry(0, h * i, self.dialog.width(), h)
            label.mousePressEvent = self.onClick(name)
            self.labels.addWidget(label)
        self.frame = QFrame()
        self.frame.setLayout(self.labels)
        self.scroll.setWidget(self.frame)

    def clear(self):
        del self.dialog
        self.dialog = QDialog()
        self.dialog.setGeometry(*DIALOG_GEOMETRY)
        self.dialog.resizeEvent = self.dialog_resize
        self.dialog.moveEvent = self.update_geometry

    def get_current_path(self):
        return self._path