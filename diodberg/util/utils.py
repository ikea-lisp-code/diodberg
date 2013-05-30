# Random maybe useful utilities

import random
from diodberg.core.types import Color
from diodberg.core.types import Location
from diodberg.core.types import DMXAddress
from diodberg.core.types import Pixel
from diodberg.core.types import Panel
from diodberg.core.renderer import PyGameRenderer


def random_color():
    """ Returns a random Color.
    """
    r, g, b = [random.randint(0, 255) for i in range(3)]
    return Color(r, g, b)


def random_location(x_upper_bound = 100, y_upper_bound = 100):
    """ Returns a bounded, random Location.
    """
    x = random.randint(0, x_upper_bound)
    y = random.randint(0, y_upper_bound)
    return Location(x, y)


def random_panel(x = 640, y = 480, num_pixels = 200):
    """ Returns a randomly populated panel, for simulation. 
    """
    panel = Panel()
    for i in xrange(num_pixels):
        color = random_color()
        location = random_location(x, y)
        address = DMXAddress(0, 0)
        pixel = Pixel(color, location, address, live = False)
        panel[location.raw] = pixel
    return panel


def show_panel(panel, debug = True):
    """ Convenience method for viewing panel.
    """ 
    renderer = PyGameRenderer(debug = debug)
    renderer.render(panel)


def read_panel(filename):
    """ Instantiates a panel from a hard-coded file specification.
    A line in the file spec corresponds to a pixel:
        <dmx universe> <dmx address> <x location> <y location>
    For example:
        0 0 10.5 3.2
        0 2 10.5 3.5
    """
    panel = Panel()
    f = open(filename, 'r')
    size = 4
    i_universe, i_address, i_x, i_y = range(size)
    for line in f:
        words = line.split()
        assert len(words) is size, "Invalid number of elements."
        location = Location(words[i_universe], words[i_address])
        address = DMXAddress(words[i_x], words[i_y])
        pixel = Pixel(Color(0, 0, 0), location, address, live = True)
        panel[location.raw] = pixel
    f.close()
    return panel


def discover_panel():
    """ Discovers the active pixels in a climbing wall.
    """ 
    # TODO: Implement
    assert 0, "Not implemented yet. Use RDM?"
