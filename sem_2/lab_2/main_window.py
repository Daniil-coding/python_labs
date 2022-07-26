from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLineEdit, QPushButton
from TableWidget import TableWidget
from calc_utils import *

class MainWindow(QWidget):

    def press(self):
        self.calc_btn.setStyleSheet("background-color: yellow")

    def resizeEvent(self, event) -> None:
        set(self.expr_in, self, 0.05, 0.04, 0.9, 0.12)
        set(self.lbound_in, self, 0.05, 0.2, 0.44, 0.12)
        set(self.rbound_in, self, 0.51, 0.2, 0.44, 0.12)
        set(self.stepsize_in, self, 0.05, 0.36, 0.9, 0.12)
        set(self.eps_in, self, 0.05, 0.52, 0.9, 0.12)
        set(self.maxiter_in, self, 0.05, 0.68, 0.9, 0.12)
        set(self.calc_btn, self, 0.05, 0.85, 0.4, 0.1)
        set(self.table_btn, self, 0.55, 0.85, 0.4, 0.1)

    def __init__(self, width, height):
        super(MainWindow, self).__init__()
        self.setGeometry(0, 0, width, height)
        self.setMinimumWidth(350)
        self.setMinimumHeight(300)
        self.table_window = TableWidget()

        font = QFont()
        font.setPointSize(20)

        expr_in = QLineEdit(self)
        expr_in.setStyleSheet("background-color: #8681e7")
        expr_in.setPlaceholderText("expresion")
        expr_in.setFont(font)
        self.expr_in = expr_in

        lbound_in = QLineEdit(self)
        lbound_in.setStyleSheet("background-color: #7197dc")
        lbound_in.setPlaceholderText("left bound")
        lbound_in.setFont(font)
        self.lbound_in = lbound_in

        rbound_in = QLineEdit(self)
        rbound_in.setStyleSheet("background-color: #7197dc")
        rbound_in.setPlaceholderText("right bound")
        rbound_in.setFont(font)
        self.rbound_in = rbound_in

        stepsize_in = QLineEdit(self)
        stepsize_in.setStyleSheet("background-color: #64bfd3")
        stepsize_in.setPlaceholderText("step size")
        stepsize_in.setFont(font)
        self.stepsize_in = stepsize_in

        eps_in = QLineEdit(self)
        eps_in.setStyleSheet("background-color: #72e5e7")
        eps_in.setPlaceholderText("accuracy")
        eps_in.setFont(font)
        self.eps_in = eps_in

        maxiter_in = QLineEdit(self)
        maxiter_in.setStyleSheet("background-color: #7bf3b4")
        maxiter_in.setPlaceholderText("greatest iteration count")
        maxiter_in.setFont(font)
        self.maxiter_in = maxiter_in

        calc_btn = QPushButton(self)
        calc_btn.setStyleSheet("background-color: #14aa05")
        calc_btn.pressed.connect( lambda: calc_btn.setStyleSheet("background-color: yellow") )
        calc_btn.released.connect( lambda: calc_btn.setStyleSheet("background-color: #14aa05") )
        calc_btn.setText("calculate")
        font.setPointSize(25)
        calc_btn.setFont(font)
        calc_btn.clicked.connect(self.build_graph)
        self.calc_btn = calc_btn

        table_btn = QPushButton(self)
        table_btn.setStyleSheet("background-color: #14aa05")
        table_btn.pressed.connect(lambda: table_btn.setStyleSheet("background-color: red"))
        table_btn.released.connect(lambda: table_btn.setStyleSheet("background-color: #14aa05"))
        table_btn.setText("show table")
        font.setPointSize(25)
        table_btn.setFont(font)
        table_btn.clicked.connect(self.show_table)
        self.table_btn = table_btn

    def get_input_data(self):
        expr = self.expr_in.text()
        l = self.lbound_in.text()
        try:
            l = float(l)
        except:
            show_error('Left bound value is invalid.')
            return
        r = self.rbound_in.text()
        try:
            r = float(r)
        except:
            show_error('Right bound value is invalid.')
            return
        if l >= r:
            show_error('Left bound is not less than the right.')
            return
        h = self.stepsize_in.text()
        try:
            h = float(h)
        except:
            show_error('Step size is invalid.')
            return
        if h < 0.01:
            show_error('Step size is under 0.01.')
            return
        eps = self.eps_in.text()
        try:
            eps = float(eps)
        except:
            show_error('Accuracy value is invalid.')
            return
        if eps <= 1e-9 or eps >= 0.9:
            show_error('Accuracy value should be in range (1e-9; 0.9).')
            return
        if eps + E >= h:
            show_error('Accuracy should be less than the step size.')
            return
        n = self.maxiter_in.text()
        try:
            n = int(n)
        except:
            show_error('Invalid maximum iteration count.')
            return
        if n <= 0:
            show_error('Maximum iteration count is under zero.')
            return
        return expr, l, r, h, eps, n

    def build_graph(self):
        data = self.get_input_data()
        if data is None:
            return
        f, l, r, h, eps, max_iter = data
        f = to_function(f)
        df = derivative(f, 1e-6)
        ddf = derivative(df, 1e-6)
        roots = []
        extremums = []
        inflections = []

        x = l
        while x + E < r:
            root = search_root(f, x, h, eps, max_iter)
            if root is not None:
                roots.append(root)

            value = search_root(df, x, h, eps, max_iter)
            if value is not None:
                extremums.append(value)

            value = search_root(ddf, x, h, eps, max_iter)
            if value is not None:
                inflections.append(value)

            x += h
        show_graph(f, roots, extremums, inflections, l, r)

    def show_table(self):
        data = self.get_input_data()
        if data is None:
            return
        f, l, r, h, eps, max_iter = data
        f = to_function(f)
        roots = []
        x = l
        while x + E < r:
            root = search_root(f, x, h, eps, max_iter)
            if root is not None:
                roots.append(root)
            x += h

        table = build_table(roots, eps)
        self.table_window.initialize(table)
        self.table_window.show()