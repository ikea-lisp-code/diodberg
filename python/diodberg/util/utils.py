# Random maybe useful utilities for panel manipulation.

import random
from diodberg.core.types import Color
from diodberg.core.types import DMXAddress
from diodberg.core.types import Pixel
from diodberg.core.types import Panel
from diodberg.renderers.simulation_renderers import PyGameRenderer


def random_location(x_upper_bound = 100, y_upper_bound = 100):
    """ Returns a bounded, random Location.
    """
    assert x_upper_bound > 0 and y_upper_bound > 0
    x = random.randint(0, x_upper_bound - 1)
    y = random.randint(0, y_upper_bound - 1)
    return (x, y)


def random_panel(size = (640, 480), num_pixels = 200, live = False):
    """ Returns a randomly populated panel, for simulation. 
    """
    x, y = size 
    assert x*y >= num_pixels, "Number of pixels exceed snumber of slots."
    panel = Panel()
    for i in xrange(num_pixels):
        color = Color.random_color()
        location = random_location(x, y)
        address = DMXAddress(universe = 0, address = i)
        pixel = Pixel(color, address, live)
        panel[location] = pixel
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
        0 0 10 3
        0 2 10 2
    """
    panel = Panel()
    f = open(filename, 'r')
    size = 4
    i_universe, i_address, i_x, i_y = range(size)
    for line in f:
        words = line.split()
        assert len(words) is size, "Invalid number of elements."
        location = (words[i_x], words[i_y])
        address = DMXAddress(words[i_universe], words[i_address])
        pixel = Pixel(Color(0, 0, 0), address, live = True)
        panel[location] = pixel
    f.close()
    return panel


def discover_panel():
    """ Discovers the active pixels in a climbing wall.
    """ 
    # TODO: Implement
    assert 0, "Not implemented yet. Use RDM?"
