# Core types and Python boilerplate for defining pixels, panels, thread-safe
# core objects, etc. I would have used collections, but I've prefer to have
# some data safety.

from collections import MutableMapping
import colorsys
from copy import deepcopy
import json
import numpy as np
import random

use_numba = False
try:
    from numba import autojit    
    use_numba = True
except ImportError as err:
    sys.stderr.write("Error: failed to import module ({})".format(err))

from diodberg.util.utils import ConditionalDecorator


COLOR_MIN = 0
COLOR_MAX = 255
COLOR_HUE_MAX = 360


@ConditionalDecorator(use_numba, autojit)
class Color(object):
    """ Color representation, stored as RGB. Saturates for invalid values (FIX).
    """

    __min = 0           # RGB min
    __max = 255         # RGB max
    __hue_max = 360.    # Hue max
    
    # __slots__ = {'red', 'green', 'blue', 'alpha'}
    
    def __init__(self, red = 0, green = 0, blue = 0, alpha = 0):
        self.red = red
        self.green = green
        self.blue = blue
        self.alpha = alpha

    @property
    def rgba(self):
        """ Raw RGB-Alpha tuple (not normalized).
        """
        return (self.red, self.green, self.blue, self.alpha)

    @property
    def hsv(self):
        """ HSV tuple (not normalized).
        """
        norm = float(COLOR_MAX)
        h, s, v = colorsys.rgb_to_hsv(self.red/norm, self.green/norm, self.blue/norm)
        return (COLOR_HUE_MAX*h, s, v)

    def set_rgb(self, red, green, blue, alpha = 0):
        """ Set RGB convenience method.
        """ 
        self.red = red
        self.green = green
        self.blue = blue
        self.alpha = alpha

    def set_hsv(self, hue, saturation, value):
        """ Set HSV convenience method. Assumes that a max range of (360., 1., 1.).
        """ 
        norm_hue = hue/COLOR_HUE_MAX
        red, green, blue = colorsys.hsv_to_rgb(norm_hue, saturation, value)
        self.red = int(round(red*COLOR_MAX))
        self.green = int(round(green*COLOR_MAX))
        self.blue = int(round(blue*COLOR_MAX))
    
    def __repr__(self):
        val = (self.red, self.green, self.blue, self.alpha)
        formatted = "<Color (r = %0.3f, g = %0.3f, b = %0.3f, alpha = %0.3f)>"
        return formatted % val


DMX_INVALID = -1
DMX_LOWER = -1
DMX_UPPER = -1


@ConditionalDecorator(use_numba, autojit)
class DMXAddress(object):
    """Defines the DMX address for a live pixel.
    """
    __invalid_address = -1
    __dmx_lower = 0
    __dmx_upper = 512

    # __slots__ = {'__universe', '__address'}
    
    def __init__(self, universe = 0, address = 0):
        self.__universe = universe
        self.__address = address

    def is_valid(self): 
        return self.__address != DMX_INVALID

    def __get_universe(self): 
        return self.__universe
    def __set_universe(self, val): 
        self.__universe = val
    def __del_universe(self): 
        del self.__universe

    def __get_address(self): 
        return self.__address
    def __set_address(self, val):
        if DMX_LOWER <= val <= DMX_UPPER:
            self.__address = val
        else:
            self.__address = DMX_INVALID
    def __del_address(self): 
        del self.__address

    universe = property(__get_universe, __set_universe, __del_universe, "DMX universe.")
    address = property(__get_address, __set_address, __del_address, "DMX address.")

    def __repr__(self):
        formatted = "<DMXAddress (universe = %0.3f, address = %0.3f)>"
        return formatted % (self.__universe, self.__address)
    

