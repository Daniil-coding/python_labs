import os
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
import sys
from DrawField import DrawField
from PIL import Image
from utils import set

was_resized = False

def moveEvent(event):
    field.screen_x = win.x() + field.x()
    field.screen_y = win.y() + field.y()
    global was_resized
    if was_resized:
        field.screen_y += 37

def resizeEvent(event):
    set(circle_btn, win, 0.02, 0.88, 0.27, 0.1)
    set(dot_btn, win, 0.31, 0.88, 0.27, 0.1)
    set(adjust_btn, win, 0.6, 0.88, 0.27, 0.1)
    set(delete_btn, win, 0.89, 0.88, 0.09, 0.1)
    set(solve_btn, win, 0.4, 0.01, 0.2, 0.09)
    set(field, win, 0.02, 0.11, 0.96, 0.76)
    os.system('rm resized_delete.jpeg')
    del_img = Image.open('delete.jpeg')
    del_img = del_img.resize((delete_btn.width(), delete_btn.height() - 4))
    del_img.save('resized_delete.jpeg')
    delete_btn.setStyleSheet("background-image: url(resized_delete.jpeg);")
    moveEvent(None)
    global was_resized
    was_resized = True

app = QApplication(sys.argv)
win = QWidget()
win.setGeometry(200, 250, 1500, 700)
win.setMinimumSize(300, 250)
font = QFont('Calibri', 20)

circle_btn = QPushButton(win)
circle_btn.setFont(font)
circle_btn.setText('+ circle')

dot_btn = QPushButton(win)
dot_btn.setFont(font)
dot_btn.setText('+ point')
dot_btn.setStyleSheet('border-radius: 10px; background: white; border: 1px solid #193441;')

field = DrawField(win)
field.ord_mode()
circle_btn.clicked.connect(field.arc_mode)
dot_btn.clicked.connect(field.dot_mode)
circle_btn.setStyleSheet('border-radius: 10px; background: white; border: 1px solid #193441;')

adjust_btn = QPushButton(win)
adjust_btn.setText('settings')
adjust_btn.setFont(font)
adjust_btn.clicked.connect(field.adjust_action)
adjust_btn.setStyleSheet('border-radius: 10px; background: white; border: 1px solid #193441;')

delete_btn = QPushButton(win)
image = Image.open('delete.jpeg')
image.save('resized_delete.jpeg')
del image
delete_btn.setStyleSheet("background-image: url(resized_delete.jpeg);")
delete_btn.clicked.connect(field.delete_action)

solve_btn = QPushButton(win)
solve_btn.setText('solve')
solve_btn.setFont(font)
solve_btn.setStyleSheet('border-radius: 20px; background: green; border: 1px solid #193441;')
solve_btn.clicked.connect(field.solve_action)

win.resizeEvent = resizeEvent
win.moveEvent = moveEvent
win.show()
was_resized = False
sys.exit(app.exec_())