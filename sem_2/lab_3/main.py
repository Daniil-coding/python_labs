from PIL import Image
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QDialog, QLineEdit, QLabel, QMessageBox
from PyQt5.QtGui import QFont
from FileSelector import FileSelector
import sys
import os

string = ''

def set(wid, win, relx, rely, relw, relh):
    width = win.width()
    height = win.height()
    x = int(relx * width)
    y = int(rely * height)
    width = int(width * relw)
    height = int(height * relh)
    wid.setGeometry(x, y, width, height)

def resizeEvent(event):
    set(str_btn, win, 0.05, 0.05, 0.45, 0.2)
    set(image_btn, win, 0.5, 0.05, 0.45, 0.2)
    set(showstr_btn, win, 0.05, 0.3, 0.45, 0.2)
    set(showimg_btn, win, 0.5, 0.3, 0.45, 0.2)
    set(hide_btn, win, 0.05, 0.55, 0.45, 0.2)
    set(decode_btn, win, 0.5, 0.55, 0.45, 0.2)
    set(save_btn, win, 0.05, 0.8, 0.9, 0.2)

def select_str():

    def resized(event):
        set(in_field, d, 0, 0, 1, 1)
        set(ok_btn, d, 0.85, 0, 0.15, 0.3)
        font.setPointSize(ok_btn.height() // 2)
        ok_btn.setFont(font)

    def save_input():
        result = in_field.text()
        global string
        string = result
        d.close()

    d = QDialog()
    d.setGeometry(100, 200, 500, 50)
    d.setWindowTitle('Click OK to finish the input.')
    font = QFont('Italic', 35)

    in_field = QLineEdit(d)
    in_field.setFont(font)

    font.setPointSize(10)
    ok_btn = QPushButton(d)
    ok_btn.setFont(font)
    ok_btn.setText('OK')
    ok_btn.clicked.connect(save_input)

    d.resizeEvent = resized
    d.exec()

def isimage(path):
    return path.endswith(".png")

def select_image():
    path = '/'
    fs = FileSelector(path)
    fs.initialize(path)
    fs.dialog.exec()
    if not isimage(fs.get_current_path()):
        show_error("Image wasn't selected or this file is not an image.")
        return None
    else:
        showimg_btn.clicked.disconnect()
        showimg_btn.clicked.connect(lambda event: show_image('initial.png'))
        return fs.get_current_path()

def show_image(path):
    try:
        image = Image.open(path)
    except:
        return
    image.show()
    image.close()

def show_string(s):
    dialog = QDialog()
    dialog.setGeometry(500, 300, 500, 50)
    field = QLabel(dialog)
    field.setFont(font)
    field.setText(s)
    dialog.resizeEvent = lambda event: set(field, dialog, 0, 0, 1, 1)
    dialog.exec()

def show_error(message):
    widget = QWidget()
    QMessageBox.critical(widget, 'Error', message, QMessageBox.Discard)

def hide(str, path, name):

    def pixel_mod(p, a):
        r = p[0] // 2 * 2 + a[0]
        g = p[1] // 2 * 2 + a[1]
        b = p[2] // 2 * 2 + a[2]
        return (r, g, b)

    image = Image.open(path)
    x, y = 0, 0
    next_point = lambda x, y: (x + 1, y) if x < image.width - 1 else (0, y + 1) if y < image.height - 1 else None
    p = [0, 0, 0]
    p[0] = len(str) // 256**2
    p[1] = len(str) % 256**2 // 256
    p[2] = len(str) % 256
    image.putpixel((x, y), tuple(p))
    x, y = next_point(x, y)
    for elem in str:
        val = f'{ord(elem):b}'
        val = (8 - len(val)) * '0' + val
        val = [int(el) for el in val] + [0]

        p = image.getpixel((x, y))
        p = pixel_mod(p, val[0:3])
        image.putpixel((x, y), p)
        x, y = next_point(x, y)

        p = image.getpixel((x, y))
        p = pixel_mod(p, val[3:6])
        image.putpixel((x, y), p)
        x, y = next_point(x, y)

        p = image.getpixel((x, y))
        p = pixel_mod(p, val[6:9])
        image.putpixel((x, y), p)
        x, y = next_point(x, y)
    image.save(name)

def decode(path):
    image = Image.open(path)
    x, y = 0, 0
    p = image.getpixel((x, y))
    size = p[0] * 256 * 256 + p[1] * 256 + p[2]
    next_point = lambda x, y: (x + 1, y) if x < image.width - 1 else (0, y + 1) if y < image.height - 1 else None
    result = ''
    for i in range(size):
        b = []
        for j in range(3):
            x, y = next_point(x, y)
            p = image.getpixel((x, y))
            b += [p[0] % 2, p[1] % 2, p[2] % 2]
        val = 0
        w = 1
        for i in range(len(b) - 2, -1, -1):
            if b[i] == 1:
                val += w
            w *= 2
        result += chr(val)
    image.close()
    return result

def exists_image(path):
    try:
        Image.open(path)
        return True
    except:
        return False

def hide_event():
    if exists_image('encoded.png'):
        show_error('Already hidden.')
        return
    if not exists_image('initial.png'):
        show_error('Select an image first.')
        return
    showimg_btn.clicked.disconnect()
    showimg_btn.clicked.connect(lambda event: show_image('encoded.png'))
    global string
    hide(string, 'initial.png', 'encoded.png')
    string = ''

def decode_event():
    image_name = 'encoded.png'
    if not exists_image(image_name):
        image_name = 'initial.png'
    if not exists_image(image_name):
        show_error('Select an image or encode a string.')
        return
    showimg_btn.clicked.disconnect()
    showimg_btn.clicked.connect(lambda event: show_image('initial.png'))
    global string
    try:
        string = decode(image_name)
    except:
        string = ''
    os.system('rm ' + image_name)

def get_initial_image():
    path = select_image()
    if path is None:
        return
    image = Image.open(path)
    image.save('initial.png')
    if exists_image('encoded.png'):
        os.system('rm encoded.png')

def clear_saved(event):
    if exists_image('initial.png'):
        os.system('rm initial.png')
    if exists_image('encoded.png'):
        os.system('rm encoded.png')

def save_encoded():
    if not exists_image('encoded.png'):
        show_error('Nothing to save.')
        return
    global string
    old_val = string
    select_str()
    path = string
    string = old_val
    try:
        image = Image.open('encoded.png')
        image.save(path)
    except:
        show_error('Cannot save.')

def str_btn_event():
    global string
    string = select_str()

app = QApplication(sys.argv)
app.aboutToQuit = clear_saved
win = QWidget()
win.setStyleSheet('background: #D1DBBD;')
str_btn = QPushButton(win)
font = QFont('Italic', 20)
str_btn.setFont(font)
str_btn.setText('select string')
set(str_btn, win, 0.05, 0.1, 0.9, 0.3)
str_btn.clicked.connect(select_str)
str_btn.setStyleSheet('border-radius: 10px; background: white; border: 1px solid #193441; margin-right: 5px;')

image_btn = QPushButton(win)
image_btn.setFont(font)
image_btn.setText('select image')
image_btn.clicked.connect(get_initial_image)
image_btn.setStyleSheet('border-radius: 10px; background: white; border: 1px solid #193441; margin-left: 5px;')

showimg_btn = QPushButton(win)
showimg_btn.setFont(font)
showimg_btn.setText('show image')
showimg_btn.clicked.connect( lambda event: show_image('initial.png'))
showimg_btn.setStyleSheet('border-radius: 10px; background: white; border: 1px solid #193441; margin-left: 5px;')

showstr_btn = QPushButton(win)
showstr_btn.setFont(font)
showstr_btn.setText('show string')
showstr_btn.clicked.connect( lambda event: show_string(string))
showstr_btn.setStyleSheet('border-radius: 10px; background: white; border: 1px solid #193441; margin-right: 5px;')


hide_btn = QPushButton(win)
hide_btn.setFont(font)
hide_btn.setText("encode string")
hide_btn.clicked.connect(hide_event)
hide_btn.setStyleSheet('border-radius: 10px; background: white; border: 1px solid #193441; margin-right: 5px;')

decode_btn = QPushButton(win)
decode_btn.setFont(font)
decode_btn.setText("decode")
decode_btn.clicked.connect(decode_event)
decode_btn.setStyleSheet('border-radius: 10px; background: white; border: 1px solid #193441; margin-left: 5px;')

save_btn = QPushButton(win)
save_btn.setFont(font)
save_btn.setText('save')
save_btn.clicked.connect(save_encoded)
save_btn.setStyleSheet('border-radius: 10px; background: white; border: 1px solid #193441; margin-bottom: 7px;')

win.resizeEvent = resizeEvent
win.show()
sys.exit(app.exec_())
