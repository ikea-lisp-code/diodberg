# Random maybe useful utilities for panel manipulation.

import random


def random_location(x_upper_bound = 100, y_upper_bound = 100):
    """ Returns a bounded, random Location.
    """
    assert x_upper_bound > 0 and y_upper_bound > 0
    x = random.randint(0, x_upper_bound - 1)
    y = random.randint(0, y_upper_bound - 1)
    return (x, y)


def read_file(filename):
    """ Reads a file containing a specification of (possible multiple) panels. 
    TODO: Being changed to a JSON representation.
    """ 
    assert 0, "Not implemented yet."
    panels = dict()
    return panels
