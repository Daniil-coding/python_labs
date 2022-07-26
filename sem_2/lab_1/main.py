import tkinter as tk
from Interface import Interface
from calc_utils import CalcButton
from tkinter import messagebox

def show_info():
    s = ''
    s += 'Written by Daniil Machilskiy.\n'
    s += 'The program applies chosen operation to two binary numbers.\n'
    s += 'The numbers can be float (with dot).\n'
    s += 'Here are two input windows.\n'
    s += 'Enter binary numbers and click calculate button.'
    messagebox.showinfo('program info', s)

def show_history():
    s = ''
    for i, (a, b, oper, res) in enumerate(interface.history):
        s += f'{i + 1}) {a} {oper} {b} = {res}\n\n'
    messagebox.showinfo('history', s)

def clear_first():
    interface.a_in.clear()

def clear_second():
    interface.b_in.clear()

def clear_output():
    interface.res_field.set_text('')

def clear_input():
    clear_first()
    clear_second()

def clear_all():
    clear_input()
    clear_output()

def clear_history():
    interface.history.clear()

win = tk.Tk()
win.geometry('1000x650')
win.title('binary calculator')
win.maxsize(1000, 650)
win.minsize(500, 300)

clear_menu = tk.Menu(win)
clear_menu.add_command(label='clear first', command=clear_first)
clear_menu.add_command(label='clear second', command=clear_second)
clear_menu.add_command(label='clear input', command=clear_input)
clear_menu.add_command(label='clear output', command=clear_output)
clear_menu.add_command(label='clear all', command=clear_all)
clear_menu.add_command(label='clear history', command=clear_history)

menu = tk.Menu(win)
menu.add_cascade(label='clear', menu=clear_menu)
menu.add_command(label='history', command=show_history)
menu.add_command(label='info', command=show_info)
win.config(menu=menu)

interface = Interface(win)
interface.frame.place(relheight=0.85, relwidth=1)
menu.add_command(label='calculate', command=interface.calc)

cb = CalcButton(win)
cb.frame.place(rely=0.85, relwidth=1, relheight=0.15)
cb.bind_action(interface.calc)

win.mainloop()