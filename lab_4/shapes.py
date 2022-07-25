from math import sqrt

E = 1e-9

class Shape:
    def __init__(self):
        self.highlight = False

class Dot(Shape):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y

    def __eq__(self, other):
        return abs(self.x - other.x) < E and abs(self.y - other.y) < E

class Circle(Shape):
    def __init__(self, x, y, r):
        super().__init__()
        self.x = x
        self.y = y
        self.r = r

    def center(self):
        return Dot(self.x, self.y)

    def __eq__(self, other):
        return self.center() == other.center() and abs(self.r - other.r) < E

def dist_arc(dot, circle):
    dx = dot.x - circle.x
    dy = dot.y - circle.y
    return abs(sqrt(dx**2 + dy**2) - circle.r)