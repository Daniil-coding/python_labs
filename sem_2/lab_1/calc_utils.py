from tkinter import Frame, Button

class CalcButton:
    def __init__(self, win):
        self.frame = Frame(win)
        self.cb = Button(self.frame)
        self.cb.place(relwidth=1, relheight=1)
        self.cb['bg'] = '#5cf77e'
        self.cb['text'] = 'calculate'
        self.cb.config(font=('Italic', '35'))

    def bind_action(self, action):
        self.cb['command'] = action

def sum(a, b):
    res = ''
    a = '0' * ( len(b) - len(a) ) + a
    b = '0' * ( len(a) - len(b) ) + b
    delta = 0
    for i in range(len(a) - 1, -1, -1):
        val = int(a[i]) + int(b[i]) + delta
        res += str(val % 2)
        delta = val // 2
    if delta > 0:
        res += str(delta)
    res = res[::-1]
    return res

def mul(a, b):
    res = '0'
    for i in range(len(b) - 1, -1, -1):
        if b[i] == '1':
            res = sum(res, a)
        a += '0'
    return res

def move_dot(a, n):
    sgn = '+'
    if a[0] == '-' or a[0] == '+':
        sgn = a[0]
        a = a[1:]
    i = len(a) - n
    if i >= 0:
        a = a[:i] + '.' + a[i:]
        if i == 0:
            a = '0' + a
    else:
        tmp = '0' * (-i)
        a = '0.' + tmp + a
    if sgn == '-':
        a = sgn + a
    return a

def format(a):
    sgn = '+'
    if a[0] == '-' or a[0] == '+':
        sgn = a[0]
        a = a[1:]
    if a.find('.') == -1:
        a += '.'
    i = 0
    while a[i] == '0':
        i += 1
    a = a[i:]
    i = len(a) - 1
    while a[i] == '0':
        i -= 1
    a = a[ : i + 1 ]
    if a[0] == '.':
        a = '0' + a
    if a[-1] == '.':
        a = a[:-1]
    if sgn == '-':
        a = '-' + a
    return a

def inv(a):
    res = ''
    for digit in a:
        res += '0' if digit == '1' else '1'
    return res

def encode(a, n):
    sgn = '0'
    if a[0] == '-':
        sgn = '1'
        a = a[1:]
    a = '0' * (n - len(a) - 1) + a
    if sgn == '1':
        a = inv(a)
        a = sum(a, '1')
    return sgn + a

def sub(a, b):
    if b == '0':
        return a
    n = max(len(a), len(b)) + 1
    b = '-' + b
    a = encode(a, n)
    b = encode(b, n)
    res = sum(a, b)
    if len(res) == n + 1:
        res = res[1:]
    sgn, res = res[0], res[1:]
    if sgn == '1':
        res = inv(res)
        res = '-' + sum(res, '1')
    return format(res)