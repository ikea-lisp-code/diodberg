# Random maybe useful utilities

import random

from core.types import *

def random_color():
    """ Returns a random Color.
    """
    r, g, b = [random.randint(0, 255) for i in range(3)]
    return Color(r, g, b)

def random_location(lower_bound, upper_bound):
    """ Returns a bounded, random Location.
    """
    x, y = [random.randint(lower_bound, upper_bound) for i in range(2)]
    return Location(x, y)

def random_panel(x = 640, y = 480, num_pixels = 200):
    """ Returns a randomly populated panel, for simulation. 
    """
    panel = Panel()
    for i in xrange(num_pixels):
        color = random_color()
        location = random_location(x, y)
        address = DMXAddress(0, 0)
        pixel = Pixel(color, location, address, live = True)
        panel[location.raw] = pixel
    return panel

def discovery_panel():
    """ Discovers the active pixels in a climbing wall.
    """ 
    pass
