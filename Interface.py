from IOManager import NumberEntry, OperatorSelector, ResultField
from calc_utils import sum, sub, mul, format, move_dot
from tkinter import Frame, messagebox, Label, Button
from PIL import Image, ImageTk

class Interface:
    def __init__(self, win):
        self.frame = Frame(win)
        self.frame['bg'] = '#ecf566'
        load = Image.open("background.png")
        load.thumbnail((1000, 1000), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(load)
        label = Label(self.frame, image=render)
        label.image = render
        label.place(relwidth=1, relheight=1)

        self.res_field = ResultField(self.frame)
        self.res_field.frame.place(relx=0.1, rely=0.05, relwidth=0.8, relheight=0.3)

        self.a_in = NumberEntry(self.frame)
        self.a_in.frame.place(relx=0.1, rely=0.4, relwidth=0.8, relheight=0.15)

        self.b_in = NumberEntry(self.frame)
        self.b_in.frame.place(relx=0.1, rely=0.8, relwidth=0.8, relheight=0.15)

        self.opsel = OperatorSelector(self.frame)
        self.opsel.frame.place(relx=0.4, rely=0.6, relwidth=0.2, relheight=0.15)

        self.clear_all = Button(self.frame, text='clear all')
        self.clear_all.place(relx=0.7, rely=0.6, relwidth=0.1, relheight=0.15)
        self.clear_all['command'] = self.clearAll
        self.clear_all.config(font=('Italic', '10'))

        self.history = []

    def calc(self):

        def check(a):
            if len(a) == 0:
                return False
            if a.count('.') > 1:
                return False
            if a[0] == '.' or a[-1] == '.':
                return False
            for digit in a:
                if digit != '0' and digit != '1' and digit != '.':
                    return False
            return True

        a = self.a_in.entry.get()
        b = self.b_in.entry.get()
        sgn_a = self.a_in.get_sgn()
        sgn_b = self.b_in.get_sgn()
        operation = self.opsel.get()
        '''if sgn_a != '+' and sgn_a != '-':
            messagebox.showerror('Error', 'The first number sign is invalid.')
            return
        if sgn_b != '+' and sgn_b != '-':
            messagebox.showerror('Error', 'The second number sign is invalid.')
            return'''
        if not check(a):
            if len(a) == 0:
                messagebox.showerror('Error', 'The first field is empty.')
            else:
                messagebox.showerror('Error', 'The first number is invalid.')
            return
        if not check(b):
            if len(b) == 0:
                messagebox.showerror('Error', 'The second field is empty.')
            else:
                messagebox.showerror('Error', 'The second number is invalid.')
            return
        a, b = format(a), format(b)
        if a.find('.') == -1:
            a += '.'
        if b.find('.') == -1:
            b += '.'
        a_i = a.find('.')
        b_i = b.find('.')
        a_n = len(a) - a_i - 1
        b_n = len(b) - b_i - 1
        n = max(a_n, b_n)
        a += (n - a_n) * '0'
        a = a[:a_i] + a[a_i + 1:]
        b += (n - b_n) * '0'
        b = b[:b_i] + b[b_i + 1:]
        if operation == '+':
            if sgn_a == '-':
                if sgn_b == '-':
                    result = '-' + sum(a, b)
                else:
                    result = sub(b, a)
            else:
                if sgn_b == '-':
                    result = sub(a, b)
                else:
                    result = sum(a, b)
        elif operation == '-':
            if sgn_a == '-':
                if sgn_b == '-':
                    result = sub(b, a)
                else:
                    result = '-' + sum(a, b)
            else:
                if sgn_b == '-':
                    result = sum(a, b)
                else:
                    result = sub(a, b)
        elif operation == '*':
            result = ('' if sgn_a == sgn_b else '-') + mul(a, b)
        else:
            messagebox.showerror('Error', 'Operation is invalid.')
            return
        if operation == '*':
            n *= 2
        result = move_dot(result, n)
        result = format(result)
        self.res_field.set_text(result)
        self.update_history(sgn_a + a, sgn_b + b, operation, result)

    def clearAll(self):
        print('ok')
        self.a_in.clear()
        self.b_in.clear()
        self.res_field.set_text('')

    def update_history(self, a, b, operation, result):
        if a[0] == '+':
            a = a[1:]
        if b[0] == '+':
            b = b[1:]
        self.history.append( (a, b, operation, result) )