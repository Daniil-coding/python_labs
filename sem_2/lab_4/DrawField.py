import pyautogui
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtWidgets import QWidget, QMessageBox
from InputWindow import InputWindow
from shapes import *
from utils import *

class DrawField(QWidget):

    linked_circle = None
    linked_dot = None

    def __init__(self, win):
        super(DrawField, self).__init__(win)
        self.screen_x = 0
        self.screen_y = 0
        self.painter = QPainter()
        self.circles = []
        self.dots = []
        self.timer = QTimer()
        self.timer.setInterval(2)
        self.timer.timeout.connect(self.timeStep)
        self.timer.start()
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.setStyleSheet('background-color: #a3ecf7')

    def paintEvent(self, event) -> None:

        def drawCircle(circle):
            x = circle.x
            y = circle.y
            r = circle.r
            self.painter.drawEllipse(x - r, y - r, r * 2, r * 2)

        self.painter.begin(self)

        pen = QPen()
        pen.setWidth(2)
        self.painter.setPen(pen)
        color = Qt.blue
        if self.linked_circle is not None:
            drawCircle(self.linked_circle)

        for circle in self.circles:
            if circle.highlight:
                color = Qt.red
            pen.setColor(color)
            self.painter.setPen(pen)
            drawCircle(circle)
            color = Qt.blue

        pen.setWidth(5)
        self.painter.setPen(pen)
        if self.linked_dot is not None:
            self.painter.drawPoint(self.linked_dot.x, self.linked_dot.y)

        for dot in self.dots:
            if dot.highlight:
                color = Qt.red
            pen.setColor(color)
            self.painter.setPen(pen)
            self.painter.drawPoint(dot.x, dot.y)
            color = Qt.blue

        self.painter.end()

    def nearest_shape(self, mouse, highlight=None, max_dist=5):
        obj = ('', 0)
        min_dist = None

        for i, circle in enumerate(self.circles):
            if highlight is not None and highlight != circle.highlight:
                continue
            r = dist_arc(mouse, circle)
            if r > max_dist:
                continue
            if min_dist is None or r < min_dist:
                min_dist = r
                obj = ('circle', i)

        for i, dot in enumerate(self.dots):
            if highlight is not None and highlight != dot.highlight:
                continue
            r = dist(mouse, dot)
            if r > max_dist:
                continue
            if min_dist is None or r < min_dist:
                min_dist = r
                obj = ('dot', i)

        if obj[0] == '':
            return None
        return obj

    def mouseClick_ord(self, event) -> None:
        mouse = self.mouseDot()
        if self.linked_circle is not None:
            center = self.linked_circle.center()
            self.linked_circle.r = int(round(dist(center, mouse), 0))
            self.circles.append(self.linked_circle)
            self.linked_circle = None
            self.update()
            return
        if self.linked_dot is not None:
            self.linked_dot.x = mouse.x
            self.linked_dot.y = mouse.y
            self.dots.append(self.linked_dot)
            self.linked_dot = None
            self.update()
            return
        obj = self.nearest_shape(mouse)
        if obj is None:
            for circle in self.circles:
                circle.highlight = False
            for dot in self.dots:
                dot.highlight = False
            self.update()
            return
        i = obj[1]
        if obj[0] == 'circle':
            if self.circles[i].highlight:
                self.circles[i].highlight = False
            else:
                self.circles[i].highlight = True
        elif obj[0] == 'dot':
            if self.dots[i].highlight:
                self.dots[i].highlight = False
            else:
                self.dots[i].highlight = True
        self.update()

    def mouseClick_arc(self, event) -> None:
        self.linked_dot = None
        mouse = self.mouseDot()
        self.linked_circle = Circle(mouse.x, mouse.y, 0)
        self.ord_mode()

    def mouseClick_dot(self, event) -> None:
        self.dots.append(self.linked_dot)
        self.linked_dot = None
        self.ord_mode()

    def timeStep(self):
        self.mouseMoveProcessing()
        self.update()

    def mouseDot(self):
        mouse = Dot(*pyautogui.position())
        mouse.x -= self.screen_x
        mouse.y -= self.screen_y
        return mouse

    def solve_action(self):
        if len(self.circles) == 0:
            return
        count = []
        for circle in self.circles:
            n = 0
            for dot in self.dots:
                if inside(dot, circle):
                    n += 1
            count.append(abs(len(self.dots) - 2 * n))
        max_val = count[0]
        for val in count:
            if val > max_val:
                max_val = val
        for i, circle in enumerate(self.circles):
            circle.highlight = count[i] == max_val

    def mouseMoveProcessing(self) -> None:
        mouse = self.mouseDot()
        if self.linked_circle is not None:
            self.linked_circle.r = int(round(dist(self.linked_circle.center(), mouse), 0))
            return
        if self.linked_dot is not None:
            self.linked_dot = mouse
            return
        obj = self.nearest_shape(mouse, highlight=True, max_dist=self.width() / 20)
        if obj is None:
            return
        i = obj[1]
        if obj[0] == 'circle' and self.circles[i].highlight:
            self.circles[i].r = dist(mouse, self.circles[i].center())
        elif obj[0] == 'dot' and self.dots[i].highlight:
            self.dots[i].x = mouse.x
            self.dots[i].y = mouse.y

    def ord_mode(self):
        self.mousePressEvent = self.mouseClick_ord

    def arc_mode(self):
        self.linked_dot = self.mouseDot()
        self.mousePressEvent = self.mouseClick_arc

    def dot_mode(self):
        mouse = self.mouseDot()
        self.linked_dot = Dot(mouse.x, mouse.y)
        self.mousePressEvent = self.mouseClick_dot

    def delete_action(self):
        mb = QMessageBox()
        mb.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        mb.setText("Are you sure?")
        ans = mb.exec_()
        if ans == QMessageBox.No:
            return

        indexes = [i for i in range(len(self.circles)) if self.circles[i].highlight]
        self.circles = remove(self.circles, indexes)
        indexes = [i for i in range(len(self.dots)) if self.dots[i].highlight]
        self.dots = remove(self.dots, indexes)

    def show_error(self, message):
        widget = QWidget()
        QMessageBox.critical(widget, 'Error', message, QMessageBox.Discard)

    def adjust_arc_action(self, indexes):
        dialog = InputWindow(3)
        dialog.add_hint('radius', 0)
        dialog.add_hint('x coordinate', 1)
        dialog.add_hint('y coordinate', 2)
        dialog.setGeometry(500, 300, 300, 100)
        dialog.exec()
        try:
            r = int(dialog.data[0]) if dialog.data[0] is not None else None
            x = int(dialog.data[1]) if dialog.data[1] is not None else None
            y = int(dialog.data[2]) if dialog.data[2] is not None else None
        except:
            self.show_error('Input data is invalid.')
            return
        for i in indexes:
            if r is not None:
                self.circles[i].r = r
            if x is not None:
                self.circles[i].x = x
            if y is not None:
                self.circles[i].y = y
        self.circles = unique(self.circles)

    def adjust_dot_action(self, indexes):
        dialog = InputWindow(2)
        dialog.add_hint('x coordinate', 0)
        dialog.add_hint('y coordinate', 1)
        dialog.setGeometry(500, 300, 300, 100)
        dialog.exec()
        x = float(dialog.data[0]) if dialog.data[0] is not None else None
        y = float(dialog.data[1]) if dialog.data[1] is not None else None
        for i in indexes:
            if x is not None:
                self.dots[i].x = x
            if y is not None:
                self.dots[i].y = y
        self.dots = unique(self.dots)

    def adjust_action(self):
        cir_ind = [i for i in range(len(self.circles)) if self.circles[i].highlight]
        dot_ind = [i for i in range(len(self.dots)) if self.dots[i].highlight]
        if len(cir_ind) > 0 and len(dot_ind) > 0:
            self.show_error('Highlighted objects are not one type.')
            return
        if len(cir_ind) > 0:
            self.adjust_arc_action(cir_ind)
        elif len(dot_ind) > 0:
            self.adjust_dot_action(dot_ind)
