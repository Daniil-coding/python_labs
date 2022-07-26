from PyQt5.QtWidgets import QDialog, QPushButton, QLineEdit
from utils import set


class InputWindow(QDialog):
    def __init__(self, n):
        super().__init__()
        self.data = None
        self.entries = []
        for i in range(n):
            self.entries.append( QLineEdit(self) )
        self.ok_btn = QPushButton(self)
        self.ok_btn.setText('ok')
        self.ok_btn.clicked.connect(self.close_action)

    def resizeEvent(self, event) -> None:
        h = 1 / len(self.entries)
        set(self.ok_btn, self, 0.85, 0.01, 0.14, 0.2)
        for i, entry in enumerate(self.entries):
            set(entry, self, 0.01, 0.01 + i * h, 0.98, h)

    def close_action(self):
        self.data = [None] * len(self.entries)
        for i, entry in enumerate(self.entries):
            text = entry.text()
            self.data[i] = text if text != '' else None
        self.close()

    def add_hint(self, hint, index):
        self.entries[index].setPlaceholderText(hint)