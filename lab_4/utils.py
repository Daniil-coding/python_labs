from math import sqrt

dist = lambda a, b: sqrt( (a.x - b.x)**2 + (a.y - b.y)**2 )

def set(widget, window, relx, rely, relw, relh):
    x = int(window.width() * relx)
    y = int(window.height() * rely)
    width = int(window.width() * relw)
    height = int(window.height() * relh)
    widget.setGeometry(x, y, width, height)

def remove(a, ind):
    ind = {*ind}
    i = j = 0
    while j < len(a):
        if not j in ind:
            a[i] = a[j]
            i += 1
        j += 1
    return a[:i]

def inside(dot, circle):
    return dist(dot, circle.center()) < circle.r

def unique(a):
    used = []
    for elem in a:
        if not elem in used:
            used.append(elem)
    return used