@ConditionalDecorator(use_numba, autojit)
class Pixel(object):
    """ A pixel has a color and location and belong to a group. If it is live, it
    must have a valid DMX address.  
    TODO: Allow multiple route numbers?
    """
    
    # __slots__ = {'__color', '__address', '__live', '__group'}
    
    def __init__(self, 
                 color = Color(0, 0, 0, 0),
                 address = DMXAddress(0, 0), 
                 live = False, 
                 group = 0):
        self.__color = color
        self.__address = address
        self.__live = live
        self.__group = group
        # assert not live or (live and address.is_valid())
        
    def __get_color(self): 
        return self.__color
    def __set_color(self, val): 
        self.__color = val
    def __del_color(self): 
        del self.__color    

    def __get_address(self): 
        return self.__address
    def __set_address(self, val): 
        self.__address = val
    def __del_address(self): 
        del self.__address

    def __get_live(self): 
        return self.__live
    def __set_live(self, val): 
        self.__live = val
    def __del_live(self): 
        del self.__live

    def __get_group(self): 
        return self.__group
    def __set_group(self, val): 
        self.__group = val
    def __del_group(self): 
        del self.__group

    color = property(__get_color, __set_color, __del_color, "RGB color.")
    address = property(__get_address, __set_address, __del_address, "DMX address.")
    live = property(__get_live, __set_live, __del_live, "Is live pixel?")
    group = property(__get_group, __set_group, __del_group, "Is the pixel part of a group?")

    def __repr__(self):
        return "".join(["<Pixel ", 
                        str(self.__color), ",", 
                        str(self.__address), ",", 
                        "live = ", str(self.__live), ",", 
                        "group = ", str(self.__group), ">"])


class Panel(object):
    """ Panel represents a collection of pixels, representing a climbing wall. It
    is currently structured as a dictionary keyed by (x, y) and can be
    constructed from a file specification or copy-constructed from another
    panel.
    TODO: Replace with a numpy matrix.
    """
    
    __base_group = 0
    __slots__ = {'__dim', '__pixels'}

    def __init__(self, size = (1, 1), panel = None, filename = None, panel_id = 0):
        self.__dim = size
        x, y = self.__dim
        color = Color(0, 0, 0, 0)
        address = DMXAddress(0, 0)
        live = False
        group = 0
        alloc = [[Pixel(color, address, live, group) for i in xrange(x)] for j in xrange(y)]
        self.__pixels = np.matrix(alloc, dtype = object).transpose()
        if panel is not None:
            assert False, "TODO: Add custom copy"
            # self.__pixels = deepcopy(panel.__pixels)
        elif filename is not None:
            assert False, "TODO: Replace with json decoder."

    @property
    def locations(self):
        """ Returns an array of (x, y) tuple locations for pixels.
        """
        return self.__pixels.keys()

    @property
    def addresses(self):
        """ Returns a dictionary, keyed by DMX universe, of available DMX
        addresses.
        """
        address_dict = dict()
        for loc, pixel in self.__pixels.items():
            address = pixel.address.address
            universe = pixel.address.universe
            if universe not in address_dict:
                address_dict[universe] = [address]
            else:
                address_dict[universe].append(address)
        return address_dict

    @property
    def width(self):
        """ Returns the (horizontal) panel width.
        """ 
        x, y = self.__dim
        return x

    @property
    def height(self):
        """ Returns the (vertical) panel height.
        """ 
        x, y = self.__dim
        return y

    @property 
    def raw(self):
        return self.__panel

    def write(self, filename, panel_id):
        assert False, "TODO: Replace with json decoder."

    def show(self, debug = True):
        """ Convenience method for viewing panel.
        """ 
        from diodberg.renderers.simulation_renderers import PyGameRenderer
        renderer = PyGameRenderer(debug = debug)
        while True:
            try:
                renderer.render(self)
            except KeyboardInterrupt:
                print "\nQuiting!"
                exit()
    
    def __contains__(self, key):
        try:
            return self.__pixels[key] is not None
        except IndexError:
            return False

    def __getitem__(self, key):
        return self.__pixels[key]

    def __setitem__(self, key, value):
        self.__pixels[key] = value

    def __delitem__(self, key):
        del self.__pixels[key]

    def __len__(self):
        return len(self.__pixels)

    def __iter__(self):
        return iter(self.__pixels)

    def __repr__(self):
        return "".join(["Panel<", str(self.__pixels), ">"])


def random_color():
    """ Returns a random Color.
    """
    r, g, b = [random.randint(0, 255) for i in range(3)]
    return Color(r, g, b, 0)


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
    panel = Panel(size)
    for i in xrange(num_pixels):
        color = random_color()
        location = random_location(x, y)
        address = DMXAddress(0, i)
        group = 0
        live = True
        panel[location] = Pixel(color, address, live, group)
    return panel
