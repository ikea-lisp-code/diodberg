# Core types and Python boilerplate for defining pixels, panels, thread-safe
# core objects, etc. I would have used collections, but I've prefer to have
# some data safety.

from collections import MutableMapping
from collections import MutableSet
from copy import deepcopy
import json
import colorsys
import random
from diodberg.util.utils import random_location


class Color(object):
    """ Color representation, stored as RGB. Saturates for invalid values (FIX).
    """

    __min = 0           # RGB min
    __max = 255         # RGB max
    __hue_max = 360.    # Hue max
    
    __slots__ = {'red', 'green', 'blue', 'alpha'}

    def __init__(self, red = 0, green = 0, blue = 0, alpha = 0):
        self.red = red
        self.green = green
        self.blue = blue
        self.alpha = alpha
        
    @classmethod
    def random_color(cls):
        """ Returns a random Color.
        """
        r, g, b = [random.randint(0, 255) for i in range(3)]
        return Color(r, g, b)

    @property
    def rgba(self):
        """ Raw RGB-Alpha tuple (not normalized).
        """
        return (self.red, self.green, self.blue, self.alpha)

    @property
    def hsv(self):
        """ HSV tuple (not normalized).
        """
        norm = float(Color.__max)
        h, s, v = colorsys.rgb_to_hsv(self.red/norm, self.green/norm, self.blue/norm)
        return (Color.__hue_max*h, s, v)

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
        norm_hue = hue/Color.__hue_max
        red, green, blue = colorsys.hsv_to_rgb(norm_hue, saturation, value)
        self.red = int(round(red*Color.__max))
        self.green = int(round(green*Color.__max))
        self.blue = int(round(blue*Color.__max))

    def __repr__(self):
        val = (self.red, self.green, self.blue, self.alpha)
        formatted = "<Color (r = %0.3f, g = %0.3f, b = %0.3f, alpha = %0.3f)>"
        return formatted % val


class DMXAddress(object):
    """Defines the DMX address for a live pixel.
    """
    __invalid_address = -1
    __dmx_lower = 0
    __dmx_upper = 512

    __slots__ = {'__universe', '__address'}
    
    def __init__(self, universe = 0, address = 0):
        self.__universe = universe
        self.__address = address

    def is_valid(self): 
        return self.__address is not DMXAddress.__invalid_address

    def __get_universe(self): 
        return self.__universe
    def __set_universe(self, val): 
        self.__universe = val
    def __del_universe(self): 
        del self.__universe

    def __get_address(self): 
        return self.__address
    def __set_address(self, val):
        if DMXAddress.__dmx_lower <= val <= DMXAddress.__dmx_upper:
            self.__address = val
        else:
            self.__address = DMXAddress.__invalid_address
    def __del_address(self): 
        del self.__address

    universe = property(__get_universe, __set_universe, __del_universe, "DMX universe.")
    address = property(__get_address, __set_address, __del_address, "DMX address.")

    def __repr__(self):
        formatted = "<DMXAddress (universe = %0.3f, address = %0.3f)>"
        return formatted % (self.universe, self.address)
    

class Pixel(object):
    """ A pixel has a color and location and belong to a group. If it is live, it
    must have a valid DMX address.  
    TODO: Allow multiple route numbers?
    """
    
    __slots__ = {'__color', '__address', '__live', '__group'}
    
    def __init__(self, 
                 color = Color(), 
                 address = DMXAddress(), 
                 live = False, 
                 group = 0):
        self.__color = color
        self.__address = address
        self.__live = live
        self.__group = group
        assert not live or (live and address.is_valid())
        
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
                        str(self.color), ",", 
                        "live = ", str(self.live), 
                        "group = ", str(self.group), ">"])


class Panel(MutableMapping):
    """ Panel represents a collection of pixels, representing a climbing wall. It
    is currently structured as a dictionary keyed by (x, y) and can be
    constructed from a file specification or copy-constructed from another
    panel.
    TODO: Replace with a numpy matrix.
    """
    
    __base_group = 0
    __slots__ = {'__pixels'}

    def __init__(self, panel = None, filename = None, panel_id = 0):
        self.__pixels = dict()
        if panel is not None:
            self.__pixels = deepcopy(panel.__pixels)
        elif filename is not None:
            f = open(filename, 'r')
            size = 6
            i_universe, i_address, i_x, i_y, index, route = range(size)
            i = 0
            for line in f:
                words = line.split()
                assert len(words) is size, \
                    "Invalid number of elements. Line: " + i
                if words[index] is not panel_index:
                    continue
                location = (int(words[i_x]), int(words[i_y]))
                address = DMXAddress(int(words[i_universe]), int(words[i_address]))
                self.__pixels[location] = Pixel(Color(0, 0, 0), address, live = True)
                i += 1
            f.close()

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
        temp = self.__pixels.items()
        temp.sort(key = lambda x: x[0][0])
        return temp[len(temp) - 1][0][0] + 1

    @property
    def height(self):
        """ Returns the (vertical) panel height.
        """ 
        temp = self.__pixels.items()
        temp.sort(key = lambda x: x[0][1])
        return temp[len(temp) - 1][0][1] + 1

    @property
    def groups(self):
        """ Returns dictionary of groups for the panel, keyed by group name.
        """ 
        return self.__groups

    def write(self, filename, panel_id):
        """ Writes a panel to a file-specification. 
        A line in the file spec corresponds to a pixel:
            <dmx universe> <dmx address> <x location> <y location> <panel id> <group id>
        For example:
            0 0 10 3 1 0
            0 2 10 2 1 1
        """ 
        f = open(filename, 'w')
        for loc, pixel in self.iteritems():
            universe = pixel.address.universe
            address = pixel.address.address
            x, y = loc
            print "".join([universe, address, x, y], " ")
        f.close()

    def show(self, debug = True):
        """ Convenience method for viewing panel.
        """ 
        from diodberg.renderers.simulation_renderers import PyGameRenderer
        renderer = PyGameRenderer(debug = debug)
        renderer.render(self)

    @classmethod
    def random_panel(self, size = (640, 480), num_pixels = 200, live = False):
        """ Returns a randomly populated panel, for simulation. 
        TODO: merge blank_panel into this.
        """
        x, y = size 
        assert x*y >= num_pixels, "Number of pixels exceed snumber of slots."
        panel = Panel()
        for i in xrange(num_pixels):
            color = Color.random_color()
            location = random_location(x, y)
            address = DMXAddress(universe = 0, address = i)
            panel[location] = Pixel(color, address, live)
        return panel

    @classmethod
    def blank_panel(self, size = (7, 11)):
        """ Returns a blank default panel with default dimensions 
        sized to the climbing wall.
        """ 
        x, y = size
        panel = Panel()
        for i in xrange(x):
            for j in xrange(y):
                color = Color(0, 0, 0)
                location = (i, j)
                address = DMXAddress(universe = 0, address = 0)
                panel[location] = Pixel(color, address, live = False)
        return panel
    
    def __contains__(self, key):
        return key in self.__pixels

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
