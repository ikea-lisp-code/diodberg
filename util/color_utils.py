# Some utilities for manipulating colors

import random

from diodberg import Color

def random_color():
    r, g, b = [random.randint(0, 255) for i in range(3)]
    return Color(r, g, b)

