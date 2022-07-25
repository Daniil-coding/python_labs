from math import log
from PyQt5.QtWidgets import QMessageBox, QWidget
from math import *
import matplotlib.pyplot as plt
import numpy as np

graphics_step = 0.001
E = 1e-20
sgn = lambda x: 0 if abs(x) < E else 1 if x > 0 else -1

def set(widget, window, relx, rely, relw, relh):
    x = int(window.width() * relx)
    y = int(window.height() * rely)
    width = int(window.width() * relw)
    height = int(window.height() * relh)
    widget.setGeometry(x, y, width, height)

def root_binsearch(f, l, r, eps, iter_limit):
    iter_count = 0
    while r - l >= eps:
        iter_limit -= 1
        iter_count += 1
        if iter_limit < 0:
            return (r + l) / 2, iter_count
        m = (l + r) / 2
        if sgn(f(m)) == sgn(f(l)):
            l = m
        else:
            r = m
    if sgn(f(l)) == sgn(f(r)):
        return None
    x = (l + r) / 2
    return x, iter_count

def show_error(message):
    widget = QWidget()
    QMessageBox.critical(widget, 'Error', message, QMessageBox.Discard)

def derivative(f, eps):
    def deriv(x):
        try:
            dy = f(x + eps) - f(x)
            return dy / eps
        except:
            return None
    return deriv

def search_root(f, x, h, eps, max_iter):
    try:
        if sgn(f(x)) == sgn(f(x + h)) and sgn(f(x)) != 0:
            return None
    except:
        return None
    error_code = 0
    try:
        value = root_binsearch(f, x, x + h, eps, max_iter)
        if value[1] > max_iter:
            error_code = 1
    except:
        return None
    return assemble_root(f, value[0], x, h, value[1], error_code)

def assemble_root(f, value, x, h, iter_count, error_code):
    root = dict()
    x1 = round(x, 3)
    x2 = round(x + h, 3)
    sec_name = '[' + str(x1) + '; ' + str(x2) + ']'
    root['sec_name'] = sec_name
    root['error_code'] = error_code
    root['point'] = value
    root['value'] = f(value)
    root['iter_count'] = iter_count
    return root

def to_function(expr):
    fun = lambda x: eval(expr.replace('x', f'({str(x)})'))
    def f(x):
        try:
            return fun(x)
        except:
            return None
    return f

def show_graph(f, roots, extremums, inflecions, l, r):
    n = int((r - l) / graphics_step) + 1
    x = np.linspace(l, r, n)
    try:
        y = [f(num) for num in x]
    except:
        show_error('Function is not defined at each point of the section.')
        return

    plt.minorticks_on()
    plt.grid(axis='both')
    plt.plot(x, y)

    x = [inflecion['point'] for inflecion in inflecions if inflecion['error_code'] == 0]
    y = [f(num) for num in x]
    plt.scatter(x, y, color='yellow', label='inflections')

    x = [root['point'] for root in roots if root['error_code'] == 0]
    y = [f(num) for num in x]
    plt.scatter(x, y, color='green', label='roots')

    x = [extremum['point'] for extremum in extremums if extremum['error_code'] == 0]
    y = [f(num) for num in x]
    plt.scatter(x, y, color='red', label='extremums')

    plt.legend()
    plt.show()

def build_table(roots, eps):
    accuracy = int(-log(eps, 10))
    table = [["№", "[x1; x2]", "x'", "f(x')", "Количество итераций", "Код ошибки"]]
    for i, root in enumerate(roots):
        table_row = [str(i + 1)]
        table_row.append(root['sec_name'])
        x = round(root['point'], accuracy)
        table_row.append( str(x) )
        y = round(root['value'], accuracy)
        table_row.append( str(y) )
        n = root['iter_count']
        table_row.append(str(n))
        table_row.append(str(root['error_code']))
        table.append(table_row)
    return table