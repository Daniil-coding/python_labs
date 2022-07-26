import tkinter as tk
from tkinter import ttk

class NumberEntry:
    def __init__(self, win):
        self.frame = tk.Frame(win)

        self.entry = tk.Entry(self.frame)
        self.entry.place(relx=0.15, relwidth=0.45, relheight=1)
        self.entry.config(font=('Italic', '20'))

        self.sgn = tk.Button(self.frame, text='+', command=self.change_sgn)
        self.sgn.place(relx=0.075, relwidth=0.075, relheight=1)
        self.sgn.config(font=('Italic', '30'))

        self.dot = tk.Button(self.frame, text='.', command=lambda: self.add('.'))
        self.dot.place(relwidth=0.075, relheight=1)
        self.dot.config(font=('Italic', '30'))

        self.backspace = tk.Button(self.frame, text='backspace')
        self.backspace.place(relx=0.6, relwidth=0.1, relheight=1)
        self.backspace['command'] = self.pop
        self.backspace.config(font=('Italic', '10'))

        self.keyboard = BinKeyBoard(self.frame)
        self.keyboard.zero['command'] = self.print_zero
        self.keyboard.one['command'] = self.print_one
        self.keyboard.frame.place(relx=0.7, relwidth=0.2, relheight=1)

        self.clear_button = tk.Button(self.frame, text='clear')
        self.clear_button.place(relx=0.9, relwidth=0.1, relheight=1)
        self.clear_button['command'] = self.clear
        self.clear_button.config(font=('Italic', '10'))

    def change_sgn(self):
        self.sgn['text'] = '-' if self.sgn['text'] == '+' else '+'

    def print_zero(self):
        self.entry.insert(tk.END, '0')

    def clear(self):
        self.entry.delete(0, tk.END)

    def print_one(self):
        self.entry.insert(tk.END, '1')

    def get(self):
        return self.entry.get()

    def get_sgn(self):
        return self.sgn['text']

    def add(self, text):
        self.entry.insert(tk.END, text)

    def pop(self):
        self.entry.delete(len(self.entry.get()) - 1)

class OperatorSelector:
    def __init__(self, win):
        self.frame = tk.Frame(win)
        self.combobox = ttk.Combobox(self.frame)
        self.combobox['values'] = ('+', '-', '*')
        self.combobox['justify'] = 'center'
        self.combobox.current(0)
        self.combobox.place(relwidth=1, relheight=1)
        self.combobox.config(font=('Italic', '30'))

    def get(self):
        return self.combobox.get()

class ResultField:
    def __init__(self, win):
        self.frame = tk.Frame(win)
        self.label = tk.Label(self.frame)
        self.label['bg'] = '#d1f8f9'
        self. label['relief'] = 'raised'
        self.label.place(relwidth=1, relheight=1)
        self.label.config(font=('Arial', '30', 'bold'))

        self.clear_btn = tk.Button(self.frame, text='clear')
        self.clear_btn.place(relx=0.9, relwidth=0.1, relheight=0.4)
        self.clear_btn['command'] = lambda: self.set_text('')
        self.clear_btn.config(font=('Arial', '10'))

    def set_text(self, string):
        self.label['text'] = string

    def get(self):
        return self.label['text']

class BinKeyBoard:
    def __init__(self, win):
        self.frame = tk.Frame(win)

        self.zero = tk.Button(self.frame, text = '0')
        self.one = tk.Button(self.frame, text = '1')

        self.zero.place(relwidth=0.5, relheight=1)
        self.one.place(relx=0.5, relwidth=0.5, relheight=1)

        self.zero.config(font=('Italic', '20'))
        self.one.config(font=('Italic', '20'))

    def bind_action(self, index, action):
        self.buttons[index]['command'] = action